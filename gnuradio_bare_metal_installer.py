#!/usr/bin/env python3
"""
gnuradio_bare_metal_installer.py

Builds and installs GNU Radio (https://github.com/gnuradio/gnuradio) from
source on bare metal, after uhd_bare_metal_installer.py has installed the
build dependencies and volk_bare_metal_installer.py has installed Volk.

Like the Volk installer, this program does not install any packages. It:

  1. Re-derives the dependency list the same way `uhd_bare_metal_installer.py
     --list-only` does (auto-detecting the host OS and parsing the matching
     EttusResearch/uhd Dockerfile) and saves it to gnuradio-dependencies.txt.
  2. Verifies that uhd-dependencies.txt, volk-dependencies.txt, and
     gnuradio-dependencies.txt were created in that order and all have the
     same content -- i.e. that UHD's dependencies and Volk were installed
     first, against the current dependency list. Aborts with an error if
     either check fails.
  3. Clones, builds, and installs GNU Radio:

         cd $HOME
         git clone https://github.com/gnuradio/gnuradio.git
         cd $HOME/gnuradio && mkdir build && cd build
         cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
         make -j$(nproc)-1
         sudo make install
         sudo ldconfig

Examples
--------
  # Just print/save the dependency list to gnuradio-dependencies.txt (no build):
  python3 gnuradio_bare_metal_installer.py --list-only

  # Check the dependency lists and show the build steps, without running them:
  python3 gnuradio_bare_metal_installer.py --dry-run

  # Check the dependency lists, then clone/build/install GNU Radio into $HOME/gnuradio:
  python3 gnuradio_bare_metal_installer.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from uhd_bare_metal_installer import (
    DEFAULT_PACKAGE_LIST_OUTPUT as UHD_PACKAGE_LIST_OUTPUT,
    BuildStep,
    DockerfileParseError,
    _confirm,
    describe_build_user,
    extract_apt_packages,
    extract_base_image,
    get_home_dir,
    get_make_jobs,
    run_build_steps,
)
from volk_bare_metal_installer import (
    DEFAULT_PACKAGE_LIST_OUTPUT as VOLK_PACKAGE_LIST_OUTPUT,
    DependencyList,
    check_dependency_lists,
    format_ok_message,
    get_dockerfile_text,
)

DEFAULT_PACKAGE_LIST_OUTPUT = "gnuradio-dependencies.txt"


def get_build_steps(home: str) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd $HOME
        git clone https://github.com/gnuradio/gnuradio.git
        cd $HOME/gnuradio && mkdir build && cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
        make -j$(nproc)-1
        sudo make install
        sudo ldconfig
    """
    gnuradio_dir = os.path.join(home, "gnuradio")
    build_dir = os.path.join(gnuradio_dir, "build")
    jobs = get_make_jobs()

    return [
        BuildStep(["git", "clone", "https://github.com/gnuradio/gnuradio.git"], home),
        BuildStep(["mkdir", "build"], gnuradio_dir),
        BuildStep(["cmake", "-DCMAKE_INSTALL_PREFIX=/usr/local", "../"], build_dir),
        BuildStep(["make", f"-j{jobs}"], build_dir),
        BuildStep(["sudo", "make", "install"], build_dir),
        BuildStep(["sudo", "ldconfig"], build_dir),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and install GNU Radio from source on bare metal, after UHD and Volk.",
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
        "--volk-deps", default=VOLK_PACKAGE_LIST_OUTPUT,
        help=(
            "Package list written by volk_bare_metal_installer.py to compare against "
            f"(default: {VOLK_PACKAGE_LIST_OUTPUT})."
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

    gnuradio_path = Path(args.output)
    gnuradio_path.write_text("\n".join(packages) + "\n", encoding="utf-8")
    print(f"Package list written to: {gnuradio_path.resolve()}")

    if args.list_only:
        print("\n--list-only set: not checking or building anything.")
        for pkg in packages:
            print(f"  {pkg}")
        return 0

    # --- 2. Compare against the lists the UHD and Volk installers wrote ---
    dep_lists = [
        DependencyList(Path(args.uhd_deps), "uhd_bare_metal_installer.py", "--uhd-deps"),
        DependencyList(Path(args.volk_deps), "volk_bare_metal_installer.py", "--volk-deps"),
        DependencyList(gnuradio_path, "gnuradio_bare_metal_installer.py", "-o"),
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
    print(f"  {describe_build_user()}")
    for step in steps:
        print(f"  $ (cd {step.cwd} && {' '.join(step.cmd)})")

    if args.dry_run:
        print("\n--dry-run set: no commands executed.")
        return 0

    if not args.yes:
        if not _confirm("\nProceed with building and installing GNU Radio? [y/N] "):
            print("Aborted.")
            return 1

    print("\nCloning and building GNU Radio from source...")
    if run_build_steps(steps) != 0:
        print("\nerror: GNU Radio build failed. Aborting.", file=sys.stderr)
        return 1

    print("\nDone. GNU Radio built and installed from source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
