#!/usr/bin/env python3
"""
gnuradio_uninstaller.py

Finds every GNU Radio installed on this machine, however it was installed,
and removes it, so that GNU Radio can be built and installed again from a
clean start. Run it before gnuradio_dependencies_installer.py (Step 1) on a
machine that has had GNU Radio on it before, or on its own to remove GNU
Radio altogether.

It first looks, without changing anything, and lists what it found and
exactly what it will do about each. Nothing is changed until you answer
"y" (or pass -y). Use --dry-run to look only.

Run it as your normal user, not with sudo. It uses sudo itself for the
commands that need root, and asks for your password once, before it
changes anything.

It looks for, and removes:

  * Ubuntu's own GNU Radio packages (gnuradio, gnuradio-dev, the
    libgnuradio-* libraries), and anything that depends on them, with
    `apt-get remove`. The list apt would remove is shown first.
  * GNU Radio PPAs (ppa:gnuradio/...): their sources files.
  * GNU Radio built from source and installed with `make install`:
    - into a folder of its own (~/gnuradio-pkg, written by
      gnuradio_clone_builder.py, or a PyBOMBS prefix): the whole folder;
    - into a shared folder such as /usr/local: GNU Radio's files and folders
      only, using the install_manifest.txt of its build directory where one
      is found, then `ldconfig`.
    It looks in /usr/local, /opt, and your home directory (4 levels deep,
    leaving out hidden folders); add --prefix for a GNU Radio elsewhere.
  * GNU Radio Companion's menu entry and icons.
  * GNU Radio build directories in your home directory (e.g.
    ~/gnuradio/build). Your source code and your branches are not touched.
  * UHD built from source and installed into /usr/local. GNU Radio's cmake
    would find it before the packaged UHD that Step 1 installs.
  * The lines in ~/.profile, ~/.bashrc, ~/.bash_aliases and
    ~/.bash_profile that set up a removed GNU Radio's environment (sourcing
    its setup_env.sh, or adding its folders to PATH, PYTHONPATH or
    LD_LIBRARY_PATH), and lines sourcing a setup_env.sh that no longer
    exists. Each changed file is first copied to <file>.bak.
  * With --settings: GNU Radio's settings and GNU Radio Companion's saved
    state in your home directory (~/.config/gnuradio, ~/.cache/gnuradio,
    ~/.local/state/gnuradio, and, from versions before 3.10, ~/.gnuradio
    and ~/.grc_gnuradio). Without it they are kept.

Some things are only listed, with the command to remove them yourself:
scripts in /etc/profile.d that mention GNU Radio, lines in
/etc/apt/sources.list naming a GNU Radio PPA, PyBOMBS' own settings
(~/.pybombs) and PyBOMBS itself.

Nothing under /usr is removed except under /usr/local (and, under
/usr/share, GRC menu files that no package owns). GNU Radio in a conda
environment is only listed: conda should remove it.

After changing ~/.profile, log out of the desktop and back in.

Examples
--------
  # See what would be removed, without changing anything:
  python3 gnuradio_uninstaller.py --dry-run

  # Remove it:
  python3 gnuradio_uninstaller.py

  # Also remove GNU Radio's settings and GRC's saved state:
  python3 gnuradio_uninstaller.py --settings

  # Also look in a prefix outside the usual places:
  python3 gnuradio_uninstaller.py --prefix /data/gr-prefix
"""

from __future__ import annotations

import argparse
import os
import pwd
import re
import shutil
import subprocess
import sys
import typing
from pathlib import Path

# Ubuntu's own GNU Radio packages (dpkg-query patterns).
GNURADIO_PACKAGE_PATTERNS = ["gnuradio", "gnuradio-dev", "gnuradio-doc", "libgnuradio-*"]

# A GNU Radio PPA, as it appears in a sources entry; group 1 is the PPA name.
GNURADIO_PPA_URI = re.compile(r"ppa\.launchpad(?:content)?\.net/gnuradio/([^/\s]+)")
APT_SOURCES_DIR = "/etc/apt/sources.list.d"
APT_SOURCES_LIST = "/etc/apt/sources.list"

