#!/usr/bin/env python3
"""
gnuradio_clone_builder.py

Step 2 of building GNU Radio from source on bare metal: builds, tests, and
installs GNU Radio from a clone that is already on this machine -- normally
your own fork, cloned into your home directory, with the branch you are
working on checked out. Run gnuradio_dependencies_installer.py (Step 1)
first; it installs UHD and everything GNU Radio needs.

This program does not clone anything and does not change branches. It builds
whatever is checked out in the source directory ($HOME/gnuradio unless
--source-dir says otherwise), so it can be run again after every change:

    cd $HOME/gnuradio
    mkdir build                     (first time only)
    cd build
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../ 2>&1 | tee cmake.log
    make -j<jobs> 2>&1 | tee make.log
    make test 2>&1 | tee make_test.log
    sudo make install
    sudo ldconfig

Any failure, including a failing test, stops before `sudo make install`; the
logs in the build directory show what went wrong. Use --no-install to stop
after the tests on purpose.

Compiling GNU Radio needs a lot of memory: some files take 2 GB each, and
make compiles several at once. With too many jobs the machine runs out of
memory and the compiler is killed part-way through. So the number of jobs is
one less than the number of processor cores, but no more than one per 2 GB of
memory (7 jobs on a 16-core machine with 16 GB). Use --jobs to choose it
yourself.

Before building, it checks that:

  * the source directory exists and holds GNU Radio's source code;
  * UHD's development package (libuhd-dev) is installed, i.e. Step 1 was run;
  * Ubuntu's own gnuradio packages are not installed;
  * no empty directories from an earlier, removed GNU Radio install are left
    under /usr/local (they make GNU Radio's tests fail).

The build runs as you, even when this program is started with sudo, so the
build directory stays yours. `sudo make install` leaves some root-owned files
in it; they are given back to you before the next build.

Examples
--------
  # Show the checks and build steps without running anything:
  python3 gnuradio_clone_builder.py --dry-run

  # Build, test, and install what is checked out in ~/gnuradio:
  sudo python3 gnuradio_clone_builder.py

  # Build and test only:
  python3 gnuradio_clone_builder.py --no-install

  # Build a clone that is somewhere else:
  sudo python3 gnuradio_clone_builder.py --source-dir ~/src/gnuradio

  # Use fewer make jobs, and leave out components you don't need:
  sudo python3 gnuradio_clone_builder.py --jobs 4 \
      --cmake-args="-DENABLE_GR_FEC=OFF -DENABLE_GR_VOCODER=OFF"
"""

from __future__ import annotations

import argparse
import os
import pwd
import shlex
import subprocess
import sys
import typing
from pathlib import Path

# Installed by gnuradio_dependencies_installer.py (Step 1).
REQUIRED_PACKAGES = ["libuhd-dev"]

# Ubuntu's own GNU Radio, which must not be installed next to a source build.
CONFLICTING_PACKAGES = ["gnuradio", "gnuradio-dev"]

# Where an earlier GNU Radio install under /usr/local keeps its files.
INSTALL_PREFIX = "/usr/local"

# Memory to allow per parallel make job. GNU Radio's Python bindings need
# about this much for each file being compiled.
MEMORY_PER_JOB_KB = 2 * 1024 * 1024

INSTALL_DIR_PATTERNS = (
    "lib/python3*/dist-packages/gnuradio",
    "lib/python3*/dist-packages/pmt",
    "lib/python3*/site-packages/gnuradio",
    "lib/python3*/site-packages/pmt",
    "include/gnuradio",
    "include/pmt",
    "share/gnuradio",
    "etc/gnuradio",
    "lib/cmake/gnuradio",
    "share/doc/gnuradio-*",
)


class BuildStep(typing.NamedTuple):
    cmd: list[str]
    cwd: str
    log: str | None = None  # if set, like `2>&1 | tee <log>`: output is shown and saved to cwd/<log>


def describe_step(step: BuildStep) -> str:
    """The step's command as a shell user would type it, including any tee log."""
    cmd = " ".join(step.cmd)
    return f"{cmd} 2>&1 | tee {step.log}" if step.log else cmd


