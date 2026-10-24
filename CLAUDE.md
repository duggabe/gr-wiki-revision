# gr-wiki-revision — GNU Radio build scripts for the GNU Radio Wiki

Trimmed 2026-10-14 (user: "trim CLAUDE.md"); the full earlier record,
including the Phase 1 history day by day, is `CLAUDE.md` at commit
`03ae87f`. Brought up to date after the `v3.0` release on 2026-10-22; the
day-by-day `v3.0` development record (rc1 runs, the 26.10 Qt6 trial in
full) is `CLAUDE.md` at commit `d8edb99`.

## Project summary

https://github.com/duggabe/gr-wiki-revision (public) holds the scripts
behind the GNU Radio Wiki page **"Building GNU Radio from Source Code"**
(https://wiki.gnuradio.org/index.php?title=Building_GNU_Radio_from_Source_Code),
which the user (Barry, GitHub `duggabe`) writes. The scripts are for GNU
Radio developers on Ubuntu (24.04 and 26.04; 26.10 works too), outside
Docker. Both run as the normal user, not with `sudo`:

- **Step 1, `gnuradio_dependencies_installer.py`:** UHD from the Ettus PPA
  (Ubuntu's own UHD where the PPA has no build) plus everything GNU Radio
  needs, with `apt-get` only; calls `sudo` itself for the root commands.
- **Step 2, `gnuradio_clone_builder.py`:** builds, tests, and installs
  whatever is checked out in `~/gnuradio` (normally the user's fork) into
  `~/gnuradio-pkg`, and writes `~/gnuradio-pkg/setup_env.sh`, which
  `~/.profile` sources.

Current release: **`v3.0`** (GitHub "Latest", 2026-10-21). Favour clarity,
reproducibility, and reader choice: the scripts back wiki instructions that
other people run.

**Working names:** "Phase 1" = the `v1.x` line (UHD and GNU Radio built from
source; removed from `main` 2026-10-14, still at tags `v1.0`–`v1.3`, whose
raw links work). "Phase 2" = the `v2.x` / `v3.x` line, the only one now. The
README, the wiki page, and the Release notes never mention phases ("as if
there had not been a Phase 1", user, 2026-10-13).

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
- **Tags** are never moved; fixes get a new tag. Next: `v3.1` (the README
  says "Further fixes will be tagged `v3.1`"). Bigger changes are tested
  through `vX.Y-rcN` tags with no Release first, so `releases/latest` stays
  on the last release; testers download from
  `https://raw.githubusercontent.com/duggabe/gr-wiki-revision/<tag>/<file>`.
- **GitHub Releases** are created or edited only on the user's request.
  Every Release must have **both scripts attached**, because the docs
  download from
  `https://github.com/duggabe/gr-wiki-revision/releases/latest/download/<file>`.
- **The wiki draft leads; the README follows.** `wiki-draft-download-section.mediawiki`
  (MediaWiki, gitignored, local only) is the user's text. The user edits in
  MediaWiki; I convert to Markdown for the README. The README is the draft
  section by section, plus README-only parts: a short repo intro (with the
  wiki page link), the two options tables (keep in sync with the scripts'
  argparse help), and the "Releases" section. The options tables' "Option"
  header is padded with 40 `&nbsp;` so GitHub doesn't wrap the options
  (`239bd31`; the user confirmed it looks good, 2026-10-15). Keep the
  padding if the tables change. The `v2.4` text is kept as
  `wiki-draft-download-section-v2.4.mediawiki` (gitignored).
- **The user updates the live wiki page by total replacement** with the
  whole local draft, so keep the draft complete and current. For bigger
  revisions the user may draft on User_talk:Duggabe first (done for
  `v3.0`); then wait until the user has finished ("Wait until I've made my
  changes"), ask for a paste, and update the local draft from it. Check
  afterwards that nothing added locally in the meantime was lost (the two
  `main`/Qt6 sentences were, once, and were restored, 2026-10-21).
- **The docs give no per-terminal fallback** for the environment (user,
  2026-10-21: "I wanted to force the user to log out and back in rather
  than suggest a way to limp along"): `~/.profile` line, log out and in.
- The wiki is behind Cloudflare and can't be fetched from here: ask the user
  to paste content.
- The user's related wiki page
  https://wiki.gnuradio.org/index.php/ModuleNotFoundError (local copy
  `ModuleNotFoundError.mediawiki`, gitignored) is linked from the draft's
  environment section. Revised by me for any install, still generic (no link
  to this project; section headings A–F kept for anchors): fallback `find`
  when `gnuradio-config-info` fails, `PATH` in D, Debian/Ubuntu vs
  Fedora/RPM instead of 32/64-bit, how `~/.profile` takes effect, Python
  3.12 (24.04) / 3.14 (26.04, 26.10), `/etc/profile.d` needs `sudo`. **The
  user pasted it to the wiki** (2026-10-22); older versions are in the
  wiki's revision history.
- **Generic wiki pages keep older-system instructions:** PyBOMBS is no
  longer supported, but many users (especially outside the US) still run
  older systems (user, 2026-10-23). So `UnInstallGR.mediawiki` (local,
  gitignored; revised by me 2026-10-23 with the user's readability edits;
  **the user pasted it to the wiki**, 2026-10-23) keeps its PyBOMBS
  section and the pre-3.10 `~/.gnuradio` / `~/.grc_gnuradio` folders. No
  Conda section: other wiki pages cover it (user, 2026-10-23).

## Current state (2026-10-22)

- **`v3.0` released** (2026-10-21, tag on `80b6b8f`, the same commit as
  `v3.0-rc1`). Live wiki page = local draft (`v3.0`) = README (`42540ca`).
  `main` pushed, working tree clean.
- **`v3.0-rc1` passed on all three releases** (see Test results): the other
  tester's clean 24.04, the clean 26.04 GMKtec, the clean 26.10 ASUS, each
  with `maint-3.10` and (26.04 / 26.10) `main`, and all SDRs.
- GitHub Releases: `v3.0` (Latest), `v2.4`, `v2.3`, `v2.2`, `v2.1`, `v2.0`,
  all with both scripts attached. The `v1.2` Release was deleted 2026-10-13
  (tags kept).
- **On hold** (user, 2026-10-16): "I'm going to wait for the developers
  decisions before I do anything else": where the scripts live, Fedora
  support, the `qa_fastnoise` backport (see Open items).
- Tracked files: the two scripts, `README.md`, `LICENSE` (CC BY-SA 4.0, by
  choice although CC advises against it for software), `.gitignore`,
  `CLAUDE.md`.

## Machines

The user's three SDRs in all of the user's tests, on every machine: USRP
B200mini (serial 315C7B7), RTL-SDR (an RTL-SDR.COM v3), PlutoSDR.

| Machine | Ubuntu | State |
| --- | --- | --- |
| LENOVO desktop (working machine, `~/gr-wiki-revision`) | 26.10 | 16 cores, 15 GiB RAM, 4 GB swap. **Reloaded with 26.10** (user, by 2026-10-22; clean presumably, my reading). Seen by me 2026-10-22: Ubuntu's UHD 4.9.0.1-1.4, `~/gnuradio` on `maint-3.10` at `273c82180`, `~/gnuradio-pkg/setup_env.sh` present, nothing in `/usr/local/bin`: so the `v3.0` scripts with the default prefix (user confirmed, 2026-10-22). **`make test` 269/269, 42 components** (user, 2026-10-22). User built `maint-3.10` and found [gnuradio/gnuradio#8250](https://github.com/gnuradio/gnuradio/issues/8250) with `gnuradio-companion --qt` (see Useful facts). Before (reloaded 2026-10-08): 26.04, UHD 4.11 from the PPA, GNU Radio 3.10.12.0 in `/usr/local`. |
| GMKtec (clean-install test machine) | reloaded per test | 4 cores, 10 GiB. Last: **clean 26.04 with `v3.0-rc1`** (2026-10-20/21), `~/gnuradio-pkg`, ended on `main` -1216. Earlier: clean 24.04 (`v2.2`, `v2.3`, 2026-10-14), Fedora 44 (2026-10-16), clean 26.04 (`v2.4`, 2026-10-17). |
| Laptop (hostname `ASUS`) | 26.10 | Last: **clean 26.10 with `v3.0-rc1`** (2026-10-20), Ubuntu's UHD 4.9.0.1-1.4, Qt6 list installed, `~/gnuradio-pkg`, ended on `main` -1216. Earlier: clean 26.10 for the Qt6 trial (2026-10-17) and the manual prefix trial (2026-10-19); before that 24.04, not clean. |
| The other tester's machine (jesternofool) | 24.04 | Reinstalls a clean OS quickly. Clean installs for the `v2.3` and `v3.0-rc1` tests. Fork `jesternofool/gnuradio` (only `main`). Devices: HackRF, LimeSDR Mini, Airspy R2, B200mini, RTL-SDR. |

## The scripts

### `gnuradio_dependencies_installer.py` (Step 1)

Self-contained, `apt-get` only. Runs as the normal user (still works under
`sudo`): one `sudo -v` first, then `sudo env DEBIAN_FRONTEND=noninteractive
...` for each root command (`as_root()`); the checks, the PPA check and the
package lookups run unprivileged. Checks the host is Ubuntu; aborts if
Ubuntu's `gnuradio` / `gnuradio-dev` are installed, a source-built UHD is
under `/usr/local`, or a PPA entry names a release the PPA has no build for
(prints the fix commands, e.g. `sudo add-apt-repository --remove -y
ppa:ettusresearch/uhd`). Then:

1. enable "Source code": `Types: deb` → `Types: deb deb-src` in
   `/etc/apt/sources.list.d/ubuntu.sources` (backup `.bak`, through
   `sudo cp -p` + `sudo tee`)
2. `apt-get update`; `apt-get install -y software-properties-common git`
3. `add-apt-repository -y ppa:ettusresearch/uhd`, only if `ppa_has_build()`:
   the PPA's `dists/<codename>/Release` answers 200. On 404: a warning, no
   PPA entry, Ubuntu's UHD. Other errors abort.
4. `apt-get install -y --no-install-recommends uhd-host libuhd-dev`
5. `apt-get install -y` `BOOST_PACKAGES`: `libboost-dev` and the chrono,
   date-time, exception, filesystem, program-options, regex, serialization,
   test, thread `-dev` packages
6. `apt-get build-dep -y gnuradio`
7. `apt-get install -y` `EXTRA_PACKAGES`: `python3-qtpy python3-pyqtgraph
   python3-matplotlib soapysdr-tools python3-pytest`
8. `<Qt6 packages>`: `QT6_PACKAGES` (`qt6-base-dev qt6-svg-dev
   libqwt-qt6-dev python3-pyqt6 python3-pyqt6.qtsvg pyqt6-dev-tools`), only
   if `apt-cache show libqwt-qt6-dev` finds it (26.10 on); else a `note:`
9. `<SoapySDR device modules>`: worked out by `soapy_module_packages()`:
   the Depends of `soapysdr-module-all` (through `soapysdr0.8-module-all`)
   minus `SOAPY_SKIP_MODULES` (`uhd`). 11 on 24.04, 13 on 26.04. Warns and
   goes on if apt doesn't know the metapackage.
10. `uhd_images_downloader` (skipped with `--no-images`)

Options: `--dry-run`, `-y`, `--no-images`, `--sources-path`, `--os-release-path`.

### `gnuradio_clone_builder.py` (Step 2)

Self-contained. Builds `~/gnuradio` (`--source-dir`); never clones or
changes branches; reuses `build/`. Steps (`get_build_steps()`): `mkdir
build` (first time) or `sudo chown -R` the build dir back to the user (only
if it has files the user doesn't own) → `cmake -DCMAKE_INSTALL_PREFIX=<prefix>`
→ make → `git clean -fdX grc/tests/resources` in the source dir (only if
`.git` and that directory exist) → make test, each tee'd to `cmake.log` /
`make.log` / `make_test.log` → install. Install: `--prefix`, default
`~/gnuradio-pkg`; if `owns_prefix()` (the prefix or its nearest existing
parent belongs to the build user), plain `make install`, then
`<prefix>/setup_env.sh` is written (PATH = `bin`, PYTHONPATH = the parents
of `lib*/python3*/{site,dist}-packages/gnuradio`, LD_LIBRARY_PATH = the
dirs with `libgnuradio-runtime.so*`; each a `case` guard, so sourcing twice
adds nothing) and the `sudo apt install gnuradio` **DON'T!** warning is
printed, with the `echo '. "$HOME/gnuradio-pkg/setup_env.sh"' >> ~/.profile`
command, or a note if `~/.profile` already has the line (`d9197fa`, for
`v3.1`; `v3.0` printed the bare line, "add this line to ~/.profile", plus a
per-terminal fallback); otherwise (e.g. `--prefix /usr/local`)
`sudo make install` + `sudo ldconfig`. `make` jobs = `min(nproc - 1,
MemTotal // 2 GB)`, at least 1. Aborts if the directory isn't GNU Radio
source, `libuhd-dev` isn't installed, Ubuntu's `gnuradio` packages are
installed, or stale install dirs exist in the prefix or `/usr/local`; warns
if a GNU Radio is still installed in `/usr/local`. Steps not starting with
`sudo` run as `$SUDO_USER` when run under `sudo`. Options: `--source-dir`,
`--prefix`, `--jobs`, `--cmake-args="..."`, `--no-install`, `--dry-run`,
`-y`.

`INSTALL_DIR_PATTERNS` and the `rm -rf` list of the old `/usr/local`
removal (wiki draft "Before you start" and the README; the `v3.0` Release
notes' "If you used an earlier release") must stay in sync.

## Releases

| Tag | Date | What |
| --- | --- | --- |
| `v2.0` | 2026-10-10 | First release: the two scripts. Commit `1f8711c`. |
| `v2.1` | 2026-10-12 | Builder: `git clean -fdX grc/tests/resources` before `make test`. Commit `22e2ca3`. |
| `v2.2` | 2026-10-12 | Step 1: SoapySDR device modules. Commit `7208a18`. |
| `v2.3` | 2026-10-14 | Step 1: Boost dev packages for UHD's cmake files. Commit `ffac9f9`; Release title "v2.3: Boost packages for gr-uhd". |
| `v2.4` | 2026-10-15 | Step 1: `python3-pytest`, so 24.04 builds run `grc_tests`. Commit `ce9806d`; Release title "v2.4: pytest for the GRC test". |
| `v3.0-rc1` | 2026-10-19 | Tag only, no Release. Commit `80b6b8f`. |
| `v3.0` | 2026-10-21 | Tag on `80b6b8f` (= `v3.0-rc1`, no rc2). Both scripts run as the normal user; PPA check with Ubuntu-UHD fallback; Qt6 list where `libqwt-qt6-dev` exists; install into `~/gnuradio-pkg` + `setup_env.sh`. Release title "v3.0: no sudo, GNU Radio in your home directory", marked Latest; `releases/latest/download` checked byte-identical. Notes: What's changed, If you used an earlier release (the three `/usr/local` removal steps), Tested (24.04 / 26.04 / 26.10 table + hardware table), Quick start (download loop, links to the wiki page and README), Known limitations (`main` without `gr-qtgui` on 24.04/26.04, #8239, Range slider, the `python3` crash dialog). README converted in `42540ca`. |
| `v1.0`–`v1.3` | 2026-09-26 – 10-10 | Phase 1, tags only. |

## Key decisions and why

- **Install into `~/gnuradio-pkg`, no `sudo` (`v3.0`):** a developer asked
  for both steps to work without `sudo` by default, and the maintainer
  proposed installing into a `gnuradio-pkg` directory; the user: "I think it
  would make everyone happier" (2026-10-19). User's decisions: default
  prefix `~/gnuradio-pkg` with `--prefix`; the builder writes
  `setup_env.sh` with the paths it finds; the docs source it from
  **`~/.profile`** (the user prefers `~/.bash_aliases`, but `~/.profile`
  also covers GRC started from the desktop); Step 1 runs as the user and
  calls `sudo` only for the root commands.
- **Qt6 for `main` only where Qwt for Qt6 exists (user, 2026-10-19):**
  "Check for libqwt-qt6-dev, add nothing before 26.10." Keyed on the
  package, not the release, so later releases need no change. Without Qwt
  the rest gives no `gr-qtgui`. **Thrift packages left out** (user: "leave
  out Thrift (they may drop controlport/thrift support entirely)"): nothing
  beyond what `build-dep` brings; `main` can't use them anyway (#8239).
- **No PPA build for the running release: warn and use Ubuntu's UHD (user,
  2026-10-19: "warn when no PPA support, use distro UHD"):** on 26.10 the
  PPA has no build, and `add-apt-repository` writes the entry anyway and
  exits 0 (apt only prints "does not have a Release file"), so `v2.4`
  silently got Ubuntu's UHD 4.9.0.1 and a stale entry. Hence the Release
  URL check before `add-apt-repository`. **SoapySDR UHD module stays out
  with Ubuntu's UHD too** (user: "leave it out"): `soapysdr0.8-module-uhd`
  on 26.10 depends on `libuhd4.9.0`, which would stay next to a later PPA
  `libuhd4.11.0`; USRPs work through `gr-uhd` anyway.
- **UHD from the Ettus PPA** (the main GNU Radio developer's proposal),
  installed with **`--no-install-recommends`**: `libuhd-dev` recommends
  `gnuradio-dev` and `python3-uhd` recommends `gnuradio`, which put Ubuntu's
  GNU Radio 3.10.12 in `/usr` next to the source build (happened on the
  LENOVO 2026-10-08). Both scripts refuse to run while those are installed.
- **GNU Radio's dependencies from `apt-get build-dep gnuradio`**, not a
  hardcoded list: tracks each Ubuntu release. It fits `maint-3.10` (Qt5).
- **Boost packages by name (`v2.3`):** the PPA's `libuhd-dev` (4.11.0.0)
  declares no Boost dependencies, while UHD's `UHDConfig.cmake` does
  `find_dependency(Boost ... COMPONENTS chrono date_time filesystem
  program_options serialization thread unit_test_framework)`. `build-dep
  gnuradio` lacks chrono, filesystem, serialization; on a clean 24.04 cmake
  then prints `Boost_FOUND = FALSE` / "Disabling gr-uhd support" and builds
  on without `gr-uhd`. Chosen over `libboost-all-dev` (much bigger).
- **SoapySDR modules, all but UHD (`v2.2`):** they are only Recommends of
  `libsoapysdr0.8`, which `build-dep` doesn't install, so `gr-soapy` had no
  drivers. The UHD module pulls Ubuntu's older `libuhd4.9.0` next to the
  PPA's. The `audio` module makes `SoapySDRUtil --find` print harmless
  `ALSA lib` / `RtApi::getDeviceInfo` lines; kept and explained in the docs
  (2026-10-13).
- **The builder removes GRC's generated test files before `make test`
  (`v2.1`):** GNU Radio's GRC tests write `test_*.py` files into
  `grc/tests/resources` (gitignored); the next pytest run collects them, and
  they import `gnuradio.qtgui`, which a `main` build without `gr-qtgui`
  lacks, so every `make test` after the first failed on `main`. Reported
  upstream by the user (2026-10-14; no issue number given). **Kept** (user,
  2026-10-19: "Keep the clean before the make test"); drop it when upstream
  fixes it.
- **Memory-aware `make` jobs:** an OOM kill at `make -j15` on the LENOVO's
  15 GiB. 2 GB per job is my estimate, not measured.
- **Any failing step stops the build, including a failing test,** so a
  failing build is never installed.
- **Removing a `v3.0` install** (draft "Changing branches..."): `rm -rf
  ~/gnuradio-pkg ~/gnuradio/build`; for full removal first
  `~/gnuradio/build/grc/scripts/freedesktop/grc_setup_freedesktop
  uninstall` (the desktop entry, icons, MIME files) and remove the
  `~/.profile` line. A `v2.x` `/usr/local` install takes the old three steps
  (manifest removal, `rm -rf` the empty leftover dirs, which break
  `grc_tests`, then `rm -rf ~/gnuradio/build`), now under "Before you start".
- **Downloads by Python from the latest Release:** "the developers do not
  like to use wget" (2026-10-14). Since `v3.0`, one `for f in ...; do
  python3 -c "...urlretrieve..." ...; done` line in `~/gr-installers`
  (user, 2026-10-21: "The chained python3 calls would hang sometimes"; my
  guess: a paste ending on a trailing `&&` leaves bash at its `>` prompt).
- **No log-order fix** (user, 2026-10-21): Step 1's own `$ ...` / `note:`
  lines appear after apt's output in `step1.log` (Python block-buffers
  `print` into a pipe); `sys.stdout.reconfigure(line_buffering=True)` would
  fix it. Cosmetic, left for a later release.

## Useful facts

- **A home prefix needs `PATH`, `PYTHONPATH` and `LD_LIBRARY_PATH`** (manual
  trial, ASUS 2026-10-19): no RPATH/RUNPATH in the binaries, so without
  `LD_LIBRARY_PATH` `gnuradio-config-info` can't find
  `libgnuradio-runtime.so.3.10.12`. Python modules go to
  `lib/python3.X/site-packages` (both branches). `setup_env.sh` needs only
  read permission (sourced with `.`). cmake finds the prefix for
  out-of-tree modules through `PATH`, no `CMAKE_PREFIX_PATH` needed
  (`gr_modtool newmod`, `cmake`, `make` worked on 24.04 and 26.10).
- **GRC's desktop entry comes with `make install`:**
  `grc/scripts/freedesktop/CMakeLists.txt` runs
  `build/grc/scripts/freedesktop/grc_setup_freedesktop install` (xdg-utils,
  per-user when not root): 45 files under `~/.local/share` (applications,
  `gnome` / `hicolor` icons in 7 sizes, `mime`). The same script's
  `uninstall` removes them all (checked, 2026-10-20); it exists only in the
  build dir. GRC from Activities starts in GTK mode.
- **The "command not found" trap:** without `setup_env.sh`, Ubuntu answers
  e.g. `gr_modtool` with "can be installed with: sudo apt install gnuradio",
  which would put Ubuntu's GNU Radio next to the source build. The docs and
  the builder say **DON'T!**
- **"python3 crashed" during `make test`** (Ubuntu's apport dialog): the
  test `qa_uncaught_exception` aborts a child process on purpose (`SIGABRT`
  in a `multiprocessing.forkserver` child; the test passes because it
  died). Harmless; the dialog stops once suppressed. Documented in the
  draft's Step 2 bullets.
- **QT GUI Range sliders on `main` with Qt6** raise `AttributeError:
  'QMouseEvent' object has no attribute 'x'` when clicked:
  `gr-qtgui/python/qtgui/range.py.cmakein`, `Slider.mousePressEvent` /
  `mouseMoveEvent` use `event.x()` / `.y()` (PyQt6 needs
  `event.position().x()`). Upstream bug; the developers know and chose not
  to open an issue (user, 2026-10-21). Flowgraphs still run.
- **PyQt6 on 26.04 and 26.10 comes with Step 1 anyway:** `python3-pyqtgraph`
  Depends `pyqt6-dev-tools | pyqt5-dev-tools`; `build-dep` brings
  `python3-pyqt5` but not `pyqt5-dev-tools`, so apt picks `pyqt6-dev-tools`,
  which Depends `python3-pyqt6` (same in `v2.4`). On 26.04 `main`,
  `gnuradio-companion --qt` then fails with `ModuleNotFoundError: No module
  named 'PyQt6.QtSvg'` (and locked up once `python3-pyqt6.qtsvg` was added
  by hand, 2026-10-18). `main`'s `grc/gui_qt/` imports PyQt6 directly, so
  `--qt` on `main` needs the 26.10 Qt6 set. On 24.04 / 26.04 `main`, use
  the default GTK front end and set the Options block to "No GUI" (in the
  draft).
- **GRC Qt front end closes the wrong tab** (`maint-3.10`, 3.10.12.0,
  LENOVO 26.10, `gnuradio-companion --qt`): with a second flowgraph open and
  active, clicking the "X" of the first (Untitled) tab closes the active
  tab instead. Filed by the user as
  [gnuradio/gnuradio#8250](https://github.com/gnuradio/gnuradio/issues/8250)
  (2026-10-22, open). Upstream GRC, not the scripts.
- `uhd-host` installs the udev rules (`/usr/lib/udev/rules.d/60-uhd-host.rules`);
  no copy in `/etc/udev/rules.d` is needed. FPGA images go to
  `/usr/share/uhd/<version>/images` (`uhd_config_info --images-dir`).
- A GitHub fork copies only `main` unless told otherwise. After
  `git fetch upstream`, a plain `git checkout maint-3.10` creates the branch
  from `upstream/maint-3.10`.
- On `main`, library names carry the commit (`.so.v3.11.0.0git-1193-g...`),
  so each rebuild after a commit leaves the old ones in the prefix's `lib`.
  The docs' listing command removes those files but can leave the
  `.so.3.11.0git` links dangling. On `maint-3.10` the names are
  `.so.3.10.12` / `.so.3.10.12.0`, so nothing piles up.
- **`main` (3.11, Qt6) components:** 40 on 24.04 / 26.04 (no `gr-qtgui`:
  needs `libqwt-qt6-dev`, only from 26.10; no Thrift), 41 on 26.10 (with
  `gr-qtgui`), vs 42 on `maint-3.10`. **Thrift on `main`** is broken by two
  bugs from `24e9f2b7e` (John Parent, "cmake: Add comprehensive
  cross-platform installer infrastructure"): `FindTHRIFT.cmake:63` still
  calls the now keyword-based `gr_python_check_module` positionally, which
  hides the second, `auto i_impl()` in `thrift_server_template.h` (lines 42,
  158), which doesn't compile. With both fixed, 42 components and 273/273
  on 26.10 (2026-10-17). Filed by the user as
  [gnuradio/gnuradio#8239](https://github.com/gnuradio/gnuradio/issues/8239)
  (2026-10-18). Thrift is a quiet subcomponent of `gr-ctrlport`, so it never
  shows as disabled. GNU Radio's CI Dockerfiles are in
  `gnuradio/gnuradio-docker` under `ci/` (`ci-ubuntu-26.10-3.11` lists its
  Qt6 packages, two under stale `libqt6*` names).
- **Ettus PPA builds** (Launchpad, 2026-10-17): `~noble3` and `~resolute3`
  (UHD 4.11.0.0), none for 26.10 `stonking`. Ubuntu's own UHD on 26.10 is
  4.9.0.1-1.4.
- `cmake` options persist in `build/CMakeCache.txt` (e.g. `ENABLE_GR_FEC`
  stayed `OFF` from an old manual build until `build/` was removed).

## Test results

Kept here only. Test counts differ by release and branch. `maint-3.10`:
269 everywhere with `python3-pytest` (`v2.4` on); 268 on 24.04 without it
(`grc_tests` is added only if cmake can `import pytest`, and pytest is in
`gnuradio`'s Build-Depends on 26.04 but not on 24.04). `main` grows with
upstream: 271 (-1193, 26.04), 272 / 273 (-1210, 26.04 / 26.10), 274 / 275
(-1216, 26.04 / 26.10); 26.10 always runs one more, `qa_qtgui`.

### `v3.0` (home prefix, no sudo)

| Date | Machine, Ubuntu | Scripts | Branch / build | Result |
| --- | --- | --- | --- | --- |
| 2026-10-19 | ASUS, 26.10 (not clean: after the manual prefix trial below, `~/gnuradio-pkg` and `build/` removed) | `main` at `169a139` by raw URL (pre-rc1) | `maint-3.10` (my reading) | Step 1 as the user: **UHD 4.9.0.1-1.4**, no-PPA warning, Qt6 list installed. **269/269**; `setup_env.sh` written with the three `case` lines. After the `~/.profile` line and a logout: **GRC from Activities works with a QT GUI Time Sink** (GTK mode); the desktop entry was already there. `setup_env.sh` needs no execute bit (checked with `chmod -x`). Out-of-tree module (`gr_modtool newmod`, `cmake`, `make`) built, 2026-10-20. |
| 2026-10-20 | same ASUS | rc1 builder | "Changing branches" (`rm -rf ~/gnuradio-pkg ~/gnuradio/build`), then `main` v3.11.0.0git-1216-gec1bf153 | **275/275**, **41 components** (`gr-qtgui` with Qt6, no Thrift). Apport "python3 crashed" dialog during the tests (`qa_uncaught_exception`, harmless). GRC from the desktop and `--qt`: Range sliders raise the `QMouseEvent.x()` error (upstream). Second builder run: 275/275. Full removal (`grc_setup_freedesktop uninstall`): 0 files left under `~/.local/share`, GRC gone from Activities. |
| 2026-10-20 | Other tester, clean 24.04 (presumably, my reading) | `v3.0-rc1` | `maint-3.10` (my reading) | **UHD 4.11.0.0-0ubuntu1~noble3** (PPA path), **269/269**, 3.10.12.0, prefix `/home/<tester>/gnuradio-pkg`, **42 components**, GRC from Activities works, out-of-tree module built ("Built target copy_module_for_tests"). Log oddities not reported. **Passed.** |
| 2026-10-20 | ASUS, **clean 26.10** (reloaded; formal rc1 test) | `v3.0-rc1` raw URLs | `maint-3.10`, default prefix | **UHD 4.9.0.1-1.4**, no-PPA warning in `step1.log`, **no `ettusresearch` file in `/etc/apt/sources.list.d/`**, `libqwt-qt6-dev` `ii`. **269/269**; 3.10.12.0, `/home/barry/gnuradio-pkg/`, **42 components**; GRC from Activities with a QT GUI Time Sink; `gr_modtool` module built. |
| 2026-10-20 | same | same | "Changing branches", then `main` -1216 | **275/275**, **41 components**; GRC from Activities with a QT GUI Time Sink works. **Clean 26.10 rc1 test: all passed.** |
| 2026-10-20/21 | GMKtec, **clean 26.04** | `v3.0-rc1` | `maint-3.10` | **UHD 4.11.0.0-0ubuntu1~resolute3** (PPA path); 13 SoapySDR modules; Qt6 `note:` (no `libqwt-qt6-dev`); `python3-pyqt6` 6.10.2 `ii` anyway (via `python3-pyqtgraph`). **269/269**; 3.10.12.0, `/home/barry/gnuradio-pkg/`, **42 components**; GRC from Activities with a QT GUI Time Sink (Qt5). |
| 2026-10-21 | same | same | "Changing branches", then `main` -1216 | **274/274**, **40 components** (no `gr-qtgui`, no Thrift), as expected. `gnuradio-companion --qt`: `ModuleNotFoundError: No module named 'PyQt6.QtSvg'`. GTK GRC: qtgui blocks missing; a "QT GUI" flowgraph fails (`cannot import name 'qtgui'`), **with "No GUI" it works**. Not the scripts (`v2.4` installs the same). **Clean 26.04 rc1 test: all passed.** |
| by 2026-10-22 | LENOVO, 26.10 (reloaded; clean presumably, my reading) | `v3.0` (user confirmed) | `maint-3.10` at `273c82180`, `~/gnuradio-pkg` | **269/269, 42 components** (user, 2026-10-22); Ubuntu's UHD 4.9.0.1-1.4. First 26.10 run of the released `v3.0` (byte-identical to rc1). `gnuradio-companion --qt` runs (user confirmed, 2026-10-22); #8250 (wrong tab closed) is upstream. |

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
| 2026-10-17 | GMKtec, clean 26.04 | `v2.4` (presumably downloaded from the wiki page; my assumption) | `maint-3.10` (user, 2026-10-17); the user also built `main` on this install ("I have done both"): "main built correctly" (user, 2026-10-17; test count, version, and components not reported) | **269/269** ("100% tests passed, 0 tests failed out of 269", user, 2026-10-17), as expected on 26.04. Step 1 ran: `uhd_config_info --version` = UHD 4.11.0.0-0ubuntu1~resolute3 (user). First real run of `v2.3`'s Boost step and `v2.4`'s `python3-pytest` on 26.04 (my reading: Step 1 finished, since UHD is installed). `SoapySDRUtil --info` (SoapySDR v0.8.1-7build1): **13 modules**, exactly the expected 26.04 set (airspy, airspyhf, audio, bladerf, hackrf, hydrasdr, lime, miri, osmosdr, plutosdr, redpitaya, remote, rtlsdr), no UHD: first run of `v2.2`'s SoapySDR step on a clean 26.04. The three checks "work" (user, 2026-10-17): 3.10.12.0, cmake's disabled-components list empty, 42 components (my reading of "work" = the expected values; numbers not pasted). **`gnuradio-companion` works** (user, 2026-10-17; whether a QT GUI flowgraph was run not stated). B200mini and PlutoSDR loopbacks and RTL-SDR stereo FM work (see Hardware). **Clean 26.04 test of `v2.4` complete: all passed**. Then (2026-10-18) `~/gnuradio` on `main` at **`862edb76b`**, the same commit as the ASUS 26.10 build (user's `git log -1`): **`make test` 272/272** (user). 272 = the ASUS's 273 minus `qa_qtgui` (no `gr-qtgui` on 26.04), so the second extra test on the ASUS is not a 26.10 difference but came with the 17 upstream commits between -1193 and -1210 (my reading). **40 components** (user), as expected: the ASUS's 41 without the Thrift fix, minus `gr-qtgui`. **Second `make test`** (plain, in `build/`, without the builder's `git clean` step; my reading, as I suggested that command): **271/272, `grc_tests` (test 28) failed**, 154.86 s: **confirmed the known generated-files problem** (`v2.1`): `ctest -R grc_tests --output-on-failure` shows pytest collecting `grc/tests/resources/test_python_hb_qt_gui_workflow.py` and `test_python_qt_gui_workflow.py`, "ImportError: cannot import name 'qtgui' from 'gnuradio'" (2 collection errors; 288 items, 56 selected). So it is **still on `main` at `862edb76b`** and the builder's `git clean` step stays |
| 2026-10-19 | ASUS, clean 26.10 (reloaded) | `v2.4` Step 1 (UHD 4.9.0.1-1.4, stale `stonking` entry removed); `v2.4` builder with `--no-install --cmake-args="-DCMAKE_INSTALL_PREFIX=$HOME/gnuradio-pkg"` (my reading: the commands I gave) | `maint-3.10` (my reading), first `v3.0` prefix trial | **269/269** ("100% tests passed, 0 tests failed out of 269", user, 2026-10-19), as on 26.04. Qt6 list **not** installed on this reload: `dpkg -l` shows `libqwt-qt6-dev` `un` (not installed) but **`python3-pyqt6` 6.11.0-3build1 `ii`** (user, 2026-10-19), so on 26.10 something in `v2.4` Step 1 pulls PyQt6 in by itself (what, not known yet; on 26.04 it was absent until installed by hand). Version and components not reported yet; **`make install` without `sudo` into `~/gnuradio-pkg` finished** (user's `tail -3`: `-- Installing: /home/barry/gnuradio-pkg/...`, last `include/gnuradio/config.h`; no errors shown, 2026-10-19). Python modules at **`~/gnuradio-pkg/lib/python3.14/site-packages/gnuradio`** (user's `find`; `site-packages`, not `dist-packages`, on `maint-3.10` too). **No RPATH/RUNPATH** in `bin/gnuradio-config-info` (`readelf -d` found nothing, user), so `LD_LIBRARY_PATH=~/gnuradio-pkg/lib` is needed (my conclusion; not run yet). `apt-cache rdepends --installed python3-pyqt6`: `pyqt6-dev-tools`, `|python3-pyqtgraph`, `python3-matplotlib` (user), so on 26.10 PyQt6 comes with Step 1's own `python3-pyqtgraph` / `python3-matplotlib` (dependency or recommends, not checked), and `pyqt6-dev-tools` is installed too (from where, not known). Environment test (new terminal, the three exports I gave): `gnuradio-config-info --version --prefix` printed `/home/barry/gnuradio-pkg/` and **`3.10.12.0`** (user, 2026-10-19); **all three exports set** (user), then **`env -u LD_LIBRARY_PATH gnuradio-config-info --version` failed**: "error while loading shared libraries: libgnuradio-runtime.so.3.10.12: cannot open shared object file" (user, 2026-10-19): **`LD_LIBRARY_PATH` is needed** (or an RPATH / an `ld.so.conf.d` entry, which needs root). `--enabled-components` (user's paste, one `;`-separated line; my `wc -l` suggestion was wrong): **42 components** (counted by me), incl. `gr-ctrlport` + `* thrift` (from `build-dep` alone), `gr-qtgui`, `gr-uhd` + RFNoC with Ubuntu's UHD 4.9.0.1, `gr-iio` + `libad9361`, `gr-soapy`: the same 42 as 26.04. **`gnuradio-companion` works with a QT GUI Time Sink, both `--gtk` and `--qt`** (user, 2026-10-19), with the three exports in a terminal; so the prefix install works at run time with `PATH` + `PYTHONPATH` + `LD_LIBRARY_PATH`, and `--qt` on `maint-3.10` runs although PyQt6 is installed (on 26.10). Python one-liner not reported (GRC implies the import works, my reading). **Trap seen** (user, 2026-10-19): in a tab without the exports, `gr_modtool` gave Ubuntu's "Command 'gr_modtool' not found, but can be installed with: sudo apt install gnuradio", and that `apt` offered Ubuntu's `gnuradio` + `gnuradio-dev` + all `libgnuradio-*3.10.12`; the user answered `n`, nothing installed. For `v3.0` (my proposal): the docs warn about it, and the builder tells the user to open a new terminal / source `setup_env.sh`. With the exports, **`gr_modtool newmod test` worked** (user, 2026-10-19). **RTL-SDR.COM v3 received a broadcast FM station in stereo, from GRC `--qt` and `--gtk`** (user, 2026-10-19; presumably `gr-soapy`, my reading). **Manual prefix trial passed**: `setup_env.sh` needs exactly `PATH`, `PYTHONPATH`, `LD_LIBRARY_PATH`. Not yet: GRC from the desktop via `~/.profile` (to test with `v3.0-rc1`'s `setup_env.sh`) |

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
| 2026-10-12 | User, LENOVO 26.04 | `maint-3.10` | RTL-SDR.COM v3 (RTL2838, R820T) | SoapySDR | `SoapySDRUtil --find` sees it; no flowgraph reported |
| 2026-10-12/13 | Other tester, 24.04 | `v2.1`, `maint-3.10` | RTL-SDR (0bda:2838, R820T) | `gr-soapy` | "No modules found!" until `soapysdr0.8-module-rtlsdr` was installed (led to `v2.2`); then `--find` / `--probe` worked as a normal user (the library detaches the DVB driver itself), and a flowgraph ran |
| 2026-10-13 | Other tester, 24.04 | `v2.1`, `maint-3.10` | USRP B200mini | `gr-uhd` | a flowgraph ran (transmit not known) |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | RTL-SDR, HackRF, LimeSDR Mini, Airspy R2 | `gr-soapy` | all work; the Airspy R2 through the Soapy Custom Source block (only it), the others presumably through their own blocks (my reading). **The HackRF and the LimeSDR Mini also transmitted** (user, 2026-10-15) |
| 2026-10-14 | Other tester, clean 24.04 | `v2.3`, `maint-3.10` | USRP B200mini | `gr-uhd` | works, **including transmit** (user, 2026-10-15) |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | USRP B200mini (315C7B7) | UHD tools, `gr-uhd` | `uhd_find_devices`, `uhd_usrp_probe` (FPGA, USB 3, loopback passed), `uhd_rx_cfile` 8,000,000 bytes; Boost_108300. **Loopback (transmit and receive) through `gr-uhd` with a 30 dB attenuator worked** (user, 2026-10-15) |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | RTL-SDR.COM v3 (RTL2838, R820T) | SoapySDR | `--find` and `--probe="driver=rtlsdr"` work (kernel driver detached/reattached by the library); receive only, as planned. `--find` also lists a "USB Audio and HID" device through the audio module |
| 2026-10-14 | User, GMKtec clean 24.04 | `v2.3`, `maint-3.10` | PlutoSDR | `gr-iio`: PlutoSDR Source and PlutoSDR Sink (user, 2026-10-15) | **"Pluto with loopback cable works."** Both at 2.435 GHz. First PlutoSDR / `gr-iio` test |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10`, Fedora's UHD 4.9.0.1 | RTL-SDR.COM v3 | presumably `gr-soapy` with `soapy-rtlsdr` (my inference; block not stated) | **Received a broadcast FM station in stereo** (user, 2026-10-16): first RTL-SDR flowgraph by the user, and the first device test on Fedora. Presumably audio out through `gr-audio` too (my inference) |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10`, Fedora's UHD 4.9.0.1 | USRP B200mini | `gr-uhd` | **Loopback file transfer worked** (user, 2026-10-16): transmit and receive with Fedora's UHD 4.9.0.1 and its `uhd-firmware` images, 30 dB attenuator, the user's own flowgraph. Works as the normal user with no udev change (Fedora's `uhd` rules are enough) |
| 2026-10-16 | User, GMKtec clean Fedora 44 | none ("option 1" by hand), `maint-3.10` | PlutoSDR | `gr-iio`: PlutoSDR Source and Sink ("PlutoSDR", user) | **Loopback worked** (user, 2026-10-16), the user's own flowgraph; frequency and attenuation not stated |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, `maint-3.10` (user) | USRP B200mini | `gr-uhd` ("UHD", user) | **Loopback worked with a 30 dB attenuator** (user, 2026-10-17): **first transmit on 26.04**. UHD tools (`uhd_find_devices` / `uhd_usrp_probe`) not reported |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, `maint-3.10` (user) | PlutoSDR | `gr-iio` PlutoSDR blocks ("PlutoSDR", user) | **Loopback worked** (user, 2026-10-17): first PlutoSDR test on 26.04; frequency and attenuation not stated |
| 2026-10-17 | User, GMKtec clean 26.04 | `v2.4`, `maint-3.10` (user) | RTL-SDR.COM v3 | `gr-soapy` ("Soapy", user; which Soapy block not stated) | **Received a broadcast FM station in stereo** (user, 2026-10-17): first RTL-SDR flowgraph on 26.04 |
| 2026-10-19 | User, ASUS clean 26.10 | `v2.4` Step 1 + builder into `~/gnuradio-pkg` (prefix trial), `maint-3.10` | RTL-SDR.COM v3 | presumably `gr-soapy` (my reading) | **Received a broadcast FM station in stereo, from GRC `--qt` and `--gtk`** (user, 2026-10-19): first device test on 26.10 and from a home prefix |
| 2026-10-20 | User, ASUS 26.10 (not clean) | `v3.0-rc1`, `maint-3.10`, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1-1.4 | USRP B200mini | `gr-uhd` (my reading) | **Loopback worked with a 30 dB attenuator** (user, 2026-10-20): first USRP use on 26.10, with Ubuntu's UHD, and from a home prefix. `uhd_find_devices` / `uhd_usrp_probe` not reported |
| 2026-10-20 | User, ASUS 26.10 (not clean) | `v3.0-rc1`, `maint-3.10`, `~/gnuradio-pkg` | PlutoSDR | `gr-iio` PlutoSDR blocks (my reading) | **Loopback worked** (user, 2026-10-20): first PlutoSDR test on 26.10 and from a home prefix; with the RTL-SDR (2026-10-19), all three SDRs work on 26.10 |
| 2026-10-20 | User, ASUS 26.10 (not clean) | `v3.0-rc1`, **`main`** v3.11.0.0git-1216-gec1bf153, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1-1.4 | USRP B200mini | `gr-uhd`, from `gnuradio-companion --qt` (`~/GRdev/bpsk_file_transfer_stage6.py`) | **Loopback file transfer worked** (user, 2026-10-20): first hardware test on `main` with Qt6 / `gr-qtgui`. Clicking the QT GUI Range sliders raises the `QMouseEvent.x()` AttributeError (upstream; see Drafts) |
| 2026-10-20 | User, ASUS **clean** 26.10 | `v3.0-rc1` (formal test), `maint-3.10`, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1-1.4 | USRP B200mini | `gr-uhd` (my reading) | **Loopback worked with a 30 dB attenuator** (user, 2026-10-20) |
| 2026-10-20 | User, ASUS **clean** 26.10 | `v3.0-rc1` (formal test), `maint-3.10`, `~/gnuradio-pkg` | PlutoSDR | `gr-iio` PlutoSDR blocks (my reading) | **Loopback worked** (user, 2026-10-20) |
| 2026-10-20 | User, ASUS **clean** 26.10 | `v3.0-rc1` (formal test), `maint-3.10`, `~/gnuradio-pkg` | RTL-SDR.COM v3 | presumably `gr-soapy` (my reading) | **Received a broadcast FM station in stereo** (user, 2026-10-20); all three SDRs work on the clean rc1 install |
| 2026-10-21 | User, GMKtec clean 26.04 | `v3.0-rc1`, `maint-3.10`, `~/gnuradio-pkg`, UHD 4.11.0.0~resolute3 (PPA) | USRP B200mini | `gr-uhd` (my reading) | **Loopback worked with a 30 dB attenuator** (user, 2026-10-21) |
| 2026-10-21 | User, GMKtec clean 26.04 | same | PlutoSDR | `gr-iio` PlutoSDR blocks (my reading) | **Loopback worked** (user, 2026-10-21) |
| 2026-10-21 | User, GMKtec clean 26.04 | same | RTL-SDR.COM v3 | presumably `gr-soapy` (my reading) | **Received a broadcast FM station in stereo** (user, 2026-10-21); all three SDRs work on 26.04 with rc1 |
| 2026-10-20 | Other tester, 24.04 (presumably clean, my reading) | `v3.0-rc1`, `maint-3.10` (my reading), `~/gnuradio-pkg`, UHD 4.11.0.0~noble3 | RTL-SDR, Airspy R2 | `gr-soapy` (tester) | **Both work** (tester via the user, 2026-10-20) |
| 2026-10-20 | Other tester, 24.04 (presumably clean, my reading) | same | LimeSDR Mini, HackRF | `gr-soapy` (tester) | **Both work, receive and transmit** (tester via the user, 2026-10-20) |
| 2026-10-20 | Other tester, 24.04 (presumably clean, my reading) | same | USRP B200mini | `gr-uhd` (tester: "the UHD driver") | **Works, receive and transmit** (tester via the user, 2026-10-20) |

Transmit: on 24.04 (GMKtec, `v2.3`; the other tester with a HackRF, a
LimeSDR Mini and a B200mini, `v2.3` and `v3.0-rc1`), on 26.04 (GMKtec,
`v2.4` and `v3.0-rc1`), on 26.10 (ASUS, `v3.0-rc1`, Ubuntu's UHD 4.9.0.1),
and on Fedora 44 (by hand): B200mini (30 dB attenuator) and PlutoSDR
loopbacks.

## Open items

- **Waiting for the developers** (user, 2026-10-16): where the scripts live
  ("the plan is to bring it into the gnuradio/gnuradio repo", details not
  settled; if it moves, the download links in the wiki draft, README, and
  Release notes, and the repo URLs here, need updating), Fedora support,
  the `qa_fastnoise` backport.
- **Upstream `grc_tests` fix:** not on `main` as of `862edb76b` (a second
  plain `make test` on 26.04 failed `grc_tests`, 2026-10-18). When it lands,
  remove the builder's `git clean` step and its doc bullet in a new tag.
- **#8239 (Thrift on `main`):** open. When fixed, `main` on 26.10 should
  give 42 components; consider adding the Thrift packages to Step 1 only if
  the developers keep ControlPort/Thrift (user, 2026-10-19). An existing
  `build/` keeps `ENABLE_CTRLPORT_THRIFT=OFF` cached.
- **Qt6 on 24.04 / 26.04:** `gr-qtgui` on `main` waits for Qwt for Qt6
  there; `gnuradio-companion --qt` on `main` doesn't work there (see Useful
  facts). Nothing for the scripts to do.
- **Step 1 log order:** possible `v3.1` fix (see Key decisions).
- **Builder `~/.profile` message (`v3.1`):** prints the `echo ... >>
  ~/.profile` command the docs give instead of "add this line" (user,
  2026-10-23: "It would be simpler to give the echo style command"); skips
  it if `~/.profile` already has the line; drops the per-terminal fallback
  (as in the docs). Committed in `d9197fa`; not run yet.
- **Test counts:** three of the four extra `main` tests on 26.04 vs 24.04
  (271 vs 267, `v2.0`) are unexplained; `main` on 24.04 not run since
  `v2.0`.
- **Docs, leftover-library command (for `v3.1`; user, 2026-10-23: "save it
  for v3.1"):** the dangling `.so.3.11.0git` links (2026-10-12) came from
  switching `main` → `maint-3.10` without clearing the old `/usr/local`
  prefix; `v3.0`'s "Changing branches" (`rm -rf ~/gnuradio-pkg
  ~/gnuradio/build`) rules that out, and each `main` install re-points the
  links to the kept version (my reasoning, not checked on a `main`
  rebuild). Remaining risk: the command asks whichever
  `gnuradio-config-info` is first in `PATH`. Change in the wiki draft and
  README: use `~/gnuradio-pkg/bin/gnuradio-config-info` in both lines (if it
  fails, the empty pattern lists nothing, so nothing is removed).
- **26.10 is interim** (~9 months, to about July 2027); the wiki page
  promises 24.04 and 26.04. When Ettus publishes a `stonking` build, Step 1
  picks it up by itself.
- **Summary for the GRC developer** (Claude Docs, "GNU Radio main with Qt6
  on Ubuntu 26.10",
  https://claude.ai/code/artifact/76d346a7-1652-47de-a7c8-f8ad69f46288;
  shared by the user 2026-10-18): describes the 26.10 Qt6 trial at
  `862edb7`; not updated for `v3.0`.
- **Fedora 44 trial (GMKtec, 2026-10-16, finished: "that's all I want to do
  on Fedora"):** neither script runs on Fedora. By hand ("option 1"):
  Fedora's UHD 4.9.0.1 (`uhd uhd-devel uhd-tools uhd-firmware`) + `dnf
  builddep gnuradio`, `maint-3.10` with cmake: 41 components (no Thrift:
  `builddep` doesn't bring `thrift-devel` / `python3-thrift`), Python in
  `/usr/local/lib64/python3.14/site-packages` (found by Fedora's Python),
  `qa_fastnoise` flaky (fixed on `main` by `aee9fd3f7`, `places=2` →
  `delta=0.05`; doesn't cherry-pick onto `maint-3.10`; by hand: 269/269).
  B200mini and PlutoSDR loopbacks and RTL-SDR stereo FM worked; no udev
  change needed. Unknown: whether the `ld.so.conf.d` line was needed, the
  `dnf search soapy` list.
- **Fedora support in the project (proposed by me 2026-10-16; not
  decided; talk to the developers first).**
  - Step 1: dispatch on `ID` in `/etc/os-release`; Ubuntu path unchanged.
    Fedora: `dnf builddep gnuradio`; `dnf install uhd uhd-devel uhd-tools
    uhd-firmware python3-QtPy python3-pyqtgraph python3-matplotlib
    python3-pytest thrift-devel python3-thrift`; SoapySDR modules from
    `dnf`'s list of `soapy-*` (no metapackage; `soapy-uhd` can stay, same
    UHD); no deb-src, PPA, or `uhd_images_downloader`. Conflict check with
    `rpm -q gnuradio gnuradio-devel python3-gnuradio`. UHD 4.9.0.1 vs 4.11:
    document it.
  - Builder: `rpm -q uhd-devel` instead of `dpkg-query libuhd-dev`;
    `lib64/python3*/site-packages/...` in `INSTALL_DIR_PATTERNS` and in
    `setup_env.sh`'s search. `qa_fastnoise` would stop every Fedora
    `maint-3.10` build: (a) upstream backport of `aee9fd3f7` (my
    preference), (b) an option to skip named tests, or (c) document the
    one-line edit.
  - Docs: Fedora notes in Step 1; `lib64` in the removal and
    leftover-library commands; `python3-QtPy` spelling, fewer Soapy
    modules, no udev change.
  - Testing: clean Fedora for every change; Ubuntu must not change. Fedora
    45 around April 2027.

## Drafts

### Thrift issue for `gnuradio/gnuradio` (drafted 2026-10-17; posted as #8239 on 2026-10-18)

Paste each part into the matching field of GNU Radio's bug report form.

~~~~markdown
**Title:** Thrift support can't be enabled on main: FindTHRIFT.cmake uses the old gr_python_check_module call, and thrift_server_template.h doesn't compile

**What happened?**

On `main`, ControlPort's Thrift back-end is never enabled, even with every Thrift package installed. cmake doesn't list Thrift as disabled; it's silently left out.

There are two bugs, both from 24e9f2b7e ("cmake: Add comprehensive cross-platform installer infrastructure"):

1. **cmake never finds Thrift.** That commit changed `GR_PYTHON_CHECK_MODULE` in `cmake/Modules/GrPython.cmake` to take keyword arguments (`DESC`, `MODULE`, `CHECK`, `VAR`). It didn't update the call in `cmake/Modules/FindTHRIFT.cmake:63`, which still passes them by position:

   ```cmake
   gr_python_check_module("Thrift" thrift "1" PYTHON_THRIFT_FOUND)
   ```

   As a result `PYTHON_THRIFT_FOUND` is never set, so `THRIFT_FOUND` stays false and `ENABLE_CTRLPORT_THRIFT` defaults to `OFF`. Because the search is quiet, cmake prints nothing after `thrift looking for version 0.13`. Fix:

   ```cmake
   gr_python_check_module(DESC "Thrift" MODULE thrift CHECK "1" VAR PYTHON_THRIFT_FOUND)
   ```

2. **With Thrift enabled, `gnuradio-runtime` doesn't compile.** The same commit changed `TserverBase* i_impl()` to `auto i_impl()` in `gnuradio-runtime/include/gnuradio/thrift_server_template.h` (lines 42 and 158). That function overrides `virtual TserverBase* i_impl() = 0;` in `thrift_application_base.h:108`, so the build fails with "conflicting return type". Changing both lines back to `TserverBase* i_impl()`, as on `maint-3.10`, fixes it.

The first bug hides the second: since Thrift is never enabled, nothing compiles that code.

With both changes, `main` builds with Thrift: `gnuradio-config-info --enabled-components` lists `* thrift` (42 components instead of 41), and `make test` passes 273/273. ControlPort itself was not exercised at run time.

One more thing: after the cmake fix, an existing build directory still has `ENABLE_CTRLPORT_THRIFT:BOOL=OFF` cached. A rebuild needs `-DENABLE_CTRLPORT_THRIFT=ON` or a fresh build directory.

**System Information**

Ubuntu 26.10 (clean install), x86_64. Thrift 0.23.0 (`libthrift-dev`, `thrift-compiler`, `python3-thrift`). The same Thrift gap is seen on `main` on Ubuntu 26.04 (Thrift 0.22.0).

**GNU Radio Version**

3.11 (main)

**Specific Version**

v3.11.0.0git-1210-g862edb76

**Steps to Reproduce the Problem**

1. Install Thrift: `sudo apt-get install libthrift-dev thrift-compiler python3-thrift`
2. Configure `main`: `cmake ..`
3. `gnuradio-config-info --enabled-components` (after install) has no `* thrift`. `CMakeCache.txt` has `THRIFT_BIN`, `THRIFT_INCLUDE_DIRS` and `THRIFT_LIBRARIES` set, but no `PYTHON_THRIFT_FOUND`, and `ENABLE_CTRLPORT_THRIFT:BOOL=OFF`.
4. Apply the cmake fix above and configure with `-DENABLE_CTRLPORT_THRIFT=ON`. `make` then fails as shown below.

**Relevant log output**

```
gnuradio-runtime/include/gnuradio/thrift_server_template.h:158:6: error: conflicting return type specified for 'auto thrift_server_template<TserverBase, TserverClass, TImplClass>::i_impl() [with TserverBase = rpcserver_base; TserverClass = rpcserver_thrift; TImplClass = rpcserver_booter_thrift]'
  158 | auto thrift_server_template<TserverBase, TserverClass, TImplClass>::i_impl()
      |      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gnuradio-runtime/include/gnuradio/thrift_application_base.h:108:26: note: overridden function is 'TserverBase* thrift_application_base<TserverBase, TserverClass>::i_impl() [with TserverBase = rpcserver_base; TserverClass = rpcserver_booter_thrift]'
  108 |     virtual TserverBase* i_impl() = 0;
```

Optional last line: "I can open a PR with these two changes."
~~~~

### rc1 test request for the other tester (drafted 2026-10-19)

For the user to send to jesternofool. Step 3 offers a plain clone first, the
fork second (the user may swap them).

~~~~markdown
Hi! Thanks again for testing `v2.3`. If you have time, I'd like your help with the next version, `v3.0`. It's not on the wiki yet; this is a release candidate, `v3.0-rc1`.

**What's new:** neither script is run with `sudo` any more. Step 1 calls `sudo` itself, only for the commands that install packages, and asks for your password once. Step 2 installs GNU Radio into `~/gnuradio-pkg` in your home directory, with no root at all, and writes `~/gnuradio-pkg/setup_env.sh`. One line in `~/.profile` then makes GNU Radio available in every terminal and from the desktop.

**What I'd like tested:** a **clean Ubuntu 24.04**, building **`maint-3.10`**.

```bash
# 1. Download the two rc1 scripts
mkdir -p ~/gr-v3 && cd ~/gr-v3
for f in gnuradio_dependencies_installer.py gnuradio_clone_builder.py; do python3 -c "import sys, urllib.request; urllib.request.urlretrieve(sys.argv[1] + sys.argv[2], sys.argv[2])" https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v3.0-rc1/ $f; done

# 2. Step 1, as yourself (NOT with sudo)
python3 gnuradio_dependencies_installer.py 2>&1 | tee step1.log

# 3. Get the source; a plain clone is fine for testing:
cd ~ && git clone https://github.com/gnuradio/gnuradio.git && cd gnuradio && git checkout maint-3.10
#    (or clone your fork, then: git remote add upstream https://github.com/gnuradio/gnuradio.git
#     && git fetch upstream && git checkout maint-3.10)

# 4. Step 2, also as yourself (NOT with sudo)
cd ~/gr-v3 && python3 gnuradio_clone_builder.py 2>&1 | tee step2.log

# 5. Set up the environment, then log out of the desktop and back in
#    (closing the terminal isn't enough)
echo '. "$HOME/gnuradio-pkg/setup_env.sh"' >> ~/.profile
```

After logging back in, open a terminal:
```bash
uhd_config_info --version
gnuradio-config-info --version --prefix
gnuradio-config-info --enabled-components | tr ';' '\n' | wc -l
```

**Please report:**
1. Whether Step 1 finished, and the UHD version. It should be 4.11 from the Ettus PPA.
2. The `make test` result. I expect 269/269.
3. The version, the prefix (should be `/home/<you>/gnuradio-pkg/`), and the component count (I expect 42).
4. Whether GNU Radio Companion shows up in Activities and runs a flowgraph when started from there.
5. Which devices work: HackRF, LimeSDR Mini, Airspy R2 through Soapy, and the B200mini through UHD, including transmit if you can.
6. Optional: whether an out-of-tree module builds against it:
   ```bash
   cd /tmp && gr_modtool newmod test && cd gr-test && mkdir build && cd build && cmake .. && make
   ```
7. Anything odd in `step1.log` or `step2.log`.

**One warning:** if a GNU Radio command ever says "command not found", Ubuntu may suggest `sudo apt install gnuradio`. Don't do that! It installs Ubuntu's older GNU Radio next to this one. It only means the `setup_env.sh` line hasn't been run in that terminal.

Thanks!
~~~~

### QT GUI Range slider issue for `gnuradio/gnuradio` (drafted 2026-10-20; not posted)

**Not to be posted** (user, 2026-10-21): the developers are aware of the Range slider issue and have chosen not to create an issue at this time. Text kept for reference.

Laid out like GNU Radio's bug report form. Log section: the user's traceback
from `--qt` (2026-10-20), with the home prefix shortened to `<prefix>`; the
fix is untested.

~~~~markdown
**Title:** QT GUI Range slider: clicking or dragging raises AttributeError with PyQt6 (`QMouseEvent.x()`)

**What happened?**

On `main` (Qt6), clicking or dragging the slider of a QT GUI Range block in a running flowgraph raises:

```
AttributeError: 'QMouseEvent' object has no attribute 'x'
```

and the slider doesn't move.

The cause is in `gr-qtgui/python/qtgui/range.py.cmakein`, class `Slider(QSlider)`. Its `mousePressEvent` and `mouseMoveEvent` still use the Qt5 calls `event.x()` and `event.y()` (lines 203, 205, 214 and 216 at `ec1bf153c`). Qt6 removed them from `QMouseEvent`; the Qt6 way is `event.position().x()` and `event.position().y()`. For example:

```python
new = self.minimum() + ((self.maximum() - self.minimum()) * event.position().x()) / self.width()
```

`maint-3.10` has the same code, but it runs on PyQt5, so it works there.

**System Information**

Ubuntu 26.10, x86_64. Qt 6.11.2, PyQt6 6.11.0 (`python3-pyqt6`), Qwt for Qt6 6.3.0 (`libqwt-qt6-dev`). GNU Radio built from source with `gr-qtgui` enabled.

**GNU Radio Version**

3.11 (main)

**Specific Version**

v3.11.0.0git-1216-gec1bf153

**Steps to Reproduce the Problem**

1. In GRC, make a flowgraph with a QT GUI Range block (GUI hint: slider, or counter + slider) controlling any parameter.
2. Run the flowgraph.
3. Click on the slider, or drag it.

**Relevant log output**

```
Traceback (most recent call last):
  File "<prefix>/lib/python3.14/site-packages/gnuradio/qtgui/range.py", line 206, in mousePressEvent
    new = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
                                                                ^^^^^^^
AttributeError: 'QMouseEvent' object has no attribute 'x'
```

Optional last line: "I can open a PR with this change."
~~~~
