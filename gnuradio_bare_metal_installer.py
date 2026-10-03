#!/usr/bin/env python3
"""
gnuradio_bare_metal_installer.py

Builds and installs GNU Radio (https://github.com/gnuradio/gnuradio) from
source on bare metal, after uhd_bare_metal_installer.py has installed UHD
and its build dependencies.

UHD's Dockerfile only lists what UHD needs, so this program installs GNU
Radio's own build dependencies too. Instead of hardcoding that list, it
fetches the Build-Depends of Ubuntu's own gnuradio package (the debian/control
file for the host's Ubuntu release, from Launchpad) -- the same list
`apt-get build-dep gnuradio` uses, and what GNU Radio's CI image for the 3.10
series installs. It:

  1. Checks that uhd-dependencies.txt (written by uhd_bare_metal_installer.py)
     exists, i.e. that the UHD installer has been run. Aborts with an error
     if it doesn't.
  2. Derives GNU Radio's dependency list and saves it to
     gnuradio-dependencies.txt. Packages that would conflict with the
     source-built UHD, or that are only needed to build Debian packages and
     documentation, are left out; a few run-time packages are added.
  3. Checks that no empty directories from an earlier, removed GNU Radio
     install are left under /usr/local (they make GNU Radio's tests fail).
  4. Installs those packages, then clones, builds, tests, and installs GNU
     Radio from the chosen branch:

         cd $HOME
         sudo apt-get update
         sudo apt-get install -y <packages>
         git clone https://github.com/gnuradio/gnuradio.git
         cd $HOME/gnuradio
         git checkout <branch>
         mkdir build && cd build
         cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../ 2>&1 | tee cmake.log
         make -j$(nproc)-1 2>&1 | tee make.log
         make test 2>&1 | tee make_test.log
         sudo make install
         sudo ldconfig

     Any failure, including a failing test, stops the build; the logs in
     $HOME/gnuradio/build show what went wrong.

The default branch is maint-3.10, the 3.10 release series. Ubuntu's gnuradio
package is a 3.10 release, which uses Qt5, so the dependency list fits it.
The main branch (3.11 development) needs Qt6 packages for its gr-qtgui
instead, which this list does not include.

Examples
--------
  # Just print/save the dependency list to gnuradio-dependencies.txt:
  python3 gnuradio_bare_metal_installer.py --list-only

  # Show the packages and build steps without running anything:
  python3 gnuradio_bare_metal_installer.py --dry-run

  # Install dependencies, then clone/build/install the 3.10 release series
  # (maint-3.10, the default):
  sudo python3 gnuradio_bare_metal_installer.py

  # The same for the main branch (3.11 development):
  sudo python3 gnuradio_bare_metal_installer.py --branch main
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.error
from pathlib import Path

from uhd_bare_metal_installer import (
    DEFAULT_PACKAGE_LIST_OUTPUT as UHD_PACKAGE_LIST_OUTPUT,
    BuildStep,
    _confirm,
    _parse_os_release,
    describe_build_user,
    describe_step,
    fetch_dockerfile as fetch_url,
    get_home_dir,
    get_make_jobs,
    run_build_steps,
    write_package_list,
)

DEFAULT_BRANCH = "maint-3.10"
DEFAULT_PACKAGE_LIST_OUTPUT = "gnuradio-dependencies.txt"

# debian/control of Ubuntu's gnuradio source package, per Ubuntu release codename.
CONTROL_URL_TEMPLATE = (
    "https://git.launchpad.net/ubuntu/+source/gnuradio/plain/debian/control?h=ubuntu/{codename}"
)

# Build-Depends entries that are not installed, and why.
SKIP_PACKAGES = {
    "libuhd-dev": "UHD is built from source into /usr/local; Ubuntu's older copy would conflict",
    "debhelper-compat": "only needed to build the Debian package",
    "dh-python": "only needed to build the Debian package",
    "dpkg-dev": "only needed to build the Debian package",
    "graphviz": "only needed to build the documentation",
    "xmlto": "only needed to build the documentation",
    "libjs-mathjax": "only needed to build the documentation",
}

# Packages added to the list: run-time dependencies that a build-dependency
# list doesn't cover.
EXTRA_PACKAGES = {
    "libvolk-dev": "GNU Radio requires Volk (>= 2.4.1); normally already in the list",
    "python3-packaging": "checked for by GNU Radio's cmake; normally already in the list",
    "python3-qtpy": "imported by maint-3.10's Python code at run time",
    "python3-pyqtgraph": "needed by the filter design tool at run time",
    "python3-matplotlib": "imported by maint-3.10's examples and gr-qtgui Python code at run time",
    "soapysdr-tools": "provides SoapySDRUtil, for checking SoapySDR devices used with gr-soapy",
}

KNOWN_OSES = ("linux", "kfreebsd", "hurd")

# Where an earlier GNU Radio install under /usr/local keeps its files.
INSTALL_PREFIX = "/usr/local"
INSTALL_DIR_PATTERNS = (
    "lib/python3*/dist-packages/gnuradio",
    "lib/python3*/site-packages/gnuradio",
    "include/gnuradio",
    "share/gnuradio",
    "lib/cmake/gnuradio",
    "share/doc/gnuradio-*",
)


class ControlParseError(RuntimeError):
    pass


def get_host_arch() -> str:
    """The Debian architecture name of this machine, e.g. amd64 or arm64."""
    try:
        result = subprocess.run(
            ["dpkg", "--print-architecture"], capture_output=True, text=True, check=True,
        )
        return result.stdout.strip() or "amd64"
    except (OSError, subprocess.CalledProcessError):
        return "amd64"


def _arch_term_matches(term: str, host_arch: str) -> bool:
    """Whether one architecture term (e.g. linux-any, hurd-amd64, arm64) matches a Linux host."""
    if term == "any":
        return True
    os_name, sep, arch = term.partition("-")
    if not sep:
        return term == host_arch  # a bare architecture implies Linux
    if os_name == "any":
        return arch == host_arch
    if os_name in KNOWN_OSES:
        return os_name == "linux" and arch in ("any", host_arch)
    return term == host_arch


def arch_restriction_applies(restriction: str, host_arch: str) -> bool:
    """
    Evaluate a Build-Depends architecture restriction such as
    "linux-any", "!hurd-amd64", or "amd64 arm64 riscv64": True if the
    dependency applies on this (Linux) host.
    """
    terms = restriction.split()
    if all(t.startswith("!") for t in terms):
        return not any(_arch_term_matches(t[1:], host_arch) for t in terms)
    return any(_arch_term_matches(t, host_arch) for t in terms if not t.startswith("!"))


def extract_build_depends(control_text: str, host_arch: str) -> list[str]:
    """
    Parse the Build-Depends field of a debian/control file and return the
    package names that apply to this host, in order. Version constraints
    "(>= 1.0)" and build profiles "<!nocheck>" are dropped, architecture
    restrictions "[linux-any]" are evaluated, and for alternatives "a | b"
    the first is taken. Build-Depends-Indep (documentation tools) is ignored.
    """
    match = re.search(
        r"^Build-Depends:(.*?)(?=^\S|\Z)", control_text, flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ControlParseError("Could not find a Build-Depends field in the control file.")

    packages: list[str] = []
    for entry in match.group(1).split(","):
        entry = entry.split("|")[0]
        entry = re.sub(r"<[^>]*>", "", entry)
        entry = re.sub(r"\([^)]*\)", "", entry)
        restriction = re.search(r"\[([^\]]*)\]", entry)
        name = re.sub(r"\[[^\]]*\]", "", entry).strip()
        if not name:
            continue
        if not re.fullmatch(r"[a-z0-9][a-z0-9+.\-]*", name):
            continue  # ignore anything unexpected rather than fail hard
        if restriction and not arch_restriction_applies(restriction.group(1), host_arch):
            continue
        if name not in packages:
            packages.append(name)

    if not packages:
        raise ControlParseError("Parsed zero packages -- the control file format may have changed.")
    return packages


def get_control_text(args: argparse.Namespace) -> str:
    """
    Obtain the debian/control text from --control-path, --control-url, or by
    reading the host's Ubuntu codename from /etc/os-release and fetching the
    matching file from Launchpad. Raises RuntimeError with a user-facing
    message on failure.
    """
    try:
        if args.control_path:
            print(f"Reading control file from local path: {args.control_path}")
            return Path(args.control_path).read_text(encoding="utf-8")
        if args.control_url:
            print(f"Fetching control file from: {args.control_url}")
            return fetch_url(args.control_url)

        info = _parse_os_release(Path(args.os_release_path))
        codename = info.get("VERSION_CODENAME") or info.get("UBUNTU_CODENAME")
        if info.get("ID") != "ubuntu" or not codename:
            raise RuntimeError(
                f"{args.os_release_path} doesn't describe an Ubuntu release (ID="
                f"{info.get('ID')!r}, VERSION_CODENAME={codename!r}). Aborting -- pass "
                f"--control-url or --control-path to use a specific control file instead."
            )
        print(f"Detected host OS: Ubuntu {info.get('VERSION_ID', '?')} ({codename})")
        url = CONTROL_URL_TEMPLATE.format(codename=codename)
        print(f"Fetching Ubuntu's gnuradio package control file from: {url}")
        return fetch_url(url)
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(
            f"failed to obtain the control file: {exc}. Pass --control-url or "
            f"--control-path to use a specific control file instead."
        ) from exc


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


def select_packages(build_depends: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Apply SKIP_PACKAGES and EXTRA_PACKAGES. Returns (packages, skipped, added)."""
    skipped = [p for p in build_depends if p in SKIP_PACKAGES]
    packages = [p for p in build_depends if p not in SKIP_PACKAGES]
    added = [p for p in EXTRA_PACKAGES if p not in packages]
    return packages + added, skipped, added