def get_build_user() -> pwd.struct_passwd | None:
    """
    When running as root via sudo, return the invoking (normal) user, whom
    the build steps without "sudo" should run as -- so the build directory
    belongs to that user, not root. Returns None when not running as root
    (the steps already run as the normal user) or when root wasn't reached
    via sudo (there's no normal user to switch to).
    """
    if os.geteuid() != 0:
        return None
    sudo_user = os.environ.get("SUDO_USER")
    if not sudo_user or sudo_user == "root":
        return None
    try:
        return pwd.getpwnam(sudo_user)
    except KeyError:
        return None


def get_owner() -> pwd.struct_passwd:
    """The user the build runs as, and who should own the build directory."""
    return get_build_user() or pwd.getpwuid(os.geteuid())


def user_kwargs_and_env(env: dict | None = None) -> tuple[dict, dict | None]:
    """subprocess arguments and environment for running a command as the build user."""
    build_user = get_build_user()
    if not build_user:
        return {}, env
    env = dict(env or os.environ)
    env.update(HOME=build_user.pw_dir, USER=build_user.pw_name, LOGNAME=build_user.pw_name)
    return dict(
        user=build_user.pw_uid,
        group=build_user.pw_gid,
        extra_groups=os.getgrouplist(build_user.pw_name, build_user.pw_gid),
    ), env


def get_total_memory_kb(meminfo_path: str = "/proc/meminfo") -> int | None:
    """The machine's memory (MemTotal) in kB, or None if it can't be read."""
    try:
        for line in Path(meminfo_path).read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    except (OSError, ValueError, IndexError):
        pass
    return None


def get_make_jobs(cpu_count: int | None = None, memory_kb: int | None = None) -> int:
    """
    Number of parallel make jobs: nproc - 1 (leave one core free), but no
    more than one per MEMORY_PER_JOB_KB of memory, and at least 1. With more
    jobs than the memory allows, the kernel kills the compiler part-way
    through the build.
    """
    cpu_count = cpu_count or os.cpu_count() or 2
    memory_kb = memory_kb or get_total_memory_kb()
    jobs = cpu_count - 1
    if memory_kb:
        jobs = min(jobs, memory_kb // MEMORY_PER_JOB_KB)
    return max(1, jobs)


def installed_packages(names: list[str]) -> list[str]:
    """Which of the given packages dpkg reports as installed."""
    found = []
    for name in names:
        try:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Status}", name], capture_output=True, text=True,
            )
        except OSError:
            return found
        if result.returncode == 0 and result.stdout.strip() == "install ok installed":
            found.append(name)
    return found


def find_stale_install_dirs(prefix: str = INSTALL_PREFIX) -> list[Path]:
    """
    Return directories left behind by an earlier GNU Radio install that was
    removed file by file (e.g. `xargs rm -f < install_manifest.txt`): they
    still exist under the install prefix but contain no files.

    These matter because Python treats an empty directory as a valid (empty)
    package. `import gnuradio.grc...` then finds the leftover instead of
    raising ModuleNotFoundError, which makes GNU Radio's grc_tests fail.
    """
    stale = []
    for pattern in INSTALL_DIR_PATTERNS:
        for path in sorted(Path(prefix).glob(pattern)):
            if path.is_dir() and not any(p.is_file() for p in path.rglob("*")):
                stale.append(path)
    return stale


def describe_checkout(source_dir: Path) -> str:
    """The branch and version of the checkout, e.g. "issue8218 (v3.11.0.0git-1194-gb09371606)"."""
    user_kwargs, env = user_kwargs_and_env()
    parts = []
    for cmd in (["git", "rev-parse", "--abbrev-ref", "HEAD"], ["git", "describe", "--tags", "--always"]):
        try:
            result = subprocess.run(
                cmd, cwd=source_dir, env=env, capture_output=True, text=True, check=True, **user_kwargs,
            )
            parts.append(result.stdout.strip())
        except (OSError, subprocess.CalledProcessError):
            parts.append("?")
    return f"{parts[0]} ({parts[1]})"


def has_files_not_owned_by(directory: Path, uid: int) -> bool:
    """Whether anything in the directory tree belongs to another user (e.g. root, after `sudo make install`)."""
    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            try:
                if os.lstat(os.path.join(root, name)).st_uid != uid:
                    return True
            except OSError:
                continue
    return False


