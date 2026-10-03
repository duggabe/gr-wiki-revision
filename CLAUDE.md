# gr-wiki-revision — Bare-Metal UHD / GNU Radio Build Tooling

## Project summary

Tooling to build and install Ettus Research's UHD (USRP Hardware Driver) —
plus Volk and GNU Radio — directly on bare metal (no Docker), by reusing the
dependency list from EttusResearch's own Docker build environment
(`.ci/docker/uhd-builder-ubuntu2604.Dockerfile` in the `EttusResearch/uhd`
repo on GitHub).

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
installers cover the UHD and GNU Radio build steps (Volk comes from apt),
and since 2026-10-03 the GNU Radio installer also covers
UbuntuInstall#Install_Dependencies (GNU Radio's own deps) for the Qt5-based
`maint-3.10`. The wiki's manual list is still written for Ubuntu 20.04–24.04
+ Qt5 while GNU Radio `main` moves to Qt6.
wiki.gnuradio.org is behind a Cloudflare challenge and can't be fetched
from here — ask the user to paste page content.

**Machines and Ubuntu versions:**

| Machine | Ubuntu | Role |
| --- | --- | --- |
| Laptop | 24.04 | `~/AIwork` trial; 24.04 testing, with both the bash script + the wiki's manual steps and the Python installers |
| LENOVO desktop | 26.04 | current working machine, `~/gr-wiki-revision`; 26.04 builds of UHD, Volk, GNU Radio |
| GMKtec (clean install) | 24.04, then 26.04.1 | 24.04: tested the new wiki page (`v1.0`) from scratch (2026-09-26), everything worked. Reinstalled from scratch with Ubuntu 26.04.1 for the 2026-10-03 test of the `main` scripts |

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

- **Removed 2026-10-02:** `volk_bare_metal_installer.py` and
  `volk-dependencies.txt` (still in `v1.0` and git history). Volk comes
  from Ubuntu's `libvolk-dev`, which is on the GNU Radio dependency list.

- **`LICENSE`** — Creative Commons Attribution-ShareAlike 4.0
  International (CC BY-SA 4.0), added 2026-09-24. Note that Creative
  Commons advises against its licenses for software; kept as-is by choice.

- **`README.md`** — user-facing docs (describes `main`; `v1.1` is the
  latest tag and lacks the dependency step): "Tested builds" (current
  scripts on 26.04: UHD 4.11.0.0 109/109, GNU Radio 3.10.12.0 269/269, no
  disabled components, incl. the `grc_tests` leftover-directory story;
  earlier `v1.1` and `v1.0` results; supported Ubuntu releases; "Known
  limitation": `--branch main` still lacks `gr-qtgui`, needs Qt6 + Qwt for
  Qt6); "Releases and changes" (on `main` since `v1.1`; in `v1.1`);
  "Download the installers" (`v1.1` links; swap in `main` to try the new
  changes); "Run the installers in order" with "Removing an earlier
  install" (manifest removal, then delete the leftover empty directories,
  and the old source-built Volk); "Environment variables"; UHD usage
  section; GNU Radio usage section with "GNU Radio's dependencies", options
  table, examples. Keep its options tables in sync with the scripts'
  argparse help.

- **`wiki-draft-download-section.txt`** — local-only (in `.gitignore`, so
  not on GitHub or other machines): MediaWiki-markup draft of the
  "Building GNU Radio from Source Code" page. Rewritten 2026-10-03 for the
  upcoming **`v1.2`**: supported systems, two scripts via tag-pinned raw
  links, both run with `sudo`, where the dependency lists come from (no
  manual package lines), `--branch` (default `maint-3.10`; `main` lacks
  `gr-qtgui`), build logs and `make test`, replacing an earlier install
  (manifest removal + leftover directories + old Volk), checking the
  result. Contains two bold "Draft note" markers to resolve before
  publishing: the `v1.2` tag doesn't exist yet, and 24.04 is untested with
  these scripts. (The live page uses `v1.0`.)

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
  local wiki draft. `~/gnuradio.main` and `~/gnuradio.old` are old build
  trees on the LENOVO and can be deleted.

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
- **No Ettus PPA; build UHD from source** (user, 2026-10-02), despite the
  main GNU Radio developer's proposal. The PPA (`ppa:ettusresearch/uhd`)
  had UHD 4.11.0.0 for 24.04 and 26.04; the evaluation is in git history
  (CLAUDE.md before this change).
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

   **UHD from the Ettus PPA — rejected 2026-10-02** (see Key decisions).

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
11. **Volk removed; GNU Radio installer revised (done 2026-10-02, code
    dry-run tested only).** Deleted the Volk installer and the volk/gnuradio
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
    - `v1.0` and the current wiki links stay unchanged; ship as the next tag
      with a wiki page update. The local `wiki-draft-download-section.txt`
      still describes `v1.0` (three scripts) — update it for the next tag.
12. **Next (as of 2026-10-03):**
    - Clean-install test of the current `main` scripts on the GMKtec (the
      LENOVO run needed manual cleanup), and a 24.04 test (untested since
      `v1.0`; 24.04's list is 67 packages).
    - Then tag `v1.2` and update the wiki page: two scripts, `maint-3.10`
      default, no manual dependency lines needed, supported releases
      (24.04, 26.04), removal procedure. The local draft is already written
      for `v1.2` (its links 404 until the tag exists).
    - Later: the `main`/Qt6 path (Qwt from source) if wanted.
