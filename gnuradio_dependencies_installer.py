#!/usr/bin/env python3
"""
gnuradio_dependencies_installer.py

Step 1 of building GNU Radio from source on bare metal: installs UHD (the
USRP Hardware Driver), from Ettus Research's PPA where it has a build for this
Ubuntu release, and everything GNU Radio needs to build and run, all with apt.
Nothing is compiled here; building GNU Radio itself is Step 2.

Run it as your normal user. It uses sudo only for the commands that need root
(it asks for your password once), which are the equivalent of:

    # enable "Source code" (deb-src) in /etc/apt/sources.list.d/ubuntu.sources,
    # which `apt-get build-dep` needs
    sudo apt-get update
    sudo apt-get install -y software-properties-common git
    sudo add-apt-repository -y ppa:ettusresearch/uhd
    sudo apt-get install -y --no-install-recommends uhd-host libuhd-dev
    sudo apt-get install -y libboost-dev libboost-chrono-dev libboost-date-time-dev ...
    sudo apt-get build-dep -y gnuradio
    sudo apt-get install -y python3-qtpy python3-pyqtgraph python3-matplotlib soapysdr-tools python3-pytest
    sudo apt-get install -y qt6-base-dev qt6-svg-dev libqwt-qt6-dev ...
    sudo apt-get install -y soapysdr0.8-module-rtlsdr soapysdr0.8-module-hackrf ...
    sudo uhd_images_downloader

Notes on those steps:

  * Before adding the PPA, it checks that the PPA has a build for this Ubuntu
    release. If not (as for 26.10 when this was written), it says so, leaves
    the PPA out, and installs Ubuntu's own (older) UHD under the same package
    names.
  * UHD's packages recommend Ubuntu's own gnuradio packages, so they are
    installed with --no-install-recommends. Otherwise Ubuntu's GNU Radio would
    be installed into /usr, next to the one you are about to build.
  * The PPA's libuhd-dev doesn't depend on the Boost development packages,
    although UHD's cmake files need them, so they are installed by name.
    Without them GNU Radio's cmake can't use UHD and quietly builds GNU Radio
    without gr-uhd (seen on a clean Ubuntu 24.04).
  * `apt-get build-dep gnuradio` installs the build dependencies of Ubuntu's
    gnuradio package for this Ubuntu release, so the list is never hardcoded
    here. That includes libuhd-dev, installed just before.
  * The apt-get line after it adds run-time packages that a build-dependency
    list doesn't cover, and pytest, which GNU Radio's GRC tests need (Ubuntu
    26.04's build dependencies include it, 24.04's don't).
  * The Qt6 line is for GNU Radio's main branch, which uses Qt6 (maint-3.10
    uses Qt5, which build-dep installs). It is run only where Ubuntu has Qwt
    for Qt6 (libqwt-qt6-dev, from Ubuntu 26.10 on): without Qwt, main's
    gr-qtgui can't be built anyway, and PyQt6 alone makes
    `gnuradio-companion --qt` hang on Ubuntu 26.04.
  * The last apt-get line installs SoapySDR's device modules (the
    drivers gr-soapy uses for an RTL-SDR, HackRF, Airspy, LimeSDR, ...). They
    are only recommended by the SoapySDR library, and `apt-get build-dep`
    leaves them out, so without this line gr-soapy would be built but find no
    devices. The list is whatever Ubuntu's soapysdr-module-all package depends
    on in this release, except the UHD module: that one needs Ubuntu's own
    UHD library, and USRPs are used through gr-uhd anyway.
  * The uhd-host package installs the udev rules for USRPs itself.

Before changing anything, it stops if it finds something that would conflict:
Ubuntu's gnuradio package already installed, a UHD built from source in
/usr/local (GNU Radio's cmake would find that one first), or an entry for the
PPA that has no build for this Ubuntu release (apt-get update would fail).

Examples
--------
  # Show what would be done, without changing anything:
  python3 gnuradio_dependencies_installer.py --dry-run

  # Install UHD and GNU Radio's dependencies:
  python3 gnuradio_dependencies_installer.py

  # The same, without downloading the USRP FPGA images:
  python3 gnuradio_dependencies_installer.py --no-images
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

UHD_PPA = "ppa:ettusresearch/uhd"
# The PPA has a build for an Ubuntu release if this file exists for its codename.
UHD_PPA_RELEASE_URL = "https://ppa.launchpadcontent.net/ettusresearch/uhd/ubuntu/dists/{codename}/Release"
# Where add-apt-repository puts the PPA's entry.
UHD_PPA_SOURCES_GLOB = "/etc/apt/sources.list.d/ettusresearch-ubuntu-uhd-*"
UBUNTU_SOURCES = "/etc/apt/sources.list.d/ubuntu.sources"

# Needed by the steps themselves: add-apt-repository, and git for Step 2's clone.
TOOL_PACKAGES = ["software-properties-common", "git"]

# UHD, from the PPA or else from Ubuntu. uhd-host depends on python3-uhd and the
# UHD library.
UHD_PACKAGES = ["uhd-host", "libuhd-dev"]

# The Boost development packages that UHD's cmake files (UHDConfig.cmake) need,
# as Ubuntu's own libuhd-dev depends on them (without the Python one). The PPA's
# libuhd-dev doesn't, and `apt-get build-dep gnuradio` brings only some.
BOOST_PACKAGES = [
    "libboost-dev",
    "libboost-chrono-dev",
    "libboost-date-time-dev",
    "libboost-exception-dev",
    "libboost-filesystem-dev",
    "libboost-program-options-dev",
    "libboost-regex-dev",
    "libboost-serialization-dev",
    "libboost-test-dev",
    "libboost-thread-dev",
]

# Run-time dependencies that a build-dependency list doesn't cover, and pytest.
EXTRA_PACKAGES = {
    "python3-qtpy": "imported by GNU Radio's Python code at run time",
    "python3-pyqtgraph": "needed by the filter design tool at run time",
    "python3-matplotlib": "imported by GNU Radio's examples and gr-qtgui Python code at run time",
    "soapysdr-tools": "provides SoapySDRUtil, for checking SoapySDR devices used with gr-soapy",
    "python3-pytest": "needed by GNU Radio's grc_tests in make test; without it that test is left out",
}

# Qt6 for GNU Radio's main branch, installed only if apt knows QT6_KEY_PACKAGE.
QT6_KEY_PACKAGE = "libqwt-qt6-dev"
QT6_PACKAGES = [
    "qt6-base-dev",
    "qt6-svg-dev",
    QT6_KEY_PACKAGE,
    "python3-pyqt6",
    "python3-pyqt6.qtsvg",
    "pyqt6-dev-tools",
]
# Stands for the Qt6 list in the command list until apt has been asked.
QT6_PLACEHOLDER = "<Qt6 packages>"

# SoapySDR's device modules: everything this metapackage depends on, except the
# modules skipped below. Worked out with apt-cache, since the set of modules
# differs between Ubuntu releases.
SOAPY_MODULES_METAPACKAGE = "soapysdr-module-all"
SOAPY_MODULE_PATTERN = re.compile(r"soapysdr[0-9.]*-module-[a-z0-9]+")
# The UHD module depends on Ubuntu's own UHD library, which would then sit next
# to the PPA's newer one.
SOAPY_SKIP_MODULES = ("uhd",)
# Stands for the module list in the command list until it has been worked out.
SOAPY_MODULES_PLACEHOLDER = "<SoapySDR device modules>"

# Ubuntu's own GNU Radio, which must not be installed next to a source build.
CONFLICTING_PACKAGES = ["gnuradio", "gnuradio-dev"]

# Where a UHD built from source and installed with `make install` keeps its files.
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


def ppa_has_build(codename: str) -> bool:
    """
    Whether the UHD PPA publishes packages for this Ubuntu release. Raises
    OSError if that can't be found out (no network, or an unexpected answer).
    """
    url = UHD_PPA_RELEASE_URL.format(codename=codename)
    try:
        with urllib.request.urlopen(url, timeout=30):
            return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise OSError(f"{url} answered HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise OSError(f"could not reach {url}: {exc.reason}") from exc


def ppa_entries_for(codename: str) -> list[Path]:
    """The PPA's sources files that name this Ubuntu release."""
    found = []
    for path in sorted(Path("/").glob(UHD_PPA_SOURCES_GLOB.lstrip("/"))):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if codename in path.name or re.search(rf"\b{re.escape(codename)}\b", text):
            found.append(path)
    return found