# Where GNU Radio built from source is looked for, besides the home directory.
SYSTEM_PREFIX = "/usr/local"
OPT_DIR = "/opt"
HOME_SEARCH_DEPTH = 4
OPT_SEARCH_DEPTH = 2

# Files that mark a folder as the prefix of an installed GNU Radio.
INSTALLED_GNURADIO_PATTERNS = (
    "bin/gnuradio-config-info",
    "lib*/libgnuradio-runtime.so*",
    "lib*/python3*/*-packages/gnuradio",
)

# GNU Radio's folders and files in a prefix shared with other software, such
# as /usr/local. Keep the folders in step with INSTALL_DIR_PATTERNS in
# gnuradio_clone_builder.py.
GNURADIO_DIR_PATTERNS = (
    "lib*/python3*/*-packages/gnuradio",
    "lib*/python3*/*-packages/pmt",
    "include/gnuradio",
    "include/pmt",
    "share/gnuradio",
    "etc/gnuradio",
    "lib*/cmake/gnuradio",
    "share/doc/gnuradio-*",
)
GNURADIO_FILE_PATTERNS = (
    "lib*/libgnuradio-*",
    "lib*/pkgconfig/gnuradio-*.pc",
)
# GNU Radio's programs in <prefix>/bin, and their manual pages. The uhd_fft,
# uhd_rx_* and uhd_siggen* programs come with GNU Radio (gr-uhd), not UHD.
GNURADIO_PROGRAM = re.compile(r"(gnuradio|gr_|gr-|grcc|uhd_fft|uhd_rx_|uhd_siggen|polar_channel_construction).*")
GNURADIO_MAN_PAGE = re.compile(
    r"(gnuradio|gr_|gr-|grcc|uhd_fft|uhd_rx_|uhd_siggen|polar_channel_construction"
    r"|dial_tone|display_qt|tags_demo).*\.1(\.gz)?"
)

# A UHD built from source and installed into /usr/local. The first patterns
# mark it (as in gnuradio_dependencies_installer.py); all are removed.
SOURCE_UHD_MARKERS = ("lib/libuhd.so*", "bin/uhd_find_devices", "include/uhd.hpp", "lib/cmake/uhd")
SOURCE_UHD_PATTERNS = (
    "include/uhd",
    "include/uhd.hpp",
    "lib*/libuhd.so*",
    "lib*/uhd",
    "lib*/cmake/uhd",
    "lib*/pkgconfig/uhd.pc",
    "lib*/python3*/*-packages/uhd",
    "lib*/python3*/*-packages/usrpctl",
    "share/uhd",
    "share/doc/uhd",
    "bin/uhd_find_devices",
    "bin/uhd_usrp_probe",
    "bin/uhd_image_loader",
    "bin/uhd_images_downloader",
    "bin/uhd_config_info",
    "bin/uhd_cal_*",
    "bin/uhd_adc_self_cal",
    "bin/usrpctl",
    "bin/rfnoc_image_builder",
    "bin/usrp2_card_burner*",
    "bin/usrp_n2xx_simple_net_burner",
    "share/man/man1/uhd_find_devices.1*",
    "share/man/man1/uhd_usrp_probe.1*",
    "share/man/man1/uhd_image_loader.1*",
    "share/man/man1/uhd_images_downloader.1*",
    "share/man/man1/uhd_config_info.1*",
    "share/man/man1/uhd_cal_*.1*",
    "share/man/man1/usrp2_card_burner.1*",
)

# GNU Radio Companion's menu entry, icons and file type, as its
# grc_setup_freedesktop script installs them (under ~/.local/share for an
# install as a normal user, under /usr/local/share or /usr/share as root).
GRC_DESKTOP_PATTERNS = (
    "applications/gnuradio-grc.desktop",
    "icons/*/*/apps/gnuradio-grc.png",
    "icons/*/*/mimetypes/*gnuradio-grc.png",
    "mime/packages/gnuradio-grc.xml",
    "mime/application/gnuradio-grc.xml",
)
SYSTEM_SHARE_DIRS = ("/usr/local/share", "/usr/share")

