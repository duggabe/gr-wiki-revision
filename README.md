# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

The main content is Python scripts that build
[GNU Radio](https://github.com/gnuradio/gnuradio) from source on Ubuntu,
without Docker. They back the "Building GNU Radio from Source Code" page on
the GNU Radio Wiki. The work is in two phases, and each has its own pair of
scripts:

- **Phase 1** (releases `v1.x`) builds both
  [UHD](https://github.com/EttusResearch/uhd) and the GNU Radio 3.10 release
  series from source. Each installer works out the packages its project
  needs from an upstream list rather than a hardcoded one, installs them,
  then builds, tests, and installs the project into `/usr/local`.
- **Phase 2** (release `v2.0`) is for developers of GNU Radio itself. It
  installs UHD from the Ettus Research PPA instead of building it, then
  builds GNU Radio from your own fork, so that you can work on an issue and
  submit a pull request. See
  [Phase 2](#phase-2-uhd-from-the-ettus-ppa-gnu-radio-from-your-fork).

Most of this README describes Phase 1; Phase 2 has its own section at the
end.

The current Phase 1 release, `v1.2`, has been tested on Ubuntu 24.04 and
26.04. It installs UHD 4.11.0.0 and GNU Radio 3.10.12.0 with every component
enabled, including the QT GUI blocks. In short:

```bash
mkdir -p ~/gr-installers && cd ~/gr-installers
for s in uhd gnuradio; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v1.2/${s}_bare_metal_installer.py
done
sudo python3 uhd_bare_metal_installer.py --build
sudo python3 gnuradio_bare_metal_installer.py
```

Look the scripts over before running them; see
[Download the installers](#download-the-installers) and
[Run the installers in order](#run-the-installers-in-order) for details.

> **Note:** This is a work in progress. Building GNU Radio's `main` branch
> (the 3.11 development version) is not fully supported yet; see the known
> limitation below.

## Tested builds

**Phase 2 scripts (`v2.0`), 2026-10-10, clean install of Ubuntu 26.04.**
The two Phase 2 scripts were downloaded onto a freshly installed machine and
run as described in
[Phase 2](#phase-2-uhd-from-the-ettus-ppa-gnu-radio-from-your-fork): UHD
from the Ettus PPA, then GNU Radio's `main` branch built from a fork:

| Component | Script | Version | `make test` |
| --- | --- | --- | --- |
| UHD | `sudo python3 gnuradio_dependencies_installer.py` (Ettus PPA) | 4.11.0.0-0ubuntu1~resolute3 | — (not built) |
| GNU Radio | `sudo python3 gnuradio_clone_builder.py` (`main`) | v3.11.0.0git-1193-g0403558f | 271 of 271 passed |

The build finished without errors. Phase 2 has not yet been tested on
Ubuntu 24.04.

**Phase 1 scripts (`v1.2`), 2026-10-02 and 2026-10-03, Ubuntu 26.04.** The
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

**Clean install of Ubuntu 24.04, 2026-10-04.** The same scripts were run on
a freshly installed Ubuntu 24.04 machine, downloading the two scripts from
`main` and nothing else. Both builds finished without errors: 109 of 109
UHD tests and 268 of 268 GNU Radio tests passed, and GNU Radio 3.10.12.0 was
installed with the same 42 enabled components as the 26.04 build above,
including `gr-qtgui`, `gr-iio`, `gr-soapy`, JACK, and PortAudio.

UHD's own `cmake.log` lists two disabled UHD components on both machines.
Both are expected: "B300" needs NI's separate `nib310rio-dev` driver
package (B200/B210 support is a different component and is enabled), and
"RFNoC/FPGA Development Files" is off by default in UHD.

Not yet tested with the `v1.2` scripts: a clean install of Ubuntu 26.04
(the 26.04 build above was on a machine with earlier builds).

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
> not affected. The same applies to a `main` build made with the Phase 2
> scripts.

## Releases and changes

`v2.0` is the Phase 2 release and `v1.2` is the current Phase 1 release.
`v1.0` and `v1.1` stay available at their links.

**In `v2.0`** (2026-10-10), two new scripts for Phase 2. The Phase 1
installers are unchanged since `v1.2`.

- **`gnuradio_dependencies_installer.py`** installs UHD from the
  [Ettus PPA](https://launchpad.net/~ettusresearch/+archive/ubuntu/uhd) and
  GNU Radio's dependencies with `apt-get`; nothing is compiled.
- **`gnuradio_clone_builder.py`** builds, tests, and installs GNU Radio from
  a clone that is already on the machine, normally your own fork. It can be
  run again after every change.
- **The number of `make` jobs is limited by the machine's memory,** so that
  the build is not killed for running out of it.

**In `v1.2`** (2026-10-04), since `v1.1`:

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

The `v1.x` releases build UHD from source; `v2.0` installs it from the
Ettus PPA.

## Download the installers

You don't need to clone this repository. Download the two scripts into one
directory. The GNU Radio script uses code from the UHD script, so both must
be in the same directory:

```bash
mkdir -p ~/gr-installers
cd ~/gr-installers
for s in uhd gnuradio; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v1.2/${s}_bare_metal_installer.py
done
```

These links are for `v1.2`, the current Phase 1 release, tested on Ubuntu
24.04 and 26.04 (see [Tested builds](#tested-builds)). `v1.0` has three
scripts (UHD, Volk, and GNU Radio); for it, see the
[`v1.0` README](https://github.com/duggabe/gr-wiki-revision/blob/v1.0/README.md).
The sections from here up to
[Phase 2](#phase-2-uhd-from-the-ettus-ppa-gnu-radio-from-your-fork) describe
`v1.2`.

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
            /usr/local/lib/python3*/dist-packages/pmt \
            /usr/local/include/gnuradio /usr/local/include/pmt \
            /usr/local/share/gnuradio /usr/local/etc/gnuradio \
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

## Phase 2: UHD from the Ettus PPA, GNU Radio from your fork

Phase 2 is for a developer of GNU Radio code who needs to test additions or
changes outside a Docker container. It has two steps, each with its own
script:

1. `gnuradio_dependencies_installer.py` installs UHD from the Ettus Research
   PPA and everything GNU Radio needs, using `apt-get`. Nothing is compiled.
2. `gnuradio_clone_builder.py` builds, tests, and installs GNU Radio from
   your own fork, which you clone into your home directory.

Phase 2 (`v2.0`) has been tested on a clean install of Ubuntu 26.04; see
[Tested builds](#tested-builds).

### Download the Phase 2 scripts

```bash
mkdir -p ~/gr-installers
cd ~/gr-installers
for s in gnuradio_dependencies_installer gnuradio_clone_builder; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v2.0/${s}.py
done
```

Each script works on its own; neither needs the Phase 1 installers. Look
them over before running them. Both have `--help` and `--dry-run`.

### Before you start

Phase 2 needs a system without another GNU Radio or a source-built UHD on
it. The scripts check for both and stop with the commands to run if they
find either.

- If Ubuntu's own GNU Radio packages are installed, remove them:

  ```bash
  sudo apt-get remove gnuradio gnuradio-dev
  ```

- If you built UHD from source (for example with Phase 1), remove it. GNU
  Radio's `cmake` looks in `/usr/local` before `/usr`, so it would otherwise
  keep using that copy instead of the PPA's:

  ```bash
  cd ~/uhd/host/build && sudo xargs rm -f < install_manifest.txt
  sudo rm -rf /usr/local/include/uhd /usr/local/lib/uhd /usr/local/lib/cmake/uhd /usr/local/share/uhd
  sudo ldconfig
  ```

- If you installed GNU Radio with Phase 1, remove it as described in
  [Removing an earlier install](#removing-an-earlier-install).

### Step 1: install UHD and the dependencies

```bash
sudo python3 gnuradio_dependencies_installer.py
```

The script runs the equivalent of:

```bash
# enable "Source code" (deb-src) in /etc/apt/sources.list.d/ubuntu.sources
sudo apt-get update
sudo apt-get install -y software-properties-common git
sudo add-apt-repository -y ppa:ettusresearch/uhd
sudo apt-get install -y --no-install-recommends uhd-host libuhd-dev
sudo apt-get build-dep -y gnuradio
sudo apt-get install -y python3-qtpy python3-pyqtgraph python3-matplotlib soapysdr-tools
sudo uhd_images_downloader
```

- **"Source code"** is the same change the "Source code" box in the
  "Software & Updates" app makes; `apt-get build-dep` needs it. The original
  file is saved as `ubuntu.sources.bak`.
- **`--no-install-recommends`** matters: UHD's packages recommend Ubuntu's
  own `gnuradio` packages, which would otherwise be installed into `/usr`,
  next to the GNU Radio you are about to build.
- **`apt-get build-dep gnuradio`** installs the build dependencies of
  Ubuntu's own `gnuradio` package for your release, so no package list is
  hardcoded. The last `apt-get` line adds run-time packages that list
  doesn't cover.
- **udev rules** for USRP devices are installed by the `uhd-host` package.
  UHD's own Python API (`import uhd`) works without `PYTHONPATH`.

| Option | Description |
| --- | --- |
| `--dry-run` | Run the checks and print what would be done, without changing anything or requiring root. |
| `-y`, `--yes` | Do not prompt for confirmation before installing. |
| `--no-images` | Do not run `uhd_images_downloader` (the USRP FPGA images, a large download). |
| `--sources-path PATH` | Ubuntu's apt sources file, in which to enable source code (default: `/etc/apt/sources.list.d/ubuntu.sources`). |
| `--os-release-path PATH` | Path to read the OS name and version from (default: `/etc/os-release`). |

### Step 2: build GNU Radio from your fork

Fork <https://github.com/gnuradio/gnuradio> on GitHub, clone your fork into
your home directory, and check out the branch you want to work on:

```bash
cd ~
git clone https://github.com/<your-username>/gnuradio.git
cd gnuradio
git remote add upstream https://github.com/gnuradio/gnuradio.git
git fetch upstream
git checkout -b issue8218 upstream/main      # example branch name
```

Then build, test, and install whatever is checked out:

```bash
cd ~/gr-installers
sudo python3 gnuradio_clone_builder.py
```

The script does not clone anything and does not change branches. It runs
`cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../`, `make`, and `make test` in
`~/gnuradio/build`, saving their output to `cmake.log`, `make.log`, and
`make_test.log` there, then `sudo make install` and `sudo ldconfig`. If any
step fails, including a failing test, it stops before installing.

Run it again after every change to the code: it reuses the `build`
directory, so only what changed is rebuilt. It works with or without `sudo`;
the build runs as you either way, and files that `sudo make install` leaves
root-owned in the `build` directory are given back to you before the next
build.

Before building, the script checks that the directory holds GNU Radio's
source code, that `libuhd-dev` is installed (Step 1 was run), that Ubuntu's
own `gnuradio` packages are not installed, and that no empty directories
from a removed GNU Radio install are left in `/usr/local`.

**Memory and `make` jobs.** Compiling GNU Radio needs a lot of memory. With
too many `make` jobs for the memory in the machine, the kernel kills the
compiler part-way through the build. The script uses one job less than the
number of processor cores, but no more than one for each 2 GB of memory
(7 jobs on a 16-core machine with 16 GB). Use `--jobs` to choose the number
yourself.

| Option | Description |
| --- | --- |
| `--source-dir DIR` | The GNU Radio clone to build. Default: `gnuradio` in the home directory of the invoking user (`$SUDO_USER` when run via `sudo`). |
| `--jobs N` | Number of parallel `make` jobs. Default: one less than the number of processor cores, but no more than one per 2 GB of memory. |
| `--cmake-args "ARGS"` | Extra options for `cmake`, in one quoted string written with `=`, e.g. `--cmake-args="-DENABLE_GR_FEC=OFF -DENABLE_GR_VOCODER=OFF"`. `cmake` remembers them in the build directory until they are changed or the directory is removed. |
| `--no-install` | Stop after the tests: do not run `sudo make install` and `sudo ldconfig`. |
| `--dry-run` | Run the checks and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before building. |

When the change works, commit it with a sign-off (`git commit -s`, which GNU
Radio requires), push the branch to your fork, and open a pull request. See
GNU Radio's
[CONTRIBUTING.md](https://github.com/gnuradio/gnuradio/blob/main/CONTRIBUTING.md).

A `main` build made this way does not include `gr-qtgui`; see the known
limitation under [Tested builds](#tested-builds).
