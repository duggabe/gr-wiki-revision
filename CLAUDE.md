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

Current release: **`v2.4`** (GitHub "Latest"). Favour clarity,
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
- **Tags** are never moved; fixes get a new tag (next: `v2.5`).
- **GitHub Releases** are created or edited only on the user's request.
  Every Release must have **both scripts attached**, because the docs
  download from
  `https://github.com/duggabe/gr-wiki-revision/releases/latest/download/<file>`.
- **The wiki draft leads; the README follows.** `wiki-draft-download-section.txt`
  (MediaWiki, gitignored, local only) is the user's text. The user edits in
  MediaWiki; I convert to Markdown for the README. The README is the draft
  section by section, plus README-only parts: a short repo intro, the two
  options tables (keep in sync with the scripts' argparse help), and the
  "Releases" section. The options tables' "Option" header is padded with 40
  `&nbsp;` so GitHub doesn't wrap the options (`239bd31`; checked with
  GitHub's renderer, and the user confirmed it looks good, 2026-10-15).
  Keep the padding if the tables change.
- **The user drafts on https://wiki.gnuradio.org/index.php?title=User_talk:Duggabe**
  and updates the Talk page and the live page by **total replacement** with
  the whole draft. So keep the draft complete and current.
- The wiki is behind Cloudflare and can't be fetched from here: ask the user
  to paste content.

## Current state (2026-10-15)

- `main` pushed; `v2.4` released.
- **On hold** (user, 2026-10-16): "I'm going to wait for the developers
  decisions before I do anything else" (where the scripts live, Fedora
  support, the `qa_fastnoise` backport).
- Live wiki page = User_talk:Duggabe = local draft = README, including
  `v2.4`'s `python3-pytest` line (user replaced both wiki pages,
  2026-10-15). None of them has test results.
- GitHub Releases: `v2.4` (Latest), `v2.3`, `v2.2`, `v2.1`, `v2.0`, all with both
  scripts attached. The `v1.2` Release was deleted 2026-10-13 (tags kept);
  the backup of its notes was deleted by the user 2026-10-15.
- Tracked files: the two scripts, `README.md`, `LICENSE` (CC BY-SA 4.0, by
  choice although CC advises against it for software), `.gitignore`,
  `CLAUDE.md`.

## Machines