def apt_knows(package: str) -> bool:
    """Whether apt has a real (not only virtual) package of this name."""
    try:
        result = subprocess.run(["apt-cache", "show", package], capture_output=True, text=True)
    except OSError:
        return False
    return result.returncode == 0 and "Package:" in result.stdout


def qt6_packages() -> list[str]:
    """The Qt6 list if apt knows QT6_KEY_PACKAGE, otherwise empty."""
    return list(QT6_PACKAGES) if apt_knows(QT6_KEY_PACKAGE) else []


def parse_apt_depends(text: str) -> list[str]:
    """The package names on the "Depends:" lines of `apt-cache depends` output."""
    return re.findall(r"^\s*\|?Depends:\s*<?([^\s>]+)>?\s*$", text, flags=re.MULTILINE)


def soapy_module_packages() -> list[str]:
    """
    The SoapySDR device module packages to install: what the metapackage depends
    on (following its versioned "-module-all" package), minus SOAPY_SKIP_MODULES.
    Empty if apt doesn't know the metapackage (yet).
    """
    modules: set[str] = set()
    seen: set[str] = set()
    todo = [SOAPY_MODULES_METAPACKAGE]
    while todo:
        package = todo.pop()
        if package in seen:
            continue
        seen.add(package)
        try:
            result = subprocess.run(["apt-cache", "depends", package], capture_output=True, text=True)
        except OSError:
            return []
        if result.returncode != 0:
            continue
        for name in parse_apt_depends(result.stdout):
            if not SOAPY_MODULE_PATTERN.fullmatch(name):
                continue
            kind = name.rsplit("-module-", 1)[1]
            if kind == "all":
                todo.append(name)
            elif kind not in SOAPY_SKIP_MODULES:
                modules.add(name)
    return sorted(modules)


