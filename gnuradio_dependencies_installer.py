#!/usr/bin/env python3
"""
gnuradio_dependencies_installer.py

Step 1 of building GNU Radio from source on bare metal: installs UHD (the
USRP Hardware Driver) from Ettus Research's PPA and everything GNU Radio
needs to build and run, all with apt. Nothing is compiled here; building
GNU Radio itself is Step 2.

It runs the equivalent of:

    # enable "Source code" (deb-src) in /etc/apt/sources.list.d/ubuntu.sources,
    # which `apt-get build-dep` needs
    sudo apt-get update
    sudo apt-get install -y software-properties-common git
    sudo add-apt-repository -y ppa:ettusresearch/uhd
    sudo apt-get install -y --no-install-recommends uhd-host libuhd-dev
    sudo apt-get build-dep -y gnuradio
    sudo apt-get install -y python3-qtpy python3-pyqtgraph python3-matplotlib soapysdr-tools
    sudo uhd_images_downloader

Notes on those steps:

  * UHD's packages recommend Ubuntu's own gnuradio packages, so they are
    installed with --no-install-recommends. Otherwise Ubuntu's GNU Radio would
    be installed into /usr, next to the one you are about to build.
  * `apt-get build-dep gnuradio` installs the build dependencies of Ubuntu's
    gnuradio package for this Ubuntu release, so the list is never hardcoded
    here. That includes libuhd-dev, which the PPA (added first) provides.
  * The last apt-get line adds run-time packages that a build-dependency list
    doesn't cover.
  * The uhd-host package installs the udev rules for USRPs itself.

Before changing anything, it stops if it finds something that would conflict:
Ubuntu's gnuradio package already installed, or a UHD built from source in
/usr/local (GNU Radio's cmake would find that one first).

Examples
--------
  # Show what would be done, without changing anything (no root needed):
  python3 gnuradio_dependencies_installer.py --dry-run

  # Install UHD and GNU Radio's dependencies:
  sudo python3 gnuradio_dependencies_installer.py

  # The same, without downloading the USRP FPGA images:
  sudo python3 gnuradio_dependencies_installer.py --no-images
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

UHD_PPA = "ppa:ettusresearch/uhd"
UBUNTU_SOURCES = "/etc/apt/sources.list.d/ubuntu.sources"

# Needed by the steps themselves: add-apt-repository, and git for Step 2's clone.
TOOL_PACKAGES = ["software-properties-common", "git"]

# UHD from the PPA. uhd-host depends on python3-uhd and the UHD library.
UHD_PACKAGES = ["uhd-host", "libuhd-dev"]

# Run-time dependencies that a build-dependency list doesn't cover.
EXTRA_PACKAGES = {
    "python3-qtpy": "imported by GNU Radio's Python code at run time",
    "python3-pyqtgraph": "needed by the filter design tool at run time",
    "python3-matplotlib": "imported by GNU Radio's examples and gr-qtgui Python code at run time",
    "soapysdr-tools": "provides SoapySDRUtil, for checking SoapySDR devices used with gr-soapy",
}

# Ubuntu's own GNU Radio, which must not be installed next to a source build.
CONFLICTING_PACKAGES = ["gnuradio", "gnuradio-dev"]

# Where a UHD built from source (e.g. by uhd_bare_metal_installer.py) keeps its files.
SOURCE_UHD_PREFIX = "/usr/local"
SOURCE_UHD_PATTERNS = (
    "lib/libuhd.so*",
    "bin/uhd_find_devices",
    "include/uhd.hpp",
    "lib/cmake/uhd",
)


def _parse_os_release(os_release_path: Path) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in os_release_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            info[key.strip()] = value.strip().strip('"')
    return info


def enable_source_code(sources_text: str) -> tuple[str, int]:
    """
    Return the deb822 sources text with "Source code" enabled, i.e. every
    `Types: deb` line changed to `Types: deb deb-src` (what the "Software &
    Updates" app's "Source code" box does), and the number of lines changed.
    Lines that already list deb-src are left alone.
    """
    return re.subn(r"^(Types:[ \t]*deb)[ \t]*$", r"\1 deb-src", sources_text, flags=re.MULTILINE)


def has_types_lines(sources_text: str) -> bool:
    return re.search(r"^Types:", sources_text, flags=re.MULTILINE) is not None


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


def find_source_built_uhd(prefix: str = SOURCE_UHD_PREFIX) -> list[Path]:
    """Files or directories of a UHD built from source and installed under the prefix."""
    found = []
    for pattern in SOURCE_UHD_PATTERNS:
        found.extend(sorted(Path(prefix).glob(pattern)))
    return found


def get_commands(download_images: bool) -> list[list[str]]:
    """The commands run (as root) after "Source code" has been enabled."""
    commands = [
        ["apt-get", "update"],
        ["apt-get", "install", "-y", *TOOL_PACKAGES],
        # add-apt-repository also refreshes the package lists.
        ["add-apt-repository", "-y", UHD_PPA],
        ["apt-get", "install", "-y", "--no-install-recommends", *UHD_PACKAGES],
        ["apt-get", "build-dep", "-y", "gnuradio"],
        ["apt-get", "install", "-y", *EXTRA_PACKAGES],
    ]
    if download_images:
        commands.append(["uhd_images_downloader"])
    return commands


def run_command(cmd: list[str], env: dict) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=env)


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install UHD from the Ettus PPA and GNU Radio's dependencies with apt.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Run the checks and print what would be done, without changing anything or requiring root.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before installing.",
    )
    parser.add_argument(
        "--no-images", action="store_true",
        help="Do not run uhd_images_downloader (the USRP FPGA images, a large download).",
    )
    parser.add_argument(
        "--sources-path", default=UBUNTU_SOURCES,
        help=f"Ubuntu's apt sources file, in which to enable source code (default: {UBUNTU_SOURCES}).",
    )
    parser.add_argument(
        "--os-release-path", default="/etc/os-release",
        help="Path to read the OS name and version from (default: /etc/os-release).",
    )
    args = parser.parse_args()

    # --- 1. Check the host OS ---
    try:
        info = _parse_os_release(Path(args.os_release_path))
    except OSError as exc:
        print(f"error: could not read {args.os_release_path}: {exc}", file=sys.stderr)
        return 1
    if info.get("ID") != "ubuntu":
        print(
            f"error: {args.os_release_path} doesn't describe an Ubuntu release "
            f"(ID={info.get('ID')!r}). The Ettus PPA only has packages for Ubuntu. Aborting.",
            file=sys.stderr,
        )
        return 1
    print(f"Detected host OS: Ubuntu {info.get('VERSION_ID', '?')} ({info.get('VERSION_CODENAME', '?')})")

    # --- 2. Check for things that would conflict ---
    conflicting = installed_packages(CONFLICTING_PACKAGES)
    if conflicting:
        print(
            "error: Ubuntu's own GNU Radio is installed (" + ", ".join(conflicting) + "). It would "
            "sit next to the GNU Radio you are about to build from source. Remove it, then run "
            "this installer again:",
            file=sys.stderr,
        )
        print("  sudo apt-get remove " + " ".join(conflicting), file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1

    source_uhd = find_source_built_uhd()
    if source_uhd:
        print(
            f"error: a UHD built from source was found under {SOURCE_UHD_PREFIX}:",
            file=sys.stderr,
        )
        for path in source_uhd:
            print(f"  {path}", file=sys.stderr)
        print(
            "GNU Radio's cmake would find it before the PPA's UHD. Remove it, then run this "
            "installer again. From the build directory it was installed from (e.g. "
            "~/uhd/host/build):",
            file=sys.stderr,
        )
        print("  sudo xargs rm -f < install_manifest.txt", file=sys.stderr)
        print(
            f"  sudo rm -rf {SOURCE_UHD_PREFIX}/include/uhd {SOURCE_UHD_PREFIX}/lib/uhd "
            f"{SOURCE_UHD_PREFIX}/lib/cmake/uhd {SOURCE_UHD_PREFIX}/share/uhd",
            file=sys.stderr,
        )
        print("  sudo ldconfig", file=sys.stderr)
        print("Aborting.", file=sys.stderr)
        return 1
    print("OK: no conflicting GNU Radio packages or source-built UHD found.")

    # --- 3. Work out the change to Ubuntu's sources file ---
    sources_path = Path(args.sources_path)
    try:
        sources_text = sources_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(
            f"error: could not read {sources_path}: {exc}. Enable 'Source code' in the "
            f"'Software & Updates' app instead, or pass --sources-path. Aborting.",
            file=sys.stderr,
        )
        return 1
    if not has_types_lines(sources_text):
        print(
            f"error: {sources_path} has no 'Types:' lines -- its format isn't the expected one. "
            f"Enable 'Source code' in the 'Software & Updates' app instead. Aborting.",
            file=sys.stderr,
        )
        return 1
    new_sources_text, changed = enable_source_code(sources_text)
    backup_path = sources_path.with_name(sources_path.name + ".bak")

    # --- 4. Show the plan ---
    commands = get_commands(download_images=not args.no_images)
    print("\nThe following will be done:")
    if changed:
        print(
            f"  enable source code in {sources_path}: {changed} 'Types: deb' line(s) become "
            f"'Types: deb deb-src' (original saved as {backup_path.name})"
        )
    else:
        print(f"  (source code is already enabled in {sources_path})")
    for cmd in commands:
        print(f"  $ sudo {' '.join(cmd)}")
    for pkg, reason in EXTRA_PACKAGES.items():
        print(f"  added: {pkg} ({reason})")

    if args.dry_run:
        print("\n--dry-run set: nothing changed.")
        return 0

    # --- 5. Root check ---
    if os.geteuid() != 0:
        print(
            "\nerror: installing packages requires root. Re-run with sudo, "
            "or use --dry-run to inspect without installing.",
            file=sys.stderr,
        )
        return 1

    # --- 6. Confirm ---
    if not args.yes:
        if not _confirm("\nProceed with installation on this machine? [y/N] "):
            print("Aborted.")
            return 1

    # --- 7. Execute ---
    if changed:
        try:
            shutil.copy2(sources_path, backup_path)
            sources_path.write_text(new_sources_text, encoding="utf-8")
        except OSError as exc:
            print(f"error: could not update {sources_path}: {exc}", file=sys.stderr)
            return 1
        print(f"\nEnabled source code in {sources_path} (original saved as {backup_path}).")

    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    try:
        for cmd in commands:
            run_command(cmd, env)
    except subprocess.CalledProcessError as exc:
        print(f"\nerror: command failed with exit code {exc.returncode}: {' '.join(exc.cmd)}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"\nerror: could not run a command: {exc}", file=sys.stderr)
        return 1

    # --- 8. Check the result ---
    conflicting = installed_packages(CONFLICTING_PACKAGES)
    if conflicting:
        print(
            "\nwarning: Ubuntu's own GNU Radio got installed as a dependency ("
            + ", ".join(conflicting) + "). Remove it before building GNU Radio:\n"
            "  sudo apt-get remove " + " ".join(conflicting),
            file=sys.stderr,
        )
    try:
        version = subprocess.run(
            ["uhd_config_info", "--version"], capture_output=True, text=True, check=True,
        ).stdout.strip()
        print(f"\nInstalled: {version}")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"\nerror: UHD doesn't run after installation: {exc}", file=sys.stderr)
        return 1

    print("\nDone. UHD and GNU Radio's dependencies are installed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
