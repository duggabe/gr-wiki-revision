#!/usr/bin/env python3
"""
volk_bare_metal_installer.py

Builds and installs Volk (https://github.com/gnuradio/volk) from source on
bare metal, after UHD's build dependencies have already been installed by
uhd_bare_metal_installer.py.

Volk needs no dependencies beyond the ones UHD's Docker build environment
already provides, so this program does not install any packages. Instead it:

  1. Re-derives the dependency list the same way `uhd_bare_metal_installer.py
     --list-only` does (auto-detecting the host OS and parsing the matching
     EttusResearch/uhd Dockerfile) and saves it to volk-dependencies.txt.
  2. Verifies that uhd-dependencies.txt (written by the earlier
     uhd_bare_metal_installer.py run) was created before volk-dependencies.txt
     and has the same content -- i.e. that the dependencies installed for UHD
     are still the current ones. Aborts with an error if either check fails.
  3. Clones, builds, and installs Volk:

         cd $HOME
         git clone --recursive https://github.com/gnuradio/volk.git
         cd $HOME/volk && mkdir build && cd build
         cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
         make -j$(nproc)-1
         sudo make install
         sudo ldconfig

Examples
--------
  # Just print/save the dependency list to volk-dependencies.txt (no build):
  python3 volk_bare_metal_installer.py --list-only

  # Check the dependency lists and show the build steps, without running them:
  python3 volk_bare_metal_installer.py --dry-run

  # Check the dependency lists, then clone/build/install Volk into $HOME/volk:
  python3 volk_bare_metal_installer.py
"""

from __future__ import annotations

import argparse
import os
import sys
import typing
import urllib.error
from pathlib import Path

from uhd_bare_metal_installer import (
    DEFAULT_PACKAGE_LIST_OUTPUT as UHD_PACKAGE_LIST_OUTPUT,
    DOCKER_DIR_API_URL,
    DOCKER_DIR_RAW_BASE,
    BuildStep,
    DockerfileParseError,
    _confirm,
    extract_apt_packages,
    extract_base_image,
    fetch_dockerfile,
    find_dockerfile_filename_for_slug,
    get_home_dir,
    get_host_os_slug,
    get_make_jobs,
    read_dockerfile,
    run_build_steps,
)

DEFAULT_PACKAGE_LIST_OUTPUT = "volk-dependencies.txt"


def get_dockerfile_text(args: argparse.Namespace) -> str:
    """
    Obtain the Dockerfile text exactly as uhd_bare_metal_installer.py does:
    from --dockerfile-path, --dockerfile-url, or by auto-detecting the host OS.
    Raises RuntimeError with a user-facing message on failure.
    """
    try:
        if args.dockerfile_path:
            print(f"Reading Dockerfile from local path: {args.dockerfile_path}")
            return read_dockerfile(args.dockerfile_path)
        if args.dockerfile_url:
            print(f"Fetching Dockerfile from: {args.dockerfile_url}")
            return fetch_dockerfile(args.dockerfile_url)

        slug, os_name, os_version = get_host_os_slug(args.os_release_path)
        print(f"Detected host OS: {os_name} {os_version} -> slug '{slug}'")

        try:
            filename = find_dockerfile_filename_for_slug(slug)
        except (OSError, urllib.error.URLError) as exc:
            raise RuntimeError(f"failed to list {DOCKER_DIR_API_URL}: {exc}") from exc

        if not filename:
            raise RuntimeError(
                f"no Dockerfile matching host OS slug '{slug}' was found in "
                f"EttusResearch/uhd's .ci/docker directory ({DOCKER_DIR_API_URL}). "
                f"Aborting -- pass --dockerfile-url or --dockerfile-path to use a "
                f"specific Dockerfile instead."
            )

        dockerfile_url = f"{DOCKER_DIR_RAW_BASE}/{filename}"
        print(f"Found matching Dockerfile: {filename}")
        print(f"Fetching Dockerfile from: {dockerfile_url}")
        return fetch_dockerfile(dockerfile_url)
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(f"failed to obtain Dockerfile: {exc}") from exc


class DependencyList(typing.NamedTuple):
    path: Path
    installer: str  # the program that writes this file
    option: str  # command-line option that points at this file


def check_dependency_lists(lists: list[DependencyList]) -> list[str]:
    """
    Verify that the given dependency-list files were created in the given
    order and all have the same content. Returns a list of error messages
    (empty if both checks pass).

    Linux filesystems don't reliably expose a file's creation time, so
    "created before" is judged by modification time -- each file is written
    in full by its installer, so its mtime is when that list was created.
    """
    missing = [
        f"{dep.path} not found. Run {dep.installer} first (it writes that file), "
        f"or pass {dep.option} to point at it."
        for dep in lists
        if not dep.path.exists()
    ]
    if missing:
        return missing

    errors = []
    for earlier, later in zip(lists, lists[1:]):
        if not earlier.path.stat().st_mtime < later.path.stat().st_mtime:
            errors.append(f"{earlier.path} was not created before {later.path}.")

    first = lists[0]
    first_text = first.path.read_text(encoding="utf-8")
    for dep in lists[1:]:
        if dep.path.read_text(encoding="utf-8") != first_text:
            errors.append(
                f"{first.path} and {dep.path} have different content -- the upstream "
                f"Dockerfile has changed since UHD's dependencies were installed. "
                f"Re-run {first.installer} to install the current dependencies, then "
                f"refresh the later lists in order with --list-only."
            )
    return errors


