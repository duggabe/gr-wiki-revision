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
