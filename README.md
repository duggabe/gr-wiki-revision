# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

> **Note:** This is a work in progress.

## Tested builds

On 2026-09-25, the three installers were run in order on Ubuntu 26.04 and
built and installed the following versions without errors:

| Component | Installer | Version |
| --- | --- | --- |
| UHD | `sudo python3 uhd_bare_metal_installer.py --build` | 4.11.0.0-0-g0d7ed3b1 |
| Volk | `python3 volk_bare_metal_installer.py` | 3.3.0 |
| GNU Radio | `python3 gnuradio_bare_metal_installer.py` | v3.11.0.0git-1174-gaee9fd3f |

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

Although the installer runs with `sudo`, the steps without `sudo` (clone,
`cmake`, `make`, `uhd_find_devices`) run as the user who invoked `sudo`, so
`<home>/uhd` belongs to you, not root. Only the `sudo` steps run as root.

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

Run it either as your normal user or with `sudo`. Either way, the clone and
build steps run as you, so `~/volk` belongs to you; only `sudo make install`
and `sudo ldconfig` run as root. Without `sudo`, you're prompted for your
password when the build reaches the install step.

### Keeping the dependency lists current

`uhd-dependencies.txt` and `volk-dependencies.txt` are committed to this
repo. When EttusResearch updates its Dockerfile, the Volk and GNU Radio
installers' content checks fail until `uhd-dependencies.txt` is refreshed. To install
any new packages and refresh the list in one step:

```bash
sudo python3 uhd_bare_metal_installer.py --skip-upgrade
```

`python3 uhd_bare_metal_installer.py --list-only` refreshes the list without
installing anything. Use it only when the packages are already installed.

Git doesn't preserve file timestamps, so on a fresh clone the committed
lists may not be in the order the checks expect. Refresh them in order
first:

```bash
python3 uhd_bare_metal_installer.py --list-only
python3 volk_bare_metal_installer.py --list-only
```

### Options

| Option | Description |
| --- | --- |
| `--dockerfile-url URL`, `--dockerfile-path PATH`, `--os-release-path PATH` | Same as for `uhd_bare_metal_installer.py`. |
| `--list-only` | Only parse and print/save the dependency list; do not check or build anything. |
| `-o`, `--output OUTPUT` | Path to save the extracted package list (default: `volk-dependencies.txt`). |
| `--uhd-deps PATH` | Package list written by `uhd_bare_metal_installer.py` to compare against (default: `uhd-dependencies.txt`). |
| `--dry-run` | Check the dependency lists and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before building. |
| `--build` | Accepted for consistency with `uhd_bare_metal_installer.py` and ignored: building Volk is already the default. |
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

## Install GNU Radio in a bare-metal environment

`gnuradio_bare_metal_installer.py` builds and installs
[GNU Radio](https://github.com/gnuradio/gnuradio) from source, after the UHD
and Volk installers have run. Like the Volk installer, it installs no
packages itself. Instead it:

1. Derives the dependency list the same way `uhd_bare_metal_installer.py
   --list-only` does and saves it to `gnuradio-dependencies.txt`.
2. Aborts with an error unless `uhd-dependencies.txt`,
   `volk-dependencies.txt`, and `gnuradio-dependencies.txt` exist, were
   created in that order, and all have the same content.
3. Clones GNU Radio into `$HOME/gnuradio`, then runs
   `cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../`, `make -j$(nproc-1)`,
   `sudo make install`, and `sudo ldconfig`.

Run it either as your normal user or with `sudo`; as with Volk, the clone
and build steps run as you either way. The GNU Radio build usually takes
longer than `sudo`'s 15-minute password cache, so without `sudo` expect a
password prompt at the install step (the build waits there, even with `-y`).
Starting with `sudo` avoids that.

### Options

Same as for `volk_bare_metal_installer.py` (default `-o` is
`gnuradio-dependencies.txt`), plus:

| Option | Description |
| --- | --- |
| `--volk-deps PATH` | Package list written by `volk_bare_metal_installer.py` to compare against (default: `volk-dependencies.txt`). |

### Examples

Check the dependency lists and show the build steps, without running them:

```bash
python3 gnuradio_bare_metal_installer.py --dry-run
```

Check the dependency lists, then clone, build, and install GNU Radio into `$HOME/gnuradio`:

```bash
python3 gnuradio_bare_metal_installer.py
```
