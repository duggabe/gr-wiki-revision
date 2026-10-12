# gr-wiki-revision — Bare-Metal UHD / GNU Radio Build Tooling

## Project summary

Tooling to build and install Ettus Research's UHD (USRP Hardware Driver)
and GNU Radio directly on bare metal (no Docker) on Ubuntu, with two Python
installers that derive their package lists from upstream instead of
hardcoding them: UHD's from EttusResearch's own Docker build environment
(`.ci/docker/uhd-builder-ubuntu<NNNN>.Dockerfile` in the `EttusResearch/uhd`
repo), GNU Radio's from the `Build-Depends` of Ubuntu's own `gnuradio`
package. Volk comes from Ubuntu's `libvolk-dev`. That is **Phase 1**
(`v1.x`). **Phase 2** (`v2.0`) adds two more scripts for GNU Radio
developers: one installs UHD from the Ettus PPA and GNU Radio's
dependencies with `apt-get` only, the other builds GNU Radio from a clone
already on the machine.

**Current state (2026-10-10):** two releases, both with GitHub Releases.
**Phase 1 = `v1.2`** (UHD and GNU Radio built from source): tested on
Ubuntu 24.04 (clean install) and 26.04 — UHD 4.11.0.0 and GNU Radio
3.10.12.0 (`maint-3.10`) with all 42 components, all tests passing; the
GNU Radio developers and documentation people reviewed the wiki page with
no negative comments. **Phase 2 = `v2.0`** (the GitHub "Latest" release;
UHD from the Ettus PPA, then GNU Radio built from a clone already on the
machine, for GNU Radio developers), two self-contained scripts,
`gnuradio_dependencies_installer.py` and `gnuradio_clone_builder.py`:
tested on a clean Ubuntu 26.04 install (`main`, v3.11.0.0git-1193, 271/271
tests, no `gr-qtgui`) and on the Ubuntu 24.04 laptop (`maint-3.10`,
3.10.12.0, 268/268 tests, 42 components incl. `gr-qtgui`). The live wiki
page "Building GNU Radio from Source Code" has Phase 2 first, then
Phase 1. Tags `v1.0` and `v1.1` stay available. Nothing is waiting on
anyone. Open: running Step 2 on the LENOVO; the Phase 1 scripts on `main` have
the memory-aware `make` job count (written 2026-10-10, tagged `v1.3`, no
real build yet, links still on `v1.2`); the `main`/Qt6 path
(Qwt for Qt6). Details are in Next steps 12 and 13.

Lives at **https://github.com/duggabe/gr-wiki-revision** (public): scripts
and programs supporting GNU Radio Wiki documents, which the user writes.
This repo is the ultimate
target project. The earlier `~/AIwork` project on the user's laptop was a
trial to learn Claude and check the feasibility of these methods; its work
was pushed here, merging with this repo's original auto-generated
`README.md` (`--allow-unrelated-histories`) rather than overwriting it.
Since the installers back wiki instructions for other GNU Radio users,
favour clarity, reproducibility, and reader choice over personal
convenience.

**Goal:** replace all of the wiki's build-from-source instructions with one
new page, "Building GNU Radio from Source Code". The current path (as of
17 Sept 2026) is: InstallingGR → LinuxInstall#From_Source →
UbuntuInstall#Install_Dependencies → LinuxInstall#Installing_UHD → the
draft page's "Building and installing UHD from source code" section →
LinuxInstall#Installing_Volk → LinuxInstall#Installing_GNU_Radio. The
Phase 1 installers cover the UHD and GNU Radio build steps (Volk comes from apt),
and since 2026-10-03 the GNU Radio installer also covers
UbuntuInstall#Install_Dependencies (GNU Radio's own deps) for the Qt5-based
`maint-3.10`. The wiki's manual list is still written for Ubuntu 20.04–24.04
+ Qt5 while GNU Radio `main` moves to Qt6.
The new page is live (since 2026-09-26; Phase 2 first since 2026-10-10).
wiki.gnuradio.org is behind a Cloudflare challenge and can't be fetched
from here — ask the user to paste page content.

**Machines and Ubuntu versions:**

| Machine | Ubuntu | Role |
| --- | --- | --- |
| Laptop | 24.04 | `~/AIwork` trial; 24.04 testing, with both the bash script + the wiki's manual steps and the Python installers. 2026-10-10: Phase 2 (`v2.0`) with `maint-3.10` — all passed |
| LENOVO desktop | 26.04 | current working machine, `~/gr-wiki-revision`; 26.04 builds of UHD, Volk, GNU Radio. Reloaded with a fresh 26.04 on 2026-10-08 (16 cores, 15 GiB RAM, 4 GB swap); since then UHD from the Ettus PPA and a hand-built GNU Radio `main` in `/usr/local`; `~/gnuradio` is the user's fork |
| GMKtec (clean install) | reloaded per test: 24.04, 26.04.1, 24.04, 26.04 | 2026-09-26: 24.04, tested the wiki page (`v1.0`) from scratch. 2026-10-03: fresh 26.04.1, tested `v1.1`. 2026-10-04: fresh 24.04, tested the current `main` scripts (dependency step, `maint-3.10`) — all passed. 2026-10-10: fresh 26.04, tested Phase 2 (`main`) — all passed |

Ettus has Dockerfiles for both (`uhd-builder-ubuntu2404.Dockerfile` and
`uhd-builder-ubuntu2604.Dockerfile`, plus 20.04, 22.04, 25.10, and Fedora),
which is why `uhd_bare_metal_installer.py` auto-detects the host OS from
`/etc/os-release` rather than hardcoding one. The 24.04 list differs from
26.04's: it adds `clang-format-14` and `swig` (and has duplicate
`libgps-dev` / `python3-ruamel.yaml` lines, which apt ignores) and lacks
`python3-setuptools`. `install-uhd-build-deps.sh` hardcodes the 26.04 list.

## Files

- **`uhd_bare_metal_installer.py`** — the main tool. Fetches UHD's Dockerfile
  from GitHub (or a local path), auto-detects the host OS from
  `/etc/os-release` to pick the matching Dockerfile (e.g. Ubuntu 24.04 →
  `ubuntu2404`), parses out the `apt-get install` package list, and can:
  - `--list-only`: just print/save the parsed package list
  - `--dry-run`: show the commands that would run, no root needed
  - (default, run as root): actually `apt-get install` the dependencies
  - `--build`: additionally clone, `cmake`/`make`/`make test` (each
    `2>&1 | tee`'d to `cmake.log` / `make.log` / `make_test.log` in
    `~/uhd/host/build`, since 2026-10-02), install UHD from source, install
    udev rules, and run `uhd_find_devices` / `uhd_images_downloader`. Any
    failure, including a failing unit test, stops the build before
    `sudo make install`.
  - Does not hardcode the package list or assume Ubuntu 26.04 — aborts if no
    matching Dockerfile is found rather than guessing.

- **`install-uhd-build-deps.sh`** — earlier, simpler bash version. Hardcodes
  the Ubuntu 26.04 dependency list inline (installs deps only, does not
  build UHD). Superseded in capability by the Python tool but kept as a
  standalone script that needs no network fetch of the Dockerfile itself.

- **`uhd-ubuntu2604-dependencies.txt`** — dependency list matching what
  `install-uhd-build-deps.sh` installs (Ubuntu 26.04).

- **`uhd-dependencies.txt`** — output of the most recent
  `uhd_bare_metal_installer.py` run (default `-o` filename). Refreshed
  2026-09-25 (`--list-only` on Ubuntu 26.04); now identical to
  `uhd-ubuntu2604-dependencies.txt`. Since 2026-10-02 the GNU Radio
  installer only checks that this file exists (no content/order checks).

