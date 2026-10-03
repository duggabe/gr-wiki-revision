# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

> **Note:** This is a work in progress.

## Tested builds

**Current scripts (`main`), 2026-10-02 and 2026-10-03, Ubuntu 26.04.** The
two installers built, tested, and installed the following:

| Component | Installer | Version | `make test` |
| --- | --- | --- | --- |
| UHD | `sudo python3 uhd_bare_metal_installer.py --build` | 4.11.0.0-0-g0d7ed3b1 | 109 of 109 passed |
| Volk | installed by the GNU Radio installer (`libvolk-dev`) | 3.3.0 (Ubuntu package) | — |
| GNU Radio | `sudo python3 gnuradio_bare_metal_installer.py` (`maint-3.10`) | 3.10.12.0 (v3.10.12.0-92-gc1a73dc34) | 269 of 269 passed |

This GNU Radio build has no disabled components: `gr-qtgui`, `gr-iio`
(with `libad9361`), `gr-soapy`, `gr-uhd`, ControlPort with Thrift, and the
ALSA, OSS, JACK, and PortAudio audio back-ends are all enabled. To see which
components your build includes:

```bash
gnuradio-config-info --enabled-components
```

On this machine the first GNU Radio run stopped at `make test`: one test,
`grc_tests`, failed because of empty directories left by a previously
removed GNU Radio install. After removing them, all 269 tests passed and the
install completed. The installer now checks for such leftovers before
building (see [Removing an earlier install](#removing-an-earlier-install)).

Not yet tested with the current scripts: a clean install, and Ubuntu 24.04.

**Earlier releases:**

- **`v1.1`** (2026-10-02 and 2026-10-03, Ubuntu 26.04, including a fresh
  install of 26.04.1): UHD 4.11.0.0 (109 of 109 tests) and GNU Radio `main`,
  v3.11.0.0git-1174-gaee9fd3f (266 of 266 tests). That build lacked
  `gr-qtgui`, `gr-iio`, `gr-soapy`, JACK, and PortAudio, because only UHD's
  dependencies were installed.
- **`v1.0`** (2026-09-25 on Ubuntu 26.04; 2026-09-26 on a clean Ubuntu
  24.04 install, following only the "Building GNU Radio from Source Code"
  wiki page): UHD 4.11.0.0, Volk 3.3.0 built from source, and GNU Radio
  v3.11.0.0git-1174-gaee9fd3f, with the same missing components.

The UHD installer works on any Ubuntu release for which Ettus provides a UHD
build Dockerfile (in
[`.ci/docker`](https://github.com/EttusResearch/uhd/tree/master/.ci/docker)).
The GNU Radio installer needs an Ubuntu release whose own `gnuradio` package
is a 3.10 release (22.04 and later). Only 24.04 and 26.04 have been tested.

> **Known limitation:** GNU Radio's `main` branch (the 3.11 development
> version, `--branch main`) needs Qt6, PyQt6, and Qwt built for Qt6 for its
> `gr-qtgui`. Ubuntu 24.04 and 26.04 have no packaged Qwt for Qt6, and the
> dependency list the installer uses is for the Qt5-based 3.10 series. So a
> `main` build still lacks `gr-qtgui`. The default branch, `maint-3.10`, is
> not affected.

## Releases and changes

`v1.0` is the release the "Building GNU Radio from Source Code" wiki page
uses. `v1.0` and `v1.1` stay available at their links.

**On `main` since `v1.1`** (will be in the next release):

- **GNU Radio's own dependencies are installed.** The GNU Radio installer
  fetches the build dependencies of Ubuntu's own `gnuradio` package for your
  Ubuntu release, leaves out the ones that don't apply, adds a few run-time
  packages, and installs them. See
  [GNU Radio's dependencies](#gnu-radios-dependencies).
- **The default GNU Radio branch is `maint-3.10`,** the 3.10 release
  series, instead of `main`.
- **A check for leftovers of an earlier install,** which would make GNU
  Radio's tests fail. See
  [Removing an earlier install](#removing-an-earlier-install).

**In `v1.1`** (2026-10-03), since `v1.0`:

- **Volk is no longer built from source.** `volk_bare_metal_installer.py`
  has been removed; Volk comes from Ubuntu's `libvolk-dev`.
- **Simpler GNU Radio installer.** It no longer compares dependency lists;
  it only checks that `uhd-dependencies.txt` exists, i.e. that the UHD
  installer has been run.
- **`--branch` option for GNU Radio.**
- **Build logs and tests.** The UHD and GNU Radio builds run `make test`
  and save the `cmake`, `make`, and `make test` output to `cmake.log`,
  `make.log`, and `make_test.log` in their `build` directories. Any failure,
  including a failing test, stops the build before `sudo make install`.

UHD will continue to be built from source.

## Download the installers

You don't need to clone this repository. Download the two scripts into one
directory. The GNU Radio script uses code from the UHD script, so both must
be in the same directory:

```bash
mkdir -p ~/gr-installers
cd ~/gr-installers
for s in uhd gnuradio; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v1.1/${s}_bare_metal_installer.py
done
```

These links are for `v1.1`, the latest release. It doesn't yet have the
changes listed under "On `main` since `v1.1`" above; to try those, replace
`v1.1` with `main` in the link. The wiki page currently uses `v1.0`, which
has three scripts (UHD, Volk, and GNU Radio); for it, follow the wiki page
or the
[`v1.0` README](https://github.com/duggabe/gr-wiki-revision/blob/v1.0/README.md).
The rest of this README describes the scripts on `main`.

Look the scripts over before running them, and don't pipe a download
straight into `python3`, especially with `sudo`. Use `--dry-run` to see
what a script will do without changing anything, and `--help` for its
options.

## Run the installers in order

Run the two installers in this order, from the same directory:

```bash
sudo python3 uhd_bare_metal_installer.py --build
sudo python3 gnuradio_bare_metal_installer.py
```

The UHD installer installs UHD's build dependencies, then builds, tests, and
installs UHD. The GNU Radio installer installs GNU Radio's dependencies,
then builds, tests, and installs GNU Radio (the 3.10 release series by
default).

Both install packages, so both need root for those steps. The UHD installer
must be started with `sudo`. The GNU Radio installer also works without
`sudo`, prompting for your password at its `sudo` steps. Either way, the
clone and build steps run as you, so `~/uhd` and `~/gnuradio` belong to you.

The UHD installer writes `uhd-dependencies.txt` into the directory it runs
from. The GNU Radio installer stops with an error unless that file exists,
so run both from the same directory (or point the GNU Radio installer at
the file with `--uhd-deps`).

**Rebuilding.** Each installer clones into a new directory and stops if it
already exists. To rebuild, remove or rename `~/uhd` or `~/gnuradio` first,
and see [Removing an earlier install](#removing-an-earlier-install).

### Removing an earlier install

Before building a different GNU Radio version or branch, remove the
installed one. Each build directory has an `install_manifest.txt` listing
the files `make install` put in `/usr/local`:

```bash
cd ~/gnuradio/build && sudo xargs rm -f < install_manifest.txt && sudo ldconfig
```

That removes files but leaves their directories behind, empty. Remove those
too:

```bash
sudo rm -rf /usr/local/lib/python3*/dist-packages/gnuradio \
            /usr/local/include/gnuradio /usr/local/share/gnuradio \
            /usr/local/lib/cmake/gnuradio /usr/local/share/doc/gnuradio-*
```

The empty directories matter: Python treats an empty directory as a valid,
empty package, so GNU Radio's `grc_tests` find the leftover instead of the
code being built, and fail. The GNU Radio installer checks for such
leftovers before building and stops with the exact `rm` command to run.

If you built Volk from source earlier (with `v1.0`), remove that copy as
well. GNU Radio's `cmake` looks in `/usr/local` before `/usr`, so it would
otherwise keep using it instead of Ubuntu's package:

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

1. Derives GNU Radio's dependency list and saves it to
   `gnuradio-dependencies.txt` (see
   [GNU Radio's dependencies](#gnu-radios-dependencies)).
2. Aborts with an error unless `uhd-dependencies.txt` exists (the UHD
   installer writes it).
3. Aborts with an error if empty directories from an earlier, removed GNU
   Radio install are left in `/usr/local` (see
   [Removing an earlier install](#removing-an-earlier-install)).
4. Runs `sudo apt-get update` and `sudo apt-get install -y` for the
   dependency list.
5. Clones GNU Radio into `$HOME/gnuradio` and checks out the chosen branch
   (`maint-3.10`, the 3.10 release series, by default).
6. Runs `cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../`, `make -j$(nproc-1)`,
   and `make test` (GNU Radio's tests), then `sudo make install` and
   `sudo ldconfig`.

The output of `cmake`, `make`, and `make test` is shown as it runs and also
saved to `cmake.log`, `make.log`, and `make_test.log` in
`$HOME/gnuradio/build`. If any of them fails, the installer stops, so a
failing test prevents installing that build.

Run it either as your normal user or with `sudo`; the clone and build steps
run as you either way. The GNU Radio build usually takes longer than
`sudo`'s 15-minute password cache, so without `sudo` expect a password
prompt at the `sudo` steps (the package install at the start, and
`sudo make install` at the end, where the build waits even with `-y`).
Starting with `sudo` avoids that.

### GNU Radio's dependencies

UHD's Dockerfile only lists what UHD needs, so the GNU Radio installer
installs GNU Radio's own dependencies. Rather than hardcoding a list, it
fetches the `debian/control` file of Ubuntu's own `gnuradio` package for
your Ubuntu release from Launchpad and takes its `Build-Depends`: the same
list `apt-get build-dep gnuradio` uses. Then it:

- **Leaves out** `libuhd-dev` (UHD is built from source; Ubuntu's older copy
  would conflict) and the packages only needed to build the Debian package
  or the documentation (`debhelper-compat`, `dh-python`, `dpkg-dev`,
  `graphviz`, `xmlto`, `libjs-mathjax`).
- **Skips** entries meant for other operating systems or architectures.
- **Adds** run-time packages a build-dependency list doesn't cover:
  `python3-qtpy`, `python3-pyqtgraph`, `python3-matplotlib`, and
  `soapysdr-tools` (and makes sure `libvolk-dev` and `python3-packaging`
  are included).

On Ubuntu 26.04 that gives 66 packages. Ubuntu's `gnuradio` package is a
3.10 release, which uses Qt5, so the list fits `maint-3.10`. GNU Radio needs
Volk 2.4.1 or later; `libvolk-dev` on the list provides it (3.1.2 on Ubuntu
24.04, 3.3.0 on 26.04).

### Options

| Option | Description |
| --- | --- |
| `--branch BRANCH` | GNU Radio branch (or tag) to check out and build, e.g. `maint-3.10` or `main` (default: `maint-3.10`). |
| `--control-url URL` | URL of the `debian/control` file to take GNU Radio's `Build-Depends` from. Default: Ubuntu's `gnuradio` package for the host's release (from `/etc/os-release`), on Launchpad. |
| `--control-path PATH` | Read the `debian/control` file from a local path instead of fetching it. |
| `--os-release-path PATH` | Path to read the Ubuntu codename from (default: `/etc/os-release`). |
| `--list-only` | Only derive and print/save the dependency list; do not install or build anything. |
| `-o`, `--output OUTPUT` | Path to save the dependency list (default: `gnuradio-dependencies.txt`). |
| `--uhd-deps PATH` | Package list written by `uhd_bare_metal_installer.py`, which must exist (default: `uhd-dependencies.txt`). |
| `--dry-run` | Derive the dependency list and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before installing and building. |
| `--build` | Accepted for consistency with `uhd_bare_metal_installer.py` and ignored: building GNU Radio is already the default. |
| `--home HOME` | Directory to clone/build GNU Radio into. Default: the invoking user's home when run via `sudo` (`$SUDO_USER`), else `$HOME`. |

### Examples

Just print and save the dependency list:

```bash
python3 gnuradio_bare_metal_installer.py --list-only
```

Show the packages and build steps without running anything:

```bash
python3 gnuradio_bare_metal_installer.py --dry-run
```

Install the dependencies, then clone, build, and install the 3.10 release
series into `$HOME/gnuradio`:

```bash
sudo python3 gnuradio_bare_metal_installer.py
```

Build the `main` branch (3.11 development) instead:

```bash
sudo python3 gnuradio_bare_metal_installer.py --branch main
```
