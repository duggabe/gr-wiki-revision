#!/usr/bin/env python3
"""
uhd_bare_metal_installer.py

Adapts EttusResearch/uhd's Docker build environment for bare-metal use:

    https://github.com/EttusResearch/uhd/blob/master/.ci/docker/uhd-builder-ubuntu2604.Dockerfile

Instead of hardcoding the package list, this program FETCHES and PARSES the
actual Dockerfile, extracts the `apt-get install` package list from its RUN
instruction, and (optionally) runs the equivalent `apt-get` commands directly
on the host instead of inside a Docker image.

By default it does not assume Ubuntu 26.04: it reads NAME and VERSION_ID from
/etc/os-release, builds a slug (e.g. "Ubuntu" + "24.04" -> "ubuntu2404"), and
looks for a matching Dockerfile in EttusResearch/uhd's .ci/docker directory.
If none matches the host OS, it aborts rather than guessing.

It does NOT build UHD itself -- like the Dockerfile it adapts, it only sets
up the build environment. See --help for usage.

Examples
--------
  # Auto-detect the host OS and just print/save the dependency list (no install):
  python3 uhd_bare_metal_installer.py --list-only

  # Show exactly what would be run, without touching the system:
  python3 uhd_bare_metal_installer.py --dry-run

  # Actually install on a bare-metal host matching one of UHD's Dockerfiles (needs root):
  sudo python3 uhd_bare_metal_installer.py

  # Skip the "apt-get upgrade" step (safer on a machine you don't want fully upgraded):
  sudo python3 uhd_bare_metal_installer.py --skip-upgrade

  # Force a specific Dockerfile instead of auto-detecting from /etc/os-release:
  python3 uhd_bare_metal_installer.py --dockerfile-url https://raw.githubusercontent.com/EttusResearch/uhd/master/.ci/docker/uhd-builder-ubuntu2604.Dockerfile

  # Install dependencies AND then clone/build/install UHD itself into $HOME/uhd:
  sudo python3 uhd_bare_metal_installer.py --build
"""

from __future__ import annotations

import argparse
import json
import os
import pwd
import re
import subprocess
import sys
import typing
import urllib.error
import urllib.request
from pathlib import Path

DOCKER_DIR_API_URL = "https://api.github.com/repos/EttusResearch/uhd/contents/.ci/docker"
DOCKER_DIR_RAW_BASE = "https://raw.githubusercontent.com/EttusResearch/uhd/master/.ci/docker"
DEFAULT_PACKAGE_LIST_OUTPUT = "uhd-dependencies.txt"


class DockerfileParseError(RuntimeError):
    pass