- **`gnuradio_bare_metal_installer.py`** — installs GNU Radio's own
  dependencies, then builds/installs GNU Radio from source, after the UHD
  installer. Imports `BuildStep`, `run_build_steps()`, `write_package_list()`
  etc. from `uhd_bare_metal_installer.py`. Flow:
  1. Fetch `debian/control` of Ubuntu's `gnuradio` source package for the
     host's codename (`VERSION_CODENAME` in `/etc/os-release`) from
     `https://git.launchpad.net/ubuntu/+source/gnuradio/plain/debian/control?h=ubuntu/<codename>`
     (or `--control-url` / `--control-path`), parse `Build-Depends`
     (`extract_build_depends()`: drops version constraints and build
     profiles, evaluates arch restrictions like `[linux-any]` /
     `[kfreebsd-any]`, first of `a | b`; ignores `Build-Depends-Indep`).
  2. `select_packages()`: drop `SKIP_PACKAGES` (`libuhd-dev`,
     `debhelper-compat`, `dh-python`, `dpkg-dev`, `graphviz`, `xmlto`,
     `libjs-mathjax`), add `EXTRA_PACKAGES` (`libvolk-dev`,
     `python3-packaging` if missing; `python3-qtpy`, `python3-pyqtgraph`,
     `python3-matplotlib`, `soapysdr-tools`). 26.04: 69 → 66 packages;
     24.04: 70 → 67. Saved to `gnuradio-dependencies.txt` (`-o`).
     `--list-only` stops here.
  3. Abort unless `uhd-dependencies.txt` (`--uhd-deps`) exists.
  4. Abort if `find_stale_install_dirs()` finds empty `gnuradio` (or
     `pmt`, `etc/gnuradio`) directories from a removed install under
     `/usr/local` (`INSTALL_DIR_PATTERNS`; prints the `sudo rm -rf`
     command). Keep that pattern list, README's "Removing an earlier
     install" command, and the wiki draft's command in sync.
  5. `sudo apt-get update` → `sudo apt-get install -y <packages>` →
     `git clone` → `git checkout <--branch>` (**default `maint-3.10`** since
     2026-10-03; `main` = 3.11 development) → `mkdir build` → `cmake ...
     2>&1 | tee cmake.log` → `make -j... 2>&1 | tee make.log` → `make test
     2>&1 | tee make_test.log` → `sudo make install` → `sudo ldconfig`, in
     `~/gnuradio`. Any failure (incl. a failing test) stops the build.
  Options: `--branch`, `--control-url`, `--control-path`,
  `--os-release-path`, `--list-only`, `-o`, `--uhd-deps`, `--dry-run`, `-y`,
  `--home`, `--build` (ignored).

- **`gnuradio-dependencies.txt`** — output of the GNU Radio installer
  (default `-o`): the 66-package list for Ubuntu 26.04, written 2026-10-03.
  (An earlier file of this name, a copy of the Ettus list, was removed
  2026-10-02.)

- **`gnuradio_dependencies_installer.py`** — **Phase 2, Step 1** (in
  `v2.0`). Self-contained (imports nothing from the Phase 1 scripts);
  `apt-get` only, nothing compiled. Checks the host is Ubuntu; aborts if
  Ubuntu's `gnuradio` / `gnuradio-dev` packages are installed or a
  source-built UHD is under `/usr/local` (prints the fix commands); enables
  "Source code" (`Types: deb` → `Types: deb deb-src` in
  `/etc/apt/sources.list.d/ubuntu.sources`, backup `.bak`); then `apt-get
  update` → `apt-get install -y software-properties-common git` →
  `add-apt-repository -y ppa:ettusresearch/uhd` → `apt-get install -y
  --no-install-recommends uhd-host libuhd-dev` → `apt-get build-dep -y
  gnuradio` → `apt-get install -y python3-qtpy python3-pyqtgraph
  python3-matplotlib soapysdr-tools` → `uhd_images_downloader`. Options:
  `--dry-run`, `-y`, `--no-images`, `--sources-path`, `--os-release-path`.

- **`gnuradio_clone_builder.py`** — **Phase 2, Step 2** (in `v2.0`).
  Self-contained: carries trimmed copies of the Phase 1 `BuildStep` /
  `run_build_steps()` / `run_logged()` / `get_build_user()` helpers and of
  `INSTALL_DIR_PATTERNS` (keep that list in sync with the Phase 1
  installer). Builds whatever is checked out in `~/gnuradio`
  (`--source-dir`) — a fork or a plain clone, any branch; never clones or
  changes branches; reuses an existing `build/`, so it serves the edit →
  rebuild loop. Steps: `mkdir build` (first time) or `sudo chown -R` the
  build dir back to the user if `sudo make install` left root-owned files
  → cmake / make / make test, tee'd to `cmake.log` / `make.log` /
  `make_test.log` → `sudo make install` → `sudo ldconfig`. `make` jobs =
  `min(nproc - 1, MemTotal // 2 GB)`, at least 1. Aborts if the directory
  isn't GNU Radio source, `libuhd-dev` isn't installed, Ubuntu's `gnuradio`
  packages are installed, or stale install dirs exist. Options:
  `--source-dir`, `--jobs`, `--cmake-args="..."`, `--no-install`,
  `--dry-run`, `-y`.

- **Removed 2026-10-02:** `volk_bare_metal_installer.py` and
  `volk-dependencies.txt` (still in `v1.0` and git history). Volk comes
  from Ubuntu's `libvolk-dev`, which is on the GNU Radio dependency list.

- **`LICENSE`** — Creative Commons Attribution-ShareAlike 4.0
  International (CC BY-SA 4.0), added 2026-09-24. Note that Creative
  Commons advises against its licenses for software; kept as-is by choice.

- **`README.md`** — user-facing docs, restructured 2026-10-11 so that
  **Phase 2 stands alone and Phase 1 can be removed in one cut**: a short
  intro with one bullet per phase; then `## Phase 2: UHD from the Ettus
  PPA, GNU Radio from your fork` (download with `v2.0` links, before you
  start, Step 1 and Step 2 with options tables and the memory note,
  "Changing branches, or removing the installed GNU Radio", "Phase 2
  tested builds", "Phase 2 known limitation", "Phase 2 releases") — it has
  no links into and no mentions of Phase 1; then `## Phase 1: UHD and GNU
  Radio 3.10 from source`, which runs to the end of the file and holds
  everything else, one heading level deeper than before (quick start,
  "Tested builds", "Releases and changes" `v1.3`/`v1.2`/`v1.1`, "Download
  the installers" with `v1.2` links, "Run the installers in order" with
  "Removing an earlier install", "Environment variables", the UHD and GNU
  Radio usage sections). **To retire Phase 1:** delete from the `## Phase
  1` heading to the end and the Phase 1 bullet in the intro. Keep the
  options tables in sync with the scripts' argparse help. The README at
  the `v2.0` tag predates all of this.

- **`wiki-draft-download-section.txt`** — local-only (in `.gitignore`, so
  not on GitHub or other machines): the user's copy, in MediaWiki markup,
  of the **live wiki page** "Building GNU Radio from Source Code". Treat
  the wiki as the master copy; after the user edits the live page, the
  local file is only current if they paste it back. Structure since
  2026-10-10: the user's introduction (Phase 2 goals first, then "Phase 1
  goals (completed)", notes on OOT modules, the README link, and
  "bare-metal" = non-container) → `== Phase 2 ==` (status line: tested on
  a clean 26.04 with `main` and on 24.04 with `maint-3.10`; downloading the
  two scripts via `v2.0` raw links; before you start; Step 1; Step 2:
  getting the source code, starting a branch, building/testing/installing
  incl. the memory note, the `main`-lacks-`gr-qtgui` note and the
  `maint-3.10` paragraph, making and submitting a change; checking the
  result) → `== Phase 1 ==` (the `v1.2` text, unchanged since 2026-10-04:
  two scripts via tag-pinned raw links, where the dependency lists come
  from, `--branch`, build logs and `make test`, replacing an earlier
  install, checking the result). History: first drafted 2026-09-26,
  rewritten for `v1.2` on 2026-10-03.

- `AI_notes.txt` (running log incl. the machine-migration checklist) was
  removed from the repo on 2026-09-25; its content survives in git history
  (before commit `7472367`).

## What's been done

- 2026-09-22: Built `install-uhd-build-deps.sh` from UHD's Ubuntu 26.04
  Dockerfile. Used it plus the GNU Radio wiki's from-source build guide
  to successfully build, with no errors, on the original
  machine (the Ubuntu 24.04 laptop):
  - UHD 4.11.0.0-0-g0d7ed3b1
  - Volk 3.3.0
  - GNU Radio v3.11.0.0git-1174-gaee9fd3f
- 2026-09-24: Wrote `uhd_bare_metal_installer.py` to generalize the bash
  script — auto-detects host OS instead of hardcoding Ubuntu 26.04, fetches
  the Dockerfile live from GitHub instead of baking in the package list, and
  adds an end-to-end `--build` path (clone → cmake → make → install → udev
  rules) instead of just printing next-step instructions.
- Set the laptop up for git/GitHub, following the migration checklist
  then recorded in `AI_notes.txt` (since removed): initialized git in `~/AIwork`, added
  `.gitignore`, committed, and pushed to the existing
  https://github.com/duggabe/gr-wiki-revision repo (merged with its
  pre-existing `README.md` via `--allow-unrelated-histories`).
- 2026-09-24: Now migrating to a new machine, **LENOVO**, which will be used
  for all future work going forward. On LENOVO the working directory will be
  the repo clone itself, `~/gr-wiki-revision` (not `~/AIwork` — that name
  only exists on the laptop). Since the project is already
  on GitHub, the migration is just: install `git`/`gh`/Claude Code, `gh auth
  login`, `git config` identity, then `gh repo clone
  duggabe/gr-wiki-revision` — no `.env` to copy (none exists in this
  project).
