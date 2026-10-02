#!/usr/bin/env python3
"""
gnuradio_bare_metal_installer.py

Builds and installs GNU Radio (https://github.com/gnuradio/gnuradio) from
source on bare metal, after uhd_bare_metal_installer.py has installed the
build dependencies (and UHD).

The only package it installs is Ubuntu's libvolk-dev (Volk, which GNU Radio
requires). It:

  1. Checks that uhd-dependencies.txt (written by uhd_bare_metal_installer.py)
     exists, i.e. that the UHD installer has been run. Aborts with an error
     if it doesn't.
  2. Installs Volk, then clones, builds, and installs GNU Radio from the
     chosen branch:

         cd $HOME
         sudo apt-get install -y libvolk-dev
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

Examples
--------
  # Show the build steps without running them:
  python3 gnuradio_bare_metal_installer.py --dry-run

  # Clone/build/install GNU Radio's main branch into $HOME/gnuradio:
  python3 gnuradio_bare_metal_installer.py

  # Build the 3.10 release series instead:
  python3 gnuradio_bare_metal_installer.py --branch maint-3.10
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from uhd_bare_metal_installer import (
    DEFAULT_PACKAGE_LIST_OUTPUT as UHD_PACKAGE_LIST_OUTPUT,
    BuildStep,
    _confirm,
    describe_build_user,
    describe_step,
    get_home_dir,
    get_make_jobs,
    run_build_steps,
)

DEFAULT_BRANCH = "main"


def get_build_steps(home: str, branch: str) -> list[BuildStep]:
    """
    Return the steps equivalent to:

        cd $HOME
        sudo apt-get install -y libvolk-dev
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
        # GNU Radio needs an external Volk (>= 2.4.1); Ubuntu's package is new enough.
        # -y because this is an unattended build (the installer already asked).
        BuildStep(["sudo", "apt-get", "install", "-y", "libvolk-dev"], home),
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
            "GNU Radio branch (or tag) to check out and build, e.g. main or maint-3.10 "
            f"(default: {DEFAULT_BRANCH})."
        ),
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
        help="Check for the UHD package list and print the build steps, without running them.",
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

    # --- 1. Check that the UHD installer has been run ---
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

    # --- 2. Build ---
    home, home_source = get_home_dir(args.home)
    print(f"\nBuild home directory: {home} (from {home_source})")
    print(f"GNU Radio branch: {args.branch}")
    steps = get_build_steps(home, args.branch)
    print("\nThe following build steps will run:")
    print(f"  {describe_build_user()}")
    for step in steps:
        print(f"  $ (cd {step.cwd} && {describe_step(step)})")

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