# Written into its prefix by gnuradio_clone_builder.py, and by PyBOMBS.
SETUP_ENV_NAME = "setup_env.sh"
SETUP_ENV_MARKER = "Written by gnuradio_clone_builder.py"
PYBOMBS_PREFIX_MARKER = ".pybombs"

# A conda environment, which conda itself should change.
CONDA_PREFIX_MARKER = "conda-meta"

# Start-up files whose GNU Radio lines are removed.
STARTUP_FILES = (".profile", ".bashrc", ".bash_aliases", ".bash_profile")
ENV_VARIABLES = ("PATH", "PYTHONPATH", "LD_LIBRARY_PATH")
PROFILE_D_DIR = "/etc/profile.d"

# GNU Radio's settings and GRC's saved state (3.10 on, then before 3.10).
SETTINGS_DIRS = (".config/gnuradio", ".cache/gnuradio", ".local/state/gnuradio", ".gnuradio", ".grc_gnuradio")

# Folders never removed as a whole, whatever they contain.
PROTECTED_DIRS = ("/", "/usr", "/usr/local", "/opt", "/home", "/root", "/etc", "/var", "/srv", "/tmp")

# Paths per rm command, to stay well within the command line length limit.
RM_CHUNK = 200


class Item(typing.NamedTuple):
    title: str                           # what was found
    details: list[str]                   # shown under the title in the survey
    commands: list[list[str]] = []       # run in order; those needing root start with "sudo"
    edits: list[tuple[Path, list[int]]] = []  # start-up file, line numbers (0-based) to remove
    needs_ldconfig: bool = False


class BuildDir(typing.NamedTuple):
    path: Path
    project: str      # CMAKE_PROJECT_NAME: "gnuradio" or "UHD"
    prefix: Path | None


def get_owner() -> pwd.struct_passwd:
    """The user whose home directory is searched: the invoking user when run via sudo."""
    if os.geteuid() == 0:
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user and sudo_user != "root":
            try:
                return pwd.getpwnam(sudo_user)
            except KeyError:
                pass
    return pwd.getpwuid(os.geteuid())


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def installed_packages_matching(patterns: list[str]) -> list[str]:
    """The installed packages whose names match the dpkg-query patterns."""
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${db:Status-Status} ${Package}\n", *patterns],
            capture_output=True, text=True,
        )
    except OSError:
        return []
    found = []
    for line in result.stdout.splitlines():
        status, _, name = line.partition(" ")
        if status not in ("not-installed", "config-files") and name:
            found.append(name)
    return sorted(set(found))


def apt_removal_list(packages: list[str]) -> list[str]:
    """
    The packages `apt-get remove` would remove: the given ones and everything
    that depends on them. Falls back to the given ones if apt can't say.
    """
    try:
        result = subprocess.run(
            ["apt-get", "-s", "remove", *packages], capture_output=True, text=True,
        )
    except OSError:
        return packages
    removed = re.findall(r"^Remv (\S+)", result.stdout, flags=re.MULTILINE)
    return sorted(set(removed)) if result.returncode == 0 and removed else packages


def owned_by_package(path: Path) -> bool:
    """Whether dpkg says the file belongs to an installed package."""
    try:
        result = subprocess.run(["dpkg-query", "-S", str(path)], capture_output=True, text=True)
    except OSError:
        return False
    return result.returncode == 0


def read_cmake_cache(build_dir: Path) -> BuildDir | None:
    """The project and install prefix of a cmake build directory, or None if it isn't one."""
    try:
        text = (build_dir / "CMakeCache.txt").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    project = re.search(r"^CMAKE_PROJECT_NAME:STATIC=(.*)$", text, flags=re.MULTILINE)
    prefix = re.search(r"^CMAKE_INSTALL_PREFIX:PATH=(.*)$", text, flags=re.MULTILINE)
    if not project:
        return None
    return BuildDir(build_dir, project.group(1).strip(), Path(prefix.group(1).strip()) if prefix else None)


def is_gnuradio_prefix(path: Path) -> bool:
    return any(any(path.glob(pattern)) for pattern in INSTALLED_GNURADIO_PATTERNS)