- 2026-09-25: Reformatted `README.md` as proper Markdown, removed
  `AI_notes.txt`, and added `volk_bare_metal_installer.py` (tested in
  `--dry-run` on Ubuntu 26.04 only; no real Volk build run yet).
- 2026-09-25: Refreshed `uhd-dependencies.txt` with `--list-only` (OS
  auto-detection picked `uhd-builder-ubuntu2604.Dockerfile` correctly on
  this Ubuntu 26.04 host), then ran `volk_bare_metal_installer.py
  --dry-run` in the repo: dependency check passed, build plan printed
  (`~/volk`, `make -j15`). Committed `volk-dependencies.txt`.
- 2026-09-25: Built UHD with `uhd_bare_metal_installer.py --build` on the
  Ubuntu 26.04 machine: installed **UHD 4.11.0.0-0-g0d7ed3b1** successfully
  (same version as the original machine's build).
- 2026-09-25: Ran `volk_bare_metal_installer.py` for real on the Ubuntu
  26.04 machine: built and installed **Volk 3.3.0** successfully (same
  version as the original machine's build).
- 2026-09-25: Ran `gnuradio_bare_metal_installer.py` for real on the same
  Ubuntu 26.04 machine: built and installed **GNU Radio
  v3.11.0.0git-1174-gaee9fd3f** successfully (same version as the original
  machine's build). Found 2026-09-26: this build lacks `gr-qtgui`,
  `gr-soapy`, `gr-iio`, and the JACK/PortAudio audio back-ends — cmake
  silently skipped them because only UHD's deps were installed (see Next
  step 8).
- 2026-09-26: Made all three installers build as the normal user even when
  started with sudo, and chown the dependency lists back to the user (see
  Key decisions). Also: the UHD `--dry-run` "Build user" line now describes
  the required sudo run, and `/usr/local/lib` is only prepended to
  `LD_LIBRARY_PATH` if missing (no duplicate, no stray `:`). Chowned the
  existing root-owned `~/uhd` and `~/gnuradio`. Verified the full dry-run
  sequence in the repo: UHD `--dry-run --build` → Volk `--list-only` →
  GNU Radio `--dry-run` passes. Added the "Run the installers in order"
  section to `README.md`.
- 2026-09-26: Recorded the wiki consolidation goal and the GNU Radio
  dependency gap (Next step 8); drafted the wiki page's download/run
  sections (`wiki-draft-download-section.txt`, local only); corrected the
  machine/Ubuntu-version facts. Created and pushed tag **`v1.0`** (commit
  `24ef53f`) and verified the draft's `wget` loop from the `v1.0` raw links
  in an empty directory (all three downloaded, `--help` works, order check
  passes). Then added "Download the installers" and the tested-Ubuntu note
  to `README.md` (after the tag, so `v1.0`'s own README lacks them; the
  scripts are unchanged).

- 2026-09-26: The user created the "Building GNU Radio from Source Code"
  wiki page and tested it on the GMKtec (clean Ubuntu 24.04) using only the
  page and the `v1.0` scripts: everything worked. Enabled GNU Radio
  components match the LENOVO's exactly. Noted the clean-install test in
  `README.md`'s "Tested builds" (commit `e96de90`).

- 2026-09-27: Investigated GNU Radio's own dependencies (Next step 8):
  found GNU Radio's CI Dockerfiles in `gnuradio/gnuradio-docker`, that the
  GNU Radio installer builds `main` (3.11git, Qt6) rather than the released
  `maint-3.10` (Qt5), and that Qwt for Qt6 is packaged only in Ubuntu 26.10.
  Updated step 8 and `README.md`'s "Known limitation" and GNU Radio section
  to explain the branch and Qt5/Qt6 split. The user is asking the GNU Radio
  developers which branch the wiki page should build. Later: evaluated the
  main developer's proposal to install UHD from the Ettus PPA, and checked
  that the `/usr/local` prefix needs no env vars except for UHD's own
  Python API (recorded in step 8). Added "Planned changes" and
  "Environment variables" sections to `README.md` (commit `001d029`).
- 2026-10-02: Decided (user) not to use the Ettus PPA; UHD stays a source
  build. Changed the UHD `--build` steps (user's list) to
  `cmake ... 2>&1 | tee cmake.log`, `make -j... 2>&1 | tee make.log`,
  `make test 2>&1 | tee make_test.log`. Added a general `log` option to the
  shared `BuildStep`/`run_build_steps()` (`run_logged()`: streams output to
  the terminal and the log, log owned by the build user) and
  `describe_step()` for previews. Tested with harmless commands, a
  simulated sudo run, and the dry-run preview. Not in `v1.0`.
- 2026-10-02: Real test on the LENOVO: `sudo python3
  uhd_bare_metal_installer.py --build --skip-upgrade` (old `~/uhd` moved to
  `~/uhd.old`) finished with no errors. `make_test.log`: 100% of 109 UHD
  unit tests passed. Installed UHD 4.11.0.0-0-g0d7ed3b1 (`master` was at
  tag `v4.11.0.0`); `uhd_find_devices` runs; udev rules installed. First
  real sudo run of the normal-user build: `~/uhd`, `~/uhd/host/build`, the
  three logs (380/1149/224 lines), and `uhd-dependencies.txt` are all owned
  by barry; root-owned files only inside `build/` (from `sudo make
  install`). Refreshed the Volk list afterwards.
- 2026-10-02: Per the user: removed Volk from the install process
  completely (deleted `volk_bare_metal_installer.py`,
  `volk-dependencies.txt`, `gnuradio-dependencies.txt`) and revised the
  GNU Radio installer (only checks `uhd-dependencies.txt` exists;
  `--branch`, default `main`, with `git checkout` after the clone; cmake /
  make / make test tee'd to logs like UHD). Dry-run tested; README and this
  file updated. See Next step 11.
- 2026-10-02: Real test of the revised GNU Radio installer on the LENOVO
  (`sudo python3 gnuradio_bare_metal_installer.py --branch main`, after
  removing the source-built Volk from `/usr/local` and moving `~/gnuradio`
  to `~/gnuradio.old`): no errors. `make_test.log`: 100% of 266 tests
  passed (128 s), without `xvfb`. cmake found Volk via `Volk::volk`;
  `libgnuradio-runtime.so` links Ubuntu's `/usr/lib/x86_64-linux-gnu/
  libvolk.so.3.3` (`libvolk-dev` 3.3.0-2); no Volk left in `/usr/local`.
  Built v3.11.0.0git-1174-gaee9fd3f (`main` unchanged since 2026-08-28);
  same 32 enabled components as before. `~/gnuradio`, `build/`, and the
  three logs owned by barry; root-owned files only inside `build/`.
  Added these results to `README.md`'s "Tested builds" (commit `55551aa`).
- 2026-10-03: Clean-install test of the `main` scripts on the GMKtec,
  freshly loaded with **Ubuntu 26.04.1** from scratch (not 24.04, and not
  the uninstall route): `wget` the two scripts from `main`, then
  `sudo ... uhd --build` and `sudo ... gnuradio --branch main`. No errors;
  UHD 109/109 and GNU Radio 266/266 tests passed; GNU Radio
  v3.11.0.0git-1174-gaee9fd3f; enabled components identical to the
  LENOVO's (same 32, still no `gr-qtgui`/`gr-soapy`/`gr-iio`/JACK/
  PortAudio). The `main` scripts are untested on 24.04. Added to README
  "Tested builds". Then tagged **`v1.1`** (user's choice of name), updated
  the local wiki draft for `v1.1`, and switched README's download section
  to `v1.1` (commit `2149651`).
- 2026-10-03: **GNU Radio's own dependencies solved for `maint-3.10`.**
  The user focused on `maint-3.10` (Qt5) and supplied the wiki's manual
  dependency lines (46 packages for 3.8 + 3.9 + 3.10). Findings: the
  LENOVO's `cmake.log` showed `gr-iio` (no `libiio`), `gr-soapy` (no
  SoapySDR), `gr-qtgui` (no Qt6/PyQt6/Qwt-Qt6 on `main`) disabled and
  JACK/PortAudio not found. The Ettus Dockerfile's "Install GNURadio
  dependencies" block is only 22 packages for Ettus's own testing (and
  stale: `liblog4cpp5-dev`). Ubuntu's `gnuradio` package `Build-Depends`
  (what `apt-get build-dep gnuradio` and GNU Radio's 24.04 CI image use) is
  the authoritative list for 3.10. Of the 46 manual packages: 31 are on
  that list, 10 only on the Ettus list, 2 come in as dependencies (`g++`,
  `libusb-1.0-0`), 3 uncovered: `python3-matplotlib` and `soapysdr-tools`
  (added as extras) and `swig` (3.8-only, dropped). Rewrote the GNU Radio
  installer to fetch/parse/install that list and made `maint-3.10` the
  default branch.
- 2026-10-03: Real run on the LENOVO (`sudo python3
  gnuradio_bare_metal_installer.py`, default `maint-3.10`, after removing
  the installed 3.11 via `install_manifest.txt`): compiled fine on 26.04;
  cmake listed **no disabled components**; first `make test` 268/269 —
  `grc_tests` failed because the manifest removal left 67 *empty*
  directories under `/usr/local/lib/python3.14/dist-packages/gnuradio`,
  which Python imports as empty namespace packages
  (`gnuradio.grc.workflows.python_nogui` has no attribute
  `PythonNoGuiGenerator`), defeating GNU Radio's ModuleNotFoundError
  fallback in `grc/core/generator/Generator.py`. After `sudo rm -rf` of the
  empty dirs (also `/usr/local/include/gnuradio`, `share/gnuradio`,
  `lib/cmake/gnuradio`, `share/doc/gnuradio-3.11.0git`) and re-running
  `make test`, `sudo make install`, `sudo ldconfig` by hand: **269/269**,
  GNU Radio **3.10.12.0** (v3.10.12.0-92-gc1a73dc34), **42 enabled
  components** (was 32): adds `gr-qtgui`, `gr-iio` + `libad9361`,
  `gr-soapy`, JACK, PortAudio, Thrift, codec2/freedv/gsm. `from gnuradio
  import qtgui, iio, soapy, uhd, audio` works with no env vars. Added the
  leftover-directory check to the installer; rewrote README; updated the
  local wiki draft. `~/gnuradio.main` and `~/gnuradio.old` were old build
  trees on the LENOVO (deleted by the user 2026-10-04).
- 2026-10-04: **Clean Ubuntu 24.04 test on the GMKtec** (reloaded from
  scratch; two scripts from `main` at `00db21e`): no errors. UHD 109/109
  tests; GNU Radio 268/268 (one fewer test than the LENOVO's 269 on 26.04 —
  not a failure; commit not reported, presumably a test that 24.04 doesn't
  register); GNU Radio 3.10.12.0; 42 enabled components, identical to the
  LENOVO's. UHD's `cmake.log` lists "B300" (needs NI's `nib310rio-dev`, only
  in the Ettus PPA; B200/B210 is separate and enabled) and "RFNoC/FPGA
  Development Files" (off by default) as disabled on both machines —
  expected. Still untested: a clean 26.04 install with the current scripts.
  Then tagged **`v1.2`** (commit `b4327fa`) and pointed README's download
  links at it. Verified: `v1.0`, `v1.1`, and `v1.2` raw links all respond;
  the two `v1.2` scripts downloaded into an empty directory run
  (`--list-only`, GNU Radio `--dry-run`: 66 packages, `maint-3.10`).
  Afterwards added an overview and quick start to the top of `README.md`
  (commit `65d333c`, after the tag, so `v1.2`'s own README lacks it; the
  scripts are unchanged).
- 2026-10-04: The user revised the live wiki page for `v1.2`, added an
  introduction, copied the page text into
  `wiki-draft-download-section.txt`, and asked the GNU Radio developers and
  documentation people to review it. Explained how to create a GitHub
  Release; the user is waiting for the reviewers' comments first. Reviewed
  the introduction and gave four comments (see Next step 12). At the user's
  request, applied the first (the Notes list's MediaWiki formatting) to the
  local file; the user made the same edit on the live page and confirmed
  it looks good.
- 2026-10-08: The user reloaded the LENOVO with a fresh Ubuntu 26.04 and
  tried their own Phase 2 plan by hand: "Source code" on, the Ettus PPA,
  `apt-get install uhd-host libuhd-dev`, `apt-get build-dep gnuradio`,
  then a fork of GNU Radio built on `main` (to fix GNU Radio issue 8218).
  The build was OOM-killed at `make -j15`; it went through with `-j7` and
  FEC / VOCODER / CTRLPORT off.
- 2026-10-09: **Phase 2 started.** From the user's manual steps, wrote
  `gnuradio_dependencies_installer.py` (Step 1) and
  `gnuradio_clone_builder.py` (Step 2), and drafted the wiki page's
  Phase 2 section. Found that the manual `apt-get install` had pulled in
  Ubuntu's own GNU Radio 3.10.12 through Recommends (unintended; hence
  `--no-install-recommends` and the conflict checks), and that the memory
  crashes came from the `make` job count (hence the memory-aware count).
- 2026-10-10: **Phase 2 tested and released.** Clean Ubuntu 26.04 on the
  GMKtec, `main`: UHD 4.11.0.0-0ubuntu1~resolute3 (PPA), GNU Radio
  v3.11.0.0git-1193-g0403558f, 271/271 tests. Tagged **`v2.0`** (commit
  `1f8711c`); README updated for Phase 2. The user replaced the whole live
  wiki page, Phase 2 before Phase 1. Created GitHub Releases for `v2.0`
  (Latest) and, the `v1.2` review having brought no negative comments, for
  `v1.2`. Then the user tested `v2.0` on the 24.04 laptop with a plain
  clone and `maint-3.10`: UHD 4.11.0.0-0ubuntu1~noble3, GNU Radio
  3.10.12.0, 268/268 tests, 42 components incl. `gr-qtgui`; recorded in
  README, the wiki page, and the `v2.0` Release notes. Details of all
  three days are in Next step 12.

## Key decisions

- **Parse the Dockerfile instead of hardcoding packages.** Keeps the
  dependency list in sync with upstream automatically rather than needing
  manual updates every time Ettus changes their Dockerfile.
- **Auto-detect OS, abort if unsupported** rather than defaulting to Ubuntu
  26.04 or guessing at a close match — avoids silently installing a wrong
  package set on an unsupported OS.
- **`--build` is opt-in and separate from dependency installation** — the
  Dockerfile itself only sets up the build environment, so building UHD from
  source is treated as an additional, explicit step (matches the Dockerfile's
  own scope).
- **Build as the normal user, even under sudo** (2026-09-26): the shared
  `run_build_steps()` runs every step not starting with `sudo` as
  `$SUDO_USER` (uid/gid/groups + `HOME`/`USER`/`LOGNAME`) when the script
  runs as root via sudo, so `~/uhd`, `~/gnuradio` (and `~/volk` in `v1.0`) aren't
  root-owned. `sudo` steps run as root. Real root (no `SUDO_USER`) builds as
  root. The dependency lists are written via the shared
  `write_package_list()`, which chowns them to `$SUDO_USER` under sudo (a
  newly created root-owned list would break a later non-sudo run). Still
  expected and harmless: `sudo make install` leaves a few root-owned files
  in each `build/` dir (`install_manifest.txt`, CMake `compiler_depend.*`;
  for UHD, ~417 files incl. `python/usrp_mpm/*` and `utils/rfnoc-newmod/`
  that `make install` generates), with or without starting the script via
  sudo — never outside `build/`. Confirmed by a real `sudo ... --build` run
  on the LENOVO 2026-10-02. `uhd_find_devices` now runs as the
  user *before* the udev rules are installed, so it couldn't see a USB USRP
  on a first build — irrelevant, since that call only checks that the
  freshly built UHD runs; no device is plugged in at that point (user
  confirmed 2026-09-26). Keep it where it is. `~/uhd` and `~/gnuradio` on
  the 26.04 machine were root-owned from builds before this change; fixed
  2026-09-26 with `sudo chown -R barry:barry ~/uhd ~/gnuradio`.
- **GNU Radio installer only checks that `uhd-dependencies.txt` exists**
  (user, 2026-10-02) — replaced the uhd → volk → gnuradio content and
  mtime-order cross-checks (and their re-run/fresh-clone ordering
  workarounds), which are gone along with the Volk installer.
- **GNU Radio's dependencies come from Ubuntu's `gnuradio` package
  `Build-Depends`** (2026-10-03), fetched per release from Launchpad, minus
  a skip list, plus a few run-time extras — same "parse upstream's list"
  idea as the Ettus Dockerfile, and it tracks each Ubuntu release, so the
  wiki's hand-maintained package lines can go. Fits `maint-3.10`/Qt5 only;
  works for Ubuntu releases whose `gnuradio` package is 3.10 (22.04+;
  20.04 ships 3.8). The UHD installer must still run first (the list
  relies on the Ettus list for basics like `git`, and `gr-uhd` needs UHD).
- **Default GNU Radio branch is `maint-3.10`** (user, 2026-10-03), the
  released Qt5 series; `--branch main` remains for 3.11 development.
- **Removing an install needs two steps:** `xargs rm -f <
  install_manifest.txt` leaves empty directories, which break `grc_tests`
  on the next build (see 2026-10-03). Always also `rm -rf` the leftover
  `gnuradio` directories; the installer refuses to build while they exist.
- **Two phases** (user, 2026-10-04). **Phase 1** is the `v1.x` line: UHD
  built from source. **Phase 2** is **`v2.0`** (released 2026-10-10),
  installing UHD from the Ettus PPA (`ppa:ettusresearch/uhd`), as the main
  GNU Radio developer proposed. So the 2026-10-02 "no Ettus PPA" decision
  applies to Phase 1 only: don't add PPA support to `v1.x`. Fixes are
  tagged `v1.3` / `v2.1` etc.; tags are never moved. The earlier PPA
  evaluation is in git history, `CLAUDE.md` before commit `1036aeb`.
- **Direction: Phase 2 only; Phase 1 will be history** (user,
  2026-10-11, as an FYI — no timing or steps given yet). So don't invest
  further in the Phase 1 scripts or their docs unless asked, and write new
  material for Phase 2. Nothing has been removed: the Phase 1 scripts,
  tags, `v1.2` Release, README sections, and the wiki's Phase 1 section
  all still exist. The Phase 2 scripts import nothing from Phase 1, so
  retiring Phase 1 breaks nothing in them. **Wait on removing Phase 1
  (user, 2026-10-11): do not remove it from the README, the wiki draft,
  or the repo until the user says so.**
- **Phase 2 is two steps, for GNU Radio developers** (user, 2026-10-09):
  Step 1 installs everything with `apt-get`; Step 2 builds a clone the
  user made by hand in `$HOME` (normally their fork, to test an issue and
  make a pull request). The builder therefore never clones or switches
  branches. Phase 2 goes **before** Phase 1 on the wiki page, as the
  page's ultimate goal (user, 2026-10-10).
- **Phase 2 scripts are self-contained** — each can be downloaded and run
  alone, unlike the Phase 1 pair (the GNU Radio installer imports from the
  UHD one). Cost: duplicated helpers and `INSTALL_DIR_PATTERNS` to keep in
  sync.
- **Install the PPA's UHD with `--no-install-recommends`.** `libuhd-dev`
  recommends `gnuradio-dev` and `python3-uhd` recommends `gnuradio`, which
  would put Ubuntu's GNU Radio in `/usr` next to the source build. Both
  Phase 2 scripts also refuse to run while those packages are installed.
- **`make` jobs are limited by memory in Phase 2**: `min(nproc - 1,
  MemTotal // 2 GB)`, after an OOM kill at `-j15` on 15 GiB. The 2 GB per
  job is my estimate, not measured. Phase 1 `v1.2` still uses plain
  `nproc - 1`; the Phase 1 scripts on `main` have the same limit since
  2026-10-10 (tag `v1.3`).
- **GitHub Releases** exist for `v2.0` (Latest) and `v1.2` (created with
  `--latest=false`), each with its scripts attached as they are at the
  tag; `v1.0`, `v1.1`, and `v1.3` are tags only (`v1.3` by the user's
  decision, 2026-10-11).
- **Any build-step failure stops the automated build** (user,
  2026-10-02), including `cmake`, `make`, and a failing `make test` unit
  test (so a failing build is never installed). The user's manual wiki
  commands (`cmd 2>&1 | tee log`) ran one at a time with the user deciding
  what to do next; the script checks each command's own exit status
  (a shell `| tee` without `pipefail` would mask it). Only
  `uhd_find_devices` is tolerated.
- **`uhd_find_devices` failure is tolerated, not fatal**, during `--build`,
  since a non-zero exit there just means no USRP hardware is attached, not a
  build failure.
- **Distribute the scripts via tag-pinned raw GitHub links** (2026-09-26)
  so wiki readers needn't clone the repo:
  `https://raw.githubusercontent.com/duggabe/gr-wiki-revision/<tag>/<script>`.
  Link a tag, not `main`, so pushes don't change what readers run (often
  with sudo). The GNU Radio script imports from the UHD script (and in
  `v1.0`, the Volk script too), so readers must download them into one
  directory (also where `uhd-dependencies.txt` lands) — chosen over making
  each script self-contained or merging them into one. Tell readers to download then
  run, never pipe into `sudo python3`.
- **`gr-wiki-revision` is the target repo; `~/AIwork` was the trial.**
  The feasibility work from `~/AIwork` was pushed into this existing repo
  (on explicit instruction) rather than a new one, and its original
  `README.md` was merged in rather than overwritten. The repo's name and
  description (GNU Radio wiki support) fit its purpose (clarified by the
  user 2026-09-26).

## Next steps

1. ~~Reconcile `uhd-dependencies.txt` with
   `uhd-ubuntu2604-dependencies.txt` / `install-uhd-build-deps.sh`~~ — done
   2026-09-25: the extra packages (`clang-format-14`, `swig`) and duplicates
   (`libgps-dev`, `python3-ruamel.yaml`) came from an older upstream
   Dockerfile, not a parsing bug. A fresh fetch dropped them (and added
   `python3-setuptools`), making the lists identical; the bash script
   needed no change.
2. ~~Confirm `uhd_bare_metal_installer.py`'s OS auto-detection~~ — done:
   works on 26.04 (LENOVO, 2026-09-25) and 24.04 (tested on the laptop;
   also checked 2026-09-26 by simulating a 24.04 `/etc/os-release`, which
   picks `uhd-builder-ubuntu2404.Dockerfile`, 60 packages). The earlier
   belief that no 24.04 Dockerfile existed upstream was wrong.
3. ~~Turn this directory into a git repo and push to GitHub~~ — done:
   pushed to https://github.com/duggabe/gr-wiki-revision.
4. ~~**Finish migrating to LENOVO**~~ — done: all work since 2026-09-25 has
   been on the LENOVO desktop in `~/gr-wiki-revision`; the laptop's
   `~/AIwork` is historical only. Original steps: install `git`, `gh`, Claude Code; `gh auth login`; set
   git identity (`duggabe` / `barry@dcsmail.net`); `gh repo clone
   duggabe/gr-wiki-revision` (clones to `~/gr-wiki-revision` by default —
   that's the working directory on LENOVO, not `AIwork`). Session-history
   continuity (`~/.claude/projects/`, see `AI_notes.txt` step 8 in
   git history) won't carry
   over automatically since the directory name is changing; rely on this
   file for context on LENOVO instead.
5. ~~Run/validate `uhd_bare_metal_installer.py --build` end-to-end on the
   Ubuntu 26.04 test machine~~ — done 2026-09-25: UHD 4.11.0.0-0-g0d7ed3b1,
   then Volk 3.3.0 and GNU Radio v3.11.0.0git-1174-gaee9fd3f via their
   installers — all three match the original machine's build.
6. ~~Run `volk_bare_metal_installer.py` for real on the 26.04 machine~~ —
   done 2026-09-25: installed Volk 3.3.0. ~~Run
   `gnuradio_bare_metal_installer.py` for real~~ — done 2026-09-25:
   installed GNU Radio v3.11.0.0git-1174-gaee9fd3f, matching the original
   machine.
7. ~~Repo visibility~~ — done: confirmed 2026-09-24 to leave public. (The
   name and description aren't a mismatch — see Key decisions.)
8. **GNU Radio's own dependencies and branch choice — resolved for
   `maint-3.10` on 2026-10-03** (dependency step + default branch; see
   What's been done). **Still open: `--branch main` (Qt6)**, whose
   `gr-qtgui` needs `qt6-base-dev`, `python3-pyqt6`, and Qwt ≥ 6.2 built
   from source for Qt6 (not packaged on 24.04/26.04; untested), and stating
   the supported Ubuntu releases on the wiki page. The notes below are the
   2026-09-27 background. Per `gnuradio-config-info --enabled-components` (identical
   on the LENOVO and the GMKtec), the installers' build lacks `gr-qtgui`,
   `gr-soapy`, `gr-iio`, and the JACK/PortAudio audio back-ends.

   **Key finding — which branch is built:** `gnuradio_bare_metal_installer.py`
   does a plain `git clone`, i.e. the default branch `main` = 3.11.0git
   (development, pre-release). Its `gr-qtgui` requires **Qt6**. The released
   series is `maint-3.10` (3.10.12.x), whose `gr-qtgui` requires **Qt5**.
   The user's impression (to confirm with the developers): released GNU Radio
   through 3.10.12 is Qt5 only on 24.04. Two paths:
   - **Build `maint-3.10` (Qt5).** Everything `gr-qtgui` needs is packaged on
     24.04 and 26.04 (Qt5, PyQt5, `libqwt-qt5-dev`); the existing
     UbuntuInstall#Install_Dependencies list (24.04, Qt5) fits. Installer
     change: clone with `--branch maint-3.10` (or a release tag) plus a
     GNU Radio dependency-install step.
   - **Build `main` (Qt6).** Needs the Qt6 package list plus **Qwt 6.3 built
     from source against Qt6**: Launchpad shows `libqwt-qt6-dev` only in
     Ubuntu 26.10 ("stonking", Qwt 6.3.0); 24.04 (noble) and 26.04
     (resolute) have Qwt 6.1.4 for Qt5 only.
   - Middle option: a `--branch` option on the GNU Radio installer (page uses
     the release; `main` still buildable for testing).

   **GNU Radio's CI Dockerfiles** are in `gnuradio/gnuradio-docker` under
   `ci/`. `ci-ubuntu-24.04-3.10` has no package list (just `apt-get build-dep
   gnuradio`, i.e. Ubuntu's packaged 3.10/Qt5 deps), so it can't be parsed.
   `ci-ubuntu-26.10-3.11` (and `ci-debian-14-3.11`) list their packages
   explicitly (69 in 26.10's build + Python blocks) and could be parsed like
   the Ettus Dockerfile for the `main`/Qt6 path. Every package on the 26.10
   list exists on 26.04 (checked with apt; `libqt6opengl6-dev` /
   `libqt6svg6-dev` / `debhelper-compat` are virtual, provided by
   `qt6-base-dev` / `qt6-svg-dev` / `debhelper`) and on 24.04 (checked the
   key ones via Launchpad: Qt 6.4.2, PyQt6 6.6.1, SoapySDR, IIO, JACK,
   PortAudio), except `libqwt-qt6-dev`. If used, exclude `libuhd-dev` and
   `libvolk-dev` (UHD/Volk are built from source into `/usr/local`; distro
   copies in `/usr` could be picked up by cmake — but see step 11: with Volk
   no longer built, `libvolk-dev` should be *installed* instead) and the packaging/docs/test
   tools (`debhelper-compat`, `dh-python`, `graphviz`, `xmlto`,
   `libjs-mathjax`, `python3-pytest`).

   **UHD from the Ettus PPA — not in Phase 1 (2026-10-02); planned for
   Phase 2, `v2.0`** (see Key decisions).

   **Install prefix: keep `/usr/local` (recommended 2026-09-27).** Checked on
   the LENOVO in a clean environment (no `LD_LIBRARY_PATH`/`PYTHONPATH`):
   Ubuntu's `/etc/ld.so.conf.d` already lists `/usr/local/lib`, so
   `ldconfig` finds libuhd/libvolk/libgnuradio; `uhd_find_devices` runs;
   GNU Radio's Python (`/usr/local/lib/python3.14/dist-packages`) imports
   fine, incl. `from gnuradio import uhd`. Only UHD's own Python API fails
   (`import uhd`: installed to `.../site-packages`, which Debian/Ubuntu
   Python doesn't search). With UHD staying a source build, `import uhd`
   needs `PYTHONPATH` (documented in README; a UHD CMake option to install
   into `dist-packages` might avoid it — not yet checked). The wiki's
   `LD_LIBRARY_PATH` step isn't needed for these libs. `/usr` was rejected: it's apt-managed
   (untracked `make install` files can be overwritten or break packages),
   Volk would collide with Ubuntu's `libvolk` in `/usr/lib/x86_64-linux-gnu`,
   removal is harder, and `/usr/local` is the from-source convention.

   **Waiting on the user**, who is asking the GNU Radio developers (a) which
   branch a from-source wiki page for 24.04/26.04 should build (`maint-3.10`
   or `main`) and (b) for `main`, how Qwt for Qt6 should be provided. Then:
   add the GNU Radio dependency step (needs sudo) and branch handling, a
   Qwt-from-source installer if needed, and/or print the enabled components
   at the end of the GNU Radio installer; update the wiki page to match and
   tag a new release.

   Also add to the wiki page (independent of the Qwt answer): which Ubuntu
   releases are supported — 24.04 and 26.04 tested; the installers work
   wherever Ettus has a matching Dockerfile. The README already says this,
   but wiki readers may never see the README.
9. ~~Publish the scripts for the wiki page~~ — done 2026-09-26: tag `v1.0`
   created and the page's raw links point at it; the page is live and
   tested (step 10). For fixes, tag `v1.1` etc. rather than moving `v1.0`.
   The page's Qt GUI warning or GNU Radio dependency step is now part of
   step 8.
10. ~~Create the "Building GNU Radio from Source Code" wiki page from
    `wiki-draft-download-section.txt` and test it on the GMKtec (clean
    Ubuntu 24.04)~~ — done 2026-09-26: the user followed only the new page
    and "everything went perfectly". `gnuradio-config-info
    --enabled-components` on the GMKtec is identical to the LENOVO's (same
    32 components; `gr-qtgui`, `gr-soapy`, `gr-iio`, JACK, PortAudio
    missing on both), so step 8 is the remaining gap on 24.04 too.
11. ~~**Volk removed; GNU Radio installer revised**~~ — done 2026-10-02,
    released as `v1.1`, then superseded by the `v1.2` dependency step (see
    step 12). The notes below are the 2026-10-02/03 record. Deleted the Volk installer and the volk/gnuradio
    lists; rewrote the GNU Radio installer (existence check, `--branch`,
    logged cmake/make/make test). Updated README ("Changes since v1.0", a
    two-script "Run the installers in order", a "Volk" subsection, rewritten
    GNU Radio section; Volk sections removed). **Open:**
    - **Where Volk comes from.** GNU Radio `main` needs an external Volk
      ≥ 2.4.1 (`gr_find_package(Volk)`, `VOLK_MIN_VERSION` in
      `cmake/Modules/GrMinReq.cmake`); nothing installs it now, so a clean
      machine would fail at GNU Radio's cmake. Ubuntu's `libvolk-dev`
      (3.1.2 on 24.04, 3.3.0 on 26.04) satisfies it — reverses the step-8
      exclusion of `libvolk-dev`. **Decided (user, 2026-10-02):** the GNU
      Radio installer's first build step runs `sudo apt-get install -y
      libvolk-dev`, before `git clone`.
    - LENOVO and GMKtec have source-built Volk 3.3.0 in `/usr/local`, which
      GNU Radio's cmake would find before Ubuntu's in `/usr` (and which
      would mask the clean-machine problem). Remove it first:
      `cd ~/volk/build && sudo xargs rm -f < install_manifest.txt && sudo
      ldconfig`.
    - ~~GNU Radio's `make test` might fail without `xvfb`~~ — all 266
      passed on the LENOVO with `--branch main` (2026-10-02).
    - ~~First real run~~ — done for `--branch main` on the LENOVO
      (2026-10-02) and on the GMKtec with a fresh Ubuntu 26.04.1 install
      (2026-10-03; all tests passed on both). Still to try: Ubuntu 24.04
      and `--branch maint-3.10`.
    - **Tagged `v1.1`** (user, 2026-10-03; I'd suggested `v2.0` since the
      changes break `v1.0`'s instructions, but the user chose `v1.1` while
      still researching GNU Radio's missing dependencies). `v1.1` has two
      scripts (no Volk). The wiki page still links `v1.0`; switching it to
      `v1.1` (and updating the local draft to two scripts) is the user's
      call.
    - `v1.0` and the current wiki links stay unchanged. (The local wiki
      draft has since been rewritten for `v1.2`.)
12. **Record of 2026-10-04 to 2026-10-10** (all done except where step 13
    says otherwise):
    - ~~Clean-install test and a 24.04 test~~ — done 2026-10-04 on the
      GMKtec (fresh 24.04, all tests passed, 42 components). Optional: a
      clean 26.04 install with the current scripts.
    - ~~Tag `v1.2`~~ — done 2026-10-04 (user's go-ahead; for fixes tag
      `v1.3` etc. rather than moving a tag).
    - ~~Update the wiki page to `v1.2`~~ — done 2026-10-04 by the user,
      who added an introduction and asked the GNU Radio developers and
      documentation people to review the page. Outcome (2026-10-10): no
      negative comments.
    - ~~GitHub Release (after the review)~~ — done 2026-10-10 for `v2.0`
      and `v1.2` (see below). Process
      explained to the user 2026-10-04: write release notes, then
      `gh release create <tag> --title ... --notes-file ...`, optionally
      attaching the two scripts as they are at that tag. The user chose to
      wait for the reviewers' comments so the Release is built on whichever
      version the reviewed page ends up using.
    - My review comments on the user's introduction (given 2026-10-04):
      (1) ~~the Notes lines start with spaces then `*`, which MediaWiki
      renders as preformatted text with literal asterisks rather than
      bullets~~ — fixed 2026-10-04 in the local file and, by the user, on
      the live page (wiki-markup bullets, `'''` bold, README as a named
      link). Comments 2–4 are not yet acted on: (2) scenario (a), "your
      distribution does not support GNU Radio", doesn't fit a page that
      only works on Ubuntu 24.04/26.04, which both package GNU Radio;
      (3) scenario (b), developers: the script always clones fresh from
      `gnuradio/gnuradio` and stops if `~/gnuradio` exists, so it is a
      first-time setup (later rebuilds are manual in `~/gnuradio/build`),
      and developers mostly use `main`, which this path builds without
      `gr-qtgui`; (4) the README link points at `main`, not `v1.2`.
    - **Phase 2: `v2.0`, UHD from the Ettus PPA — started 2026-10-09**
      (see Key decisions). The user's plan is **two steps**: Step 1 is
      completely different from Phase 1, Step 2 is similar to it.
      - **Step 1 = `gnuradio_dependencies_installer.py`** (written
        2026-10-09, self-contained; first real runs 2026-10-10, see
        below). From the user's manual steps
        (tried on the LENOVO, reloaded with a fresh 26.04 on 2026-10-08):
        enable "Source code" (`Types: deb` → `Types: deb deb-src` in
        `/etc/apt/sources.list.d/ubuntu.sources`, backup `.bak`; replaces
        the "Software & Updates" GUI steps) → `apt-get update` →
        `apt-get install -y software-properties-common git` →
        `add-apt-repository -y ppa:ettusresearch/uhd` → `apt-get install -y
        --no-install-recommends uhd-host libuhd-dev` → `apt-get build-dep -y
        gnuradio` → the four run-time extras (`python3-qtpy`,
        `python3-pyqtgraph`, `python3-matplotlib`, `soapysdr-tools`) →
        `uhd_images_downloader`. Aborts first if Ubuntu's `gnuradio` /
        `gnuradio-dev` packages are installed or a source-built UHD is in
        `/usr/local`. Options: `--dry-run`, `-y`, `--no-images`,
        `--sources-path`, `--os-release-path`.
      - **Why `--no-install-recommends`:** `libuhd-dev` recommends
        `gnuradio-dev` and `python3-uhd` recommends `gnuradio`. The user's
        manual `apt-get install -y uhd-host libuhd-dev` put Ubuntu's GNU
        Radio 3.10.12 in `/usr` next to the source build (unintended).
        Step 1 refuses to run until `sudo apt-get remove gnuradio
        gnuradio-dev` (done on the LENOVO 2026-10-10). `autoremove` before
        Step 1 would have taken 82 packages, including
        `python3-matplotlib`, `python3-pyqtgraph`, `soapysdr-tools`.
      - `uhd-host` installs the udev rules itself
        (`/usr/lib/udev/rules.d/60-uhd-host.rules`); `python3-uhd` makes
        `import uhd` work without `PYTHONPATH`.
      - **Step 2 is for a GNU Radio code developer** testing an issue and
        making a pull request (user, 2026-10-09), from the commands the
        user used to fix issue 8218: fork → clone the fork to `~/gnuradio`
        → branch → cmake / make / make test (tee'd) → `sudo make install`
        → `sudo ldconfig`, on `main`. The user clones the fork into `$HOME`
        by hand, "then we work on that" (user, 2026-10-09 — I took this as
        confirming a build script for the existing clone).
      - **Step 2 script = `gnuradio_clone_builder.py`** (written
        2026-10-09, self-contained: carries a trimmed copy of the Phase 1
        `BuildStep` / `run_build_steps()` / `run_logged()` /
        `get_build_user()` helpers and of `INSTALL_DIR_PATTERNS` — keep that
        list in sync with the Phase 1 installer). Builds whatever is
        checked out in `~/gnuradio` (`--source-dir`); never clones or
        changes branches; reuses an existing `build/`, so it serves the
        edit → rebuild loop. Steps: `mkdir build` (first time) or `sudo
        chown -R` the build dir back to the user if `sudo make install`
        left root-owned files (149 on the LENOVO) → cmake / make / make
        test, tee'd to logs → `sudo make install` → `sudo ldconfig`.
        Aborts if the directory isn't GNU Radio source, `libuhd-dev` isn't
        installed, Ubuntu's `gnuradio` packages are installed, or stale
        install dirs exist. Options: `--source-dir`, `--jobs`,
        `--cmake-args`, `--no-install`, `--dry-run`, `-y`. Tested first by
        dry-run on `~/gnuradio` and a real `--no-install` run on a tiny
        fake CMake project (passing and failing test); real GNU Radio
        builds 2026-10-10, see below.
      - **Make jobs are limited by memory** (2026-10-09). The user's
        manual `main` build on the LENOVO (16 cores, 15 GiB RAM, 4 GB swap)
        was OOM-killed at `make -j15` (kernel log 2026-10-08 10:44:
        `cc1plus invoked oom-killer`); they worked around it with `-j7`,
        no `tee` on make, and `ENABLE_GR_FEC` / `ENABLE_GR_VOCODER` /
        `ENABLE_GR_CTRLPORT` (+ `ENABLE_CTRLPORT_THRIFT`) `=OFF` — still OFF
        in `~/gnuradio/build/CMakeCache.txt`, so cmake keeps them off there
        until set `=ON` or `build/` is removed. The job count is the cause;
        `tee` is not. `gnuradio_clone_builder.py` uses `min(nproc - 1,
        MemTotal // 2 GB)` (7 on the LENOVO; the 2 GB per job is my
        estimate, not measured) and has `--jobs` and `--cmake-args="..."`.
        **The Phase 1 `v1.2` scripts still use plain `nproc - 1`** and
        could hit the same on a many-core, low-memory machine — a possible
        `v1.3` fix, not made.
      - **Wiki draft** (`wiki-draft-download-section.txt`): the user
        rewrote the intro for two phases (Phase 1 text now under
        `== Phase 1 ==`); I drafted `== Phase 2 ==` on 2026-10-09:
        downloading both scripts, before you start, Step 1, Step 2 (fork,
        clone, `upstream` remote, `git checkout -b <branch> upstream/main`,
        the builder script, then `git commit -s` → push → PR), checking the
        result. Dropped the user's copy of `60-uhd-host.rules` into
        `/etc/udev/rules.d/` (already active from `/usr/lib/udev/rules.d/`;
        a copy still sits there on the LENOVO). The download links use tag
        `v2.0`. A `main` build has no
        `gr-qtgui` (Qt6/Qwt), as in Phase 1.
      - **2026-10-10: first real runs.** The user reported "everything
        worked! 100% tests passed, 0 tests failed out of 271 (main)" with
        the scripts from `main` at `1f8711c`, on the **GMKtec, clean
        install of Ubuntu 26.04**: UHD 4.11.0.0-0ubuntu1~resolute3 (PPA),
        GNU Radio v3.11.0.0git-1193-g0403558f (enabled components not
        reported). Phase 2 is untested on 24.04. On the LENOVO the same day:
        `apt-get remove gnuradio gnuradio-dev` done and Step 1 run for
        real (extras incl. `python3-qtpy` installed; deb-src was already
        on, so no `.bak`; no images in `/usr/share/uhd/images`), but
        Step 2 has not been run there (`/usr/local` still has
        3.11.0git-1193, no logs in `~/gnuradio/build`). `gh` installed and
        logged in on the LENOVO; `main` pushed.
      - **Tagged `v2.0`** at `1f8711c` and pushed, 2026-10-10 (user's
        go-ahead); both `v2.0` raw links verified. The local wiki draft's
        Phase 2 status line now says tested on a clean 26.04, untested on
        24.04. For fixes tag `v2.1` etc.
      - **README updated for Phase 2** 2026-10-10 (after the tag, so
        `v2.0`'s own README lacks it): two-phase intro, a `v2.0` entry in
        "Tested builds" and "Releases and changes", and a new last section
        "Phase 2: UHD from the Ettus PPA, GNU Radio from your fork"
        (download, before you start, Step 1 and Step 2 with options
        tables, memory note). Keep those tables in sync with the two
        Phase 2 scripts' argparse help.
      - 2026-10-10 (user): **Phase 2 goes before Phase 1 on the wiki
        page**, since it is the page's ultimate goal. Reordered in the
        local draft (intro unchanged, then `== Phase 2 ==`, then
        `== Phase 1 ==`).
      - 2026-10-10: **the user replaced the entire live wiki page** with
        the draft (Phase 2 first; intro now lists the Phase 2 goals first
        and "Phase 1 goals (completed)"), so the local file is again the
        user's copy of the live page. I then found my own error in it: the
        "equivalent" commands had `make -j7  # comment 2>&1 | tee
        make.log` (the comment swallowed the `tee`). Fixed locally to
        `make -j7 2>&1 | tee make.log   # ...`; the user made the same
        one-line fix on the live page (confirmed 2026-10-10).
      - **GitHub Release for `v2.0` created 2026-10-10** (the repo's
        first Release; `v1.0`–`v1.2` are still tags only):
        https://github.com/duggabe/gr-wiki-revision/releases/tag/v2.0 —
        notes cover what's new, the clean 26.04 test, a quick start, and
        known limitations; the two Phase 2 scripts as they are at the tag
        are attached.
      - **`v1.2` review outcome (user, 2026-10-10): no negative comments**
        from the GNU Radio developers and documentation people. So no
        `v1.3` is needed for the review, and the wait on a `v1.2` GitHub
        Release is over. **`v1.2` Release created 2026-10-10** (user's
        go-ahead), not marked latest so `v2.0` stays "Latest":
        https://github.com/duggabe/gr-wiki-revision/releases/tag/v1.2 —
        with the two Phase 1 scripts from the tag attached. Its notes list
        the plain `nproc - 1` make job count as a known limitation.
      - **2026-10-10: Phase 2 tested on Ubuntu 24.04** (user, on the
        laptop — not a clean install): built `maint-3.10` and got GNU Radio
        3.10.12.0, `make test` 268 of 268 passed (same count as Phase 1
        on 24.04); UHD 4.11.0.0-0ubuntu1~noble3 from the PPA; the `v2.0`-tag
        scripts were used. `--enabled-components` lists 42 components, the
        same number as Phase 1 `v1.2`, incl. `gr-qtgui`, `gr-iio` +
        `libad9361`, `gr-soapy`, `gr-uhd` + RFNoC, JACK, PortAudio, Thrift,
        codec2/freedv/gsm — so Phase 2 with `maint-3.10` gives the full
        Qt5 build. The user did not fork for this test: a plain `git clone
        https://github.com/gnuradio/gnuradio`, then `git checkout
        maint-3.10`. The local wiki draft has a paragraph saying so after
        the `main`/`gr-qtgui` note. The user updated the live wiki page the
        same day (user's report; exact live wording not seen). The `v2.0`
        GitHub Release notes were edited the same day (user's request):
        the "Tested" section has a second table for this 24.04 run in
        place of "not yet tested on Ubuntu 24.04", and the `gr-qtgui`
        limitation adds that a `maint-3.10` build includes it. Tag, title,
        and attached scripts unchanged. README "Tested builds" and the local wiki draft's
        status line updated.
    - (`~/gnuradio.main` and `~/gnuradio.old` on the LENOVO were deleted
      2026-10-04.)
13. **Next (as of 2026-10-11).** Direction (user, 2026-10-11): moving
    toward Phase 2 only, Phase 1 becoming history (see Key decisions) —
    which makes the `v1.3` items below low priority. Open:
    - 2026-10-11: the user pointed out that the wiki's Phase 1 section
      "Rebuilding, or replacing an earlier install" told readers to remove
      `~/gnuradio` and then use `~/gnuradio/build/install_manifest.txt`
      (my wording). Rewritten in the local draft and README as three
      ordered steps (manifest removal → leftover directories → only then
      remove/rename the source directory). At the user's request, added a
      Phase 2 counterpart without Volk or UHD, "Changing branches, or
      removing the installed GNU Radio" (end of Step 2; last step is
      `sudo rm -rf ~/gnuradio/build`, the source is kept), in the draft
      and README. Removing `build/` when changing branches is my
      recommendation, untested.
    - 2026-10-11 (user's request): made Phase 2 stand-alone in the README
      (see Files) and in the local wiki draft, so Phase 1 is easy to
      remove from both. In the draft, Phase 2's "Before you start" no
      longer names Phase 1 and links to Phase 2's own removal section
      instead of Phase 1's; the Phase 2 section now has no references to
      Phase 1. To retire Phase 1 on the wiki: delete from `== Phase 1 ==`
      to the end, and edit the user's intro (the "two phases" sentence,
      "rather than the Phase 1 methods", the "Phase 1 goals" list).
    - 2026-10-11: the user updated the live wiki page from the local
      draft "with no changes" — which I take to mean the draft's text was
      used as it is, so the local file again matches the live page
      (Phase 1 "Rebuilding" fix, the new Phase 2 removal section, and the
      two "Before you start" bullets).
    - 2026-10-11: **result from the other tester** (via the user; run
      that day, user confirmed): "100%
      tests passed, 0 tests failed out of 267", on a clean install of
      Ubuntu "24.04.5.1" (as the user reported it), with the **`v2.0`
      scripts, `main` branch**. This fills two gaps: a clean 24.04
      install with Phase 2, and `main` on 24.04. Not reported: machine,
      UHD and GNU Radio versions, enabled components. 267 on 24.04 vs 271
      for `main` on 26.04 (-1193) is unexplained (commit and components
      unknown; `maint-3.10` also has one test fewer on 24.04). Added to
      README "Phase 2 tested builds" and the local wiki draft's status
      line. The `v2.0` Release notes got a line for this run in their
      "Tested" section the same day (user's request). The user updated
      the live page's status line the same day (user's report; exact
      wording not seen).
    - `v1.3`: the user will reload the GMKtec with 26.04 and test it
      there (4 cores, 10 GiB → `-j3`, same as `v1.2`, so a regression
      test only); another tester is using a different computer (what
      they test is not known). **Decided (user, 2026-10-11): keep the
      `v1.3` tag, but no GitHub Release for it.**
    - ~~Step 2 on the LENOVO~~ — **done 2026-10-11 (user), as a rebuild
      in the existing build directory** (the user's choice: the machine
      took a lot of work to set up, so nothing was removed first).
      `sudo python3 gnuradio_clone_builder.py` on the fork, branch
      `issue8218` (one commit ahead of `main`): the `sudo chown -R` of the
      root-owned build files worked (first real use), `make -j7`,
      **247 of 247 tests passed**, installed
      v3.11.0.0git-1194-gb0937160; the three logs are owned by barry.
      FEC / VOCODER / CTRLPORT are still off from the old CMake cache
      (so is `gr-dtv`, which needs FEC, and `gr-qtgui` as on any `main`
      build) — hence 247 tests, not 271. This was an incremental build,
      so it did not exercise the memory limit under a full compile.
      **Finding:** installing over the earlier build left its 18
      versioned libraries (`libgnuradio-*.so.v3.11.0.0git-1193-g0403558f`,
      14 MB) in `/usr/local/lib`: the version string is in the file name
      and changes with every commit, and the new `install_manifest.txt`
      does not list the old files. Harmless (the `.so.3.11.0git` links
      point at the new ones), but it means the docs' "the new install
      replaces the old one" is not quite true, and such files pile up
      over an edit → commit → rebuild loop. Added 2026-10-11 (user's
      request) to the README and the local wiki draft, at the end of the
      Phase 2 "Changing branches..." section: a "Libraries left by
      earlier builds" paragraph with commands to list and remove them
      (the listing was checked on the LENOVO: 18 old files; the `rm` was
      not run), and "replaces the old one" reworded. Seen on `main` only;
      not checked on `maint-3.10`. **The live page still needs it.** As always, `sudo make install` left root-owned
      files in `build/` again (147). Still on the LENOVO: the unneeded
      `/etc/udev/rules.d/60-uhd-host.rules` copy; `sudo apt autoremove`
      not run. A full from-scratch build there (the wiki's "Changing
      branches..." steps, incl. my untested `rm -rf build`) has not been
      done.
    - **Memory-aware `make` jobs in the Phase 1 scripts — written
      2026-10-10 (user's request), on `main`, not tagged.** The shared
      `get_make_jobs()` in `uhd_bare_metal_installer.py` (imported by the
      GNU Radio installer) now matches the Phase 2 builder: `min(nproc -
      1, MemTotal // 2 GB)`, at least 1, with `MEMORY_PER_JOB_KB` and
      `get_total_memory_kb()`. No `--jobs` option was added. It applies to
      the UHD build too, which had built fine at `-j15` on the LENOVO's
      15 GiB, so UHD now builds there at `-j7` (slower, not needed for
      UHD). Checked against the Phase 2 function for six core/memory
      combinations and by dry-run of both installers (`make -j7` on the
      LENOVO); **no real build with it yet**. README notes it under
      "Releases and changes". **Tagged `v1.3`** at `6d49f95` on
      2026-10-10 (user's request). README's and the wiki's Phase 1 links
      still point at `v1.2` — my recommendation is to switch them only
      after a real build with `v1.3`; no GitHub Release for it yet.
    - **The `main`/Qt6 path:** `gr-qtgui` on `main` needs Qwt built from
      source for Qt6 (see step 8); applies to both phases.
    - Untested: Phase 2 with a fork on 24.04 (the tests there used plain
      clones, as far as reported); a clean 26.04 install with `v1.2`.
      (The laptop's 24.04 was not a clean install — my assumption, not
      confirmed by the user.)
    - Wiki page: my comments 2–4 on the introduction (step 12) were
      written for the Phase 1-only page and were never acted on; the two
      "Checking the result" headings share a name.
    - Minor, unresolved: which GNU Radio test accounts for 268 tests on
      24.04 vs 269 on 26.04.