def get_commands(use_ppa: bool, download_images: bool) -> list[list[str]]:
    """The commands run as root after "Source code" has been enabled."""
    commands = [
        ["apt-get", "update"],
        ["apt-get", "install", "-y", *TOOL_PACKAGES],
    ]
    if use_ppa:
        # add-apt-repository also refreshes the package lists.
        commands.append(["add-apt-repository", "-y", UHD_PPA])
    commands += [
        ["apt-get", "install", "-y", "--no-install-recommends", *UHD_PACKAGES],
        ["apt-get", "install", "-y", *BOOST_PACKAGES],
        ["apt-get", "build-dep", "-y", "gnuradio"],
        ["apt-get", "install", "-y", *EXTRA_PACKAGES],
        # The placeholders are replaced by the real package names when their
        # turn comes: apt only knows them once the package lists are refreshed.
        ["apt-get", "install", "-y", QT6_PLACEHOLDER],
        ["apt-get", "install", "-y", SOAPY_MODULES_PLACEHOLDER],
    ]
    if download_images:
        commands.append(["uhd_images_downloader"])
    return commands


def as_root(cmd: list[str], is_root: bool) -> list[str]:
    """The command to run: through sudo unless already root, with apt kept non-interactive."""
    if is_root:
        return cmd
    # sudo clears the environment, so DEBIAN_FRONTEND is passed through env.
    return ["sudo", "env", "DEBIAN_FRONTEND=noninteractive", *cmd]


def shown(cmd: list[str]) -> str:
    """The command as printed: without the env part that as_root() adds."""
    if cmd[:3] == ["sudo", "env", "DEBIAN_FRONTEND=noninteractive"]:
        cmd = ["sudo", *cmd[3:]]
    return " ".join(cmd)


