# gr-wiki-revision — GNU Radio build scripts for the GNU Radio Wiki

Trimmed 2026-10-14 (user: "trim CLAUDE.md"). The full earlier record,
including the Phase 1 history day by day, is in git history: `CLAUDE.md` at
commit `03ae87f`.

## Project summary

https://github.com/duggabe/gr-wiki-revision (public) holds the scripts
behind the GNU Radio Wiki page **"Building GNU Radio from Source Code"**,
which the user (Barry, GitHub `duggabe`) writes. The scripts are for GNU
Radio developers on Ubuntu (24.04 and 26.04), outside Docker:

- **Step 1, `gnuradio_dependencies_installer.py`:** UHD from the Ettus PPA
  plus everything GNU Radio needs, with `apt-get` only.
- **Step 2, `gnuradio_clone_builder.py`:** builds, tests, and installs
  whatever is checked out in `~/gnuradio` (normally the user's fork).

Current release: **`v2.3`** (GitHub "Latest"). Favour clarity,
reproducibility, and reader choice: the scripts back wiki instructions that
other people run, often with `sudo`.

**Working names:** "Phase 1" = the `v1.x` line (UHD and GNU Radio built from
source; removed from `main` 2026-10-14, still at tags `v1.0`–`v1.3`, whose
raw links work). "Phase 2" = the `v2.x` line, the only one now. The README,
the wiki page, and the Release notes never mention phases ("as if there had
not been a Phase 1", user, 2026-10-13).

## Working conventions

- **Commits:** directly to `main`, only when the user says "commit this";
  push only on "push it" (`timeout 90 git push`). Report the short hash,
  title, and whether it is pushed. End messages with
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Recording:** when the user reports a fact or result, record it here
  (left uncommitted until asked). Label my own assumptions as mine.
- **Test results live only in this file** (user, 2026-10-14: "cut all test
  results on both the wiki page and the README.md, leaving them only in
  CLAUDE.md"). Record them in full under "Test results" below. The GitHub
  Release notes keep their "Tested" sections (user: "OK").
- **Tags** are never moved; fixes get a new tag (next: `v2.4`).
- **GitHub Releases** are created or edited only on the user's request.
  Every Release must have **both scripts attached**, because the docs
  download from
  `https://github.com/duggabe/gr-wiki-revision/releases/latest/download/<file>`.
- **The wiki draft leads; the README follows.** `wiki-draft-download-section.txt`
  (MediaWiki, gitignored, local only) is the user's text. The user edits in
  MediaWiki; I convert to Markdown for the README. The README is the draft
  section by section, plus README-only parts: a short repo intro, the two
  options tables (keep in sync with the scripts' argparse help), and the
  "Releases" section.
- **The user drafts on https://wiki.gnuradio.org/index.php?title=User_talk:Duggabe**
  and updates the Talk page and the live page by **total replacement** with
  the whole draft. So keep the draft complete and current.
- The wiki is behind Cloudflare and can't be fetched from here: ask the user
  to paste content.

## Current state (2026-10-14)

- `main` pushed at `03ae87f` before this trim; working tree clean apart
  from this file.
- Live wiki page = User_talk:Duggabe = local draft = README (since `1f680ae`).
  None of them has test results.
- GitHub Releases: `v2.3` (Latest), `v2.2`, `v2.1`, `v2.0`, all with both
  scripts attached. The `v1.2` Release was deleted 2026-10-13 (tags kept);
  its notes are backed up in `~/v1.2-release-notes-backup.json` (the user
  may delete it).
- Tracked files: the two scripts, `README.md`, `LICENSE` (CC BY-SA 4.0, by
  choice although CC advises against it for software), `.gitignore`,
  `CLAUDE.md`.

## Machines

| Machine | Ubuntu | State |
| --- | --- | --- |
| LENOVO desktop (working machine, `~/gr-wiki-revision`) | 26.04 | 16 cores, 15 GiB RAM, 4 GB swap. Reloaded 2026-10-08. UHD 4.11 from the PPA (only UHD; `libuhd4.9.0` removed 2026-10-12). `~/gnuradio` = plain clone of `gnuradio/gnuradio` on `maint-3.10`, GNU Radio 3.10.12.0 in `/usr/local`, 42 components. 13 SoapySDR modules (`v2.2` Step 1 run for real). `v2.3`'s Boost step not run here (would add 4 small metapackages). Hardware: USRP B200mini, RTL-SDR, PlutoSDR. |
| GMKtec (clean-install test machine) | reloaded per test | 4 cores, 10 GiB. Last: clean 24.04 on 2026-10-14, where `gr-uhd` was missing (the Boost problem). Whether the user applied the workaround or `v2.3` there is not recorded. |
| Laptop | 24.04 | Not clean (Phase 1 had installed `libboost-all-dev`). Original `~/AIwork` trial. |
| The other tester's machine | 24.04 | Clean install for the `v2.3` test. Fork `jesternofool/gnuradio` (only `main`). |

## The scripts

### `gnuradio_dependencies_installer.py` (Step 1)

Self-contained, `apt-get` only. Checks the host is Ubuntu; aborts if
Ubuntu's `gnuradio` / `gnuradio-dev` are installed or a source-built UHD is
under `/usr/local` (prints the fix commands). Then:

1. enable "Source code": `Types: deb` → `Types: deb deb-src` in
   `/etc/apt/sources.list.d/ubuntu.sources` (backup `.bak`)
2. `apt-get update`; `apt-get install -y software-properties-common git`
3. `add-apt-repository -y ppa:ettusresearch/uhd`
4. `apt-get install -y --no-install-recommends uhd-host libuhd-dev`
5. (`v2.3`) `apt-get install -y` `BOOST_PACKAGES`: `libboost-dev` and the
   chrono, date-time, exception, filesystem, program-options, regex,
   serialization, test, thread `-dev` packages
6. `apt-get build-dep -y gnuradio`
7. `apt-get install -y python3-qtpy python3-pyqtgraph python3-matplotlib soapysdr-tools`
8. (`v2.2`) `apt-get install -y` the SoapySDR device modules, worked out at
   run time by `soapy_module_packages()`: the Depends of
   `soapysdr-module-all` (followed through `soapysdr0.8-module-all`) minus
   `SOAPY_SKIP_MODULES` (`uhd`). 13 on 26.04, 11 expected on 24.04. Warns
   and goes on if apt doesn't know the metapackage.
9. `uhd_images_downloader` (skipped with `--no-images`)

Options: `--dry-run`, `-y`, `--no-images`, `--sources-path`, `--os-release-path`.

### `gnuradio_clone_builder.py` (Step 2)

Self-contained (carries trimmed copies of the old `BuildStep` /
`run_build_steps()` / `run_logged()` / `get_build_user()` helpers and
`INSTALL_DIR_PATTERNS`). Builds `~/gnuradio` (`--source-dir`); never clones
or changes branches; reuses `build/`. Steps: `mkdir build` (first time) or
`sudo chown -R` the build dir back to the user → cmake → make → (`v2.1`)
`git clean -fdX grc/tests/resources` in the source dir (only if `.git` and
that directory exist) → make test, each tee'd to `cmake.log` / `make.log` /
`make_test.log` → `sudo make install` → `sudo ldconfig`. `make` jobs =
`min(nproc - 1, MemTotal // 2 GB)`, at least 1. Aborts if the directory
isn't GNU Radio source, `libuhd-dev` isn't installed, Ubuntu's `gnuradio`
packages are installed, or stale install dirs exist. Options:
`--source-dir`, `--jobs`, `--cmake-args="..."`, `--no-install`,
`--dry-run`, `-y`.

INSTALL_DIR_PATTERNS, the "Changing branches..." step-2 `rm -rf` command in
the wiki draft, and the same command in the README must stay in sync.

## Releases

| Tag | Date | What |
| --- | --- | --- |
| `v2.0` | 2026-10-10 | First release: the two scripts. Commit `1f8711c`. |
| `v2.1` | 2026-10-12 | Builder: `git clean -fdX grc/tests/resources` before `make test`. Commit `22e2ca3`. |
| `v2.2` | 2026-10-12 | Step 1: SoapySDR device modules. Commit `7208a18`. |
| `v2.3` | 2026-10-14 | Step 1: Boost dev packages for UHD's cmake files. Commit `ffac9f9`; Release title "v2.3: Boost packages for gr-uhd". |
| `v1.0`–`v1.3` | 2026-09-26 – 10-10 | Phase 1, tags only. |

## Key decisions and why

- **UHD from the Ettus PPA** (the main GNU Radio developer's proposal),
  installed with **`--no-install-recommends`**: `libuhd-dev` recommends
  `gnuradio-dev` and `python3-uhd` recommends `gnuradio`, which put Ubuntu's
  GNU Radio 3.10.12 in `/usr` next to the source build (happened on the
  LENOVO 2026-10-08). Both scripts refuse to run while those are installed.
- **GNU Radio's dependencies from `apt-get build-dep gnuradio`**, not a
  hardcoded list: tracks each Ubuntu release. It fits `maint-3.10` (Qt5).
- **Boost packages by name (`v2.3`):** the PPA's `libuhd-dev` (4.11.0.0)
  declares no Boost dependencies (Depends: only `libuhd4.11.0`), while
  Ubuntu's own `libuhd-dev` 4.9 depends on 11 Boost dev packages. UHD's
  `UHDConfig.cmake` does `find_dependency(Boost ... COMPONENTS chrono
  date_time filesystem program_options serialization thread
  unit_test_framework)`. `build-dep gnuradio` lacks chrono, filesystem,
  serialization on both releases. On 26.04 (Boost 1.90) they mostly come in
  as dependencies of others; on a clean 24.04 (Boost 1.83) they don't, and
  GNU Radio's cmake prints `Boost_FOUND = FALSE` / "Disabling gr-uhd
  support" and builds on without `gr-uhd`. Chosen over `libboost-all-dev`
  (much bigger). All ten exist on both releases (six in universe on 24.04).
- **SoapySDR modules, all but UHD (`v2.2`):** they are only Recommends of
  `libsoapysdr0.8`, which `build-dep` doesn't install, so `gr-soapy` had no
  drivers. The UHD module pulls Ubuntu's older `libuhd4.9.0` next to the
  PPA's. The `audio` module makes `SoapySDRUtil --find` print harmless
  `ALSA lib` / `RtApi::getDeviceInfo` lines; decided (2026-10-13) to keep it
  and explain them in the docs.
- **The builder removes GRC's generated test files before `make test`
  (`v2.1`):** GNU Radio's GRC tests write `test_*.py` files into
  `grc/tests/resources` (gitignored); the next pytest run collects them, and
  they import `gnuradio.qtgui`, which a `main` build lacks, so every
  `make test` after the first failed on `main`. Reported upstream by the
  user (2026-10-14; no issue number given). Drop the step when upstream
  fixes it.
- **Memory-aware `make` jobs:** an OOM kill at `make -j15` on the LENOVO's
  15 GiB. 2 GB per job is my estimate, not measured.
- **Build as the normal user even under `sudo`:** steps not starting with
  `sudo` run as `$SUDO_USER`. `sudo make install` still leaves some
  root-owned files in `build/` (~150), which the builder chowns back.
- **Any failing step stops the build, including a failing test,** so a
  failing build is never installed.
- **Install prefix `/usr/local`:** `ldconfig` already covers
  `/usr/local/lib`; GNU Radio's Python imports with no env vars;
  `python3-uhd` makes `import uhd` work.
- **Removing an install takes three steps** (wiki/README "Changing
  branches..."): manifest removal, then `rm -rf` the empty leftover
  directories (they break `grc_tests`, seen 2026-10-03), then
  `rm -rf ~/gnuradio/build`.
- **Downloads by Python from the latest Release** (2026-10-14): "the
  developers do not like to use wget"; the user chose the Python one-liner,
  then chained the commands with `&&`.

## Useful facts

- `uhd-host` installs the udev rules (`/usr/lib/udev/rules.d/60-uhd-host.rules`);
  no copy in `/etc/udev/rules.d` is needed (checked 2026-10-12). FPGA images
  go to `/usr/share/uhd/4.11.0/images` (`uhd_config_info --images-dir`).
- A GitHub fork copies only `main` unless told otherwise. After
  `git fetch upstream`, a plain `git checkout maint-3.10` creates the branch
  from `upstream/maint-3.10`.
- On `main`, library names carry the commit (`.so.v3.11.0.0git-1193-g...`),
  so each rebuild after a commit leaves the old ones in `/usr/local/lib`.
  The docs' listing command removes those files but can leave the
  `.so.3.11.0git` links dangling (seen on the LENOVO 2026-10-12). On
  `maint-3.10` the names are `.so.3.10.12` / `.so.3.10.12.0`, so nothing
  piles up.
- `main` (3.11, Qt6) builds without `gr-qtgui` (needs Qwt for Qt6:
  `libqwt-qt6-dev` exists only from Ubuntu 26.10) and without Thrift
  (`gr-ctrlport` itself builds; cause not looked into); 40 components vs 42
  on `maint-3.10`. GNU Radio's CI Dockerfiles are in
  `gnuradio/gnuradio-docker` under `ci/` (`ci-ubuntu-26.10-3.11` lists its
  Qt6 packages explicitly).
- On a `main` build that has the cmake cache of the LENOVO's 2026-10-08
  manual build, `ENABLE_GR_FEC` / `VOCODER` / `CTRLPORT` stayed `OFF` until
  `build/` was removed: `cmake` options persist in the cache.

## Test results

Kept here only. Test counts differ by release and branch: `main` 271 on
26.04 (267 on 24.04); `maint-3.10` 269 on 26.04, 268 on 24.04 (the
differences are unexplained).

### `v2.x` (UHD from the PPA)

| Date | Machine, Ubuntu | Scripts | Branch / build | Result |
| --- | --- | --- | --- | --- |
| 2026-10-10 | GMKtec, clean 26.04 | `main` at `1f8711c` (= `v2.0`) | `main`, v3.11.0.0git-1193-g0403558f | 271/271; UHD 4.11.0.0-0ubuntu1~resolute3 |
| 2026-10-10 | Laptop, 24.04 (not clean) | `v2.0` | plain clone, `maint-3.10`, 3.10.12.0 | 268/268, 42 components incl. `gr-qtgui`; UHD ~noble3 |
| 2026-10-11 | Other tester, clean 24.04 | `v2.0` | `main` | 267/267; versions and components not reported |
| 2026-10-11 | LENOVO, 26.04 | `v2.0` builder | fork, `issue8218` (`main` + 1), rebuild in place, FEC/VOCODER/CTRLPORT off from old cache | 247/247, v3.11.0.0git-1194-gb0937160; first real chown of root-owned build files; left 18 old versioned libraries |
| 2026-10-12 | GMKtec, clean 26.04 (reloaded) | `v2.0` | `main`, -1193 | 271/271 |
| 2026-10-12 | same | `v2.0` | "Changing branches..." steps, then `maint-3.10` | 269/269, 3.10.12.0, 42 components; `dpkg -l 'libuhd*'`: only 4.11 (no `libuhd4.9.0`); no 3.11 libraries left |
| 2026-10-12 | same | `v2.0` | back to `main` | **270/271, `grc_tests` failed** (generated files; fixed in `v2.1`) |
| 2026-10-12 | same | `v2.1` builder | same clone, `main` | 271/271; 40 components (no `gr-qtgui`, no thrift; `doxygen` is `doxygen-documentation` on `main`) |
| 2026-10-12 | LENOVO, 26.04 | `v2.0`/`v2.1` | plain clone, `maint-3.10`, full from-scratch build at `-j7` | 269/269, 3.10.12.0 (v3.10.12.0-92-gc1a73dc34), 42 components; no OOM kill |
| 2026-10-12 | Other tester, 24.04 (clean?) | `v2.1` | fork with only `main`; `git fetch upstream`, `git checkout maint-3.10` | 268/268, 3.10.12.0, UHD ~noble3, 42 components (his first paste showed 40 with the mistaken count 267; the revised paste had all 42) |
| 2026-10-13 | LENOVO, 26.04 (not clean) | `v2.2` Step 1, real run | — | SoapySDR step installed the 4 missing modules; `SoapySDRUtil --info`: 13 modules (airspy, airspyhf, audio, bladerf, hackrf, hydrasdr, lime, miri, osmosdr, plutosdr, redpitaya, remote, rtlsdr); still one UHD |
| 2026-10-14 | GMKtec, clean 24.04 | `v2.2` (presumably; not confirmed) | `maint-3.10` | **`gr-uhd` disabled**: `Boost_FOUND = FALSE` under "Configuring gr-uhd support", call stack through `UHDConfig.cmake:31`; cmake 3.28. Led to `v2.3`. |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3` | `maint-3.10` | 268/268, 3.10.12.0, UHD 4.11.0.0-0ubuntu1~noble3, 42 components incl. `gr-uhd` + RFNoC: **Boost fix confirmed** |

Phase 1 (`v1.x`, for the record): UHD 4.11.0.0 source builds 109/109 tests
(LENOVO 26.04, GMKtec clean 26.04.1 and clean 24.04). GNU Radio `main`
v3.11.0.0git-1174 266/266 (LENOVO, GMKtec clean 26.04.1; 32 components, no
`gr-qtgui`/`gr-soapy`/`gr-iio`/JACK/PortAudio). `maint-3.10` with the
`build-dep` list: 269/269 on the LENOVO, 268/268 on a clean 24.04 GMKtec,
42 components each. `v1.0` wiki page tested from scratch on a clean 24.04
GMKtec, 2026-09-26. `v1.3` never built for real.

### Hardware

| Date | Who, Ubuntu | Scripts / branch | Device | Path | Result |
| --- | --- | --- | --- | --- | --- |
| 2026-10-12 | User, LENOVO 26.04 | `v2.0`, fork `main` -1194 | USRP B200mini (serial 315C7B7) | UHD tools, `gr-uhd` | `uhd_find_devices` found it (firmware from the PPA's images); `uhd_usrp_probe`: FPGA loaded, USB 3, loopback passed, 16 MHz; `uhd_rx_cfile -f 100e6 -r 1e6 -N 1000000` wrote 8,000,000 bytes, no overflows. Normal user, no sudo. Still found after removing the extra udev rules copy. |
| 2026-10-12 | User, LENOVO 26.04 | `maint-3.10` | RTL-SDR (RTL2838, R820T) | SoapySDR | `SoapySDRUtil --find` sees it; no flowgraph reported |
| 2026-10-12/13 | Other tester, 24.04 | `v2.1`, `maint-3.10` | RTL-SDR (0bda:2838, R820T) | `gr-soapy` | "No modules found!" until `soapysdr0.8-module-rtlsdr` was installed (led to `v2.2`); then `--find` / `--probe` worked as a normal user (the library detaches the DVB driver itself), and a flowgraph ran |
| 2026-10-13 | Other tester, 24.04 | `v2.1`, `maint-3.10` | USRP B200mini | `gr-uhd` | a flowgraph ran (transmit not known) |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | RTL-SDR, HackRF, LimeSDR, Airspy R2 | `gr-soapy` | all work; the Airspy R2 through the Soapy Custom Source block (only it), the others presumably through their own blocks (my reading) |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | USRP B200mini | `gr-uhd` | works |

Transmit has not been reported for any device.

## Open items

- **`v2.3` on 26.04:** the Boost step has only had a dry run there
  (`apt-get install -s` on the LENOVO: 4 metapackages). A real Step 1 run on
  the LENOVO, or a clean 26.04 install.
- **Transmit** with the B200mini (suggested: `uhd_siggen -f 915e6 -s 1e6
  --sine -x 100e3 -g 0 -m 0.1`, into a dummy load or attenuator); ask
  whether the other tester transmitted.
- **PlutoSDR / `gr-iio`:** untested.
- **RTL-SDR flowgraph on the LENOVO:** not run.
- **A second `make test` on `maint-3.10`** in the same build, to confirm
  repeated test runs pass there (the `grc_tests` problem was seen on `main`).
- **Unexplained test-count differences** (267 vs 271, 268 vs 269).
- **Upstream `grc_tests` fix:** when it lands, remove the builder's
  `git clean` step and its doc bullet in a new tag.
- **Docs:** the leftover-library command can leave dangling
  `.so.3.11.0git` links; the cause of the missing Thrift on `main`.
- **Longer term:** Qwt for Qt6, for `gr-qtgui` on `main`.
- **`~/v1.2-release-notes-backup.json`:** the user may delete it.
