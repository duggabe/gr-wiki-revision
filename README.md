# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

The main content is two Python scripts that build
[GNU Radio](https://github.com/gnuradio/gnuradio) from source on Ubuntu,
without Docker. They back the "Building GNU Radio from Source Code" page on
the GNU Radio Wiki, and this README follows that page. The current release
is `v2.3`; see [Releases](#releases).

The goals of these instructions are to:

- Use the Ettus PPA repository for UHD rather than building UHD from source.
- Use the `~/gnuradio` folder already cloned in the user's system so that
  developers/testers can build from their own fork.

They are useful when a Developer of GNU Radio code needs to test additions or
revisions to the code, and needs to operate outside of a Docker container.
All others should follow the instructions in
[LinuxInstall#From_Binaries](https://wiki.gnuradio.org/index.php?title=LinuxInstall#From_Binaries).

**Note: Running and developing OOT (out-of-tree) modules does _not_ require
GNU Radio to be installed from source.**

---

There are two steps, each with its own script. Step 1 installs UHD from the
Ettus Research PPA and everything GNU Radio needs, using `apt-get`; nothing is
compiled. Step 2 builds, tests, and installs GNU Radio from your own fork,
which you clone into your home directory, so that you can work on an issue
and submit a pull request.

## Downloading the scripts

The scripts are maintained in this repository. You do not need to clone the
repository; just download the two scripts. Each one works on its own.

Download them with Python, which every Ubuntu system has:

```bash
mkdir -p ~/gr-installers && cd ~/gr-installers &&
python3 -c "import urllib.request; urllib.request.urlretrieve('https://github.com/duggabe/gr-wiki-revision/releases/latest/download/gnuradio_dependencies_installer.py', 'gnuradio_dependencies_installer.py')" &&
python3 -c "import urllib.request; urllib.request.urlretrieve('https://github.com/duggabe/gr-wiki-revision/releases/latest/download/gnuradio_clone_builder.py', 'gnuradio_clone_builder.py')"
```

These links always give the latest release; the
[Releases page](https://github.com/duggabe/gr-wiki-revision/releases) lists
what changed in each one. Look the scripts over before running them. Don't
pipe a download straight into `python3`, especially with `sudo`. Both scripts
have `--help` and `--dry-run`.

## Before you start

The scripts need a system without another GNU Radio or a source-built UHD on
it. The scripts check for both and stop with the commands to run if they
find either.

- If Ubuntu's own GNU Radio packages are installed, remove them:

  ```bash
  sudo apt-get remove gnuradio gnuradio-dev
  ```

- If you built UHD from source earlier, remove it. GNU Radio's `cmake` looks
  in `/usr/local` before `/usr`, so it would otherwise keep using that copy
  instead of the PPA's:

  ```bash
  cd ~/uhd/host/build && sudo xargs rm -f < install_manifest.txt
  sudo rm -rf /usr/local/include/uhd /usr/local/lib/uhd /usr/local/lib/cmake/uhd /usr/local/share/uhd
  sudo ldconfig
  ```

- If you built and installed GNU Radio from source earlier, remove it with
  steps 1 and 2 of
  [Changing branches, or removing the installed GNU Radio](#changing-branches-or-removing-the-installed-gnu-radio).

## Step 1: Installing UHD and the dependencies

To see what the script will do without changing anything:

```bash
cd ~/gr-installers
python3 gnuradio_dependencies_installer.py --dry-run
```

Then run it:

```bash
sudo python3 gnuradio_dependencies_installer.py
```

The script:

- enables "Source code" in Ubuntu's software sources (the same change as the
  "Source code" box in the "Software & Updates" app), which
  `apt-get build-dep` needs. The original file is saved as
  `/etc/apt/sources.list.d/ubuntu.sources.bak`.
- adds the Ettus Research PPA (`ppa:ettusresearch/uhd`) and installs UHD from
  it (`uhd-host` and `libuhd-dev`).
- installs the Boost development packages that UHD needs. The PPA's
  `libuhd-dev` doesn't bring them, and without them GNU Radio is built
  without `gr-uhd`, with no error.
- installs the build dependencies of Ubuntu's own `gnuradio` package for your
  release (`apt-get build-dep gnuradio`), `git`, and a few packages that are
  needed at run time.
- installs SoapySDR's device modules, the drivers `gr-soapy` uses for an
  RTL-SDR, HackRF, Airspy, bladeRF, LimeSDR, PlutoSDR, and others. It
  installs every module Ubuntu packages for your release except the one for
  UHD; a USRP is used through `gr-uhd`. The `--dry-run` output lists them.
- downloads the USRP FPGA images (`uhd_images_downloader`). This is a large
  download; add `--no-images` to skip it.

The `uhd-host` package installs the udev rules for USRP devices, so there is
nothing to copy by hand. If a USRP was plugged in during the installation,
unplug it and plug it in again.

The script's options:

| Option | Description |
| --- | --- |
| `--dry-run` | Run the checks and print what would be done, without changing anything or requiring root. |
| `-y`, `--yes` | Do not prompt for confirmation before installing. |
| `--no-images` | Do not run `uhd_images_downloader` (the USRP FPGA images, a large download). |
| `--sources-path PATH` | Ubuntu's apt sources file, in which to enable source code (default: `/etc/apt/sources.list.d/ubuntu.sources`). |
| `--os-release-path PATH` | Path to read the OS name and version from (default: `/etc/os-release`). |

## Step 2: Building GNU Radio from your fork

### Getting the source code

Fork <https://github.com/gnuradio/gnuradio> on GitHub, then clone your fork
into your home directory and add the GNU Radio repository as a second
remote, so that you can keep up to date with it:

```bash
cd ~
git clone https://github.com/<your-username>/gnuradio.git
cd gnuradio
git remote add upstream https://github.com/gnuradio/gnuradio.git
```

### Starting a branch

Make a new branch for each issue, starting from the current `main` of the
GNU Radio repository. The branch name is your choice; `issue8218` is an
example:

```bash
cd ~/gnuradio
git fetch upstream
git checkout -b issue8218 upstream/main
```

### Building, testing, and installing

The second script builds whatever is checked out in `~/gnuradio`. It does
not clone anything and does not change branches:

```bash
cd ~/gr-installers
sudo python3 gnuradio_clone_builder.py
```

It runs the equivalent of:

```bash
cd ~/gnuradio
mkdir build && cd build        # first time only
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../ 2>&1 | tee cmake.log
make -j7 2>&1 | tee make.log   # the number of jobs depends on memory; see below
git -C ~/gnuradio clean -fdX grc/tests/resources   # see below
make test 2>&1 | tee make_test.log
sudo make install
sudo ldconfig
```

- The output of `cmake`, `make`, and `make test` is shown as it runs and
  also saved to `cmake.log`, `make.log`, and `make_test.log` in
  `~/gnuradio/build`. If any step fails, including a failing test, the
  script stops before installing; the logs show what went wrong.
- The script works with or without `sudo`. Either way, the build runs as
  you, so `~/gnuradio/build` belongs to you.
- Before `make test`, the script removes the files that GNU Radio's GRC tests
  generated in `~/gnuradio/grc/tests/resources` during an earlier test run.
  Without this, on a build that has no `gr-qtgui`, the second and every later
  `make test` fails in `grc_tests`. Only those generated files, which git
  ignores, are removed; your source code is not touched. (Version v2.0 of
  the script did not do this.)
- To build and test without installing, add `--no-install`.
- Compiling GNU Radio needs a lot of memory. With too many `make` jobs for
  the memory in the machine, the compiler is killed part-way through the
  build. The script therefore uses one job less than the number of processor
  cores, but no more than one for each 2 GB of memory (7 jobs on a 16-core
  machine with 16 GB). To choose the number yourself, add `--jobs`, for
  example `--jobs 4`.
- To leave out components you don't need, which shortens the build, pass
  options to `cmake` with `--cmake-args`, for example
  `--cmake-args="-DENABLE_GR_FEC=OFF -DENABLE_GR_VOCODER=OFF"`. `cmake`
  remembers them in `~/gnuradio/build` until you change them or remove that
  directory.
- If your clone is not in `~/gnuradio`, add `--source-dir` with its location.

The script's options:

| Option | Description |
| --- | --- |
| `--source-dir DIR` | The GNU Radio clone to build. Default: `gnuradio` in the home directory of the invoking user (`$SUDO_USER` when run via `sudo`). |
| `--jobs N` | Number of parallel `make` jobs. Default: one less than the number of processor cores, but no more than one per 2 GB of memory. |
| `--cmake-args "ARGS"` | Extra options for `cmake`, in one quoted string written with `=`, e.g. `--cmake-args="-DENABLE_GR_FEC=OFF -DENABLE_GR_VOCODER=OFF"`. `cmake` remembers them in the build directory until they are changed or the directory is removed. |
| `--no-install` | Stop after the tests: do not run `sudo make install` and `sudo ldconfig`. |
| `--dry-run` | Run the checks and print the build steps, without running them. |
| `-y`, `--yes` | Do not prompt for confirmation before building. |

The `main` branch is moving from Qt5 to Qt6. Its QT GUI blocks (`gr-qtgui`)
need Qt6 and a Qt6 build of Qwt, which Ubuntu 24.04 and 26.04 do not
package, so a `main` build made this way does not include `gr-qtgui`. It
also lacks the Thrift back-end of `gr-ctrlport` (ControlPort over Thrift),
although `gr-ctrlport` itself is built. The list of components that were
not built is near the end of `cmake.log`.

To build the 3.10 release series instead, switch to the `maint-3.10` branch
before running the script. A `maint-3.10` build made this way has every
component enabled, including `gr-qtgui`. A plain clone of the GNU Radio
repository is enough if you only want to build and test and do not plan to
submit a change:

```bash
cd
git clone https://github.com/gnuradio/gnuradio.git
cd gnuradio
git checkout maint-3.10
```

In a clone of your own fork, `git checkout maint-3.10` may fail at first:
GitHub copies only the `main` branch into a fork unless you ask for all
branches when creating it. The branch then has to come from the `upstream`
remote. After `git fetch upstream`, a plain `git checkout maint-3.10` works
and is enough for building and testing. To make a change, start your own
branch from `upstream/maint-3.10` rather than `upstream/main`:

```bash
cd ~/gnuradio
git fetch upstream
git checkout -b my-3.10-work upstream/maint-3.10     # example branch name
```

### Making and submitting a change

After editing the code, run the script again. It reuses `~/gnuradio/build`,
so only what changed is rebuilt:

```bash
cd ~/gr-installers
sudo python3 gnuradio_clone_builder.py
```

When the change works, commit it and push the branch to your fork. GNU Radio
requires every commit to be signed off (`-s`), and the first line of the
commit message to start with the name of the module that was changed:

```bash
cd ~/gnuradio
git add <changed files>
git commit -s -m "gr-filter: describe what the change does"   # use the name of the module: 'gr-filter' is an example
git push -u origin issue8218
```

Then open a pull request from your branch on GitHub. See
[CONTRIBUTING.md](https://github.com/gnuradio/gnuradio/blob/main/CONTRIBUTING.md)
in the GNU Radio repository for the coding and pull request guidelines.

### Changing branches, or removing the installed GNU Radio

Do the three steps below before building a different branch or version of
GNU Radio (for example changing between `main` and `maint-3.10`), or to
remove the installed GNU Radio altogether. Keep them in this order: the
first step needs a file inside `~/gnuradio/build`.

You do not need these steps to rebuild the same branch after changing the
code. Run `gnuradio_clone_builder.py` again, and the new install is used in
place of the old one.

1. Remove the installed files. The build directory has an
   `install_manifest.txt` listing the files that were installed:

   ```bash
   cd ~/gnuradio/build && sudo xargs rm -f < install_manifest.txt && sudo ldconfig
   ```

2. That removes the files but leaves empty directories behind, which make
   GNU Radio's tests fail on the next build. Remove them too:

   ```bash
   sudo rm -rf /usr/local/lib/python3*/dist-packages/gnuradio \
               /usr/local/lib/python3*/dist-packages/pmt \
               /usr/local/include/gnuradio /usr/local/include/pmt \
               /usr/local/share/gnuradio /usr/local/etc/gnuradio \
               /usr/local/lib/cmake/gnuradio /usr/local/share/doc/gnuradio-*
   ```

   The script checks for these leftover directories before it builds, and
   stops with the exact command to run if it finds any.

3. Only now remove the build directory, so that the other branch is
   configured and built from scratch. Your source code and your branches in
   `~/gnuradio` are not touched:

   ```bash
   cd && sudo rm -rf ~/gnuradio/build
   ```

Then check out the other branch in `~/gnuradio` and run the script again.

**Libraries left by earlier builds.** On the `main` branch, the names of GNU
Radio's library files include the version of the code they were built from
(for example `libgnuradio-runtime.so.v3.11.0.0git-1193-g0403558f`), and that
version changes with every commit. So when you rebuild after committing a
change, the new libraries are installed next to the previous ones, which
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

## Checking the result

```bash
uhd_config_info --version
gnuradio-config-info --version
gnuradio-config-info --enabled-components
```

The list of components should include `gr-uhd`, `gr-iio`, `gr-soapy`, and
`gnuradio-companion`.

If you have a USRP, plug it in and check it with UHD and then through GNU
Radio. No `sudo` is needed:

```bash
uhd_find_devices
uhd_usrp_probe
uhd_rx_cfile -f 100e6 -r 1e6 -N 1000000 /tmp/test.cfile
ls -l /tmp/test.cfile
```

`uhd_find_devices` should list the device, and `uhd_usrp_probe` should load
its FPGA image and print its properties. `uhd_rx_cfile` receives one million
samples through GNU Radio's `gr-uhd` and should leave a file of 8,000,000
bytes without reporting errors.

If you have an SDR that GNU Radio uses through SoapySDR, such as an RTL-SDR,
plug it in and check that SoapySDR sees it:

```bash
SoapySDRUtil --info
SoapySDRUtil --find
SoapySDRUtil --probe="driver=rtlsdr"     # use the driver name that --find printed
```

`SoapySDRUtil --info` should list your device's driver under "Available
factories", and `SoapySDRUtil --find` should list the device. Before the
device, `--find` may print lines starting with `ALSA lib` or
`RtApi::getDeviceInfo`. They come from SoapySDR's audio module looking at
the computer's sound devices and can be ignored. If `--info` prints "No
modules found!", the device modules are missing: that happened with versions
**v2.0** and **v2.1** of the Step 1 script. Run the current Step 1 script
again, or install the module for your device, for example
`sudo apt-get install soapysdr0.8-module-rtlsdr`. GNU Radio does not need to
be rebuilt.

## Releases

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
every later one failed in `grc_tests`: GNU Radio's GRC tests generate Python
files in `grc/tests/resources` in the source tree, the next test run picks
two of them up as tests, and they need `gr-qtgui`, which a `main` build does
not have. The script now removes those generated files before each
`make test`. If you are using `v2.0`, run
`git -C ~/gnuradio clean -fdX grc/tests/resources` before the script, or
download `v2.1`. `gnuradio_dependencies_installer.py` is unchanged.

Further fixes will be tagged `v2.4` and so on; a tag is never moved, so a
link to a tag always gives the same scripts.
