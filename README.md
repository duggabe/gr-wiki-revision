# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

The main content is two Python scripts that build
[GNU Radio](https://github.com/gnuradio/gnuradio) from source on Ubuntu,
without Docker. They back the "Building GNU Radio from Source Code" page on
the GNU Radio Wiki. The current release is `v2.3`.

The scripts are for developers of GNU Radio itself: they install
[UHD](https://github.com/EttusResearch/uhd) from the Ettus Research PPA
instead of building it, then build GNU Radio from your own fork, so that
you can work on an issue and submit a pull request.

## UHD from the Ettus PPA, GNU Radio from your fork

The scripts are for a developer of GNU Radio code who needs to test
additions or changes outside a Docker container. There are two steps, each
with its own script:

1. `gnuradio_dependencies_installer.py` installs UHD from the Ettus Research
   PPA and everything GNU Radio needs, using `apt-get`. Nothing is compiled.
2. `gnuradio_clone_builder.py` builds, tests, and installs GNU Radio from
   your own fork, which you clone into your home directory.

### Download the scripts

```bash
mkdir -p ~/gr-installers
cd ~/gr-installers
for s in gnuradio_dependencies_installer gnuradio_clone_builder; do
  wget https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v2.3/${s}.py
done
```

Each script works on its own and needs nothing else from this repository. Look
them over before running them. Both have `--help` and `--dry-run`.

### Before you start

The scripts need a system without another GNU Radio or a source-built UHD on
it. The scripts check for both and stop with the commands to run if they
find either.

- If Ubuntu's own GNU Radio packages are installed, remove them:

  ```bash
  sudo apt-get remove gnuradio gnuradio-dev
  ```

- If you built UHD from source earlier, remove it. GNU
  Radio's `cmake` looks in `/usr/local` before `/usr`, so it would otherwise
  keep using that copy instead of the PPA's:

  ```bash
  cd ~/uhd/host/build && sudo xargs rm -f < install_manifest.txt
  sudo rm -rf /usr/local/include/uhd /usr/local/lib/uhd /usr/local/lib/cmake/uhd /usr/local/share/uhd
  sudo ldconfig
  ```

- If you built and installed GNU Radio from source earlier, remove it with
  steps 1 and 2 of
  [Changing branches, or removing the installed GNU Radio](#changing-branches-or-removing-the-installed-gnu-radio).

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
sudo apt-get install -y libboost-dev libboost-chrono-dev libboost-filesystem-dev ...   # see below
sudo apt-get build-dep -y gnuradio
sudo apt-get install -y python3-qtpy python3-pyqtgraph python3-matplotlib soapysdr-tools
sudo apt-get install -y soapysdr0.8-module-rtlsdr soapysdr0.8-module-hackrf ...   # see below
sudo uhd_images_downloader
```

- **"Source code"** is the same change the "Source code" box in the
  "Software & Updates" app makes; `apt-get build-dep` needs it. The original
  file is saved as `ubuntu.sources.bak`.
- **`--no-install-recommends`** matters: UHD's packages recommend Ubuntu's
  own `gnuradio` packages, which would otherwise be installed into `/usr`,
  next to the GNU Radio you are about to build.
- **Boost development packages** (since `v2.3`): UHD's cmake files need
  Boost's `chrono`, `date_time`, `filesystem`, `program_options`,
  `serialization`, `thread`, and `unit_test_framework`, but the PPA's
  `libuhd-dev` does not depend on them, and `apt-get build-dep gnuradio`
  brings only some. Without them GNU Radio's cmake prints
  `Boost_FOUND = FALSE` under "Configuring gr-uhd support" and builds GNU
  Radio without `gr-uhd`, with no error. The script installs the same Boost
  packages that Ubuntu's own `libuhd-dev` depends on (without the Python
  one).
- **`apt-get build-dep gnuradio`** installs the build dependencies of
  Ubuntu's own `gnuradio` package for your release, so no package list is
  hardcoded. The `apt-get` line after it adds run-time packages that list
  doesn't cover.
- **SoapySDR device modules** (since `v2.2`) are the drivers `gr-soapy` uses
  for an RTL-SDR, HackRF, Airspy, bladeRF, LimeSDR, PlutoSDR, and others. The
  SoapySDR library only recommends them and `apt-get build-dep` leaves them
  out, so without this step `gr-soapy` is built but finds no devices. The
  script installs every module that Ubuntu's `soapysdr-module-all` package
  lists for your release, except the UHD module: that one needs Ubuntu's
  own, older UHD library, and a USRP is used through `gr-uhd` anyway.
  `--dry-run` prints the list. With the modules installed,
  `SoapySDRUtil --find` may print lines starting with `ALSA lib` or
  `RtApi::getDeviceInfo` before it lists your device. They come from
  SoapySDR's audio module looking at the computer's sound devices and can
  be ignored.
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

Before `make test`, the script runs `git clean -fdX grc/tests/resources` in
the source directory. GNU Radio's GRC tests write generated files there, and
on a build without `gr-qtgui` two of them make the next test run fail
(`grc_tests`). Only those generated files, which git ignores, are removed;
your source code is not touched.

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

A `main` build made this way does not include `gr-qtgui`; see
[Known limitation](#known-limitation).

To see which components your build includes:

```bash
gnuradio-config-info --enabled-components
```

### Changing branches, or removing the installed GNU Radio

Do the three steps below before building a different branch or version of
GNU Radio (for example changing between `main` and `maint-3.10`), or to
remove the installed GNU Radio altogether. Keep them in this order: the
first one needs a file inside `~/gnuradio/build`.

You do not need these steps to rebuild the same branch after changing the
code. Run `gnuradio_clone_builder.py` again, and the new install is used in
place of the old one.

1. Remove the installed files, using the build directory's
   `install_manifest.txt`:

   ```bash
   cd ~/gnuradio/build && sudo xargs rm -f < install_manifest.txt && sudo ldconfig
   ```

2. Remove the empty directories that leaves behind, which make GNU Radio's
   tests fail on the next build. `gnuradio_clone_builder.py` checks for
   them and stops with this command if it finds any:

   ```bash
   sudo rm -rf /usr/local/lib/python3*/dist-packages/gnuradio \
               /usr/local/lib/python3*/dist-packages/pmt \
               /usr/local/include/gnuradio /usr/local/include/pmt \
               /usr/local/share/gnuradio /usr/local/etc/gnuradio \
               /usr/local/lib/cmake/gnuradio /usr/local/share/doc/gnuradio-*
   ```

3. Only now remove the build directory, so that the other branch is
   configured and built from scratch. Your source code and branches in
   `~/gnuradio` are not touched:

   ```bash
   cd && sudo rm -rf ~/gnuradio/build
   ```

Then check out the other branch in `~/gnuradio` and run the script again.

**Libraries left by earlier builds.** On the `main` branch, the names of
GNU Radio's library files include the version of the code they were built
from (for example `libgnuradio-runtime.so.v3.11.0.0git-1193-g0403558f`), and
that version changes with every commit. So when you rebuild after committing
a change, the new libraries are installed next to the previous ones, which
stay in `/usr/local/lib`. They do no harm, because programs use the newest
ones, but they add up. To list the ones that do not belong to the installed
version, and then remove them:

```bash
ls /usr/local/lib/libgnuradio-*.so.v* | grep -v -- "$(gnuradio-config-info --version)"
ls /usr/local/lib/libgnuradio-*.so.v* | grep -v -- "$(gnuradio-config-info --version)" | sudo xargs -r rm
sudo ldconfig
```

A `maint-3.10` build does not need this. Its library files are named after
the release only (for example `libgnuradio-runtime.so.3.10.12.0`), so each
rebuild replaces them, and the first command above just reports that it
found no such files.

### Known limitation

GNU Radio's `main` branch (the 3.11 development version) needs Qt6, PyQt6,
and Qwt built for Qt6 for its `gr-qtgui`. Ubuntu 24.04 and 26.04 have no
packaged Qwt for Qt6, and the packages Step 1 installs are those of the
Qt5-based 3.10 series. So a `main` build has no `gr-qtgui`. A `maint-3.10`
build is not affected.

A `main` build also lacks the Thrift back-end of `gr-ctrlport` (ControlPort
over Thrift), which a `maint-3.10` build has. `gr-ctrlport` itself is
built.

### Releases

**`v2.0`** (2026-10-10) is the first release, with two scripts:

- **`gnuradio_dependencies_installer.py`** installs UHD from the
  [Ettus PPA](https://launchpad.net/~ettusresearch/+archive/ubuntu/uhd) and
  GNU Radio's dependencies with `apt-get`; nothing is compiled.
- **`gnuradio_clone_builder.py`** builds, tests, and installs GNU Radio from
  a clone that is already on the machine, normally your own fork. It can be
  run again after every change.
- **The number of `make` jobs is limited by the machine's memory,** so that
  the build is not killed for running out of it.

**`v2.3`** (2026-10-14) makes `gnuradio_dependencies_installer.py` install
the Boost development packages that UHD's cmake files need. With `v2.2` and
earlier, a clean Ubuntu 24.04 machine built GNU Radio without `gr-uhd`:
`cmake.log` showed `Boost_FOUND = FALSE` and "Disabling gr-uhd support",
and the build went on without an error. (On Ubuntu 26.04 the missing
packages happened to come in as dependencies of others.) If you used an
earlier release, install them, remove the build directory so that cmake
starts afresh, and run the builder again:

```bash
sudo apt-get install libboost-chrono-dev libboost-filesystem-dev libboost-serialization-dev
rm -rf ~/gnuradio/build
```

`gnuradio_clone_builder.py` is unchanged from `v2.1`.

**`v2.2`** (2026-10-12) makes `gnuradio_dependencies_installer.py` install
SoapySDR's device modules. With `v2.0` and `v2.1`, a machine set up by
Step 1 had `gr-soapy` but no drivers for it: `SoapySDRUtil --info` printed
"No modules found!" and `SoapySDRUtil --find` found no devices. If you
used `v2.0` or `v2.1`, you do not need to rebuild GNU Radio: either run the
`v2.2` Step 1 script again, or install the module for your device, for
example `sudo apt-get install soapysdr0.8-module-rtlsdr`.
`gnuradio_clone_builder.py` is unchanged from `v2.1`.

**`v2.1`** (2026-10-12) fixes `gnuradio_clone_builder.py` for repeated
builds of `main`. With `v2.0`, the first `make test` in a clone passed, and
every later one failed in `grc_tests`: GNU Radio's
GRC tests generate Python files in `grc/tests/resources` in the source tree,
the next test run picks two of them up as tests, and they need `gr-qtgui`,
which a `main` build does not have. The script now removes those generated
files before each `make test`. If you are using `v2.0`, run
`git -C ~/gnuradio clean -fdX grc/tests/resources` before the script, or
download `v2.1`. `gnuradio_dependencies_installer.py` is unchanged.

Further fixes will be tagged `v2.4` and so on; a tag is never moved, so a
link to a tag always gives the same scripts.