def get_build_steps(source_dir: Path, install: bool, jobs: int,
                    cmake_args: list[str]) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd <source_dir>
        mkdir build                     (first time only)
        cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr/local <cmake_args> ../ 2>&1 | tee cmake.log
        make -j<jobs> 2>&1 | tee make.log
        make test 2>&1 | tee make_test.log
        sudo make install
        sudo ldconfig
    """
    source = str(source_dir)
    build_dir_path = source_dir / "build"
    build_dir = str(build_dir_path)
    owner = get_owner()

    steps = []
    if not build_dir_path.exists():
        steps.append(BuildStep(["mkdir", "build"], source))
    elif has_files_not_owned_by(build_dir_path, owner.pw_uid):
        # An earlier `sudo make install` left root-owned files; the build
        # (which runs as the normal user) must be able to rewrite them.
        steps.append(BuildStep(
            ["sudo", "chown", "-R", f"{owner.pw_uid}:{owner.pw_gid}", build_dir], source,
        ))
    steps += [
        BuildStep(
            ["cmake", f"-DCMAKE_INSTALL_PREFIX={INSTALL_PREFIX}", *cmake_args, "../"],
            build_dir, log="cmake.log",
        ),
        BuildStep(["make", f"-j{jobs}"], build_dir, log="make.log"),
        BuildStep(["make", "test"], build_dir, log="make_test.log"),
    ]
    if install:
        steps += [
            BuildStep(["sudo", "make", "install"], build_dir),
            BuildStep(["sudo", "ldconfig"], build_dir),
        ]
    return steps


def run_logged(step: BuildStep, env: dict | None, user_kwargs: dict) -> None:
    """
    Run step.cmd like `cmd 2>&1 | tee <step.log>`: stream its combined
    stdout/stderr to the terminal and to the log file in step.cwd. Raises
    CalledProcessError if the command exits non-zero.
    """
    log_path = os.path.join(step.cwd, step.log)
    build_user = get_build_user()
    with open(log_path, "w", encoding="utf-8") as log_file:
        if build_user:
            os.chown(log_path, build_user.pw_uid, build_user.pw_gid)
        proc = subprocess.Popen(
            step.cmd, cwd=step.cwd, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, errors="replace", **user_kwargs,
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            log_file.write(line)
        returncode = proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, step.cmd)


def run_build_steps(steps: list[BuildStep]) -> int:
    """
    Runs the given build steps in order. Aborts on the first command that
    fails (non-zero exit, or missing executable/working directory) and
    returns 1; returns 0 if all succeed.

    When running as root via sudo, steps that don't start with "sudo" run as
    the invoking user (see get_build_user()); "sudo" steps run as root.

    A step with log set behaves like `cmd 2>&1 | tee <log>`. Unlike a shell
    pipeline without `pipefail`, a failing command still fails the step
    rather than taking tee's exit status.
    """
    for step in steps:
        user_kwargs: dict = {}
        env = None
        if step.cmd[0] != "sudo":
            user_kwargs, env = user_kwargs_and_env()

        print(f"\n$ (cd {step.cwd} && {describe_step(step)})")
        try:
            if step.log:
                run_logged(step, env, user_kwargs)
            else:
                subprocess.run(step.cmd, cwd=step.cwd, env=env, check=True, **user_kwargs)
        except subprocess.CalledProcessError as exc:
            print(
                f"\nerror: build step failed (exit code {exc.returncode}): "
                f"{' '.join(step.cmd)} (in {step.cwd})",
                file=sys.stderr,
            )
            return 1
        except OSError as exc:
            print(
                f"\nerror: could not run '{' '.join(step.cmd)}' in {step.cwd}: {exc}",
                file=sys.stderr,
            )
            return 1
    return 0


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build, test, and install GNU Radio from a clone already on this machine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--source-dir", default=None,
        help=(
            "The GNU Radio clone to build. Default: gnuradio in the home directory of the "
            "invoking user (SUDO_USER when run via sudo)."
        ),
    )
    parser.add_argument(
        "--jobs", type=int, default=None,
        help=(
            "Number of parallel make jobs. Default: one less than the number of processor "
            "cores, but no more than one per 2 GB of memory."
        ),
    )
    parser.add_argument(
        "--cmake-args", default="",
        help=(
            "Extra options for cmake, in one quoted string written with '=', e.g. "
            "--cmake-args=\"-DENABLE_GR_FEC=OFF -DENABLE_GR_VOCODER=OFF\". cmake remembers "
            "them in the build directory until they are changed or the directory is removed."
        ),
    )
    parser.add_argument(
        "--no-install", action="store_true",
        help="Stop after the tests: do not run 'sudo make install' and 'sudo ldconfig'.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Run the checks and print the build steps, without running them.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before building.",
    )
    args = parser.parse_args()
    if args.jobs is not None and args.jobs < 1:
        parser.error("--jobs must be at least 1")
    try:
        cmake_args = shlex.split(args.cmake_args)
    except ValueError as exc:
        parser.error(f"--cmake-args: {exc}")

    # --- 1. Find the clone ---
    owner = get_owner()
    if args.source_dir:
        source_dir = Path(args.source_dir).expanduser().resolve()
    else:
        source_dir = Path(owner.pw_dir) / "gnuradio"
    if not (source_dir / "CMakeLists.txt").is_file() or not (source_dir / "gnuradio-runtime").is_dir():
        print(
            f"error: {source_dir} doesn't hold GNU Radio's source code. Clone your fork first, "
            f"e.g.:\n  cd {owner.pw_dir}\n  git clone https://github.com/<your-username>/gnuradio.git\n"
            f"or pass --source-dir to point at an existing clone. Aborting.",
            file=sys.stderr,
        )
        return 1
    print(f"Source directory: {source_dir}")
    print(f"Checked out: {describe_checkout(source_dir)}")

    # --- 2. Check that Step 1 was run and nothing conflicts ---
    missing = [p for p in REQUIRED_PACKAGES if p not in installed_packages(REQUIRED_PACKAGES)]
    if missing:
        print(
            "error: " + ", ".join(missing) + " is not installed. Run "
            "gnuradio_dependencies_installer.py first; it installs UHD and GNU Radio's "
            "dependencies. Aborting.",
            file=sys.stderr,
        )
        return 1

    conflicting = installed_packages(CONFLICTING_PACKAGES)
    if conflicting:
        print(
            "error: Ubuntu's own GNU Radio is installed (" + ", ".join(conflicting) + "). It would "
            "sit next to the GNU Radio built here. Remove it, then run this program again:",
            file=sys.stderr,
        )
        print("  sudo apt-get remove " + " ".join(conflicting), file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1

    stale_dirs = find_stale_install_dirs()
    if stale_dirs:
        print(
            "error: empty directories from an earlier GNU Radio install were found. They make "
            "GNU Radio's tests fail (Python imports them as empty packages). Remove them, then "
            "run this program again:",
            file=sys.stderr,
        )
        print("  sudo rm -rf " + " ".join(str(d) for d in stale_dirs), file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1
    print("OK: UHD is installed; no conflicting packages or leftover directories found.")

    # --- 3. Show the plan ---
    jobs = args.jobs or get_make_jobs()
    steps = get_build_steps(source_dir, install=not args.no_install, jobs=jobs, cmake_args=cmake_args)
    memory_kb = get_total_memory_kb()
    if args.jobs:
        print(f"\nMake jobs: {jobs} (from --jobs)")
    else:
        memory = f"{memory_kb / 1024 / 1024:.1f} GB of memory" if memory_kb else "memory unknown"
        print(f"\nMake jobs: {jobs} ({os.cpu_count()} processor cores, {memory})")
    print("\nThe following build steps will run:")
    if get_build_user():
        print(f"  Build user: {owner.pw_name} (steps without 'sudo' run as {owner.pw_name}; "
              f"'sudo' steps run as root)")
    elif any(step.cmd[0] == "sudo" for step in steps) and os.geteuid() != 0:
        print(f"  Build user: {owner.pw_name} (you'll be prompted for your sudo password at the "
              f"'sudo' steps)")
    else:
        print(f"  Build user: {owner.pw_name}")
    for step in steps:
        print(f"  $ (cd {step.cwd} && {describe_step(step)})")

    if args.dry_run:
        print("\n--dry-run set: no commands executed.")
        return 0

    if not args.yes:
        if not _confirm("\nProceed with building GNU Radio? [y/N] "):
            print("Aborted.")
            return 1

    # --- 4. Build ---
    if run_build_steps(steps) != 0:
        print("\nerror: GNU Radio build failed. Aborting.", file=sys.stderr)
        return 1

    if args.no_install:
        print("\nDone. GNU Radio built and tested; --no-install set, so nothing was installed.")
    else:
        print("\nDone. GNU Radio built, tested, and installed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