def fetch_dockerfile(url: str) -> str:
    """Download the Dockerfile text from a URL."""
    req = urllib.request.Request(url, headers={"User-Agent": "uhd-bare-metal-installer/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def read_dockerfile(path: str) -> str:
    """Read the Dockerfile text from a local file."""
    return Path(path).read_text(encoding="utf-8")


def extract_base_image(dockerfile_text: str) -> str | None:
    m = re.search(r"^FROM\s+(\S+)", dockerfile_text, flags=re.MULTILINE)
    return m.group(1) if m else None


def extract_apt_packages(dockerfile_text: str) -> list[str]:
    """
    Parse the `RUN apt-get update && ... apt-get -y install -q \\ <packages> \\
    && rm -rf /var/lib/apt/lists/*` block and return the list of package names,
    in the order they appear, with inline `# comment` lines preserved as
    section markers (stripped out of the returned package list itself).
    """
    # Isolate the RUN block that starts with "apt-get update" (the install block),
    # bounded by the next top-level RUN instruction (or end of file).
    start_match = re.search(r"RUN\s+apt-get update", dockerfile_text)
    if not start_match:
        raise DockerfileParseError("Could not find 'RUN apt-get update' block in Dockerfile.")

    rest = dockerfile_text[start_match.end():]
    next_run = re.search(r"\nRUN\s", rest)
    block = rest[: next_run.start()] if next_run else rest

    # Within that block, packages are the backslash-continued lines between
    # "apt-get -y install -q" and the "rm -rf /var/lib/apt/lists" line.
    install_match = re.search(r"apt-get\s+-y\s+install\s+-q", block)
    if not install_match:
        raise DockerfileParseError("Could not find 'apt-get -y install -q' in Dockerfile.")

    tail = block[install_match.end():]
    rm_match = re.search(r"rm\s+-rf\s+/var/lib/apt/lists", tail)
    package_region = tail[: rm_match.start()] if rm_match else tail

    packages: list[str] = []
    for raw_line in package_region.splitlines():
        line = raw_line.strip()
        # Strip trailing line-continuation backslash.
        line = re.sub(r"\\\s*$", "", line).strip()
        if not line:
            continue
        if line.startswith("#"):
            continue  # section-header comment, e.g. "# Install UHD dependencies"
        if line == "&&":
            continue
        # A valid Debian package name: lowercase letters, digits, + - .
        if re.fullmatch(r"[a-z0-9][a-z0-9+.\-]*", line):
            packages.append(line)
        # else: silently ignore anything unexpected rather than fail hard

    if not packages:
        raise DockerfileParseError("Parsed zero packages -- Dockerfile format may have changed.")

    return packages


def extract_pip_index_args(dockerfile_text: str) -> tuple[bool, bool]:
    """Detect whether the Dockerfile supports PIP_INDEX_URL / PIP_INDEX_HOST build args."""
    has_url = bool(re.search(r"ARG\s+PIP_INDEX_URL", dockerfile_text))
    has_host = bool(re.search(r"ARG\s+PIP_INDEX_HOST", dockerfile_text))
    return has_url, has_host


def _parse_os_release(os_release_path: Path) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in os_release_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            info[key] = value.strip().strip('"')
    return info


def get_host_os_slug(os_release_path: str = "/etc/os-release") -> tuple[str, str, str]:
    """
    Reads NAME and VERSION_ID from /etc/os-release and derives a slug used to
    find the matching Dockerfile, e.g. NAME="Ubuntu", VERSION_ID="24.04" ->
    slug "ubuntu2404" (concatenated, lower-cased, periods removed).

    Returns (slug, name, version_id). Raises RuntimeError if os-release is
    missing or lacks the needed fields.
    """
    path = Path(os_release_path)
    if not path.exists():
        raise RuntimeError(f"{os_release_path} not found; cannot determine host OS.")

    info = _parse_os_release(path)
    name = info.get("NAME")
    version_id = info.get("VERSION_ID")
    if not name or not version_id:
        raise RuntimeError(
            f"NAME and/or VERSION_ID missing from {os_release_path}; cannot determine host OS."
        )

    slug = (name + version_id).lower().replace(".", "").replace(" ", "")
    return slug, name, version_id


def find_dockerfile_filename_for_slug(slug: str) -> str | None:
    """
    Looks up EttusResearch/uhd's .ci/docker directory (via the GitHub API) for
    a Dockerfile whose name contains the given OS slug -- e.g. slug
    "ubuntu2604" matches "uhd-builder-ubuntu2604.Dockerfile". Returns the
    matching filename, or None if no file in the directory matches.
    """
    req = urllib.request.Request(
        DOCKER_DIR_API_URL,
        headers={
            "User-Agent": "uhd-bare-metal-installer/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        listing = json.load(resp)

    candidates = [
        entry["name"]
        for entry in listing
        if entry.get("type") == "file" and slug in entry["name"].lower()
    ]
    if not candidates:
        return None

    # Prefer an exact "uhd-builder-<slug>.dockerfile" match if there is one.
    exact = f"uhd-builder-{slug}.dockerfile"
    for name in candidates:
        if name.lower() == exact:
            return name
    return sorted(candidates)[0]


def build_commands(
    packages: list[str],
    skip_upgrade: bool,
    pip_index_url: str | None,
    pip_index_host: str | None,
) -> list[list[str]]:
    """Build the ordered list of shell commands equivalent to the Dockerfile's RUN steps."""
    commands: list[list[str]] = [["apt-get", "update"]]
    if not skip_upgrade:
        commands.append(["apt-get", "-y", "upgrade"])
    commands.append(["apt-get", "-y", "install", "-q", *packages])

    if pip_index_url:
        commands.append(
            ["python3", "-m", "pip", "config", "--global", "set", "global.index-url", pip_index_url]
        )
        if pip_index_host:
            commands.append(
                ["python3", "-m", "pip", "config", "--global", "set", "global.trusted-host", pip_index_host]
            )

    return commands


def run_command(cmd: list[str], env: dict) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=env)


def get_home_dir(explicit_home: str | None = None) -> tuple[str, str]:
    """
    Resolve the home directory to clone/build UHD into. Returns (path, source)
    where source describes how it was chosen, for logging.

    `sudo` resets $HOME to the target user's home (e.g. /root) by default,
    even without -H, because `always_set_home` is on by default on
    Debian/Ubuntu. That means a plain os.environ.get("HOME") inside
    `sudo python3 ...` returns /root instead of the invoking user's home. To
    build into the invoking user's home instead (matching what most people
    expect when they run `sudo <this script> --build`), this prefers the
    SUDO_USER sudo sets, falling back to $HOME / the current user's home.

    --home always wins, for explicit control.
    """
    if explicit_home:
        return os.path.expanduser(explicit_home), "--home"

    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user and sudo_user != "root":
        try:
            return pwd.getpwnam(sudo_user).pw_dir, f"home of SUDO_USER={sudo_user}"
        except KeyError:
            pass  # fall through if the user lookup fails

    return os.environ.get("HOME", os.path.expanduser("~")), "$HOME"


def get_make_jobs() -> int:
    """
    Number of parallel make jobs: nproc - 1 (i.e. leave one core free), like
    `-j$(nproc)-1`. Falls back to 1 if the core count can't be determined or
    the host only has a single core.
    """
    nproc = os.cpu_count() or 2
    return max(1, nproc - 1)


class BuildStep(typing.NamedTuple):
    cmd: list[str]
    cwd: str
    env_extra: dict[str, str] | None = None  # overlaid onto the subprocess env
    capture: bool = False  # if True, capture stdout/stderr and print in a labeled block
    label: str | None = None  # heading used when capture=True
    tolerate_failure: bool = False  # if True, a non-zero exit is a warning, not an abort


def get_build_steps(home: str) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd $HOME/
        git clone https://github.com/EttusResearch/uhd.git
        cd $HOME/uhd/host && mkdir build && cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
        make -j$(nproc)-1
        sudo make install
        sudo ldconfig
        export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
        uhd_find_devices
        sudo uhd_images_downloader
        cd $HOME/uhd/host/utils
        sudo cp uhd-usrp.rules /etc/udev/rules.d/
        sudo udevadm control --reload-rules
        sudo udevadm trigger
    """
    host_dir = os.path.join(home, "uhd", "host")
    build_dir = os.path.join(host_dir, "build")
    utils_dir = os.path.join(host_dir, "utils")
    jobs = get_make_jobs()

    # `export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH` is a shell builtin,
    # not a command -- it's applied here as an env overlay for the steps after it,
    # rather than a subprocess call.
    ld_library_path = "/usr/local/lib:" + os.environ.get("LD_LIBRARY_PATH", "")
    post_ldconfig_env = {"LD_LIBRARY_PATH": ld_library_path}

    return [
        BuildStep(["git", "clone", "https://github.com/EttusResearch/uhd.git"], home),
        BuildStep(["mkdir", "build"], host_dir),
        BuildStep(["cmake", "-DCMAKE_INSTALL_PREFIX=/usr/local", "../"], build_dir),
        BuildStep(["make", f"-j{jobs}"], build_dir),
        BuildStep(["sudo", "make", "install"], build_dir),
        BuildStep(["sudo", "ldconfig"], build_dir),
        BuildStep(
            ["uhd_find_devices"], build_dir,
            env_extra=post_ldconfig_env, capture=True, label="uhd_find_devices output",
            # uhd_find_devices exits non-zero when no USRP hardware is attached --
            # that's not a build failure, so don't abort the rest of the build over it.
            tolerate_failure=True,
        ),
        BuildStep(["sudo", "uhd_images_downloader"], build_dir, env_extra=post_ldconfig_env),
        BuildStep(["sudo", "cp", "uhd-usrp.rules", "/etc/udev/rules.d/"], utils_dir),
        BuildStep(["sudo", "udevadm", "control", "--reload-rules"], utils_dir),
        BuildStep(["sudo", "udevadm", "trigger"], utils_dir),
    ]


def build_uhd_from_source(home: str) -> int:
    """
    Runs the clone/configure/build/install/verify steps from get_build_steps()
    in order. Aborts on the first command that fails (non-zero exit, or
    missing executable/working directory) and returns 1; returns 0 if all
    succeed. A step with tolerate_failure=True (uhd_find_devices, which exits
    non-zero simply when no USRP hardware is attached) only warns on failure
    and lets the build continue.
    """
    for step in get_build_steps(home):
        env = None
        if step.env_extra:
            env = os.environ.copy()
            env.update(step.env_extra)

        print(f"\n$ (cd {step.cwd} && {' '.join(step.cmd)})")
        try:
            if step.capture:
                result = subprocess.run(
                    step.cmd, cwd=step.cwd, env=env, check=True,
                    capture_output=True, text=True,
                )
                heading = step.label or " ".join(step.cmd)
                print(f"\n----- {heading} -----")
                sys.stdout.write(result.stdout)
                if result.stderr:
                    sys.stderr.write(result.stderr)
                print(f"----- end {heading} -----")
            else:
                subprocess.run(step.cmd, cwd=step.cwd, env=env, check=True)
        except subprocess.CalledProcessError as exc:
            if step.capture:
                if exc.stdout:
                    heading = step.label or " ".join(step.cmd)
                    print(f"\n----- {heading} -----")
                    sys.stdout.write(exc.stdout)
                    print(f"----- end {heading} -----")
                if exc.stderr:
                    sys.stderr.write(exc.stderr)

            if step.tolerate_failure:
                print(
                    f"\nwarning: '{' '.join(step.cmd)}' exited with code {exc.returncode} "
                    "(continuing -- this is expected if no USRP hardware is attached).",
                    file=sys.stderr,
                )
                continue

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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Adapt the UHD Ubuntu 26.04 Docker build environment for bare-metal installation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dockerfile-url", default=None,
        help=(
            "URL of the Dockerfile to fetch. Default: auto-detect from /etc/os-release "
            "and look up the matching file in EttusResearch/uhd's .ci/docker directory."
        ),
    )
    parser.add_argument(
        "--dockerfile-path", default=None,
        help="Read the Dockerfile from a local path instead of fetching it.",
    )
    parser.add_argument(
        "--list-only", action="store_true",
        help="Only parse and print/save the dependency list; do not install anything.",
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_PACKAGE_LIST_OUTPUT,
        help=f"Path to save the extracted package list (default: {DEFAULT_PACKAGE_LIST_OUTPUT}).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the apt/pip commands that would run, without executing or requiring root.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before installing.",
    )
    parser.add_argument(
        "--skip-upgrade", action="store_true",
        help="Skip 'apt-get upgrade' (recommended on a machine you don't want fully upgraded).",
    )
    parser.add_argument("--pip-index-url", default=os.environ.get("PIP_INDEX_URL"))
    parser.add_argument("--pip-index-host", default=os.environ.get("PIP_INDEX_HOST"))
    parser.add_argument(
        "--os-release-path", default="/etc/os-release",
        help="Path to read NAME/VERSION_ID from for OS auto-detection (default: /etc/os-release).",
    )
    parser.add_argument(
        "--build", action="store_true",
        help=(
            "After dependencies install successfully, also clone and build UHD itself "
            "into <home>/uhd (git clone, cmake, make -j(nproc-1), sudo make install, sudo ldconfig, "
            "uhd_find_devices, sudo uhd_images_downloader, then installs the udev rules and "
            "triggers udevadm so USRPs are usable without root). "
            "Aborts with exit code 1 if any build step fails."
        ),
    )
    parser.add_argument(
        "--home", default=None,
        help=(
            "Directory to clone/build UHD into (used with --build), overriding auto-detection. "
            "Default: the invoking user's home when run via sudo (SUDO_USER), else $HOME."
        ),
    )
    args = parser.parse_args()

    # --- 1. Get the Dockerfile text ---
    try:
        if args.dockerfile_path:
            print(f"Reading Dockerfile from local path: {args.dockerfile_path}")
            dockerfile_text = read_dockerfile(args.dockerfile_path)
        elif args.dockerfile_url:
            print(f"Fetching Dockerfile from: {args.dockerfile_url}")
            dockerfile_text = fetch_dockerfile(args.dockerfile_url)
        else:
            # Auto-detect the matching Dockerfile from the host's /etc/os-release.
            try:
                slug, os_name, os_version = get_host_os_slug(args.os_release_path)
            except RuntimeError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
            print(f"Detected host OS: {os_name} {os_version} -> slug '{slug}'")

            try:
                filename = find_dockerfile_filename_for_slug(slug)
            except (OSError, urllib.error.URLError) as exc:
                print(f"error: failed to list {DOCKER_DIR_API_URL}: {exc}", file=sys.stderr)
                return 1

            if not filename:
                print(
                    f"error: no Dockerfile matching host OS slug '{slug}' was found in "
                    f"EttusResearch/uhd's .ci/docker directory "
                    f"({DOCKER_DIR_API_URL}). Aborting -- pass --dockerfile-url or "
                    f"--dockerfile-path to use a specific Dockerfile instead.",
                    file=sys.stderr,
                )
                return 1

            dockerfile_url = f"{DOCKER_DIR_RAW_BASE}/{filename}"
            print(f"Found matching Dockerfile: {filename}")
            print(f"Fetching Dockerfile from: {dockerfile_url}")
            dockerfile_text = fetch_dockerfile(dockerfile_url)
    except (OSError, urllib.error.URLError) as exc:
        print(f"error: failed to obtain Dockerfile: {exc}", file=sys.stderr)
        return 1

    # --- 2. Parse it ---
    try:
        base_image = extract_base_image(dockerfile_text)
        packages = extract_apt_packages(dockerfile_text)
        has_pip_url_arg, has_pip_host_arg = extract_pip_index_args(dockerfile_text)
    except DockerfileParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Base image declared in Dockerfile: {base_image}")
    print(f"Extracted {len(packages)} apt packages.")

    # Save the extracted list for reference regardless of mode.
    out_path = Path(args.output)
    out_path.write_text("\n".join(packages) + "\n", encoding="utf-8")
    print(f"Package list written to: {out_path.resolve()}")

    if args.list_only:
        print("\n--list-only set: not installing anything.")
        for pkg in packages:
            print(f"  {pkg}")
        return 0

    # --- 3. Build commands ---
    # (No separate OS-compatibility check here: the Dockerfile fetched above was
    # already selected to match this host's /etc/os-release, or was explicitly
    # provided via --dockerfile-url/--dockerfile-path.)
    commands = build_commands(
        packages,
        skip_upgrade=args.skip_upgrade,
        pip_index_url=args.pip_index_url,
        pip_index_host=args.pip_index_host,
    )

    print("\nThe following commands will run:")
    for cmd in commands:
        preview = " ".join(cmd)
        if len(preview) > 200:
            preview = preview[:200] + " ... (truncated for display)"
        print(f"  $ {preview}")

    home, home_source = get_home_dir(args.home)
    print(f"\nBuild home directory: {home} (from {home_source})")
    if args.build:
        print("\n--build set: after dependencies install, will also run:")
        for step in get_build_steps(home):
            env_note = f"  [env: {step.env_extra}]" if step.env_extra else ""
            print(f"  $ (cd {step.cwd} && {' '.join(step.cmd)}){env_note}")

    if args.dry_run:
        print("\n--dry-run set: no commands executed.")
        return 0

    # --- 4. Root check ---
    if os.geteuid() != 0:
        print(
            "\nerror: installing packages requires root. Re-run with sudo, "
            "or use --dry-run / --list-only to inspect without installing.",
            file=sys.stderr,
        )
        return 1

    # --- 5. Confirm ---
    if not args.yes:
        if not _confirm("\nProceed with installation on this machine? [y/N] "):
            print("Aborted.")
            return 1

    # --- 6. Execute ---
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    try:
        for cmd in commands:
            run_command(cmd, env)
    except subprocess.CalledProcessError as exc:
        print(f"\nerror: command failed with exit code {exc.returncode}: {' '.join(exc.cmd)}", file=sys.stderr)
        return exc.returncode

    print("\nDone. Build dependencies installed.")

    if not args.build:
        print("\nNext steps to actually build UHD (not covered by the Dockerfile either):")
        print(f"  cd {home}/")
        print("  git clone https://github.com/EttusResearch/uhd.git")
        print(f"  cd {home}/uhd/host && mkdir build && cd build")
        print("  cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../")
        print(f"  make -j{get_make_jobs()}")
        print("  sudo make install")
        print("  sudo ldconfig")
        print("  export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH")
        print("  uhd_find_devices")
        print("  sudo uhd_images_downloader")
        print(f"  cd {home}/uhd/host/utils")
        print("  sudo cp uhd-usrp.rules /etc/udev/rules.d/")
        print("  sudo udevadm control --reload-rules")
        print("  sudo udevadm trigger")
        return 0

    print("\n--build set: cloning and building UHD from source...")
    build_result = build_uhd_from_source(home)
    if build_result != 0:
        print("\nerror: UHD build failed. Aborting.", file=sys.stderr)
        return 1

    print("\nDone. UHD built and installed from source.")
    return 0


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


if __name__ == "__main__":
    sys.exit(main())