def format_ok_message(lists: list[DependencyList]) -> str:
    names = ", ".join(str(dep.path) for dep in lists)
    return f"OK: {names} were created in that order and have the same content."


def get_build_steps(home: str) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd $HOME
        git clone --recursive https://github.com/gnuradio/volk.git
        cd $HOME/volk && mkdir build && cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
        make -j$(nproc)-1
        sudo make install
        sudo ldconfig
    """
    volk_dir = os.path.join(home, "volk")
    build_dir = os.path.join(volk_dir, "build")
    jobs = get_make_jobs()

    return [
        BuildStep(["git", "clone", "--recursive", "https://github.com/gnuradio/volk.git"], home),
        BuildStep(["mkdir", "build"], volk_dir),
        BuildStep(["cmake", "-DCMAKE_INSTALL_PREFIX=/usr/local", "../"], build_dir),
        BuildStep(["make", f"-j{jobs}"], build_dir),
        BuildStep(["sudo", "make", "install"], build_dir),
        BuildStep(["sudo", "ldconfig"], build_dir),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and install Volk from source on bare metal, after UHD's dependencies.",
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
        "--os-release-path", default="/etc/os-release",
        help="Path to read NAME/VERSION_ID from for OS auto-detection (default: /etc/os-release).",
    )
    parser.add_argument(
        "--list-only", action="store_true",
        help="Only parse and print/save the dependency list; do not check or build anything.",
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_PACKAGE_LIST_OUTPUT,
        help=f"Path to save the extracted package list (default: {DEFAULT_PACKAGE_LIST_OUTPUT}).",
    )
    parser.add_argument(
        "--uhd-deps", default=UHD_PACKAGE_LIST_OUTPUT,
        help=(
            "Package list written by uhd_bare_metal_installer.py to compare against "
            f"(default: {UHD_PACKAGE_LIST_OUTPUT})."
        ),
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Check the dependency lists and print the build steps, without running them.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before building.",
    )
    parser.add_argument(
        "--build", action="store_true",
        help=(
            "Accepted for consistency with uhd_bare_metal_installer.py and ignored: "
            "building Volk is already the default."
        ),
    )
    parser.add_argument(
        "--home", default=None,
        help=(
            "Directory to clone/build Volk into, overriding auto-detection. "
            "Default: the invoking user's home when run via sudo (SUDO_USER), else $HOME."
        ),
    )
    args = parser.parse_args()

    # --- 1. Derive the dependency list and save it ---
    try:
        dockerfile_text = get_dockerfile_text(args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        base_image = extract_base_image(dockerfile_text)
        packages = extract_apt_packages(dockerfile_text)
    except DockerfileParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Base image declared in Dockerfile: {base_image}")
    print(f"Extracted {len(packages)} apt packages.")

    volk_path = Path(args.output)
    volk_path.write_text("\n".join(packages) + "\n", encoding="utf-8")
    print(f"Package list written to: {volk_path.resolve()}")

    if args.list_only:
        print("\n--list-only set: not checking or building anything.")
        for pkg in packages:
            print(f"  {pkg}")
        return 0

    # --- 2. Compare against the list UHD's installer wrote ---
    dep_lists = [
        DependencyList(Path(args.uhd_deps), "uhd_bare_metal_installer.py", "--uhd-deps"),
        DependencyList(volk_path, "volk_bare_metal_installer.py", "-o"),
    ]
    errors = check_dependency_lists(dep_lists)
    if errors:
        for msg in errors:
            print(f"error: {msg}", file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1
    print(format_ok_message(dep_lists))

    # --- 3. Build ---
    home, home_source = get_home_dir(args.home)
    print(f"\nBuild home directory: {home} (from {home_source})")
    steps = get_build_steps(home)
    print("\nThe following build steps will run:")
    for step in steps:
        print(f"  $ (cd {step.cwd} && {' '.join(step.cmd)})")

    if args.dry_run:
        print("\n--dry-run set: no commands executed.")
        return 0

    if not args.yes:
        if not _confirm("\nProceed with building and installing Volk? [y/N] "):
            print("Aborted.")
            return 1

    print("\nCloning and building Volk from source...")
    if run_build_steps(steps) != 0:
        print("\nerror: Volk build failed. Aborting.", file=sys.stderr)
        return 1

    print("\nDone. Volk built and installed from source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