def run_command(cmd: list[str], env: dict, input_text: str | None = None) -> None:
    print(f"\n$ {shown(cmd)}")
    subprocess.run(
        cmd, check=True, env=env, input=input_text, text=True,
        stdout=subprocess.DEVNULL if input_text is not None else None,
    )


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install UHD (from the Ettus PPA where it has a build) and GNU Radio's dependencies with apt.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Run the checks and print what would be done, without changing anything.",
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
            f"(ID={info.get('ID')!r}). This installer uses Ubuntu's packages. Aborting.",
            file=sys.stderr,
        )
        return 1
    codename = info.get("VERSION_CODENAME", "")
    if not codename:
        print(f"error: {args.os_release_path} has no VERSION_CODENAME. Aborting.", file=sys.stderr)
        return 1
    print(f"Detected host OS: Ubuntu {info.get('VERSION_ID', '?')} ({codename})")

    is_root = os.geteuid() == 0
    if not is_root and not args.dry_run and shutil.which("sudo") is None:
        print("error: sudo is needed to install packages, and it isn't installed. Aborting.", file=sys.stderr)
        return 1

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
            "GNU Radio's cmake would find it before the packaged UHD. Remove it, then run this "
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

    # --- 3. Check whether the PPA has a build for this release ---
    try:
        use_ppa = ppa_has_build(codename)
    except OSError as exc:
        print(
            f"error: could not check whether the Ettus PPA has packages for Ubuntu {codename}: "
            f"{exc}. apt needs the network too. Aborting.",
            file=sys.stderr,
        )
        return 1
    if not use_ppa:
        stale = ppa_entries_for(codename)
        if stale:
            print(
                f"error: the Ettus PPA has no packages for Ubuntu {codename}, but apt has an "
                "entry for it, which makes `apt-get update` fail:",
                file=sys.stderr,
            )
            for path in stale:
                print(f"  {path}", file=sys.stderr)
            print("Remove it, then run this installer again:", file=sys.stderr)
            print(f"  sudo add-apt-repository --remove -y {UHD_PPA}", file=sys.stderr)
            print("Aborting.", file=sys.stderr)
            return 1
    print("OK: no conflicting GNU Radio packages, source-built UHD, or stale PPA entry found.")

    # --- 4. Work out the change to Ubuntu's sources file ---
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
    sources_commands = [
        as_root(["cp", "-p", str(sources_path), str(backup_path)], is_root),
        as_root(["tee", str(sources_path)], is_root),
    ]

    # --- 5. Show the plan ---
    commands = [as_root(cmd, is_root) for cmd in get_commands(use_ppa, download_images=not args.no_images)]
    if use_ppa:
        print(f"\nUHD: from the Ettus PPA, which has packages for Ubuntu {codename}.")
    else:
        print(
            f"\nwarning: the Ettus PPA has no packages for Ubuntu {codename} (yet), so it is left "
            "out and UHD comes from Ubuntu itself. That UHD is older than the PPA's; GNU Radio "
            "builds and works with it."
        )
    print("\nThe following will be done:")
    if changed:
        print(
            f"  enable source code in {sources_path}: {changed} 'Types: deb' line(s) become "
            f"'Types: deb deb-src' (original saved as {backup_path.name}):"
        )
        for cmd in sources_commands:
            print(f"    $ {shown(cmd)}")
    else:
        print(f"  (source code is already enabled in {sources_path})")
    for cmd in commands:
        print(f"  $ {shown(cmd)}")
    for pkg, reason in EXTRA_PACKAGES.items():
        print(f"  added: {pkg} ({reason})")
    if apt_knows(QT6_KEY_PACKAGE):
        print(f"  {QT6_PLACEHOLDER}, for GNU Radio's main branch: " + " ".join(QT6_PACKAGES))
    else:
        print(
            f"  {QT6_PLACEHOLDER}: installed only if apt knows {QT6_KEY_PACKAGE} once the package "
            "lists have been refreshed (it exists from Ubuntu 26.10 on)"
        )
    soapy_modules = soapy_module_packages()
    if soapy_modules:
        print(f"  {SOAPY_MODULES_PLACEHOLDER}, the drivers gr-soapy uses: " + " ".join(soapy_modules))
    else:
        print(
            f"  {SOAPY_MODULES_PLACEHOLDER}: the drivers gr-soapy uses; the list is worked out "
            "once the package lists have been refreshed"
        )

    if args.dry_run:
        print("\n--dry-run set: nothing changed.")
        return 0

    # --- 6. Confirm ---
    if not args.yes:
        if not _confirm("\nProceed with installation on this machine? [y/N] "):
            print("Aborted.")
            return 1

    # --- 7. Execute ---
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    try:
        if not is_root:
            # Ask for the password once, before anything changes.
            run_command(["sudo", "-v"], env)
        if changed:
            run_command(sources_commands[0], env)
            run_command(sources_commands[1], env, input_text=new_sources_text)
            print(f"Enabled source code in {sources_path} (original saved as {backup_path}).")
        for cmd in commands:
            if QT6_PLACEHOLDER in cmd:
                packages = qt6_packages()
                if not packages:
                    print(
                        f"\nnote: apt doesn't know {QT6_KEY_PACKAGE} in this Ubuntu release, so no "
                        "Qt6 packages were installed. That doesn't matter for maint-3.10 (Qt5); "
                        "a build of GNU Radio's main branch (Qt6) will have no gr-qtgui."
                    )
                    continue
                cmd = [*(arg for arg in cmd if arg != QT6_PLACEHOLDER), *packages]
            if SOAPY_MODULES_PLACEHOLDER in cmd:
                packages = soapy_module_packages()
                if not packages:
                    print(
                        f"\nwarning: apt doesn't know the {SOAPY_MODULES_METAPACKAGE} package, so no "
                        "SoapySDR device modules were installed. gr-soapy will be built, but it "
                        "will find no devices until the module for yours is installed.",
                        file=sys.stderr,
                    )
                    continue
                cmd = [*(arg for arg in cmd if arg != SOAPY_MODULES_PLACEHOLDER), *packages]
            run_command(cmd, env)
    except subprocess.CalledProcessError as exc:
        print(f"\nerror: command failed with exit code {exc.returncode}: {shown(exc.cmd)}", file=sys.stderr)
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
        source = "the Ettus PPA" if use_ppa else "Ubuntu (no PPA build for this release)"
        print(f"\nInstalled: {version}, from {source}")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"\nerror: UHD doesn't run after installation: {exc}", file=sys.stderr)
        return 1

    print("\nDone. UHD and GNU Radio's dependencies are installed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
