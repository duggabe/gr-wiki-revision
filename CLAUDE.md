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

Current release: **`v3.0`** (GitHub "Latest", 2026-10-21). Favour clarity,
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
- **Tags** are never moved; fixes get a new tag (next: `v3.0-rc1`,
  then `v3.0`; user, 2026-10-19).
- **GitHub Releases** are created or edited only on the user's request.
  Every Release must have **both scripts attached**, because the docs
  download from
  `https://github.com/duggabe/gr-wiki-revision/releases/latest/download/<file>`.
- **The wiki draft leads; the README follows.** `wiki-draft-download-section.mediawiki`
  (MediaWiki, gitignored, local only) is the user's text. The user edits in
  MediaWiki; I convert to Markdown for the README. The README is the draft
  section by section, plus README-only parts: a short repo intro, the two
  options tables (keep in sync with the scripts' argparse help), and the
  "Releases" section. The options tables' "Option" header is padded with 40
  `&nbsp;` so GitHub doesn't wrap the options (`239bd31`; checked with
  GitHub's renderer, and the user confirmed it looks good, 2026-10-15).
  Keep the padding if the tables change.
- **The user updates the live wiki page by total replacement** with the
  whole local draft. So keep the draft complete and current. (Drafting on
  User_talk:Duggabe first was dropped 2026-10-19, but the user is **using it again for the `v3.0` revision**,
  2026-10-21: "Wait until I've made my changes"; then ask for a paste and update the local draft from it.)
  **Done** (user, 2026-10-21): the user copied the Talk page into the local draft. **Download section changed to the `for` loop** (user asked, 2026-10-21: "The chained python3 calls would hang sometimes"; my guess at the cause: a paste ending on a trailing `&&` leaves bash waiting at its `>` prompt): `mkdir -p ~/gr-installers && cd ~/gr-installers`, then one `for f in ...; do python3 -c "...urlretrieve(sys.argv[1] + sys.argv[2], sys.argv[2])" https://github.com/duggabe/gr-wiki-revision/releases/latest/download/ $f; done` line. Tested by me: it downloads both scripts, identical to `v2.4` (the current latest). The README follows at release time. **The two `main`/Qt6 sentences (`--qt`, "No GUI") were lost** when the Talk page was copied over the draft; **restored** (user: "restore 1", 2026-10-21). My other two suggestions (fuller "command not found" causes with the per-terminal fallback; "add a line to your `~/.profile` that runs ..." wording) not taken. Why for the first (user, 2026-10-21): "I wanted to force the user to log out and back in rather than suggest a way to limp along without doing what needs to be done": the docs give no per-terminal fallback. **Then both made** (user: "yes, make both changes", 2026-10-21): "command not found" now also names "or the line isn't at the end of `~/.profile`" (no fallback), and the `echo` lead-in reads "to add a line to your `~/.profile` that runs `~/gnuradio-pkg/setup_env.sh`:".
- The wiki is behind Cloudflare and can't be fetched from here: ask the user
  to paste content.
- **The wiki page URL** (user, 2026-10-21): https://wiki.gnuradio.org/index.php?title=Building_GNU_Radio_from_Source_Code .
  Linked from the `v3.0` Release notes' Quick start; the README intro's page name becomes a link at the `v3.0` README conversion (user agreed, 2026-10-21).

## Current state (2026-10-17)

- `main` pushed; `v2.4` released.
- `v2.4` tested on both releases: 24.04 (with pytest by hand, 269/269,
  2026-10-15) and a clean 26.04 GMKtec (all passed, incl. B200mini /
  PlutoSDR transmit and RTL-SDR, 2026-10-17). Transmit, "`v2.3` on 26.04",
  and the RTL-SDR flowgraph items closed.
- **On hold** (user, 2026-10-16): "I'm going to wait for the developers
  decisions before I do anything else" (where the scripts live, Fedora
  support, the `qa_fastnoise` backport).
- Live wiki page = local draft = README, including
  `v2.4`'s `python3-pytest` line (user replaced both wiki pages,
  2026-10-15). None of them has test results.
- GitHub Releases: `v2.4` (Latest), `v2.3`, `v2.2`, `v2.1`, `v2.0`, all with both
  scripts attached. `v2.4`'s "Tested" has the 24.04 run and (added
  2026-10-17) the clean 26.04 GMKtec run; it says `maint-3.10`, `gr-uhd`, `gr-iio`,
  and `gr-soapy` for the RTL-SDR, all confirmed by the user (2026-10-17). The `v1.2` Release was deleted 2026-10-13 (tags kept);
  the backup of its notes was deleted by the user 2026-10-15.
- Tracked files: the two scripts, `README.md`, `LICENSE` (CC BY-SA 4.0, by
  choice although CC advises against it for software), `.gitignore`,
  `CLAUDE.md`.

- **`v3.0` Step 1 coded** (2026-10-19, uncommitted, not run for real): runs as
  the normal user (`sudo env DEBIAN_FRONTEND=noninteractive ...` for the root
  commands, one `sudo -v` first; still works under `sudo`); the sources-file
  edit through `sudo cp -p` + `sudo tee`; `ppa_has_build()` fetches the PPA's
  `dists/<codename>/Release` (404: warning, no `add-apt-repository`, Ubuntu's
  UHD; other errors abort); aborts with the `add-apt-repository --remove`
  fix if a PPA entry names a release with no build; `<Qt6 packages>`
  placeholder, installed only if `apt-cache show libqwt-qt6-dev` finds it.
  Dry runs checked by me on the LENOVO (resolute: PPA kept) and with a fake
  `stonking` os-release (PPA left out; stale entry caught).
- **`v3.0` builder coded** (2026-10-19, uncommitted, not run for real):
  `--prefix`, default `~/gnuradio-pkg`; `owns_prefix()` (the prefix or its
  nearest existing parent belongs to the build user) picks plain `make
  install` with no `ldconfig`, else `sudo make install` + `sudo ldconfig`
  (e.g. `--prefix /usr/local`); after a user-prefix install it writes
  `<prefix>/setup_env.sh` (PATH = `bin`, PYTHONPATH = the parents of
  `lib*/python3*/{site,dist}-packages/gnuradio`, LD_LIBRARY_PATH = the dirs
  with `libgnuradio-runtime.so*`; each a `case` guard so sourcing twice adds
  nothing) and prints the `~/.profile` line and the `sudo apt install
  gnuradio` warning; stale-dir check in the prefix and `/usr/local`; warns
  if a GNU Radio is still installed in `/usr/local`. Checked by me: dry runs
  on the LENOVO (default prefix: warning shown, `make install`; `/usr/local`:
  sudo steps), and `setup_env.sh` on a fake ASUS-like prefix sourced twice
  with `sh`. Not set (my note): `CMAKE_PREFIX_PATH` for out-of-tree modules
  (cmake should find the prefix through `PATH`; to check with a
  `gr_modtool` module build in rc1).