def search(top: Path, max_depth: int, prefixes: list[Path], build_dirs: list[BuildDir]) -> None:
    """
    Look through the folders under top, down to max_depth levels, for GNU
    Radio prefixes and for GNU Radio and UHD build directories, adding them
    to the lists. Hidden folders and mount points are left out, and neither
    a prefix nor a build directory is looked into any further.
    """
    todo = [(top, 0)]
    while todo:
        path, depth = todo.pop()
        build_dir = read_cmake_cache(path)
        if build_dir:
            if build_dir.project in ("gnuradio", "UHD"):
                build_dirs.append(build_dir)
            continue
        if depth > 0 and is_gnuradio_prefix(path):
            prefixes.append(path)
            continue
        if depth == max_depth:
            continue
        try:
            entries = sorted(os.scandir(path), key=lambda e: e.name, reverse=True)
        except OSError:
            continue
        for entry in entries:
            if entry.name.startswith(".") or not entry.is_dir(follow_symlinks=False):
                continue
            child = Path(entry.path)
            if os.path.ismount(child):
                continue
            todo.append((child, depth + 1))


def glob_all(prefix: Path, patterns: typing.Iterable[str]) -> list[Path]:
    found: list[Path] = []
    for pattern in patterns:
        for path in sorted(prefix.glob(pattern)):
            if path not in found:
                found.append(path)
    return found


def files_in_dir(directory: Path, regex: re.Pattern) -> list[Path]:
    try:
        return sorted(p for p in directory.iterdir() if regex.fullmatch(p.name))
    except OSError:
        return []


def shared_prefix_paths(prefix: Path) -> list[Path]:
    """GNU Radio's folders and files in a prefix shared with other software."""
    paths = glob_all(prefix, GNURADIO_DIR_PATTERNS + GNURADIO_FILE_PATTERNS)
    paths += files_in_dir(prefix / "bin", GNURADIO_PROGRAM)
    paths += files_in_dir(prefix / "share/man/man1", GNURADIO_MAN_PAGE)
    return paths


def manifest_files(build_dirs: list[BuildDir], prefix: Path, project: str) -> tuple[Path | None, list[Path]]:
    """
    The files still installed under the prefix according to the
    install_manifest.txt of a build directory of the project that installed
    there, and that manifest; (None, []) if there is none.
    """
    for build_dir in build_dirs:
        manifest = build_dir.path / "install_manifest.txt"
        if build_dir.project != project or build_dir.prefix != prefix or not manifest.is_file():
            continue
        try:
            lines = manifest.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        files = []
        for line in lines:
            path = Path(line.strip())
            if line.strip() and path.is_relative_to(prefix) and (path.exists() or path.is_symlink()):
                files.append(path)
        return manifest, files
    return None, []


def is_protected(path: Path, home: Path) -> bool:
    """Whether the folder must never be removed as a whole."""
    return str(path) in PROTECTED_DIRS or path == home or home.is_relative_to(path) or len(path.parts) < 3


def own_prefix_kind(prefix: Path, home: Path) -> str | None:
    """
    How the prefix is known to hold only GNU Radio (and what was built for
    it), so that it can be removed as a whole: "gnuradio_clone_builder.py",
    "PyBOMBS", or None.
    """
    if is_protected(prefix, home):
        return None
    try:
        if SETUP_ENV_MARKER in (prefix / SETUP_ENV_NAME).read_text(encoding="utf-8", errors="replace"):
            return "gnuradio_clone_builder.py"
    except OSError:
        pass
    if (prefix / PYBOMBS_PREFIX_MARKER).is_dir():
        return "PyBOMBS"
    return None


def has_files_not_owned_by(path: Path, uid: int) -> bool:
    """Whether the file, or anything in the folder tree, belongs to another user (e.g. root)."""
    try:
        if os.lstat(path).st_uid != uid:
            return True
    except OSError:
        return False
    if not path.is_dir() or path.is_symlink():
        return False
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            try:
                if os.lstat(os.path.join(root, name)).st_uid != uid:
                    return True
            except OSError:
                continue
    return False