def get_build_steps(home: str, branch: str, packages: list[str]) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd $HOME
        sudo apt-get update
        sudo apt-get install -y <packages>
        git clone https://github.com/gnuradio/gnuradio.git
        cd $HOME/gnuradio
        git checkout <branch>
        mkdir build && cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../ 2>&1 | tee cmake.log
        make -j$(nproc)-1 2>&1 | tee make.log
        make test 2>&1 | tee make_test.log
        sudo make install
        sudo ldconfig
    """
    gnuradio_dir = os.path.join(home, "gnuradio")
    build_dir = os.path.join(gnuradio_dir, "build")
    jobs = get_make_jobs()

    return [
        BuildStep(["sudo", "apt-get", "update"], home),
        # -y because this is an unattended build (the installer already asked).
        BuildStep(["sudo", "apt-get", "install", "-y", *packages], home),
        BuildStep(["git", "clone", "https://github.com/gnuradio/gnuradio.git"], home),
        BuildStep(["git", "checkout", branch], gnuradio_dir),
        BuildStep(["mkdir", "build"], gnuradio_dir),
        BuildStep(["cmake", "-DCMAKE_INSTALL_PREFIX=/usr/local", "../"], build_dir, log="cmake.log"),
        BuildStep(["make", f"-j{jobs}"], build_dir, log="make.log"),
        BuildStep(["make", "test"], build_dir, log="make_test.log"),
        BuildStep(["sudo", "make", "install"], build_dir),
        BuildStep(["sudo", "ldconfig"], build_dir),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and install GNU Radio from source on bare metal, after UHD.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--branch", default=DEFAULT_BRANCH,
        help=(
            "GNU Radio branch (or tag) to check out and build, e.g. maint-3.10 or main "
            f"(default: {DEFAULT_BRANCH})."
        ),
    )
    parser.add_argument(
        "--control-url", default=None,
        help=(
            "URL of the debian/control file to take GNU Radio's Build-Depends from. Default: "
            "Ubuntu's gnuradio package for the host's release (from /etc/os-release), on Launchpad."
        ),
    )
    parser.add_argument(
        "--control-path", default=None,
        help="Read the debian/control file from a local path instead of fetching it.",
    )
    parser.add_argument(
        "--os-release-path", default="/etc/os-release",
        help="Path to read the Ubuntu codename from (default: /etc/os-release).",
    )
    parser.add_argument(
        "--list-only", action="store_true",
        help="Only derive and print/save the dependency list; do not install or build anything.",
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_PACKAGE_LIST_OUTPUT,
        help=f"Path to save the dependency list (default: {DEFAULT_PACKAGE_LIST_OUTPUT}).",
    )
    parser.add_argument(
        "--uhd-deps", default=UHD_PACKAGE_LIST_OUTPUT,
        help=(
            "Package list written by uhd_bare_metal_installer.py, which must exist "
            f"(default: {UHD_PACKAGE_LIST_OUTPUT})."
        ),
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Derive the dependency list and print the build steps, without running them.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before installing and building.",
    )
    parser.add_argument(
        "--build", action="store_true",
        help=(
            "Accepted for consistency with uhd_bare_metal_installer.py and ignored: "
            "building GNU Radio is already the default."
        ),
    )
    parser.add_argument(
        "--home", default=None,
        help=(
            "Directory to clone/build GNU Radio into, overriding auto-detection. "
            "Default: the invoking user's home when run via sudo (SUDO_USER), else $HOME."
        ),
    )
    args = parser.parse_args()

    # --- 1. Derive GNU Radio's dependency list and save it ---
    try:
        control_text = get_control_text(args)
        build_depends = extract_build_depends(control_text, get_host_arch())
    except (RuntimeError, ControlParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    packages, skipped, added = select_packages(build_depends)
    print(f"Extracted {len(build_depends)} build dependencies of Ubuntu's gnuradio package.")
    for pkg in skipped:
        print(f"  left out: {pkg} ({SKIP_PACKAGES[pkg]})")
    for pkg in added:
        print(f"  added:    {pkg} ({EXTRA_PACKAGES[pkg]})")

    out_path = Path(args.output)
    try:
        write_package_list(out_path, packages)
    except OSError as exc:
        print(f"error: could not write {out_path}: {exc}", file=sys.stderr)
        return 1
    print(f"Package list ({len(packages)} packages) written to: {out_path.resolve()}")

    if args.list_only:
        print("\n--list-only set: not installing or building anything.")
        for pkg in packages:
            print(f"  {pkg}")
        return 0

    # --- 2. Check that the UHD installer has been run ---
    uhd_path = Path(args.uhd_deps)
    if not uhd_path.exists():
        print(
            f"error: {uhd_path} not found. Run uhd_bare_metal_installer.py first (it writes "
            f"that file), or pass --uhd-deps to point at it.",
            file=sys.stderr,
        )
        print("Aborting.", file=sys.stderr)
        return 1
    print(f"OK: found {uhd_path}.")

    # --- 3. Check for leftovers of a removed GNU Radio install ---
    stale_dirs = find_stale_install_dirs()
    if stale_dirs:
        print(
            "error: empty directories from an earlier GNU Radio install were found. They make "
            "GNU Radio's tests fail (Python imports them as empty packages). Remove them, then "
            "run this installer again:",
            file=sys.stderr,
        )
        print("  sudo rm -rf " + " ".join(str(d) for d in stale_dirs), file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1

    # --- 4. Install dependencies and build ---
    home, home_source = get_home_dir(args.home)
    print(f"\nBuild home directory: {home} (from {home_source})")
    print(f"GNU Radio branch: {args.branch}")
    steps = get_build_steps(home, args.branch, packages)
    print("\nThe following build steps will run:")
    print(f"  {describe_build_user()}")
    for step in steps:
        preview = describe_step(step)
        if len(preview) > 200:
            preview = preview[:200] + f" ... ({len(packages)} packages; truncated for display)"
        print(f"  $ (cd {step.cwd} && {preview})")

    if args.dry_run:
        print("\n--dry-run set: no commands executed.")
        return 0

    if not args.yes:
        if not _confirm("\nProceed with installing dependencies and building GNU Radio? [y/N] "):
            print("Aborted.")
            return 1

    print("\nInstalling dependencies, then cloning and building GNU Radio from source...")
    if run_build_steps(steps) != 0:
        print("\nerror: GNU Radio build failed. Aborting.", file=sys.stderr)
        return 1

    print("\nDone. GNU Radio built and installed from source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
