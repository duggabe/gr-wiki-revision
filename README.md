# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

> **Note:** This is a work in progress.

## Tested builds

On 2026-09-25, the three `v1.0` installers (UHD, Volk, GNU Radio) were run
in order on Ubuntu 26.04 and built and installed the following versions
without errors:

| Component | Installer | Version |
| --- | --- | --- |
| UHD | `sudo python3 uhd_bare_metal_installer.py --build` | 4.11.0.0-0-g0d7ed3b1 |
| Volk | `python3 volk_bare_metal_installer.py` | 3.3.0 |
| GNU Radio | `python3 gnuradio_bare_metal_installer.py` | v3.11.0.0git-1174-gaee9fd3f |

The installers have also been tested on Ubuntu 24.04. On 2026-09-26 they
were tested on a clean Ubuntu 24.04 install, following only the
"Building GNU Radio from Source Code" page on the GNU Radio Wiki and the
`v1.0` scripts. Everything worked, and the resulting GNU Radio build has
the same components as the 26.04 build above. The installers work on any
Ubuntu release for which Ettus provides a UHD build Dockerfile (in
[`.ci/docker`](https://github.com/EttusResearch/uhd/tree/master/.ci/docker)),
but only 24.04 and 26.04 have been tested.

On 2026-10-02, the revised installers on `main` (see
[Changes since v1.0](#changes-since-v10)) were run on Ubuntu 26.04, with
`sudo`, and built, tested, and installed the following without errors:

| Component | Installer | Version | `make test` |
| --- | --- | --- | --- |
| UHD | `sudo python3 uhd_bare_metal_installer.py --build` | 4.11.0.0-0-g0d7ed3b1 | 109 of 109 passed |
| Volk | installed by the GNU Radio installer (`libvolk-dev`) | 3.3.0 (Ubuntu package) | — |
| GNU Radio | `sudo python3 gnuradio_bare_metal_installer.py --branch main` | v3.11.0.0git-1174-gaee9fd3f | 266 of 266 passed |

The clone and build directories and the build logs were owned by the
normal user, not root.

On 2026-10-03 the same `main` scripts were tested on a fresh install of
Ubuntu 26.04.1, downloading the two scripts from `main`. Both builds
finished without errors, and all tests passed: 109 of 109 for UHD and 266 of
266 for GNU Radio (the same GNU Radio version, v3.11.0.0git-1174-gaee9fd3f,
with the same enabled components as the build above). The `main` scripts
haven't yet been tested on Ubuntu 24.04 or with `--branch maint-3.10`.

> **Known limitation:** the installers only install UHD's build
> dependencies, not GNU Radio's own. CMake skips any GNU Radio component
> whose dependencies it can't find, so this GNU Radio build does **not**
> include `gr-qtgui` (the QT GUI blocks), `gr-soapy`, `gr-iio`, or the JACK
> and PortAudio audio back-ends.
>
> By default the installer builds GNU Radio's `main` branch, the 3.11
> development version, whose `gr-qtgui` requires Qt6, PyQt6, and Qwt built
> for Qt6. Ubuntu 24.04 and 26.04 have no packaged Qwt for Qt6. The
> released 3.10 series (`maint-3.10`, selectable with `--branch`) uses Qt5
> instead, which both releases package in full. How to provide the missing
> dependencies is still being worked out.
>
> To see which components your build includes:
>
> ```bash
> gnuradio-config-info --enabled-components
> ```

## Changes since v1.0

`v1.0` is the release the "Building GNU Radio from Source Code" wiki page
uses, and it stays available at its current links. These changes are in
`v1.1` (tagged 2026-10-03):

- **Volk is no longer built from source.** `volk_bare_metal_installer.py`
  has been removed. GNU Radio still needs Volk (2.4.1 or later), so the
  GNU Radio installer now installs Ubuntu's `libvolk-dev`; see
  [Volk](#volk) below.
- **Simpler GNU Radio installer.** It no longer compares dependency lists;
  it only checks that `uhd-dependencies.txt` exists, i.e. that the UHD
  installer has been run.
- **`--branch` option for GNU Radio,** to build `main` (the default) or
  another branch or tag, such as `maint-3.10`.
- **Build logs and tests.** The UHD and GNU Radio builds run `make test`
  and save the `cmake`, `make`, and `make test` output to `cmake.log`,
  `make.log`, and `make_test.log` in their `build` directories. Any failure,
  including a failing test, stops the build before `sudo make install`.

Still under discussion with the GNU Radio developers: which GNU Radio branch
the wiki page should build, and installing GNU Radio's own dependencies so
that `gr-qtgui`, `gr-soapy`, `gr-iio`, JACK, and PortAudio are included. UHD
will continue to be built from source.

## Download the installers

You don't need to clone this repository. Download the two `v1.1` scripts
into one directory. The GNU Radio script uses code from the UHD script, so
both must be in the same directory:

```bash
mkdir -p ~/gr-installers
cd ~/gr-installers
for s in uhd gnuradio; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v1.1/${s}_bare_metal_installer.py
done
```

`v1.1` has been tested on Ubuntu 26.04 (see [Tested builds](#tested-builds)).
The wiki page currently uses `v1.0`, which has three scripts (UHD, Volk, and
GNU Radio) and was tested on 24.04 and 26.04. For `v1.0`, follow the wiki
page or the
[`v1.0` README](https://github.com/duggabe/gr-wiki-revision/blob/v1.0/README.md).
The rest of this README describes `v1.1`.

Look the scripts over before running them, and don't pipe a download
straight into `python3`, especially with `sudo`. Use `--dry-run` to see
what a script will do without changing anything, and `--help` for its
options.

## Run the installers in order

Run the two installers in this order, from the same directory. GNU Radio
builds on the dependencies (and UHD) that the UHD installer installs:

```bash
sudo python3 uhd_bare_metal_installer.py --build
python3 gnuradio_bare_metal_installer.py
```

The UHD installer needs `sudo`, because it installs packages. The GNU Radio
installer works with or without `sudo`. Either way, the clone and build
steps run as you, so `~/uhd` and `~/gnuradio` belong to you.

The UHD installer writes `uhd-dependencies.txt` into the directory it runs
from. The GNU Radio installer stops with an error unless that file exists,
so run both from the same directory (or point the GNU Radio installer at
the file with `--uhd-deps`).

**Rebuilding.** Each installer clones into a new directory and stops if it
already exists. To rebuild, remove or rename `~/uhd` or `~/gnuradio` first.

### Volk

GNU Radio needs Volk 2.4.1 or later. The installers no longer build it;
instead, the GNU Radio installer's first step installs Ubuntu's package
(3.1.2 on Ubuntu 24.04, 3.3.0 on 26.04):

```bash
sudo apt-get install -y libvolk-dev
```

If you built Volk from source earlier (for example with `v1.0`), remove
that copy first. GNU Radio's `cmake` looks in `/usr/local` before `/usr`,
so it would otherwise keep using it:

```bash
cd ~/volk/build && sudo xargs rm -f < install_manifest.txt && sudo ldconfig
```

## Environment variables

Everything is installed under `/usr/local`. On Ubuntu 24.04 and 26.04 you
don't need to set `LD_LIBRARY_PATH`: Ubuntu already lists `/usr/local/lib`
in `/etc/ld.so.conf.d`, and the installers run `sudo ldconfig`. GNU Radio's
Python modules (including `from gnuradio import uhd`) are found without
`PYTHONPATH` too.

The one exception is UHD's own Python API (`import uhd`). The UHD source
build installs it in `/usr/local/lib/python3.X/site-packages`, which Ubuntu's
Python doesn't search. If you need it, add that directory to `PYTHONPATH`
in your shell startup file (for example `~/.bashrc` or `~/.bash_aliases`),
replacing `3.X` with your Python version:

```bash
export PYTHONPATH=/usr/local/lib/python3.X/site-packages:$PYTHONPATH
```

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
2. `cmake`, then `make -j$(nproc-1)`, then `make test` (UHD's unit tests)
3. `sudo make install` and `sudo ldconfig`
4. `uhd_find_devices` (a failure here just means no USRP is attached)
5. `sudo uhd_images_downloader`
6. Install the udev rules and trigger `udevadm`, so USRPs are usable without root

The output of `cmake`, `make`, and `make test` is shown as it runs and also
saved to `cmake.log`, `make.log`, and `make_test.log` in `<home>/uhd/host/build`,
as with `2>&1 | tee <file>`. If any of them fails, the installer stops, so a
failing unit test prevents installing that build.

Although the installer runs with `sudo`, the steps without `sudo` (clone,
`cmake`, `make`, `make test`, `uhd_find_devices`) run as the user who invoked `sudo`, so
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

## Install GNU Radio in a bare-metal environment

`gnuradio_bare_metal_installer.py` builds and installs
[GNU Radio](https://github.com/gnuradio/gnuradio) from source, after the UHD
installer has run. It:

1. Aborts with an error unless `uhd-dependencies.txt` exists (the UHD
   installer writes it).
2. Installs Volk with `sudo apt-get install -y libvolk-dev` (see [Volk](#volk)).
3. Clones GNU Radio into `$HOME/gnuradio` and checks out the chosen branch
   (`main`, the 3.11 development version, by default).
4. Runs `cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../`, `make -j$(nproc-1)`,
   and `make test` (GNU Radio's tests), then `sudo make install` and
   `sudo ldconfig`.

The output of `cmake`, `make`, and `make test` is shown as it runs and also
saved to `cmake.log`, `make.log`, and `make_test.log` in
`$HOME/gnuradio/build`. If any of them fails, the installer stops, so a
failing test prevents installing that build.

Run it either as your normal user or with `sudo`; the clone and build steps
run as you either way. The GNU Radio build usually takes longer than
`sudo`'s 15-minute password cache, so without `sudo` expect a password
prompt at the `sudo` steps (Volk's install at the start, and
`sudo make install` at the end, where the build waits even with `-y`).
Starting with `sudo` avoids that.

### Options

| Option | Description |
| --- | --- |
| `--branch BRANCH` | GNU Radio branch (or tag) to check out and build, e.g. `main` or `maint-3.10` (default: `main`). |
| `--uhd-deps PATH` | Package list written by `uhd_bare_metal_installer.py`, which must exist (default: `uhd-dependencies.txt`). |
| `--dry-run` | Check for the UHD package list and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before building. |
| `--build` | Accepted for consistency with `uhd_bare_metal_installer.py` and ignored: building GNU Radio is already the default. |
| `--home HOME` | Directory to clone/build GNU Radio into. Default: the invoking user's home when run via `sudo` (`$SUDO_USER`), else `$HOME`. |

### Examples

Show the build steps without running them:

```bash
python3 gnuradio_bare_metal_installer.py --dry-run
```

Clone, build, and install GNU Radio's `main` branch into `$HOME/gnuradio`:

```bash
python3 gnuradio_bare_metal_installer.py
```

Build the 3.10 release series instead:

```bash
python3 gnuradio_bare_metal_installer.py --branch maint-3.10
```