- **`v3.0` wiki draft written by me** (2026-10-19, for the user to review;
  `v2.4` text kept as `wiki-draft-download-section-v2.4.mediawiki`, also
  gitignored): goals + Step 2 sentence mention `~/gnuradio-pkg`; "Before you
  start" gains the old three-step `/usr/local` removal for v2.x installs
  (the `rm -rf` list stays in sync with `INSTALL_DIR_PATTERNS`); Step 1 run
  without `sudo`, PPA check (26.10 example), Qt6 bullet; Step 2 without
  `sudo`, `make install`, `--prefix` bullet, "with or without sudo" bullet
  and "(Version v2.0 ...)" dropped; new sections "Setting up the
  environment" (`~/.profile` line, log out, "command not found" /
  **DON'T!** (was "don't!"; capitals like the builder, user, 2026-10-20), link to [[ModuleNotFoundError]]) and "The main branch and Qt6"
  (26.10 has `gr-qtgui`; Thrift with #8239); "Changing branches..." now `rm
  -rf ~/gnuradio-pkg ~/gnuradio/build`, plus `grc_setup_freedesktop
  uninstall` and the `~/.profile` line for full removal; leftover-library
  commands in `~/gnuradio-pkg/lib` without sudo/ldconfig; "Checking" adds
  `--prefix` and the desktop entry. Intro rewording (decision 6): not done,
  waiting for the user's wording. README not updated yet.
  **The user pasted the whole `v3.0` draft, unaltered, into the live wiki
  page** (user, 2026-10-19: "I pasted the entire text unaltered"; my reading:
  the `v3.0` draft, not the `v2.4` backup); the `#` links work (user). So the
  live page describes `v3.0` while `releases/latest` still gives `v2.4`
  (mismatch until the `v3.0` Release, or until the `v2.4` text goes back).
  **Then the user put the `v2.4` text back** (from
  `wiki-draft-download-section-v2.4.mediawiki`; user, 2026-10-19): live page =
  `v2.4` again, matching `releases/latest`. The `v3.0` draft goes live only
  after the `v3.0` Release.
- **rc1 test by the other tester** (user, 2026-10-19: jesternofool "is
  available to help again and can install a clean OS much faster"): my
  suggestion, a **clean 24.04 with `maint-3.10`** first (the PPA / Boost /
  `add-apt-repository` half of Step 1 and Python 3.12, untested in `v3.0`;
  compares with the `v2.3` run; the tester's HackRF / LimeSDR Mini / Airspy R2 /
  B200mini from a home prefix); then `main` from the fork on 24.04, then a
  clean 26.04; the user keeps 26.10 on the ASUS. Message drafted (full text
  under "Drafts"); sent (results came back). **First results** (tester's
  report via the user, 2026-10-20; presumably clean 24.04 + `maint-3.10` as
  asked, my reading): **UHD 4.11.0.0-0ubuntu1~noble3** (PPA path works on
  24.04), **`make test` 269/269**, **3.10.12.0, prefix
  `/home/<tester>/gnuradio-pkg`**, **GRC starts from Activities and works**;
  **RTL-SDR and Airspy R2 work**; **LimeSDR Mini and HackRF work, receive
  and transmit**; **B200mini works, receive and transmit, through UHD**
  (tester via the user, 2026-10-20). All the others through Soapy (tester).
  **42 components** (tester via the user, 2026-10-20). **Out-of-tree
  module built** (step 6: `make` reached 100%, last line "Built target
  copy_module_for_tests"; tester via the user, 2026-10-20). **Tester's rc1
  test on 24.04 passed.** Not reported: log oddities.
  README: intro now says `v2.4` (was `v2.3`), and "The next release will be
  `v3.0`" replaces "Further fixes will be tagged `v2.5`" (user asked).
- **First real run of the `v3.0` scripts** (ASUS, 26.10, not clean: after
  the manual prefix trial, `~/gnuradio-pkg` and `~/gnuradio/build` removed
  first; scripts from `main` at `169a139` by raw URL, no tag yet, my
  suggestion): **Step 1 finished, UHD 4.9.0.1-1.4** (user, 2026-10-19; run as
  the normal user, my reading). **The no-PPA warning and the Qt6 packages are there** (user, 2026-10-19; my reading: the `step1.log` grep and `dpkg -l` I suggested). Builder (default prefix `~/gnuradio-pkg`, presumably `maint-3.10`, my reading): **`make test` 269/269** (user, 2026-10-19), now with the full Qt6 list installed: step (5) of the Qt6 trial passes (my reading). **`~/gnuradio-pkg/setup_env.sh` written, with the three `case` lines** (user, 2026-10-19), so `make install` into the prefix ran (my reading). `step2.log`: the user couldn't find it (run without `tee`, my guess). **GRC started from the desktop works** (user, 2026-10-19), after the `~/.profile` line; but the user **"had to make setup_env.sh executable before it worked"**. Then (user): "I may have made the setup_env executable before I tried the log out", so probably not needed (sourcing with `.` needs only read permission, my understanding); **confirmed not needed**: after `chmod -x` and logging in again, it works (user, 2026-10-19: "the chmod -x works"; my reading: GRC from the desktop). **GRC was already in Activities** (user, 2026-10-19: "no search was needed"): the menu entry comes with the prefix install (my guess: GNU Radio's `post-install` component, xdg-utils into `~/.local/share/applications` for a non-root install; possibly left from the manual trial's install, same mechanism). **`~/.local/share/applications/gnuradio-companion.desktop` exists** (user, 2026-10-19). So removing a prefix install = `rm -rf ~/gnuradio-pkg` plus the GNU Radio files under `~/.local/share` (which others, e.g. MIME/icons, not checked); for the docs. The desktop GRC **comes up in GTK mode** (user, 2026-10-19; the default, my reading; `--qt` only from a terminal). **A QT GUI Time Sink flowgraph works from the desktop GRC** (user, 2026-10-19). **First real `v3.0` run passed** on the ASUS (not clean). **Out-of-tree module** (2026-10-20, same install, `maint-3.10`): `gr_modtool newmod test`, then `cmake ..` and `make` in `gr-test/build` **finished with no errors** (user): cmake finds the prefix without `CMAKE_PREFIX_PATH` (my reading: through `PATH`), so `setup_env.sh` needs nothing more. B200mini and PlutoSDR loopbacks work too (see Hardware). **"Changing branches" (`v3.0` steps: `rm -rf ~/gnuradio-pkg ~/gnuradio/build`), then `main`** (`git checkout main && git pull`, builder from `~/gr-v3`): **`make test` 275/275** (user, 2026-10-20), two more than the 273 at `862edb76b` (my guess: tests added in the 6 upstream commits since). Version **v3.11.0.0git-1216-gec1bf153**, **41 components** (user, 2026-10-20), as expected: `gr-qtgui` with Qt6, no Thrift (#8239; whether the grep showed `gr-qtgui` not stated). **"python3 crashed in the middle of the tests"** (user, 2026-10-20), although all 275 passed: presumably Ubuntu's crash dialog (apport) for a Python process started by a test (my reading); which test and which signal not known yet. **"It has done it before, but seems random"** (user, 2026-10-20): so not new with `-1216`; on which builds / branches before not stated. **Identified** (user's `/var/crash/_usr_bin_python3.14.1000.crash`, 2026-10-20 08:47): `SIGABRT` in a `multiprocessing.forkserver` child of **`gnuradio-runtime/python/gnuradio/gr/qa_uncaught_exception.py`**. That test (read by me) runs a flowgraph in a child `Process` whose block throws with `catch_exceptions=False` and asserts the child **died** (`exitcode` not None): the abort is deliberate, and the test passes because of it. Ubuntu's apport reports the abort; "random" presumably because apport doesn't report every repeat (my guess). Not a bug in GNU Radio or the scripts. **Suppressing the notice works** (user, 2026-10-21): the user chose the dialog's option to suppress the notice for the same condition; first said later runs "did give that notice", then corrected: "IIRC I did not get the notice on repeated runs". That fits "seems random": the dialog appears until suppressed (or on a new install), my reading. Docs bullet unchanged. **Docs note added to the `v3.0` draft** (user: "yes", 2026-10-20): a Step 2 bullet after the logs bullet, "During `make test`, Ubuntu may report that `python3` crashed. That is the test `qa_uncaught_exception`, which crashes a process on purpose ... It can be ignored." **GRC from the desktop on `main`** (user, 2026-10-20): clicking with the mouse gives **`AttributeError: 'QMouseEvent' object has no attribute 'x'`** (Qt6 removed `QMouseEvent.x()`; PyQt6 code needs `position().x()`, my note). Clicked: **the transmit and receive gain sliders** (user), i.e. QT GUI Range widgets in the running flowgraph. **Cause (read by me on `main` at `ec1bf153c`, the ASUS's commit):** `gr-qtgui/python/qtgui/range.py.cmakein`, class `Slider(QSlider)`, `mousePressEvent` (lines 203, 205) and `mouseMoveEvent` (214, 216) use `event.x()` / `event.y()`, which PyQt6 doesn't have (`event.position().x()`). Same code on `maint-3.10` (PyQt5, works). No existing issue found by `gh search`. **Same error from `gnuradio-companion --qt`** (user's terminal output, 2026-10-20), running `~/GRdev/bpsk_file_transfer_stage6.py` with the B200mini (`UHD_4.9.0.1-1.4`, USB 3, `Boost_109000`): traceback `File "/home/barry/gnuradio-pkg/lib/python3.14/site-packages/gnuradio/qtgui/range.py", line 206, in mousePressEvent` (installed file; line 203 in the `.cmakein`), then a harmless-looking `GLib-CRITICAL ... g_main_context_pop_thread_default: assertion 'stack != NULL' failed` from gnuradio-companion. **The loopback file transfer worked** (user, 2026-10-20), sliders aside. **Second builder run on `main`** (no changes): `make_test.log` **275/275** (user, 2026-10-20). On 26.10 this doesn't exercise the `git clean` step's purpose: with `gr-qtgui` the leftover `test_*_qt_gui_workflow.py` files import fine (my reading); that matters on 24.04 / 26.04 `main`. **Full removal checked** (user, 2026-10-20): `~/gnuradio/build/grc/scripts/freedesktop/grc_setup_freedesktop uninstall`, then the `~/.local/share` find count is **0** and GRC is gone from Activities: the draft's removal step works. **ASUS checks before its clean reload: all done.** Upstream bug, not the scripts. **Issue drafted** (user asked, 2026-10-20; full text under "Drafts"; not posted as far as I know). Traceback not pasted. GRC not reported yet. Files under `~/.local/share` (user's `find`, counted by folder, 2026-10-19): 1 in `applications`, 1 `apps` + 2 `mimetypes` icons in each of 7 sizes (16-256) for both the `gnome` and `hicolor` themes, 1 in `mime/application`, 1 in `mime/packages`: 45 files. Source (read by me, `maint-3.10`): `grc/scripts/freedesktop/CMakeLists.txt` runs `build/grc/scripts/freedesktop/grc_setup_freedesktop install` at `make install` (xdg-utils; per-user when not root); the same script takes **`uninstall`**, and it exists only in the build dir (not installed). So the `v3.0` removal (my proposal): `~/gnuradio/build/grc/scripts/freedesktop/grc_setup_freedesktop uninstall`, then `rm -rf ~/gnuradio-pkg ~/gnuradio/build`.

## Machines

| Machine | Ubuntu | State |
| --- | --- | --- |
| LENOVO desktop (working machine, `~/gr-wiki-revision`) | 26.04 | 16 cores, 15 GiB RAM, 4 GB swap. Reloaded 2026-10-08. UHD 4.11 from the PPA (only UHD; `libuhd4.9.0` removed 2026-10-12). `~/gnuradio` = plain clone of `gnuradio/gnuradio` on `maint-3.10`, GNU Radio 3.10.12.0 in `/usr/local`, 42 components. 13 SoapySDR modules (`v2.2` Step 1 run for real). `v2.3`'s Boost step not run here (would add 4 small metapackages). Hardware: USRP B200mini (serial 315C7B7), RTL-SDR (an RTL-SDR.COM v3), PlutoSDR. **The same three SDRs in all of the user's tests** (user, 2026-10-17), on every machine. |
| GMKtec (clean-install test machine) | reloaded per test | **Clean 26.04 for the `v3.0-rc1` 26.04 test** (user, 2026-10-20: "it is clean"; the user first said "the 26.04 is on the ASUS", but the prompt shows `barry@GMKtec`; my reading: the GMKtec). rc1 builder, `maint-3.10` (my reading): **`make test` 269/269** (user, 2026-10-20). After the `~/.profile` line and a logout (my reading): **3.10.12.0, `/home/barry/gnuradio-pkg/`, 42 components** (user, 2026-10-20). **GRC from Activities works with a QT GUI Time Sink** (user, 2026-10-21; `maint-3.10`, Qt5, with PyQt6 also installed). B200mini, PlutoSDR, RTL-SDR work (see Hardware): **`maint-3.10` part passed.** Then "Changing branches" and `main`: **`make test` 274/274** (user, 2026-10-21), as expected (26.10's 275 minus `qa_qtgui`). **v3.11.0.0git-1216-gec1bf153, 40 components** (user, 2026-10-21), as expected (no `gr-qtgui`, no Thrift). **`gnuradio-companion --qt` fails: `ModuleNotFoundError: No module named 'PyQt6.QtSvg'`** (user, 2026-10-21): with the PyQt6 that `python3-pyqtgraph` pulls in but no `python3-pyqt6.qtsvg`, the Qt front end picks PyQt6 and stops at once (my reading). With `python3-pyqt6.qtsvg` added (GMKtec 2026-10-18) it locked up instead. So on 26.04 `main`, `--qt` doesn't work either way; with rc1 it at least fails with a clear error rather than hanging (my reading). Not caused by rc1: `v2.4` installs the same packages. `main`'s `grc/gui_qt/` imports PyQt6 directly (`Utils.py`: `from PyQt6.QtSvg import QSvgGenerator`; read by me at `7a45079b1`), so keeping PyQt6 off wouldn't help: **no rc2 for this**. **GRC from Activities (GTK) on `main`: "blocks associated with qtgui are missing"** (user, 2026-10-21), as expected without `gr-qtgui`; a flowgraph with the default Options "QT GUI" fails at run time (`ImportError: cannot import name 'qtgui' from 'gnuradio'`, user's `~/GRdev/null_sink_test.py`); **with Generate Options "No GUI" it works** (user, 2026-10-21). **GMKtec clean 26.04 rc1 test: all passed** (`--qt` and QT GUI on `main` unavailable on 26.04, upstream/expected, not the scripts). **Draft sentence added** (user: "yes, add it to the draft", 2026-10-21) to "The main branch and Qt6": "There, use GNU Radio Companion's default front end; `gnuradio-companion --qt` does not work on those releases with `main`." **Second sentence added** (user: "yes, add the No GUI sentence", 2026-10-21): "A flowgraph's Options block must then be set to "No GUI", since the default, "QT GUI", needs `gr-qtgui`." **UHD 4.11.0.0-0ubuntu1~resolute3** (user, 2026-10-20): the PPA path on 26.04. PPA file, Qt6 note, no PyQt6 not reported yet. `grep -i qt6 step1.log` showed only the two plan lines (user), but **the Qt6 `note:` line is there** (user's `tail -15`, 2026-10-20; why the grep missed it, not known). Same tail: 13 SoapySDR modules (the expected 26.04 set), `uhd_images_downloader`, "Installed: UHD 4.11.0.0-0ubuntu1~resolute3, from the Ettus PPA", "Done.". **Log order (seen by me in that tail):** all of Step 1's own `$ ...` and `note:` lines come together at the end, after apt's output: Python block-buffers `print` when stdout is a pipe (`| tee`), while apt writes straight to it. Cosmetic, but it makes the log hard to read; fix candidate: `sys.stdout.reconfigure(line_buffering=True)` (the builder flushes after each logged line, so mostly fine). **Not fixed** (user, 2026-10-21: "no log order fix"): no rc2; `v3.0` goes on `80b6b8f`. **`python3-pyqt6` 6.10.2-2build5 `ii`** (user, 2026-10-20). Cause (checked by me on the LENOVO, 26.04): `python3-pyqtgraph` Depends `pyqt6-dev-tools | pyqt5-dev-tools` (and `python3-pyqt6 | python3-pyqt5`); `build-dep gnuradio` brings `python3-pyqt5` but not `pyqt5-dev-tools`, so apt picks `pyqt6-dev-tools`, which Depends `python3-pyqt6`. The LENOVO has the same (`pyqt6-dev-tools` + `python3-pyqt6` `ii`, `pyqt5-dev-tools` `un`). Same order in `v2.4`, so **not new in `v3.0`**: the clean 26.04 `v2.4` GMKtec of 2026-10-17 very likely had PyQt6 too, and my earlier "absent until installed by hand" / "PyQt6 alone makes `--qt` lock up" reading is doubtful: the 2026-10-18 hand install may have added only `python3-pyqt6.qtsvg` (my guess). Deciding test: `main` `--qt` on this GMKtec. 4 cores, 10 GiB. Clean 24.04 with `v2.2` on 2026-10-14 lost `gr-uhd` (the Boost problem); reloaded the same day with a clean 24.04 and `v2.3`: all passed, 42 components, B200mini / RTL-SDR / PlutoSDR tested (see Test results). **Reloaded with Fedora 44** (user, 2026-10-16) for a Fedora trial; see "Fedora 44 trial" under Open items. **Reloaded with a clean 26.04** (user, 2026-10-17) for the `v2.4` test; the Fedora unknowns can no longer be checked there. |
| Laptop (hostname `ASUS`) | 26.10 | **Reloaded with a clean 26.10 for the formal `v3.0-rc1` test** (user, 2026-10-20); the scripts are unchanged since the `v3.0-rc1` tag (checked by me), so the test uses the rc1 raw URLs. **rc1 Step 1 finished, UHD 4.9.0.1-1.4** (user, 2026-10-20). The no-PPA warning is in `step1.log`, **no `ettusresearch` file in `/etc/apt/sources.list.d/`** (first clean-machine proof that the PPA check leaves no stale entry), `libqwt-qt6-dev` `ii` (user, 2026-10-20). Builder (`maint-3.10`, default prefix, `tee step2.log`): **`make test` 269/269** (user, 2026-10-20). After the `~/.profile` line and a desktop logout (my reading): **3.10.12.0, prefix `/home/barry/gnuradio-pkg/`, 42 components** (user, 2026-10-20). **GRC from Activities works with a QT GUI Time Sink** (user, 2026-10-20). **Out-of-tree module build worked** (user, 2026-10-20: "gr_modtool worked"; my reading: `newmod`, `cmake`, `make`). B200mini, PlutoSDR, RTL-SDR all work (see Hardware). **`maint-3.10` part of the formal rc1 test passed.** Then "Changing branches" and `main` (`tee step2-main.log`, my suggestion): **`make test` 275/275** (user, 2026-10-20). **v3.11.0.0git-1216-gec1bf153, 41 components** (user, 2026-10-20), the same as the earlier ASUS run. **GRC from Activities works with a QT GUI Time Sink on `main`** (user, 2026-10-20). **Formal `v3.0-rc1` test on the clean 26.10 ASUS: all passed** (Range slider bug upstream, not the scripts). **Clean Ubuntu 26.10 loaded** (user, 2026-10-17) for the Qt6 trial (see Open items). **Reloaded with a clean 26.10** (user, 2026-10-19) for the `v3.0` prefix trial (Step 1 of `v2.4` run again: UHD 4.9.0.1-1.4, user; it wrote the `stonking` PPA entry again; removed afterwards, `apt-get update` clean, user, 2026-10-19; whether `add-apt-repository --remove` or `rm` removed it not stated) (user, 2026-10-19: "I think it got confused with some of the Qt6 tests we did"). Before that: 24.04, not clean (Phase 1 had installed `libboost-all-dev`); original `~/AIwork` trial. |
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
| `v3.0-rc1` | 2026-10-19 | Tag only, no Release: run as the user, PPA check with Ubuntu-UHD fallback, Qt6 where `libqwt-qt6-dev` exists, install into `~/gnuradio-pkg` + `setup_env.sh`. Commit `80b6b8f`; raw URLs checked (200). |
| `v3.0` | 2026-10-21 | Tag on `80b6b8f`, the same commit as `v3.0-rc1` (no rc2); pushed, raw URLs checked (200). **Release created 2026-10-21** (user: "create it"), title "v3.0: no sudo, GNU Radio in your home directory", both scripts attached (from the tag), marked Latest; `releases/latest/download` gives the `v3.0` scripts (checked by me with the download loop, byte-identical). **The user pasted the whole `v3.0` draft into the live wiki page** (user, 2026-10-21). **README converted from the draft** (2026-10-21, uncommitted): download loop, `~/gnuradio-pkg`, no `sudo`, Qt6 bullet and section, `--prefix` row in the options table, environment section, new removal steps, wiki-page link in the intro, `v3.0` entry in Releases, closing line "Further fixes will be tagged `v3.1`" (my wording). Notes: What's changed, If you used an earlier release (the three `/usr/local` removal steps), Tested (24.04 / 26.04 / 26.10 table + hardware table), Quick start (download loop, link to the wiki page and README), Known limitations (`main` without `gr-qtgui` on 24.04/26.04, #8239, Range slider, the `python3` crash dialog). |
| `v1.0`–`v1.3` | 2026-09-26 – 10-10 | Phase 1, tags only. |

## Key decisions and why

- **Qt6 for `main` only where Qwt for Qt6 exists (user's decision,
  2026-10-19, for `v2.5`; not coded yet):** "Check for libqwt-qt6-dev, add
  nothing before 26.10." Step 1 installs the Qt6 list (`qt6-base-dev
  qt6-svg-dev libqwt-qt6-dev python3-pyqt6 python3-pyqt6.qtsvg
  pyqt6-dev-tools`) only when apt knows `libqwt-qt6-dev`. Why: without Qwt
  the rest gives no `gr-qtgui`, and PyQt6 alone makes `gnuradio-companion
  --qt` lock up on 26.04 `main` (GMKtec, 2026-10-18). **Thrift packages left
  out** (user's decision, 2026-10-19: "leave out Thrift (they may drop
  controlport/thrift support entirely)"): Step 1 adds no `libthrift-dev` /
  `thrift-compiler` / `python3-thrift` beyond what `build-dep` brings.
- **No PPA build for the running release: warn and use the distro's UHD
  (user's decision, 2026-10-19, for `v2.5`; not coded yet):** "warn when no
  PPA support, use distro UHD". Seen on the ASUS with 26.10 (2026-10-17):
  the PPA has no `stonking` build and Step 1 silently installed Ubuntu's UHD
  4.9.0.1-1.4. The ASUS's `/etc/apt/sources.list.d/ettusresearch*` (user,
  2026-10-19): `Types: deb`, `URIs: https://ppa.launchpadcontent.net/ettusresearch/uhd/ubuntu/`,
  **`Suites: stonking`**, `Components: main`: `add-apt-repository` wrote the
  entry anyway and (since Step 1 runs it with `check=True` and went on) exited
  0. The PPA's `dists/<codename>/Release` gives HTTP 404 for `stonking`, 200
  for `resolute` and `noble` (checked by me 2026-10-19). The ASUS's
  `step1.log` (user, 2026-10-19): the update run by `add-apt-repository`
  printed `Ign:5 ... ettusresearch/uhd/ubuntu stonking InRelease`, `Err:6 ...
  stonking Release` and **`E: The repository
  'https://ppa.launchpadcontent.net/ettusresearch/uhd/ubuntu stonking Release'
  does not have a Release file.`**, yet `add-apt-repository` exited 0 and
  Step 1 went on: the error is printed but nothing stops on it. My proposed check: fetch that Release URL before
  `add-apt-repository`; on 404, warn, skip the PPA (no stale entry), and
  install the same package names from Ubuntu. The ASUS keeps the stale
  `stonking` entry until removed (`sudo add-apt-repository --remove -y
  ppa:ettusresearch/uhd`, my suggestion, not run). **SoapySDR UHD module
  stays out with the distro UHD too** (user's decision, 2026-10-19: "leave
  it out"). Why: `soapysdr0.8-module-uhd` 0.4.1-7 on 26.10 depends on
  `libuhd4.9.0` (read by me from the .deb), so once Ettus publishes a build,
  or someone switches to the PPA, it would keep a second UHD next to
  `libuhd4.11.0`; module counts stay the same across releases; USRPs work
  through `gr-uhd` anyway. Users can still `apt-get install` it by hand.
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
  fixes it. **Kept** (user's decision, 2026-10-19: "Keep the clean before the
  make test"), after the bug was seen again on `main` at `862edb76b`.
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
- **Upstream `grc_tests` fix:** not on `main` as of `862edb76b` (a second plain
  `make test` on the GMKtec failed `grc_tests`, 2026-10-18). When it lands, remove the builder's
  `git clean` step and its doc bullet in a new tag.
- **Docs:** the leftover-library command can leave dangling
  `.so.3.11.0git` links. (Missing Thrift on `main`: cause found 2026-10-17,
  a `FindTHRIFT.cmake` call not updated for the keyword macro; see the 26.10
  trial.)
- **Longer term:** Qwt for Qt6, for `gr-qtgui` on `main`. See the 26.10
  Qt6 trial below.
- **Ubuntu 26.10 trial, `main` with Qt6 (proposed 2026-10-17, user asked to
  record it; not started).** User: "with 26.10 and a little extra from us,
  we could get main working with Qt6"; the laptop is to get a clean 26.10
  ("stonking", now the current stable release). Not one of the three
  decisions on hold, but the developers may want a say.
  - Checked by me on Launchpad (2026-10-17): the Ettus PPA has **no
    `stonking` build** (newest `~resolute3`, `~questing1` = 4.10); Ubuntu's
    own UHD on 26.10 is 4.9.0.1, `gnuradio` 3.10.12.0-6build2, SoapySDR
    0.8.1. **`libqwt-qt6-dev` 6.3.0 exists on 26.10, not on 26.04.**
  - GNU Radio's CI image `gnuradio-docker` `ci/ci-ubuntu-26.10-3.11/Dockerfile`
    (copy in my scratchpad, not kept) adds, beyond our `build-dep` list:
    `libqt6opengl6-dev`, `libqt6svg6-dev`, `libqwt-qt6-dev`,
    `python3-pyqt6`, `python3-pyqt6.qtsvg`, `pyqt6-dev-tools`,
    `libthrift-dev`, `thrift-compiler`, `python3-thrift`. The two `libqt6*`
    names have no published binaries since lunar / jammy (probably virtual
    now, my guess); the real ones are `qt6-base-dev` and `qt6-svg-dev`
    (6.11.2 on 26.10). PyQt6 6.11.0 and Thrift 0.23.0 on 26.10 (6.10.2 and
    0.22.0 on 26.04). The Thrift packages might explain the missing Thrift
    on `main` (my guess).
  - Trial by hand on the laptop: (1) `v2.4` Step 1 as is, to see where it
    fails (expected: at the PPA, `apt-get update`; not seen yet); (2) point
    the PPA's sources file at `resolute` and finish Step 1; (3) `sudo apt-get
    install qt6-base-dev qt6-svg-dev libqwt-qt6-dev python3-pyqt6
    python3-pyqt6.qtsvg pyqt6-dev-tools libthrift-dev thrift-compiler
    python3-thrift`; (4) build `main`: `gr-qtgui` and thrift enabled (40
    components before), `make test`, a QT GUI flowgraph in GRC; (5) build
    `maint-3.10` too, to check the Qt6 packages don't disturb it.
  - **Step 1 on the clean 26.10 laptop (2026-10-17): `v2.4` as is "all
    loaded"** (user); the user thought Ettus now has a 26.10 PPA, but
    Launchpad still shows none (checked by me). `uhd_config_info --version`:
    **UHD 4.9.0.1-1.4**, i.e. Ubuntu's own UHD from universe, not the PPA's
    4.11: Step 1 fell back silently. How the PPA step got through (`apt-get
    update` warning, or `add-apt-repository` not adding it) not seen yet.
  - Then (user, 2026-10-17): the Qt6/Thrift `apt-get install` line of
    step (3), clone of `main` to `~/gnuradio` (fork or upstream not stated),
    builder: **"no disabled components"**, i.e. cmake's disabled list is
    empty on `main`: **`gr-qtgui` (Qt6) and thrift are enabled** (my reading).
    First `main` build with `gr-qtgui`. **`make test`: 273/273** ("100%
    tests passed, 0 tests failed out of 273", user, 2026-10-17): two more
    than `main`'s 271 on 26.04. One is **`qa_qtgui`** (test 245, passed;
    user's `grep -iE "qtgui|ctrlport|thrift"` found only it); the other is
    not a 26.10 difference: the GMKtec on 26.04 at the same commit gives
    272/272 (2026-10-18), i.e. 273 minus `qa_qtgui`, so it came with the
    upstream commits between -1193 and -1210 (my reading; not named). Version
    **v3.11.0.0git-1210-g862edb76** (user). **41 components** (user), one more than
    `main`'s 40 on 26.04, not the 42 I expected with both `gr-qtgui` and
    thrift. The user's list: `gr-qtgui` and `gr-ctrlport` present, **`* thrift`
    missing**. On `main` (`862edb7`, read by me) thrift is a subcomponent of
    `gr-ctrlport` (`gr_append_subcomponent`), on only if `ENABLE_CTRLPORT_THRIFT`,
    whose default is a quiet `find_package(THRIFT)` (`FindTHRIFT.cmake`, min
    0.13: `thrift/Thrift.h`, libthrift, the `thrift` binary, Python `thrift`),
    so it never shows as disabled. User's `cmake.log`: lines 208-210 "Checking
    for module 'thrift'", "Found thrift, version 0.23.0", "thrift looking for
    version 0.13", then nothing. **Cause (found by me reading `862edb7`): a
    `main` bug.** `GR_PYTHON_CHECK_MODULE` in `GrPython.cmake` now takes
    keywords (`cmake_parse_arguments`: `DESC MODULE CHECK VAR`; the top-level
    `CMakeLists.txt` uses them), but `FindTHRIFT.cmake:63` still calls it
    positionally, `gr_python_check_module("Thrift" thrift "1"
    PYTHON_THRIFT_FOUND)`, so `PYTHON_THRIFT_FOUND` is never set and
    `THRIFT_FOUND` stays false. On `maint-3.10` the macro is still positional
    (`GR_PYTHON_CHECK_MODULE desc mod cmd have`), so thrift works there. This
    is also **the cause of the missing Thrift on `main` on 26.04**. Which
    commit changed the macro: not found. Expected in `cmake.log` (not yet
    seen): "Python checking for  - not found". Suggested test (not run):
    change line 63 to `gr_python_check_module(DESC "Thrift" MODULE thrift
    CHECK "1" VAR PYTHON_THRIFT_FOUND)`, rebuild, expect 42 components.
    Worth an upstream report. User's `CMakeCache.txt` (2026-10-17) fits:
    `THRIFT_BIN=/usr/bin/thrift`, `THRIFT_INCLUDE_DIRS=/usr/include`,
    `THRIFT_LIBRARIES=.../libthrift.so`, `PC_THRIFT_VERSION=0.23.0` all found,
    **no `PYTHON_THRIFT_FOUND`** entry, and **`ENABLE_CTRLPORT_THRIFT:BOOL=OFF`
    cached**: after the fix, a rebuild in place keeps it OFF, so pass
    `--cmake-args="-DENABLE_CTRLPORT_THRIFT=ON"` (or remove `build/`).
    **Fix tried (user, 2026-10-17):** line 63 edited to keywords, builder
    with `--cmake-args="-DENABLE_CTRLPORT_THRIFT=ON"`: cmake now found Thrift,
    but **`make -j3` failed** (exit 2, "GNU Radio build failed. Aborting."):
    `thrift_server_template.h:158: error: conflicting return type specified
    for 'auto thrift_server_template<...>::i_impl()'`, overriding
    `thrift_application_base.h:108` `virtual TserverBase* i_impl() = 0;`
    (compiling `rpcserver_selector.cc`). **Both bugs come from one `main`
    commit, `24e9f2b7e`** (John Parent, "cmake: Add comprehensive
    cross-platform installer infrastructure", committed 2026-02-09, 149
    files; checked by me): it made `GR_PYTHON_CHECK_MODULE` keyword-based
    without updating `FindTHRIFT.cmake:63` (it did edit that file's HINTS),
    and changed `TserverBase* i_impl()` to `auto i_impl()` in
    `thrift_server_template.h` (lines 42, 158). The first hides the second:
    Thrift is never enabled, so nothing compiles that code. `maint-3.10` has
    `TserverBase* i_impl()`. The cache now has `ENABLE_CTRLPORT_THRIFT=ON`.
    Next build (user, 2026-10-17): **with both fixes** ("just (a)": line 63
    of `FindTHRIFT.cmake` in keywords, and `TserverBase* i_impl()` restored in
    `thrift_server_template.h` lines 42 and 158), builder with the cached
    `ENABLE_CTRLPORT_THRIFT=ON`: **built, `make test` 273/273**, so `main`
    builds with Thrift on 26.10 with a two-part fix (same test count as
    without Thrift: no Thrift-only tests). **42 components** (user): the
    41 plus `* thrift` (my reading), the same count as `maint-3.10`. A
    ControlPort run-time check not done. **`gnuradio-companion` works with a
    QT GUI Time Sink** (user, 2026-10-17), with **both front ends,
    `gnuradio-companion --gtk` and `--qt`** (user: "I ran both of them"),
    each running the same Time Sink flowgraph (user confirmed): `gr-qtgui` with Qt6 works at run
    time, so **`main` with Qt6 works on 26.10**. Still to do: step (5),
    `maint-3.10` on 26.10 with the Qt6 packages; the upstream report.
  - **Summary for the GRC developer** (user asked, 2026-10-17): a Claude Docs
    doc, "GNU Radio main with Qt6 on Ubuntu 26.10",
    https://claude.ai/code/artifact/76d346a7-1652-47de-a7c8-f8ad69f46288
    (private until the user shares it; exportable to Markdown / PDF).
    Sections: lead (273/273, both GRC front ends, one extra `apt-get` line);
    Setup (`main` `862edb7`, `build-dep`, UHD 4.9.0.1, `libqwt-qt6-dev`, the
    Qt6 install line, the CI Dockerfile's stale `libqt6*` names); Results
    (26.10 vs 26.04 table: disabled components, 42 vs 40 components, 273 vs
    271 tests, `--gtk` / `--qt`; `qa_qtgui` and the unidentified second
    test); Thrift on `main` (the two `24e9f2b7e` bugs with the fixes, the
    cached `ENABLE_CTRLPORT_THRIFT`); Not yet checked (ControlPort at run
    time, `maint-3.10` on 26.10, the second test, no Qwt-Qt6 on 26.04).
    **Shared with the GRC developer** (user, 2026-10-18).
    Updated 2026-10-18 (user asked): the Results table's 26.04 column is now
    `main` at the same commit (272 of 272, 40 components); the note under it
    says 26.10 runs exactly one more test (`qa_qtgui`) and that a second
    plain `make test` on 26.04 fails `grc_tests` (the leftover files, still
    on `main` at `862edb7`); "The second extra test" bullet removed.
  - **Thrift issue drafted** (user asked, 2026-10-17; text in this
    conversation only, not posted as far as I know). Laid out to match
    GNU Radio's bug report form (What happened / System Information / GNU
    Radio Version / Specific Version / Steps to Reproduce / Relevant log
    output). Title: "Thrift support can't be enabled on main:
    FindTHRIFT.cmake uses the old gr_python_check_module call, and
    thrift_server_template.h doesn't compile". Content: the two
    `24e9f2b7e` bugs with both fixes, "the first hides the second", the
    tested result (`* thrift`, 42 components, 273/273; ControlPort not run),
    the cached `ENABLE_CTRLPORT_THRIFT=OFF` note; Ubuntu 26.10, Thrift
    0.23.0, same gap on 26.04 (0.22.0); version v3.11.0.0git-1210-g862edb76;
    repro steps; the compiler error. Leaves out this project; optional last
    line offering a PR. **The user presented the text** (2026-10-18; to
    the GRC developer, my reading). **Posted as
    [gnuradio/gnuradio#8239](https://github.com/gnuradio/gnuradio/issues/8239)**,
    "Thrift support can't be enabled on main" (user; checked by me with `gh`:
    opened by `duggabe` 2026-10-18, open). Full text under "Drafts" at the end of
    this file. The edits
    are still in the user's `~/gnuradio` working tree (my reading). Worth an
    upstream issue / PR. GRC not reported yet.
  - **Does adding the Qt6 packages depend on the OS version?** (user asked,
    2026-10-18.) Only through `libqwt-qt6-dev`. Checked by me on Launchpad
    (amd64): `qt6-base-dev` / `qt6-svg-dev` 6.4.2 (24.04), 6.10.2 (26.04),
    6.11.2 (26.10); `python3-pyqt6` / `python3-pyqt6.qtsvg` / `pyqt6-dev-tools`
    6.6.1, 6.10.2, 6.11.0; **`libqwt-qt6-dev` only on 26.10** (6.3.0). My
    proposal: key on the package, not the release (install the Qt6 list when
    `apt-cache show libqwt-qt6-dev` succeeds, like the SoapySDR step; no
    version table, 27.04+ automatic); on 24.04 / 26.04 nothing extra, since
    without Qwt the rest doesn't give `gr-qtgui`; keep the Thrift packages out
    of Step 1 until #8239 is fixed. Open question: does PyQt6 alone make
    `gnuradio-companion --qt` work on a `main` build without `gr-qtgui`?
    Suggested test on the GMKtec (26.04, `main` `862edb7`): `sudo apt-get
    install python3-pyqt6 python3-pyqt6.qtsvg`, `gnuradio-companion --qt`. If
    yes, PyQt6 could go in on every release and only Qwt waits.
    **Result (user, 2026-10-18): on the GMKtec, installing `python3-pyqt6
    python3-pyqt6.qtsvg` makes `gnuradio-companion --qt` lock up.** So
    PyQt6 without Qwt / `gr-qtgui` is not just useless but harmful on 26.04
    `main`: Step 1 must not install PyQt6 where `libqwt-qt6-dev` is missing
    (my conclusion). Then (user, 2026-10-18): **"On 26.04 GRC works with Qt5
    but not Qt6"**: `--qt` runs on PyQt5 and locks up on PyQt6 (my reading;
    how Qt5 was selected, by removing PyQt6 or with `QT_API=pyqt5`, not
    stated). Why it hangs on PyQt6 without `gr-qtgui`: not known.
  - If it works, `v2.5` (my proposal): Step 1 installs the Qt6 list when
    apt knows `libqwt-qt6-dev` (worked out at run time, like the SoapySDR
    step), otherwise prints that a `main` build lacks `gr-qtgui`; 24.04 /
    26.04 unchanged; builder probably unchanged. UHD on 26.10 needs a
    decision: wait for Ettus, fall back to the `resolute` build, or use
    Ubuntu's 4.9.0.1. 26.10 is interim (~9 months, to about July 2027);
    the wiki page promises only 24.04 and 26.04.
  - Cost: the laptop is the user's only 24.04 machine; a clean 24.04 can
    go on the GMKtec when needed.
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
- **Developer feedback: operate without `sudo` by default** (user,
  2026-10-19): one of the developers "was thinking of defaults in both steps
  would be to operate without 'sudo'". Not decided; exact meaning not known.
  Today (checked by me): Step 1 refuses to run unless root ("installing
  packages requires root. Re-run with sudo"), docs say `sudo python3
  gnuradio_dependencies_installer.py`; the builder already works as the
  normal user (it runs `sudo chown` / `sudo make install` / `sudo ldconfig`
  itself and only switches users when run under sudo), but the README /
  draft say `sudo python3 gnuradio_clone_builder.py` (README lines 163, 256).
  Two readings (mine): (A) run both as the normal user and let each call
  `sudo` only for the commands that need root; (B) nothing privileged by
  default (Step 1 only prints its commands; the builder installs into a
  prefix in the home directory, which needs environment setup).
  **Then (user, 2026-10-19): the maintainer proposed `mkdir gnuradio-pkg`
  and installing into it, like (B); the user: "I think it would make
  everyone happier."** Not decided in detail, not coded. My notes: on
  `main`, `GrPython.cmake` installs Python modules to
  `lib/python3.X/site-packages` under the prefix (`posix_prefix` scheme), so
  using it needs `PATH`, `PYTHONPATH`, `LD_LIBRARY_PATH` (no setup script
  found upstream; the builder could write one). Step 1 still needs root for
  `apt-get` whatever the builder does.
  The user's wiki page https://wiki.gnuradio.org/index.php/ModuleNotFoundError
  (local copy `ModuleNotFoundError.mediawiki` in the repo dir, gitignored
  at the user's request, 2026-10-19) covers this: (A) `gnuradio-config-info
  --prefix`; (B) `find {your-prefix} -name gnuradio | grep "packages"`; (C)
  `PYTHONPATH` (`lib/{Py-version}/dist-packages` and `site-packages` on
  Debian/Ubuntu, `lib64/.../site-packages` elsewhere); (D) `LD_LIBRARY_PATH`
  (`lib` / `lib64`); (E) put them in `~/.bash_aliases`, `~/.bashrc` or
  `~/.profile`; (F) for GRC started from the GUI, `~/.profile` or
  `/etc/profile.d/`. Not on it: `PATH` (not needed for `/usr/local`, needed
  for a home prefix). Its example still says python3.6.
  **User's decisions for the prefix install (2026-10-19; not coded):**
  (1) the docs say to source `setup_env.sh` from **`~/.profile`** (user's
  own preference is `~/.bash_aliases`, but `~/.profile` also covers GRC
  started from the desktop); (2) default prefix **`~/gnuradio-pkg`**, with a
  **`--prefix`** option; (3) **the builder writes
  `~/gnuradio-pkg/setup_env.sh`** after `make install`, with the paths it
  finds (like section B of the wiki page). (4) **Release: one `v3.0`**
  (user, 2026-10-19, after asking about "a tag without a release while we
  test it"): the prefix install plus the `v2.5` decisions (Qt6 when
  `libqwt-qt6-dev` exists, no Thrift, PPA check with distro-UHD fallback, no
  Soapy UHD module, `git clean` kept). Tested through tags **`v3.0-rc1`,
  `v3.0-rc2`, ...** with no Release, so `releases/latest` stays `v2.4` for
  wiki users; testers download from
  `https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v3.0-rcN/<file>`.
  When it passes: tag `v3.0` on the last rc's commit and create the Release
  with both scripts; only then the user replaces the live wiki page, and the
  README follows. (No separate `v2.5`.) (5) **Step 1 runs as the normal
  user and calls `sudo` only for the commands that need root** (reading A;
  user, 2026-10-19): the apt commands, `add-apt-repository`, the sources-file
  edit, `uhd_images_downloader`; checks, the PPA Release check and the module
  lookup run unprivileged. Docs drop `sudo` in front of both scripts. (6) **The intro section of the
  wiki draft and README gets reworded with `v3.0`, not before** (user,
  2026-10-19: "as long as we stay on v2.4 Release, we're OK with it as is").
 asked about renaming
  the repo, then said they will talk to the GNU Radio developers; "the
  plan is to bring it into the gnuradio/gnuradio repo", details not settled.
  Nothing changed yet. If it moves, the download links in the wiki draft,
  README, and Release notes, and the repo URLs here, need updating.

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