def needs_root(paths: list[Path], uid: int) -> bool:
    """Whether removing the paths needs root: a parent folder or a file in them isn't the user's."""
    return any(
        not os.access(path.parent, os.W_OK) or has_files_not_owned_by(path, uid) for path in paths
    )


def rm_commands(paths: list[Path], root: bool) -> list[list[str]]:
    sudo = ["sudo"] if root else []
    return [
        [*sudo, "rm", "-rf", "--", *(str(p) for p in paths[i:i + RM_CHUNK])]
        for i in range(0, len(paths), RM_CHUNK)
    ]


def shorten(path: Path, home: Path) -> str:
    """The path with the home directory written as ~."""
    return "~/" + str(path.relative_to(home)) if path.is_relative_to(home) and path != home else str(path)


def list_paths(paths: list[Path], home: Path, limit: int = 12) -> list[str]:
    shown = [shorten(p, home) + ("/" if p.is_dir() and not p.is_symlink() else "") for p in paths[:limit]]
    if len(paths) > limit:
        shown.append(f"... and {len(paths) - limit} more")
    return shown


def expand_home(text: str, home: Path) -> str:
    """The text with $HOME, ${HOME} and a leading ~/ replaced by the home directory."""
    text = text.replace("${HOME}", str(home)).replace("$HOME", str(home))
    return re.sub(r"(?<![\w/])~(?=/)", str(home), text)


SOURCED_FILE = re.compile(r"""^\s*(?:\.|source)\s+["']?([^"'\s;]+)""")


def startup_lines_to_remove(text: str, removed: list[Path], home: Path) -> list[int]:
    """
    The (0-based) numbers of the lines that set up a removed GNU Radio's
    environment: sourcing a setup_env.sh in a removed prefix or one that no
    longer exists, or setting PATH, PYTHONPATH or LD_LIBRARY_PATH to
    include a removed prefix.
    """
    numbers = []
    for number, line in enumerate(text.splitlines()):
        if line.lstrip().startswith("#"):
            continue
        expanded = expand_home(line, home)
        sourced = SOURCED_FILE.match(expanded)
        if sourced and sourced.group(1).endswith("/" + SETUP_ENV_NAME):
            target = Path(sourced.group(1))
            if not target.exists() or any(target.is_relative_to(p) for p in removed):
                numbers.append(number)
            continue
        if not re.match(rf"^\s*(?:export\s+)?({'|'.join(ENV_VARIABLES)})=", expanded):
            continue
        for prefix in removed:
            if str(prefix) == SYSTEM_PREFIX:
                # /usr/local holds other software too: only a PYTHONPATH line
                # naming its Python folders is GNU Radio's.
                if re.search(rf"PYTHONPATH=.*{re.escape(SYSTEM_PREFIX)}/lib\w*/python3", expanded):
                    numbers.append(number)
                    break
            elif re.search(rf"{re.escape(str(prefix))}(/|\b|$)", expanded):
                numbers.append(number)
                break
    return numbers


def backup_path(path: Path) -> Path:
    """<file>.bak, or <file>.bak.1, .bak.2, ... if that exists already."""
    backup = path.with_name(path.name + ".bak")
    n = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.bak.{n}")
        n += 1
    return backup


def apply_edit(path: Path, numbers: list[int], owner: pwd.struct_passwd) -> Path:
    """Remove the lines from the file, after copying it to a backup. Returns the backup."""
    text = path.read_text(encoding="utf-8", errors="surrogateescape")
    backup = backup_path(path)
    shutil.copy2(path, backup)
    lines = text.splitlines(keepends=True)
    kept = [line for number, line in enumerate(lines) if number not in numbers]
    path.write_text("".join(kept), encoding="utf-8", errors="surrogateescape")
    if os.geteuid() == 0:
        os.chown(backup, owner.pw_uid, owner.pw_gid)
    return backup