| Machine | Ubuntu | State |
| --- | --- | --- |
| LENOVO desktop (working machine, `~/gr-wiki-revision`) | 26.04 | 16 cores, 15 GiB RAM, 4 GB swap. Reloaded 2026-10-08. UHD 4.11 from the PPA (only UHD; `libuhd4.9.0` removed 2026-10-12). `~/gnuradio` = plain clone of `gnuradio/gnuradio` on `maint-3.10`, GNU Radio 3.10.12.0 in `/usr/local`, 42 components. 13 SoapySDR modules (`v2.2` Step 1 run for real). `v2.3`'s Boost step not run here (would add 4 small metapackages). Hardware: USRP B200mini, RTL-SDR, PlutoSDR. |
| GMKtec (clean-install test machine) | reloaded per test | 4 cores, 10 GiB. Clean 24.04 with `v2.2` on 2026-10-14 lost `gr-uhd` (the Boost problem); reloaded the same day with a clean 24.04 and `v2.3`: all passed, 42 components, B200mini / RTL-SDR / PlutoSDR tested (see Test results). **Reloaded with Fedora 44** (user, 2026-10-16) for a Fedora trial; see "Fedora 44 trial" under Open items. **Reloaded with a clean 26.04** (user, 2026-10-17) for the `v2.4` test; the Fedora unknowns can no longer be checked there. |
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
   and (`v2.4`) `python3-pytest`
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
| `v2.4` | 2026-10-15 | Step 1: `python3-pytest`, so 24.04 builds run `grc_tests`. Commit `ce9806d`; Release title "v2.4: pytest for the GRC test". Download link checked: gives the `v2.4` Step 1 script. |
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
26.04 (267 on 24.04); `maint-3.10` 269 on 26.04, 268 on 24.04. The
`maint-3.10` difference is test 25, `grc_tests` (user, 2026-10-15). Its
cause (checked by me): `grc/tests/CMakeLists.txt` adds `grc_tests` only if
cmake can `import pytest`, and `python3-pytest` is in Ubuntu's `gnuradio`
Build-Depends on 26.04 (3.10.12.0-6) but not on 24.04 (Launchpad's
`debian/control` for noble), so `build-dep gnuradio` installs it only on
26.04. On `main` the same test accounts for one of the four; the other
three are unexplained.

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
| 2026-10-14 | GMKtec, clean 24.04 | `v2.2` (user confirmed) | `maint-3.10` | **`gr-uhd` disabled**: `Boost_FOUND = FALSE` under "Configuring gr-uhd support", call stack through `UHDConfig.cmake:31`; cmake 3.28. Led to `v2.3`. |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3` | `maint-3.10` | 268/268, 3.10.12.0, UHD 4.11.0.0-0ubuntu1~noble3, 42 components incl. `gr-uhd` + RFNoC: **Boost fix confirmed** |
| 2026-10-14 | GMKtec, clean 24.04 (user; `~/share/Clean_build_261014.txt`) | `v2.3`, downloaded from the wiki page | `maint-3.10` | 268/268, 3.10.12.0, UHD ~noble3; cmake's "Gnuradio disabled components" list **empty**; 42 components incl. `gr-uhd` + RFNoC, `gr-iio` + `libad9361`, `gr-qtgui`, `gr-soapy`, thrift. `SoapySDRUtil --info`: **11 modules**, exactly the expected 24.04 set (airspy, audio, bladerf, hackrf, lime, miri, osmosdr, redpitaya, remote, rfspace, rtlsdr), no UHD; first real run of `v2.2`'s SoapySDR step on 24.04 and on a clean install. Boost fix confirmed by the user too. |
| 2026-10-15 | LENOVO, 26.04 | — (plain `make test 2>&1 \| tee make_test.log` in `~/gnuradio/build`, run once by me and once by the user) | `maint-3.10`, 3.10.12.0, the existing build | **269/269, `grc_tests` passed** although the previous run's generated files were still in `grc/tests/resources` (not cleaned): repeated test runs pass on `maint-3.10` without `v2.1`'s `git clean` step. 132 s. The user's own run: "100% tests passed, 0 tests failed out of 269" |
| 2026-10-15 | GMKtec, clean 24.04 (the `v2.3` install of 2026-10-14) | `v2.3` + `python3-pytest` installed by hand | `maint-3.10` | **269/269** ("100% tests passed, 0 tests failed out of 269"): with pytest, 24.04 adds `grc_tests` and it passes; same count as 26.04 |
| 2026-10-16 | GMKtec, clean **Fedora 44** (prompt still shows hostname `ubuntu`) | none: "option 1" by hand (Fedora's UHD 4.9.0.1, `dnf builddep gnuradio`, cmake/make/make install) | plain clone, `maint-3.10` | **Installed and imports**: 3.10.12.0; 41 components, the Ubuntu 42 minus **thrift** (`gr-ctrlport` without its Thrift back-end; Fedora's `builddep` doesn't bring `thrift-devel` / `python3-thrift`, both exist in f44 at 0.20.0), incl. `gr-uhd` + RFNoC, `gr-iio` + `libad9361`, `gr-qtgui`, `gr-soapy`. Python module at `/usr/local/lib64/python3.14/site-packages/gnuradio/` and found by `import gnuradio.gr` (Fedora's Python searches `/usr/local/lib64`). **`make test`: `qa_fastnoise` failed** (user; overall count not given). `ctest -R qa_fastnoise --output-on-failure`: only `test_001_real_laplacian_moments`, 11 of 12 sub-tests pass; `data.var()` = 1.99293 vs 2, off by 0.0071, over `places=2`'s 0.005 and well inside `aee9fd3f7`'s `delta=0.05`. `main` has `aee9fd3f7` (2026-08-26, "qa_fastnoise: Widen the Laplacian variance tolerance": `places=2` → `delta=0.05`, the correct distribution failed `places=2` 2–12% of runs) and `56d230fd3` (2026-06-02, Marcus Müller, "analog/fastnoise+gr::random: simplify, fix unit test"); neither is on `maint-3.10` (checked by me). So it is the flaky tolerance fixed by `aee9fd3f7` on `main`, not a Fedora fault. `aee9fd3f7` doesn't cherry-pick cleanly onto `maint-3.10` (`56d230fd3` changed the same lines on `main`), so the user changed the one line by hand (`places=2` → `delta=0.05`, line 75, checked by me on a copy): **`make test` 269/269** (user, 2026-10-16), the same count as 26.04 and as 24.04 with pytest. Undo with `git restore gr-analog/python/analog/qa_fastnoise.py`. **`gnuradio-companion` works** (user, 2026-10-16; whether a QT GUI flowgraph was run not stated). Disabled-components list, SoapySDR modules, and whether the `ld.so.conf.d` line was needed not reported yet |
| 2026-10-17 | GMKtec, clean 26.04 | `v2.4` (presumably downloaded from the wiki page; my assumption) | presumably `maint-3.10` (my assumption; not stated) | **269/269** ("100% tests passed, 0 tests failed out of 269", user, 2026-10-17), as expected on 26.04. Step 1 ran: `uhd_config_info --version` = UHD 4.11.0.0-0ubuntu1~resolute3 (user). First real run of `v2.3`'s Boost step and `v2.4`'s `python3-pytest` on 26.04 (my reading: Step 1 finished, since UHD is installed). `SoapySDRUtil --info` (SoapySDR v0.8.1-7build1): **13 modules**, exactly the expected 26.04 set (airspy, airspyhf, audio, bladerf, hackrf, hydrasdr, lime, miri, osmosdr, plutosdr, redpitaya, remote, rtlsdr), no UHD: first run of `v2.2`'s SoapySDR step on a clean 26.04. The three checks "work" (user, 2026-10-17): 3.10.12.0, cmake's disabled-components list empty, 42 components (my reading of "work" = the expected values; numbers not pasted). **`gnuradio-companion` works** (user, 2026-10-17; whether a QT GUI flowgraph was run not stated). B200mini and PlutoSDR loopbacks and RTL-SDR stereo FM work (see Hardware). **Clean 26.04 test of `v2.4` complete: all passed** |

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
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | RTL-SDR, HackRF, LimeSDR Mini, Airspy R2 | `gr-soapy` | all work; the Airspy R2 through the Soapy Custom Source block (only it), the others presumably through their own blocks (my reading). **The HackRF and the LimeSDR Mini also transmitted** (user, 2026-10-15) |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | USRP B200mini | `gr-uhd` | works, **including transmit** (user, 2026-10-15) |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | USRP B200mini (315C7B7) | UHD tools, `gr-uhd` | `uhd_find_devices`, `uhd_usrp_probe` (FPGA, USB 3, loopback passed), `uhd_rx_cfile` 8,000,000 bytes; Boost_108300. **Loopback (transmit and receive) through `gr-uhd` with a 30 dB attenuator worked** (user, 2026-10-15) |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | RTL-SDR (RTL2838, R820T) | SoapySDR | `--find` and `--probe="driver=rtlsdr"` work (kernel driver detached/reattached by the library); receive only, as planned. `--find` also lists a "USB Audio and HID" device through the audio module |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | PlutoSDR | `gr-iio`: PlutoSDR Source and PlutoSDR Sink (user, 2026-10-15) | **"Pluto with loopback cable works."** Both at 2.435 GHz. First PlutoSDR / `gr-iio` test |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10`, Fedora's UHD 4.9.0.1 | RTL-SDR | presumably `gr-soapy` with `soapy-rtlsdr` (my inference; block not stated) | **Received a broadcast FM station in stereo** (user, 2026-10-16): first RTL-SDR flowgraph by the user, and the first device test on Fedora. Presumably audio out through `gr-audio` too (my inference) |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10`, Fedora's UHD 4.9.0.1 | USRP B200mini | `gr-uhd` | **Loopback file transfer worked** (user, 2026-10-16): transmit and receive with Fedora's UHD 4.9.0.1 and its `uhd-firmware` images, 30 dB attenuator, the user's own flowgraph. Works as the normal user with no udev change (Fedora's `uhd` rules are enough) |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10` | PlutoSDR | `gr-iio`: PlutoSDR Source and Sink ("PlutoSDR", user) | **Loopback worked** (user, 2026-10-16), the user's own flowgraph; frequency and attenuation not stated |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, presumably `maint-3.10` (my assumption) | USRP B200mini | `gr-uhd` (presumably; path not stated, my assumption) | **Loopback worked with a 30 dB attenuator** (user, 2026-10-17): **first transmit on 26.04**. UHD tools (`uhd_find_devices` / `uhd_usrp_probe`) not reported |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, presumably `maint-3.10` (my assumption) | PlutoSDR | presumably `gr-iio` PlutoSDR Source and Sink (my assumption; not stated) | **Loopback worked** (user, 2026-10-17): first PlutoSDR test on 26.04; frequency and attenuation not stated |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, presumably `maint-3.10` (my assumption) | RTL-SDR | presumably `gr-soapy` (my assumption; block not stated) | **Received a broadcast FM station in stereo** (user, 2026-10-17): first RTL-SDR flowgraph on 26.04 |

Transmit: PlutoSDR loopback (2.435 GHz) and B200mini loopback, both on the
GMKtec, clean 24.04, `v2.3`, `maint-3.10` (2026-10-14). The other tester
transmitted with a HackRF, a LimeSDR Mini, and a B200mini on 2026-10-14
(clean 24.04, `v2.3`, `maint-3.10`). B200mini loopback file transfer on the
GMKtec with Fedora 44 (2026-10-16), and PlutoSDR loopback there too.
On 26.04: B200mini loopback with a 30 dB attenuator and PlutoSDR loopback
on the GMKtec, clean 26.04, `v2.4` (2026-10-17).

## Open items

- ~~**`v2.3` on 26.04**~~ **Closed 2026-10-17:** the Boost step ran for
  real in `v2.4`'s Step 1 on a clean 26.04 GMKtec, and the build gave
  269/269 with 42 components (see Test results).
- **Transmit:** B200mini and PlutoSDR loopbacks work on 24.04
  (2026-10-14), as do the other tester's HackRF, LimeSDR Mini, and
  B200mini. On 26.04 the B200mini and PlutoSDR loopbacks work too
  (GMKtec, clean 26.04, `v2.4`, 2026-10-17). Done on both releases.
- ~~**RTL-SDR flowgraph on the LENOVO**~~ **Closed 2026-10-17** (user:
  "close rtlsdr on Lenovo"): covered by the RTL-SDR stereo FM flowgraph on
  the GMKtec, clean 26.04 (2026-10-17).
- **Test counts:** 268 vs 269 on `maint-3.10` is `grc_tests` (no pytest
  on 24.04); three of the four on `main` (267 vs 271) are unexplained.
  `v2.4` (user: "yes, make v2.4", 2026-10-15) installs `python3-pytest`
  in Step 1 so 24.04 runs `grc_tests` too. With pytest installed by hand,
  24.04 gave 269/269 (2026-10-15); not yet tried twice in a row or on
  `main`. pytest is in universe on 24.04 (7.4.4). GNU Radio's pytest check
  isn't cached, so re-running cmake picks it up.
- **Upstream `grc_tests` fix:** when it lands, remove the builder's
  `git clean` step and its doc bullet in a new tag.
- **Docs:** the leftover-library command can leave dangling
  `.so.3.11.0git` links; the cause of the missing Thrift on `main`.
- **Longer term:** Qwt for Qt6, for `gr-qtgui` on `main`.
- **Fedora 44 trial (GMKtec, started 2026-10-16):** neither script runs on
  Fedora (Step 1 requires Ubuntu; the builder's `dpkg-query` check for
  `libuhd-dev` fails, as does `v1.3`, whose UHD installer parses only `apt-get`
  Dockerfiles and gets the slug `fedoralinux44`). User chose "option 1":
  Fedora's own UHD 4.9.0.1 + `dnf builddep gnuradio` (Fedora's `gnuradio` is
  3.10.12.0), then GNU Radio `maint-3.10` built by hand with cmake. Package
  names checked by me on mdapi.fedoraproject.org (f44): `uhd`, `uhd-devel`,
  `uhd-tools`, `uhd-firmware`, `boost-devel`, `python3-QtPy`,
  `python3-pyqtgraph`, `python3-matplotlib`, `python3-pytest`, `SoapySDR`,
  `soapy-rtlsdr`, `soapy-airspyhf`, `soapy-uhd` (no HackRF / Lime / Pluto /
  bladeRF Soapy modules found under the names tried). Expected differences
  (mine, unverified): GNU Radio installs to `/usr/local/lib64`, which
  Fedora's `ldconfig` may not search; the builder's stale-dir patterns know
  only `lib/`. (USRP udev: no change needed, B200mini works as the normal
  user, 2026-10-16.) Ettus also publishes
  `uhd-builder-fedora44.Dockerfile` (for a UHD-from-source option 2, not
  chosen). The user finished the Fedora trial 2026-10-16 ("that's all I
  want to do on Fedora").
- **Fedora support in the project (proposed by me 2026-10-16, user asked to
  record it; not decided).** Suggested tag `v3.0`; talk to the developers
  first (Fedora on the wiki page, the move into `gnuradio/gnuradio`, the
  `qa_fastnoise` backport).
  - Step 1: dispatch on `ID` in `/etc/os-release`; Ubuntu path unchanged.
    Fedora path: `dnf builddep gnuradio`; `dnf install` `uhd uhd-devel
    uhd-tools uhd-firmware python3-QtPy python3-pyqtgraph python3-matplotlib
    python3-pytest thrift-devel python3-thrift`; SoapySDR modules from
    `dnf`'s list of `soapy-*` (no metapackage; `soapy-uhd` can stay, same
    UHD); no deb-src, PPA, or `uhd_images_downloader`. Conflict check with
    `rpm -q gnuradio gnuradio-devel python3-gnuradio`, fix with `dnf remove`.
    UHD is 4.9.0.1 on Fedora vs 4.11 on Ubuntu: document it.
  - Builder: `rpm -q uhd-devel` instead of `dpkg-query libuhd-dev`;
    `lib64/python3*/site-packages/...` in `INSTALL_DIR_PATTERNS`; add
    `/usr/local/lib64` to `ld.so.conf.d` if needed. `qa_fastnoise` fails on
    Fedora `maint-3.10` and the builder stops on any failed test, so Fedora
    users would never install: (a) upstream backport of `aee9fd3f7` (my
    preference), (b) an option to skip named tests, or (c) document the
    one-line edit.
  - Docs (draft first, then README): Fedora notes in Step 1; `lib64` in the
    "Changing branches..." removal commands (kept in sync with the patterns)
    and in the leftover-library command; `python3-QtPy` spelling, fewer
    Soapy modules, no udev change needed.
  - Testing: clean Fedora for every change, and Ubuntu 24.04 / 26.04 must
    not change. Fedora releases every 6 months (~13 months support): Fedora
    45 around April 2027.
  - Unknown before coding (from Fedora, before the GMKtec is reloaded): was
    the `ld.so.conf.d` line needed; did `dnf builddep` need `dnf5-plugins`;
    the `dnf search soapy` list; whether Thrift gives 42 components.
- **Where the scripts will live** (user, 2026-10-14): asked about renaming
  the repo, then said they will talk to the GNU Radio developers; "the
  plan is to bring it into the gnuradio/gnuradio repo", details not settled.
  Nothing changed yet. If it moves, the download links in the wiki draft,
  README, and Release notes, and the repo URLs here, need updating.
