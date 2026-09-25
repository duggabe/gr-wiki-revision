# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

> **Note:** This is a work in progress.

## Install UHD in a bare-metal environment

`uhd_bare_metal_installer.py` adapts the build environment from
[EttusResearch/uhd](https://github.com/EttusResearch/uhd)'s `.ci/docker`
Dockerfiles for a bare-metal installation of UHD (no Docker required).

### Usage

```bash
python3 uhd_bare_metal_installer.py [options]
```

### Options

| Option | Description |
| --- | --- |
| `-h`, `--help` | Show the help message and exit. |
| `--dockerfile-url URL` | URL of the Dockerfile to fetch. Default: auto-detect from `/etc/os-release` and look up the matching file in EttusResearch/uhd's `.ci/docker` directory. |
| `--dockerfile-path PATH` | Read the Dockerfile from a local path instead of fetching it. |
| `--list-only` | Only parse and print/save the dependency list; do not install anything. |
| `-o`, `--output OUTPUT` | Path to save the extracted package list (default: `uhd-dependencies.txt`). |
| `--dry-run` | Print the apt/pip commands that would run, without executing them or requiring root. |
| `-y`, `--yes` | Do not prompt for confirmation before installing. |
| `--skip-upgrade` | Skip `apt-get upgrade` (recommended on a machine you don't want fully upgraded). |
| `--pip-index-url URL` | pip index URL to use (default: `$PIP_INDEX_URL`). |
| `--pip-index-host HOST` | pip trusted host to use (default: `$PIP_INDEX_HOST`). |
| `--os-release-path PATH` | Path to read `NAME`/`VERSION_ID` from for OS auto-detection (default: `/etc/os-release`). |
| `--build` | After dependencies install successfully, also clone, build, and install UHD itself into `<home>/uhd` (see below). Aborts with exit code 1 if any build step fails. |
| `--home HOME` | Directory to clone/build UHD into (used with `--build`), overriding auto-detection. Default: the invoking user's home when run via `sudo` (`$SUDO_USER`), else `$HOME`. |

#### What `--build` does

1. `git clone` UHD into `<home>/uhd`
2. `cmake`, then `make -j$(nproc-1)`
3. `sudo make install` and `sudo ldconfig`
4. `uhd_find_devices` (a failure here just means no USRP is attached)
5. `sudo uhd_images_downloader`
6. Install the udev rules and trigger `udevadm`, so USRPs are usable without root

### Examples

Auto-detect the host OS and just print/save the dependency list (no install):

```bash
python3 uhd_bare_metal_installer.py --list-only
```

Show exactly what would be run, without touching the system:

```bash
python3 uhd_bare_metal_installer.py --dry-run
```

Install on a bare-metal host matching one of UHD's Dockerfiles (needs root):

```bash
sudo python3 uhd_bare_metal_installer.py
```

Skip the `apt-get upgrade` step (safer on a machine you don't want fully upgraded):

```bash
sudo python3 uhd_bare_metal_installer.py --skip-upgrade
```

Force a specific Dockerfile instead of auto-detecting from `/etc/os-release`:

```bash
python3 uhd_bare_metal_installer.py \
  --dockerfile-url https://raw.githubusercontent.com/EttusResearch/uhd/master/.ci/docker/uhd-builder-ubuntu2604.Dockerfile
```

Install dependencies, then clone, build, and install UHD itself into `$HOME/uhd`:

```bash
sudo python3 uhd_bare_metal_installer.py --build
```

## Install Volk in a bare-metal environment

`volk_bare_metal_installer.py` builds and installs
[Volk](https://github.com/gnuradio/volk) from source, after
`uhd_bare_metal_installer.py` has installed the build dependencies. It
installs no packages itself. Instead it:

1. Derives the dependency list the same way `uhd_bare_metal_installer.py
   --list-only` does and saves it to `volk-dependencies.txt`.
2. Aborts with an error unless `uhd-dependencies.txt` exists, was created
   before `volk-dependencies.txt`, and has the same content (i.e. the
   dependencies installed for UHD are still current).
3. Clones Volk (`git clone --recursive`) into `$HOME/volk`, then runs
   `cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../`, `make -j$(nproc-1)`,
   `sudo make install`, and `sudo ldconfig`.

Run it as your normal user (not with `sudo`); `sudo` prompts for your
password at the install steps, and `~/volk` stays owned by you.

### Keeping the dependency lists current

Both `uhd-dependencies.txt` and `volk-dependencies.txt` are committed to
this repo. When EttusResearch updates its Dockerfile, the Volk installer's
content check fails until `uhd-dependencies.txt` is refreshed. To install
any new packages and refresh the list in one step:

```bash
sudo python3 uhd_bare_metal_installer.py --skip-upgrade
```

`python3 uhd_bare_metal_installer.py --list-only` refreshes the list without
installing anything. Use it only when the packages are already installed.

### Options

| Option | Description |
| --- | --- |
| `--dockerfile-url URL`, `--dockerfile-path PATH`, `--os-release-path PATH` | Same as for `uhd_bare_metal_installer.py`. |
| `--list-only` | Only parse and print/save the dependency list; do not check or build anything. |
| `-o`, `--output OUTPUT` | Path to save the extracted package list (default: `volk-dependencies.txt`). |
| `--uhd-deps PATH` | Package list written by `uhd_bare_metal_installer.py` to compare against (default: `uhd-dependencies.txt`). |
| `--dry-run` | Check the dependency lists and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before building. |
| `--home HOME` | Directory to clone/build Volk into. Default: the invoking user's home when run via `sudo` (`$SUDO_USER`), else `$HOME`. |

### Examples

Check the dependency lists and show the build steps, without running them:

```bash
python3 volk_bare_metal_installer.py --dry-run
```

Check the dependency lists, then clone, build, and install Volk into `$HOME/volk`:

```bash
python3 volk_bare_metal_installer.py
```