def survey(home: Path, owner: pwd.struct_passwd, extra_prefixes: list[Path],
           remove_settings: bool) -> tuple[list[Item], list[str]]:
    """
    Look for every GNU Radio on the machine. Returns what to remove, in the
    order to remove it, and notes about what is only listed.
    """
    uid = owner.pw_uid
    items: list[Item] = []
    notes: list[str] = []

    # --- Folders of GNU Radio built from source, and build directories ---
    prefixes: list[Path] = []
    build_dirs: list[BuildDir] = []
    search(home, HOME_SEARCH_DEPTH, prefixes, build_dirs)
    search(Path(OPT_DIR), OPT_SEARCH_DEPTH, prefixes, build_dirs)
    for prefix in [Path(SYSTEM_PREFIX), *extra_prefixes]:
        if prefix not in prefixes:
            prefixes.append(prefix)
    # Under /usr, only /usr/local: the rest belongs to packages.
    prefixes = [p for p in prefixes if not p.is_relative_to("/usr") or p.is_relative_to(SYSTEM_PREFIX)]

    removed_prefixes: list[Path] = []
    for prefix in prefixes:
        if (prefix / CONDA_PREFIX_MARKER).is_dir():
            notes.append(f"GNU Radio in the conda environment {shorten(prefix, home)}: remove it with "
                         f"conda (conda remove -p {prefix} gnuradio), or remove the environment.")
            continue
        kind = own_prefix_kind(prefix, home)
        if kind:
            root = needs_root([prefix], uid)
            items.append(Item(
                f"GNU Radio installed in its own folder {shorten(prefix, home)} (by {kind})",
                ["The whole folder is removed."],
                rm_commands([prefix], root),
            ))
            removed_prefixes.append(prefix)
            continue
        paths = shared_prefix_paths(prefix)
        manifest, listed = manifest_files(build_dirs, prefix, "gnuradio")
        paths += [p for p in listed if not any(p.is_relative_to(q) for q in paths)]
        if not paths:
            continue
        root = needs_root(paths, uid)
        details = []
        if manifest:
            details.append(f"Files listed in {shorten(manifest, home)}, and GNU Radio's folders:")
        else:
            details.append("GNU Radio's folders and files (no install_manifest.txt found):")
        details += ["  " + line for line in list_paths(paths, home)]
        empty = [p for p in paths if p.is_dir() and not any(q.is_file() for q in p.rglob("*"))]
        if empty and len(empty) == len(paths):
            details.insert(0, "Only empty folders, left by an earlier removal. They make GNU Radio's tests fail.")
        is_shared = not prefix.is_relative_to(home) or prefix == Path(SYSTEM_PREFIX)
        items.append(Item(
            f"GNU Radio built from source in {shorten(prefix, home)}",
            details,
            rm_commands(paths, root),
            needs_ldconfig=root and is_shared,
        ))
        removed_prefixes.append(prefix)

    # --- GNU Radio Companion's menu entry and icons ---
    desktop = glob_all(home / ".local/share", GRC_DESKTOP_PATTERNS)
    system_desktop = [
        p for share in SYSTEM_SHARE_DIRS for p in glob_all(Path(share), GRC_DESKTOP_PATTERNS)
        if not owned_by_package(p)
    ]
    if desktop or system_desktop:
        commands = rm_commands(desktop, False) + rm_commands(system_desktop, True)
        # As root, these would leave root-owned cache files in the home directory.
        if desktop and os.geteuid() != 0 and has_command("update-mime-database"):
            commands.append(["update-mime-database", str(home / ".local/share/mime")])
        if desktop and os.geteuid() != 0 and has_command("update-desktop-database"):
            commands.append(["update-desktop-database", str(home / ".local/share/applications")])
        items.append(Item(
            "GNU Radio Companion's menu entry and icons",
            [f"{len(desktop) + len(system_desktop)} files:",
             *("  " + line for line in list_paths(desktop + system_desktop, home, limit=4))],
            commands,
        ))

    # --- Build directories ---
    gr_builds = [b for b in build_dirs if b.project == "gnuradio"]
    if gr_builds:
        paths = [b.path for b in gr_builds]
        items.append(Item(
            "GNU Radio build director" + ("ies" if len(paths) > 1 else "y"),
            [*list_paths(paths, home), "The source code next to it is not touched."],
            rm_commands(paths, needs_root(paths, uid)),
        ))

    # --- UHD built from source in /usr/local ---
    uhd_prefix = Path(SYSTEM_PREFIX)
    if glob_all(uhd_prefix, SOURCE_UHD_MARKERS):
        paths = glob_all(uhd_prefix, SOURCE_UHD_PATTERNS)
        manifest, listed = manifest_files(build_dirs, uhd_prefix, "UHD")
        paths += [p for p in listed if not any(p.is_relative_to(q) for q in paths)]
        details = [
            "GNU Radio's cmake would use it instead of the packaged UHD that Step 1 installs.",
            (f"Files listed in {shorten(manifest, home)}, and UHD's folders:" if manifest
             else "UHD's folders and files (no install_manifest.txt found):"),
            *("  " + line for line in list_paths(paths, home)),
        ]
        uhd_builds = [b.path for b in build_dirs if b.project == "UHD"]
        if uhd_builds:
            details.append("Its build directory and source code are kept: " +
                           ", ".join(shorten(p, home) for p in uhd_builds))
        items.append(Item(
            f"UHD built from source in {SYSTEM_PREFIX}", details, rm_commands(paths, True),
            needs_ldconfig=True,
        ))

    # --- Ubuntu's packages ---
    if has_command("dpkg-query"):
        packages = installed_packages_matching(GNURADIO_PACKAGE_PATTERNS)
        if packages:
            removal = apt_removal_list(packages)
            extra = [p for p in removal if p not in packages]
            details = [f"{len(removal)} packages: " + " ".join(removal)]
            if extra:
                details.append("(" + " ".join(extra) + ": they depend on GNU Radio)")
            items.append(Item(
                "GNU Radio packages",
                details,
                [["sudo", "env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "remove", "-y", *packages]],
            ))
            notes.append(
                "Packages installed only for GNU Radio's packages may be left. To see and remove "
                "them: sudo apt-get autoremove (check the list before answering Y)."
            )

    # --- GNU Radio PPAs ---
    ppa_files = []
    for path in sorted(Path(APT_SOURCES_DIR).glob("*")):
        if path.suffix not in (".list", ".sources") or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        uris = re.findall(r"\b[a-z+]+://\S+", text)
        if uris and all(GNURADIO_PPA_URI.search(u) for u in uris):
            ppa_files.append(path)
        elif GNURADIO_PPA_URI.search(text):
            notes.append(f"{path} names a GNU Radio PPA among other entries: edit it with sudo.")
    if ppa_files:
        items.append(Item(
            "GNU Radio PPA",
            [str(p) for p in ppa_files],
            [*rm_commands(ppa_files, True), ["sudo", "apt-get", "update"]],
        ))
    try:
        if GNURADIO_PPA_URI.search(Path(APT_SOURCES_LIST).read_text(encoding="utf-8", errors="replace")):
            notes.append(f"{APT_SOURCES_LIST} names a GNU Radio PPA: remove that line with sudo.")
    except OSError:
        pass

    # --- Start-up files ---
    edits = []
    details = []
    for name in STARTUP_FILES:
        path = home / name
        try:
            text = path.read_text(encoding="utf-8", errors="surrogateescape")
        except OSError:
            continue
        numbers = startup_lines_to_remove(text, removed_prefixes, home)
        if numbers:
            edits.append((path, numbers))
            lines = text.splitlines()
            details += [f"~/{name}, line {n + 1}: {lines[n].strip()}" for n in numbers]
    if edits:
        details.append("Each file is copied to <file>.bak first.")
        items.append(Item("GNU Radio lines in your start-up files", details, edits=edits))

    try:
        for path in sorted(Path(PROFILE_D_DIR).glob("*.sh")):
            text = expand_home(path.read_text(encoding="utf-8", errors="replace"), home)
            if "gnuradio" in text.lower() or any(str(p) in text for p in removed_prefixes if p != Path(SYSTEM_PREFIX)):
                notes.append(f"{path} mentions GNU Radio. If it is yours, remove it: sudo rm {path}")
    except OSError:
        pass

    # --- Settings ---
    settings = [home / d for d in SETTINGS_DIRS if (home / d).exists()]
    if settings and remove_settings:
        items.append(Item(
            "GNU Radio's settings and GNU Radio Companion's saved state",
            list_paths(settings, home),
            rm_commands(settings, needs_root(settings, uid)),
        ))
    elif settings:
        notes.append(
            "GNU Radio's settings are kept (" + ", ".join(shorten(p, home) for p in settings) +
            "). Add --settings to remove them too."
        )

    # --- PyBOMBS ---
    if (home / ".pybombs").is_dir():
        notes.append("PyBOMBS' settings are in ~/.pybombs. If you no longer use PyBOMBS: rm -rf ~/.pybombs")
    if has_command("pybombs"):
        notes.append(f"PyBOMBS is installed ({shutil.which('pybombs')}). To remove it: "
                     "pip3 uninstall pybombs (with sudo if it was installed with sudo)")

    return items, notes


def run_command(cmd: list[str]) -> None:
    shown = ["sudo", *cmd[3:]] if cmd[:3] == ["sudo", "env", "DEBIAN_FRONTEND=noninteractive"] else cmd
    if len(shown) > 12:
        shown = [*shown[:8], f"... ({len(shown) - 8} more)"]
    print(f"$ {' '.join(shown)}")
    if os.geteuid() == 0 and cmd[0] == "sudo":
        cmd = cmd[1:]
    subprocess.run(cmd, check=True)


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    # Print each line as it is written, also into a pipe (`| tee uninstall.log`),
    # so that this script's own lines stay in order with the commands' output.
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(
        description="Find every installed GNU Radio, and remove it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--prefix", action="append", default=[], metavar="DIR",
        help="Also look for GNU Radio in this folder (can be given more than once).",
    )
    parser.add_argument(
        "--settings", action="store_true",
        help="Also remove GNU Radio's settings and GNU Radio Companion's saved state.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List what would be removed, without removing anything.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Do not prompt for confirmation before removing.",
    )
    args = parser.parse_args()

    owner = get_owner()
    home = Path(owner.pw_dir)
    extra_prefixes = [Path(p).expanduser().resolve() for p in args.prefix]
    print(f"Looking for GNU Radio (home directory {home}) ...")
    items, notes = survey(home, owner, extra_prefixes, args.settings)

    if not items:
        print("\nNo installed GNU Radio found.")
    else:
        print("\nFound, and to be removed:")
        for number, item in enumerate(items, 1):
            print(f"\n{number}. {item.title}")
            for line in item.details:
                print(f"     {line}")
    if notes:
        print("\nNot changed by this program:")
        for note in notes:
            print(f"  * {note}")
    if not items:
        return 0

    if args.dry_run:
        print("\n--dry-run set: nothing removed.")
        return 0
    if not args.yes and not _confirm("\nRemove all of the above? [y/N] "):
        print("Aborted.")
        return 1

    uses_sudo = any(cmd[0] == "sudo" for item in items for cmd in item.commands)
    if uses_sudo and os.geteuid() != 0:
        print("\nSome of this needs root; sudo asks for your password once.")
        if subprocess.run(["sudo", "-v"]).returncode != 0:
            print("error: sudo failed. Nothing was removed.", file=sys.stderr)
            return 1

    ldconfig = False
    for number, item in enumerate(items, 1):
        print(f"\n--- {number}. {item.title} ---")
        try:
            for cmd in item.commands:
                run_command(cmd)
            for path, numbers in item.edits:
                backup = apply_edit(path, numbers, owner)
                print(f"Removed {len(numbers)} line(s) from {shorten(path, home)} "
                      f"(the original is {shorten(backup, home)}).")
        except subprocess.CalledProcessError as exc:
            print(f"\nerror: command failed (exit code {exc.returncode}). Stopping; "
                  f"run this program again to see what is left.", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"\nerror: {exc}. Stopping; run this program again to see what is left.",
                  file=sys.stderr)
            return 1
        ldconfig = ldconfig or item.needs_ldconfig
    if ldconfig:
        print()
        run_command(["sudo", "ldconfig"])

    print("\nDone.")
    if any(item.edits for item in items):
        print("Your start-up files changed: log out of the desktop and back in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
