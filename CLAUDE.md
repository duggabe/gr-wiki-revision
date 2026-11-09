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

Current release: **`v3.1`** (GitHub "Latest", 2026-10-31). Favour clarity,
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
- **Tags** are never moved; fixes get a new tag. Next: `v3.2` (the README said
  "Further fixes will be tagged `v3.2`" until it became static, 2026-11-02). Bigger changes are tested
  through `vX.Y-rcN` tags with no Release first, so `releases/latest` stays
  on the last release; testers download from
  `https://raw.githubusercontent.com/duggabe/gr-wiki-revision/<tag>/<file>`.
- **GitHub Releases** are created or edited only on the user's request.
  Every Release must have **all its scripts attached** (two up to `v3.1`,
  three from `v3.2` on, with `gnuradio_uninstaller.py`), because the docs
  download from
  `https://github.com/duggabe/gr-wiki-revision/releases/latest/download/<file>`.
- **The wiki holds the instructions; the README is static** (user,
  2026-11-02: "after the overview section I would like to refer the reader
  to the Wiki page rather than reproducing the content in the README. That
  way, the README would be static and the only editing would be in the
  Wiki"). `wiki-draft-download-section.mediawiki` (MediaWiki, gitignored,
  local only) is the user's text, edited in MediaWiki. It stays out of
  git (user, 2026-11-02: "the wiki has its own history and roll-back
  functions, so I don't see a need to track it with the repo"). The README is
  the intro and overview (from the draft's top), then "Instructions"
  (a link to the wiki page), "Releases" (a link to the Releases page, no
  per-release text: the Release notes hold that), and "License". No
  "current release" line. Until 2026-11-02 the README copied the draft
  section by section, with a per-release history; that version is
  `README.md` at `ec4d534`. The two options tables (keep in sync with the
  scripts' argparse help) are now in the wiki draft only (user, 2026-11-02:
  "the Options tables need to be in the Wiki"), at the end of Step 1 and
  after Step 2's bullets, as `wikitable`s with `white-space:nowrap` on the
  option cells. **Draft reorganised** (user's outline, 2026-11-02): Before
  you start, Downloading the scripts, Getting the source code, Starting a
  branch, Step 1, Step 2 (Building..., Setting up the environment, The
  main branch and Qt6, Checking the result), Making and submitting a PR
  (Pull Request), Changing branches (incl. the leftover-library
  paragraph), Removing an installed GNU Radio package. My additions:
  `sudo apt-get install git` in "Getting the source code" (cloning now
  comes before Step 1, which installs git). The pre-reorganisation draft is
  saved in the session scratchpad only, not in git. Then (user, 2026-11-02: "Otherwise
  it's rather overwhelming to see all of the commands at the top of the
  document"): "Before you start" is one paragraph (for a system without
  any form of GNU Radio; otherwise see "Removing an installed GNU Radio
  package"), and its three removals moved into that section as
  subsections (Ubuntu's packages, UHD built from source, GNU Radio in
  `/usr/local`), before the `~/gnuradio-pkg` removal, with a link to
  [[UnInstallGR]] for other installs. The `v2.4` text is kept as
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

## Current state (2026-10-31)

- **`v3.1` released** (2026-10-31, tag on `ce7229d`, the same commit as
  `v3.1-rc1`; marked Latest). **Live wiki page = local draft** (user,
  2026-11-02: "the wiki has been updated"): with the options tables, the
  reorganised layout, the short "Before you start", and the user's own
  comment on the `git push` line in "Making and submitting a PR" (`git
  push -u origin issue8218        # use your branch name; 'issue8218' is
  only an example`, also in the local draft). README static, pointing to
  the wiki (`2d08122`). `gnuradio_uninstaller.py` on `main` (`379ef82`),
  not in a Release. **Local draft now ahead of the live wiki** (user,
  2026-11-02: "update the wiki draft to use the uninstaller"): the
  download loop has `gnuradio_uninstaller.py` as a third file ("the three
  scripts", "All three scripts have `--help`"); "Before you start" says
  to remove GNU Radio "with the uninstaller script"; "Removing an
  installed GNU Radio package" is rewritten around the uninstaller
  (`--dry-run`, run, what it removes, what it keeps or only lists, log
  out if `~/.profile` changed, options table, [[UnInstallGR]] for
  removal by hand). Its four manual subsections are gone. "Changing
  branches" keeps its `rm -rf ~/gnuradio-pkg ~/gnuradio/build`.
  "Before you start" now ends "The Step 1 and Step 2 scripts check for
  some of these and stop, pointing to the uninstaller."
  **Scripts' messages point to the uninstaller** (user, 2026-11-02:
  "update the builder and Step 1 messages to point to the uninstaller";
  uncommitted). Each script has `UNINSTALLER_NAME` and
  `uninstaller_lines()`: `python3 <path next to this script>` (`~/`
  shortened), plus a "download it as described under 'Downloading the
  scripts'" note if the file isn't there. Step 1: Ubuntu's packages →
  uninstaller first, `sudo apt-get remove ...` as "only these packages";
  source-built UHD → uninstaller only (the three manual commands
  dropped). Builder (my choice, since the uninstaller also removes the
  prefix install and build dir, forcing a full rebuild): Ubuntu's
  packages and the empty leftover dirs keep their one command first, the
  uninstaller as the alternative with that cost stated; the `/usr/local`
  warning now says to run the uninstaller first, then the builder again
  (it pointed to "Changing branches", which never covered it). Step 1's
  post-install "got installed as a dependency" warning unchanged. Both
  docstrings mention it. Checked by me: all five messages with stubbed
  checks, the missing-file note, and both `--dry-run` outputs on the
  LENOVO byte-identical to `HEAD`'s. **Not to
  be pasted before a Release has the uninstaller attached**: the loop
  downloads from `releases/latest`. Pre-change draft in the session
  scratchpad only.
- **`v3.1-rc1` passed** (see Test results): the clean 26.04 GMKtec with
  `maint-3.10` and `main`, the 26.10 ASUS (not clean) with `main`, GRC
  in both front ends and all three SDRs on the ASUS. Step 1 is unchanged
  from `v3.0` apart from the log order; the builder adds only the
  `~/.profile` message (`d9197fa`) and the log order.
- GitHub Releases: `v3.1` (Latest), `v3.0`, `v2.4`, `v2.3`, `v2.2`, `v2.1`, `v2.0`, all with both
  scripts attached. The `v1.2` Release was deleted 2026-10-13 and the
  `v3.1-rc1` pre-release 2026-10-31 (user's requests; tags kept).
- **Debian support paused** (user, 2026-10-30) and its code reverted
  (`7af39ab`); the work is kept in `fa1db6b` and `a8a93dc` (see Open
  items). The GMKtec has since been reloaded with 26.04.
- **On hold** (user, 2026-10-16): "I'm going to wait for the developers
  decisions before I do anything else": where the scripts live, Fedora
  (and now Debian) support, the `qa_fastnoise` backport (see Open items).
- Tracked files: the two scripts, `README.md`, `LICENSE` (CC BY-SA 4.0, by
  choice although CC advises against it for software), `.gitignore`,
  `CLAUDE.md`.

## Machines

The user's three SDRs in all of the user's tests, on every machine: USRP
B200mini (serial 315C7B7), RTL-SDR (an RTL-SDR.COM v3), PlutoSDR.

| Machine | Ubuntu | State |
| --- | --- | --- |
| LENOVO desktop (working machine, `~/gr-wiki-revision`) | 26.10 | 16 cores, 15 GiB RAM, 4 GB swap. **Reloaded with 26.10** (user, by 2026-10-22; clean presumably, my reading). Seen by me 2026-10-22: Ubuntu's UHD 4.9.0.1-1.4, `~/gnuradio` on `maint-3.10` at `273c82180`, `~/gnuradio-pkg/setup_env.sh` present, nothing in `/usr/local/bin`: so the `v3.0` scripts with the default prefix (user confirmed, 2026-10-22). **`make test` 269/269, 42 components** (user, 2026-10-22). User built `maint-3.10` and found [gnuradio/gnuradio#8250](https://github.com/gnuradio/gnuradio/issues/8250) with `gnuradio-companion --qt` (see Useful facts). Before (reloaded 2026-10-08): 26.04, UHD 4.11 from the PPA, GNU Radio 3.10.12.0 in `/usr/local`. |
| GMKtec (clean-install test machine) | reloaded per test | 4 cores, 10 GiB. **Now: 24.04 with `v3.2-rc1`** (by 2026-11-06; 24.04 my reading from UHD `~noble3`), `maint-3.10` in `~/gnuradio-pkg`, 269/269. Before (2026-11-02): 26.04, the uninstaller's Rounds 1 and 2. Before that: **clean 26.04 with `v3.1-rc1`** (2026-10-31), `~/gnuradio-pkg`, ended on `main` -1216. Before: **clean Debian 13** (user, 2026-10-29), for the Debian look: no root password set at install, so the user's `sudo` works (user); SMB link set up; the whole LENOVO is shared over SMB (user; `~/share` on the LENOVO only holds a copy of `smb.conf` for editing). Nothing is mounted on the LENOVO side, so the GMKtec writes to the LENOVO, not the reverse (my reading). **Remote Desktop (RDP) works** (user, 2026-10-30), used from the LENOVO: the GNOME Settings switch locked up, so it was set up by hand with `openssl req` (cert/key in `~/.local/share/gnome-remote-desktop`), `grdctl rdp set-tls-key/set-tls-cert/set-credentials/disable-view-only/enable`, `systemctl --user enable --now gnome-remote-desktop`; `grdctl`'s "RDP server certificate is invalid" message was harmless. Before: **clean 26.04 with `v3.0-rc1`** (2026-10-20/21), `~/gnuradio-pkg`, ended on `main` -1216. Earlier: clean 24.04 (`v2.2`, `v2.3`, 2026-10-14), Fedora 44 (2026-10-16), clean 26.04 (`v2.4`, 2026-10-17). |
| Laptop (hostname `ASUS`) | 26.10 | Last: **`v3.1-rc1` on `main` -1216** (2026-10-31, not clean): 275/275, 41 components, GRC both front ends, three SDRs. Before: **clean 26.10 with `v3.0-rc1`** (2026-10-20), Ubuntu's UHD 4.9.0.1-1.4, Qt6 list installed, `~/gnuradio-pkg`, ended on `main` -1216. Earlier: clean 26.10 for the Qt6 trial (2026-10-17) and the manual prefix trial (2026-10-19); before that 24.04, not clean. |
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

**Unknown package names are skipped, not fatal** (user, 2026-11-08: "make
the package lists warn and skip instead of failing"; uncommitted, for after
`v3.2`). Before each `apt-get install`, `skip_unknown_packages()` drops the
names `apt_knows()` doesn't find, with a warning that names them and says
to check cmake's disabled components; a command with nothing left is
skipped. `REQUIRED_PACKAGES` (`TOOL_PACKAGES` + `UHD_PACKAGES`: git,
`software-properties-common`, `uhd-host`, `libuhd-dev`) still fail (my
choice: the later steps can't work without them). The plan gets a `note:`
for names apt doesn't know yet. Checked by me: all 25 listed names are real
packages on 26.10; `--dry-run` output byte-identical to `HEAD`'s; stubbed
tests (one fake name dropped, all fake → skipped, required kept, other
commands untouched); a dry run with a fake Boost name prints the note. Not
run for real.

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

`INSTALL_DIR_PATTERNS` and the uninstaller's `GNURADIO_DIR_PATTERNS`
must stay in sync (also the `v3.0` Release notes' "If you used an earlier
release" `rm -rf` list; the wiki draft's manual `/usr/local` commands
were replaced by the uninstaller, 2026-11-02, and `UnInstallGR` has its
own list).

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
| `v3.1-rc1` | 2026-10-30 | Tag (annotated) on `ce7229d`. GitHub pre-release, not Latest (user's request), both scripts attached and checked byte-identical; `releases/latest` stayed `v3.0` (checked). **Pre-release deleted 2026-10-31, tag kept** (user). Title "v3.1-rc1: release candidate (not for general use yet)". Contents: builder `~/.profile` echo message (`d9197fa`), log-order fix in both scripts, full-path leftover-library command in the README (wiki draft too, not pasted). Not run on a real build yet. |
| `v3.1` | 2026-10-31 | Tag (annotated) on `ce7229d` (= `v3.1-rc1`). Release title "v3.1: clearer ~/.profile step, logs in order", marked **Latest**, both scripts attached; `releases/latest/download` checked byte-identical to the tag. Notes: What's changed (builder `~/.profile` echo command or "already runs" note; log order in both scripts; docs' full-path leftover-library command), If you used v3.0 (nothing to redo), Tested (26.04 GMKtec clean: `maint-3.10` 269/269, `main` 274/40; 26.10 ASUS not clean: `main` 275/41, GRC both front ends, three SDRs), Quick start, Known limitations (as `v3.0`, Range slider now links #8253). README `v3.1` entry in `a15f600`. **Live wiki page updated with the local draft** (user, 2026-10-31), incl. the full-path leftover-library command. |
| `v3.2-rc1` | 2026-11-02 | Tag (annotated) on `5197d45`, pushed (user: "let's create a v3.2-rc1"). Contents: `gnuradio_uninstaller.py` (tested on the GMKtec, Rounds 1 and 2), Step 1's and the builder's messages pointing to it (`5197d45`, not run on a real machine yet). Raw tag links checked byte-identical for all three scripts; `releases/latest` still `v3.1`. **GitHub pre-release created by the user** (2026-11-02, with `! gh release create ...`, since my own `gh release create` was blocked by Claude Code's permission check as "Create Public Surface"): title "v3.2-rc1: release candidate (not for general use yet)", pre-release, not Latest, notes from my draft (What's new, Testing it with a tag download loop, Tested so far). Checked by me: the three attached scripts byte-identical to the tag; `releases/latest` still `v3.1`. For future Releases: give the user the `!` command, with the files prepared in a separate step first (the first try failed because the blocked command was also the one that wrote the `rc/` copies). **Every Release from `v3.2` on needs all three scripts attached** (the wiki draft's loop downloads three). |
| `v3.2-rc2` | 2026-11-08 | Tag (annotated) on `091d480`, pushed (user: "let's make v3.2-rc2 with the OS check"). Contents beyond rc1: the uninstaller's OS check (`091d480`) and Step 1's unknown-package skipping (`074cca9`, came along as it is on `main` between them). Raw tag links checked byte-identical for all three scripts; `releases/latest` still `v3.1`. **GitHub pre-release created by the user** (2026-11-08, `! gh release create ...`): title "v3.2-rc2: release candidate (not for general use yet)", pre-release, not Latest; checked by me: the three attached scripts byte-identical to the tag, `releases/latest` still `v3.1`. Not run on a real machine yet. |
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
- **No container mode** (user, 2026-11-08: "In my opinion there is no
  value added. It was just one person's suggestion"): the scripts stay for
  bare metal, outside Docker. Running them inside a container would need
  `python3` / `ca-certificates` in the image, `-y`, `xvfb` for `make
  test`, `make` jobs from the container's limits, `ENV` instead of
  `~/.profile`, and USB / display passthrough (my list, 2026-11-08; not
  tried). Root without `sudo` already works in both scripts.
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
  `event.position().x()`). Upstream bug; at first the developers chose
  not to open an issue (user, 2026-10-21), but the user filed it as
  [gnuradio/gnuradio#8253](https://github.com/gnuradio/gnuradio/issues/8253)
  (2026-10-24, open; on the watch list, user 2026-10-31). Flowgraphs
  still run.
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
  (2026-10-22). Upstream GRC, not the scripts. Issue timeline (checked by
  me with `gh`, 2026-10-31): closed and reopened by Marcus Müller on
  2026-10-22 (he first thought PR #7811 fixed it, then "misread #7811");
  the user found it **works on `main` -1216** (comment 2026-10-24, with a
  harmless-looking `g_main_context_pop_thread_default` GLib-CRITICAL
  warning) but **still fails on `maint-3.10` on 26.04** (2026-10-31);
  Marcus (2026-10-31): no bugfix yet, probably backportable to
  `maint-3.10` for a later 3.10 release. **Still open** (user and `gh`, 2026-10-31).
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
- **GNU Radio 4.0 is a separate project** (user, 2026-11-08: "the 4.0 work
  is totally separate and is a joint project with the Facility for
  Antiproton and Ion Research (FAIR). I don't know how much for 3.x will
  apply to it"). Its CI images are the `-4.0` ones in `gnuradio-docker`
  (C++ rewrite deps: `vir-simd`, `libboost-ext-ut-dev`, `libcpr-dev`; no
  Qt, UHD or Thrift). These scripts are for 3.x (`maint-3.10`, `main`).
- **Boost may be reduced or removed** (user, 2026-11-08: "there is effort
  to reduce or eliminate BOOST, there again it may be only for 4.0").
  Step 1's `BOOST_PACKAGES` are there for UHD's `UHDConfig.cmake` (the
  PPA's `libuhd-dev` declares no Boost dependencies), not for GNU Radio
  itself, so they stay needed as long as UHD's cmake files ask for Boost,
  whatever GNU Radio does (my reading).
- `cmake` options persist in `build/CMakeCache.txt` (e.g. `ENABLE_GR_FEC`
  stayed `OFF` from an old manual build until `build/` was removed).

## Test results

Kept here only. Test counts differ by release and branch. `maint-3.10`:
269 everywhere with `python3-pytest` (`v2.4` on); 268 on 24.04 without it
(`grc_tests` is added only if cmake can `import pytest`, and pytest is in
`gnuradio`'s Build-Depends on 26.04 but not on 24.04). `main` grows with
upstream: 271 (-1193, 26.04), 272 / 273 (-1210, 26.04 / 26.10), 274 / 275
(-1216, 26.04 / 26.10); 26.10 always runs one more, `qa_qtgui`.

### `v3.2-rc1`

| Date | Machine, Ubuntu | Scripts | Branch / build | Result |
| --- | --- | --- | --- | --- |
| by 2026-11-06 | GMKtec, **24.04** (UHD `~noble3`; reloaded with 24.04 after the 26.04 uninstaller rounds, my reading) | `v3.2-rc1` (my reading) | the tester request run by the user (user, 2026-11-06: "I have not heard from jesternofool and decided to run the tests myself"); logs `~/share/uninst-dry.log`, `uninst-run.log`, `uninst-ppa.log`, `step1.log`, `step2.log` | **Part A** (set up by the user with a `v2.x`-style `/usr/local` `maint-3.10` install and Ubuntu's own 3.10.9 packages, `libgnuradio-*3.10.9t64`): dry run and real run found and removed the `/usr/local` install from the manifest (140 paths, `python3.12/dist-packages`), 14 GRC files in `/usr/share` (the `mimetypes` icons, 7 sizes x 2 names; the `.desktop`, `apps` icons and `mime/packages` file are owned by Ubuntu's package, so left to apt, and no `update-mime-database` was needed: correct), `~/gnuradio/build` (with `sudo`), the 24 Ubuntu packages (`libuhd4.6.0t64` etc. left for autoremove), then `sudo ldconfig`; the second dry run found nothing (user). **Part B:** with `ppa:gnuradio/gnuradio-releases` and its `gnuradio` (3.10.12, `libgnuradio-*3.10.12`) installed, **Step 1 stopped and pointed to the uninstaller** (user, 2026-11-06: first real run of `5197d45`'s message; not in a log); the uninstaller removed the 24 PPA packages and `gnuradio-ubuntu-gnuradio-releases-noble.sources` (then `apt-get update`: only the Ettus PPA left). **Part C:** Step 1 `OK:` line, **UHD 4.11.0.0-0ubuntu1~noble3** (PPA path); `maint-3.10`, **269/269**, 3.10.12.0, prefix `/home/barry/gnuradio-pkg/`, **42 components**; the builder printed the `echo ... >> ~/.profile` command (the line was gone); **GRC from Activities works** (user, 2026-11-06). Doxygen's "has become obsolete" tag warnings in `step2.log`: harmless. **All four items confirmed** (user); SDRs not reported. |

### `v3.1-rc1`

| Date | Machine, Ubuntu | Scripts | Branch / build | Result |
| --- | --- | --- | --- | --- |
| 2026-10-31 | GMKtec, **clean 26.04** (reloaded after Debian 13) | `v3.1-rc1` (my reading) | `maint-3.10`, fresh clone | **UHD 4.11.0.0-0ubuntu1~resolute3** (PPA path), cmake's disabled-components list **empty**, **269/269** (user, 2026-10-31). Components: **42 as recalled by the user**, not captured (2026-10-31); left out of the Release notes. Log order and `~/.profile` message: see the next row. GRC and SDRs on this install not reported. |
| 2026-10-31 | same | same | "Changing branches" (`rm -rf ~/gnuradio-pkg ~/gnuradio/build`), then `main` **v3.11.0.0git-1216-gec1bf153**, prefix `/home/barry/gnuradio-pkg/` (user, 2026-10-31) | **274/274**, **40 components** (no `gr-qtgui`, no Thrift, as expected on 26.04), cmake's disabled-components list empty (user, 2026-10-31). **`step1.log` and `step2.log` look good** (user): log-order fix confirmed. **The builder's `~/.profile` note said the line was already there**, which was correct (user): the "already runs" branch of `d9197fa` confirmed; **the first run printed the `echo` command** (user, 2026-10-31): both branches of `d9197fa` confirmed. Not reported yet: GRC from the desktop, SDRs. |
| 2026-10-31 | ASUS, 26.10 (**not clean**, user) | `v3.1-rc1` (my reading) | `main` **v3.11.0.0git-1216-gec1bf153**, prefix `/home/barry/gnuradio-pkg/` | **275/275**, **41 components** (`gr-qtgui` with Qt6, no Thrift), cmake's disabled-components list empty (user, 2026-10-31): the same as `v3.0-rc1` on 26.10 at this commit. UHD version, log order and `~/.profile` message not reported for this run. **GRC `--gtk` and `--qt` work** (user, 2026-10-31, on the ASUS). |

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
| 2026-10-29 | GMKtec, **clean Debian 13** (trixie, netinst 13.7.0) | **Debian draft** (uncommitted working tree, copied over SMB) | `maint-3.10`, `~/gnuradio-pkg` (my reading: the steps I gave) | **UHD 4.8.0.0+ds1-2** (Debian's), **269/269**, 3.10.12.0, prefix `/home/barry/gnuradio-pkg/`, **42 components** (user's paste, 2026-10-29): the same as Ubuntu's `maint-3.10`. **A flowgraph runs from the desktop** (user; GRC from the desktop via the `~/.profile` line, my reading). First run of the scripts on Debian. **`uhd_find_devices`: "Could not find path for image: usrp_b200_fw.hex", no devices** (user, 2026-10-30): the images are in `/usr/share/uhd/4.8.0/images`, but `uhd_config_info` gives `Package path: /lib` and an empty images directory (Debian's UHD loaded through `/lib`, a link to `/usr/lib`, so it looks under `/share`; my reading). Led to the builder's `UHD_IMAGES_DIR` line (`a8a93dc`); with it, **the B200mini is found** (user, 2026-10-30; my reading: builder `a8a93dc` re-run, then a new login). Step 1's plan listed **11 SoapySDR modules**, the same set as 24.04 (airspy, audio, bladerf, hackrf, lms7, mirisdr, osmosdr, redpitaya, remote, rfspace, rtlsdr; no plutosdr). SDRs not reported yet. |

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
| 2026-10-30 | User, GMKtec **clean Debian 13** | Debian draft (`fa1db6b`) + builder `a8a93dc` (`UHD_IMAGES_DIR`), `maint-3.10`, `~/gnuradio-pkg`, Debian's UHD 4.8.0.0+ds1-2 | USRP B200mini | `gr-uhd` (my reading) | **Found** once `UHD_IMAGES_DIR` was set; **loopback works** (user, 2026-10-30; 30 dB attenuator presumably, my reading): first USRP use on Debian |
| 2026-10-30 | User, GMKtec **clean Debian 13** | same | RTL-SDR.COM v3 | presumably `gr-soapy` (my reading) | **Works** (user, 2026-10-30; presumably the usual broadcast FM in stereo, my reading). PlutoSDR not working on Debian yet (USB network; see Open items) |
| 2026-10-31 | User, ASUS 26.10 (user) | `v3.1-rc1`, **`main`** -1216, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1 (my reading) | USRP B200mini | `gr-uhd` (my reading) | **Good** (user, 2026-10-31) |
| 2026-10-31 | User, ASUS 26.10 (user) | `v3.1-rc1`, **`main`** -1216, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1 (my reading) | PlutoSDR | `gr-iio` (my reading) | **Good** (user, 2026-10-31) |
| 2026-10-31 | User, ASUS 26.10 (user) | `v3.1-rc1`, **`main`** -1216, `~/gnuradio-pkg`, Ubuntu's UHD 4.9.0.1 (my reading) | RTL-SDR.COM v3 | presumably `gr-soapy` (my reading) | **Good** (user, 2026-10-31) |

Transmit: on 24.04 (GMKtec, `v2.3`; the other tester with a HackRF, a
LimeSDR Mini and a B200mini, `v2.3` and `v3.0-rc1`), on 26.04 (GMKtec,
`v2.4` and `v3.0-rc1`), on 26.10 (ASUS, `v3.0-rc1`, Ubuntu's UHD 4.9.0.1),
and on Fedora 44 (by hand): B200mini (30 dB attenuator) and PlutoSDR
loopbacks.

## Open items

- **`v3.2` release on hold until after the weekend** (user, 2026-11-06, a Friday: "wait until after the weekend in case jesternofool does run the tests"), so not before Monday 2026-11-09. Ready otherwise: `v3.2-rc1` passed on the 26.04 and 24.04 GMKtec; `v3.2` would be a new tag on `5197d45` with all three scripts attached, then the wiki draft pasted (its loop downloads three files from `releases/latest`). If the tester reports, record the results first.
- **Waiting for the developers** (user, 2026-10-16): where the scripts live
  ("the plan is to bring it into the gnuradio/gnuradio repo", details not
  settled; if it moves, the download links in the wiki draft, README, and
  Release notes, and the repo URLs here, need updating), Fedora support,
  the `qa_fastnoise` backport. **Update (user, 2026-11-02):** "the lead
  developer/maintainer is inclined to put this package in the
  https://github.com/gnuradio/gnuradio-docker repo". Checked by me
  (2026-11-02): default branch `master`; no license file; no Releases and
  no tags; top level `.github`, `ci`, `tools`, `README.md`; its README
  says the repo holds the CI containers (`ci/<distro>-<version>-<GR
  version>`), built by `.github/workflows/build-dockers.yml` on pushes and
  PRs to `master`; the images include Debian 12/13/14, Fedora 42/43/44
  (`fedora-44-3.11`, `-4.0` too), and Ubuntu 24.04/26.04 `-4.0`. The user
  is considering renaming this repo, as the current name doesn't fit the
  project any more (information only, before 2026-11-02); moot if it moves.
- **Uninstaller, `gnuradio_uninstaller.py` (user, 2026-11-02: "write a
  shell or Python program to check for and uninstall any GNU Radio version
  previously installed ... avoid copy and paste instructions"; to replace
  UnInstallGR and "Before you start"'s clean-up).** Drafted by me;
  on `main` since `379ef82`, not in a Release. Python, same conventions as the other two (as the user,
  `sudo` only for root commands, `--dry-run`, `-y`; plus `--prefix` and
  `--settings`). It surveys first and changes nothing until confirmed. It
  finds Ubuntu's packages (`apt-get -s remove` shows dependents), GNU
  Radio PPA files, and source installs in `/usr/local`, `/opt` (2 levels)
  and `~` (4 levels, no hidden dirs or mounts). A prefix is removed whole
  only if it has our `setup_env.sh` marker or a PyBOMBS `.pybombs`;
  otherwise file by file (manifest from a matching build dir, plus the
  UnInstallGR patterns), then `ldconfig`. It also removes the GRC desktop
  files, GNU Radio build dirs in `~`, and a source-built UHD in
  `/usr/local`. Conda environments, `/etc/profile.d`, `sources.list`
  lines and PyBOMBS itself are only listed. **User's decisions
  (2026-11-02):** remove a source-built UHD too, as its own item; remove
  GNU Radio lines from `~/.profile`, `~/.bashrc`, `~/.bash_aliases` (and
  `~/.bash_profile`, my addition) with a `.bak` copy; keep the settings
  folders unless `--settings`. Checked by me: dry run on the LENOVO
  (`~/gnuradio-pkg`, 45 desktop files, build dir, `~/.profile` line 28);
  a real run on a fake home and prefix (PyBOMBS prefix, shared prefix with
  manifest, conda env kept, start-up lines); the program and man-page
  patterns match all 20 / 23 in `~/gnuradio-pkg`. **GMKtec Round 1
  (26.04, 2026-11-02; `379ef82` from `main`):** set up with Ubuntu's
  `gnuradio` (`apt-get install`) and `ppa:gnuradio/gnuradio-releases`
  (no `resolute` build, Release 404; entry written anyway) on top of the
  `v3.1-rc1` `~/gnuradio-pkg` install. Dry run and real run
  (`~/share/uninst-dry1.log`, `uninst-run1.log`): `~/gnuradio-pkg`, GRC
  desktop files, `~/gnuradio/build`, the 24 Ubuntu packages (`apt-get
  remove`; `libuhd4.9.0`, `python3-networkx`, `python3-pyqt5.qwt` left
  for autoremove), the PPA `.sources` file (then `apt-get update`: only
  the Ettus PPA left), the `~/.profile` line (`.bak` written): **all
  removed as listed**. **Bug found:** the 46th GRC file was
  `/usr/share/mime/application/gnuradio-grc.xml`, which
  `update-mime-database` generates from Ubuntu's package (so `dpkg -S`
  doesn't claim it); it was removed with `sudo rm`. No harm this time
  (apt's `shared-mime-info` trigger rebuilt `/usr/share/mime` right
  after). **Fixed (uncommitted):** `mime/application/gnuradio-grc.xml`
  dropped from `GRC_DESKTOP_PATTERNS`; `sudo update-mime-database` /
  `update-desktop-database` run for a system share dir whose GRC files
  are removed (LENOVO dry run: 44 files, was 45). **Not run yet:** the
  `/usr/local` and source-UHD paths (Round 2: builder `--prefix
  /usr/local` on `maint-3.10`, UHD `v4.11.0.0` from source into
  `/usr/local`, dry runs with and without the build dir visible).
  **Round 2 so far** (user, 2026-11-02): the builder's `--prefix
  /usr/local` build finished; **GRC's desktop files went to `/usr/share`**
  (root's `grc_setup_freedesktop`, xdg system mode), not
  `/usr/local/share`, so the system branch of the `7c872b1` fix runs
  there. UHD `v4.11.0.0` from source on 26.04: `apt-get build-dep uhd`
  (Ubuntu's older UHD) is not enough; cmake also needed
  `libprotobuf-dev protobuf-compiler` and then `libgrpc++-dev
  protobuf-compiler-grpc` (`lib/usrp/common/CMakeLists.txt:72/74`).
  **Round 2 dry runs** (`7c872b1`; `~/share/uninst-dry2-manifest.log`,
  `uninst-dry2-patterns.log`, 2026-11-02): GNU Radio in `/usr/local`
  140 paths from the manifest vs 138 from the patterns alone (build dir
  hidden as `~/.gr-build-hidden`); GRC: 23 files in `/usr/share`
  (hicolor icons only in system mode); `~/gnuradio/build`; UHD in
  `/usr/local` from `~/uhd/host/build/install_manifest.txt` (169 paths;
  its build dir kept). The two the patterns missed (found by me with a
  fake tree built from `step2-usrlocal.log`'s 17,268 installed files):
  `share/bash-completion/completions/gr_modtool` and
  `share/zsh/site-functions/_gr_modtool`. **Added to
  `GNURADIO_FILE_PATTERNS`** (uncommitted); the patterns now cover all
  17,268 (140 paths).
  **Round 2 real run** (`7c872b1`, manifest path, user's checks,
  2026-11-02): `find /usr/local` for gnuradio / uhd / `gr_modtool`:
  nothing; `/usr/share/applications/gnuradio-grc.desktop` gone and no
  GRC file left in `/usr/share/mime/application` (the MIME rebuild
  worked); `ldconfig -p`: no `gnuradio`, `libuhd` only in
  `/usr/lib/x86_64-linux-gnu` (4.11.0 from the PPA, plus Ubuntu's 4.9.0
  left from Round 1 because `apt autoremove` wasn't run).
  `~/share/uninst-run2.log`: `sudo rm` of the 140 GNU Radio paths, the 23
  GRC files, then `sudo update-mime-database /usr/share/mime` and `sudo
  update-desktop-database /usr/share/applications`; `sudo rm -rf
  ~/gnuradio/build` (root-owned files from `sudo make install`); `sudo
  rm` of the 169 UHD paths; one `sudo ldconfig` at the end; "Done."
  **All `sudo` paths now run once on the GMKtec.** `uhd_find_devices`
  with the PPA's UHD afterwards **found the B200mini** (user,
  2026-11-02). **Rounds 1 and 2 passed.** Docs not changed yet (my proposal: "Before you start"
  runs it; the builder's / Step 1's errors point to it; UnInstallGR gets a
  "Use the script" section with the manual sections kept); planned as
  `v3.2-rc1`.
- **UnInstallGR with the uninstaller** (user, 2026-11-08: "yes, draft
  both"; uncommitted). **Uninstaller OS check:** it had none, and
  `owned_by_package()` answers "not owned" when `dpkg-query` is missing, so
  on Fedora it would have listed the `gnuradio` RPM's GRC files in
  `/usr/share` for `sudo rm` (found by me). Now `main()` reads
  `/etc/os-release` (`--os-release-path`, as in Step 1) and stops unless
  `ID` or `ID_LIKE` has `ubuntu` or `debian` and `dpkg-query` exists;
  docstring updated. Checked by me: LENOVO `--dry-run` byte-identical to
  `HEAD`'s; fake os-release files: Fedora 44 stops (rc 1, "Nothing was
  changed"), Linux Mint (`ID_LIKE="ubuntu debian"`) and Debian 13 run; a
  missing file stops. Not in `v3.2` (tag planned on `5197d45`), so the
  `v3.2` uninstaller has no OS check (my note). **`UnInstallGR.mediawiki`
  draft** (local; the live-page version saved in the session scratchpad
  only): intro sentence pointing to the script; new first section "Using
  the uninstaller script" (Ubuntu, Debian and derivatives; one-line Python
  download from `releases/latest` into `~/gr-installers`, checked against
  the `v3.2-rc1` asset; `--dry-run`, run, what it removes / keeps / only
  lists, log out, options table), adapted from the Building draft's
  section; the manual `/usr/local` `rm -f` list gains the two `gr_modtool`
  completion files; new "UHD Built from Source" subsection (`sudo make
  uninstall` in UHD's build dir, `sudo ldconfig`; UHD's `host/CMakeLists.txt`
  has an `uninstall` target, checked by me, not run). All manual sections
  kept (PyBOMBS, pre-3.10 folders). **Not to be pasted before a Release has
  the uninstaller**; better after the one with the OS check (my
  recommendation), since Fedora users read the same page and the `v3.2`
  script has no OS check.
- **Upstream `grc_tests` fix:** not on `main` as of `862edb76b` (a second
  plain `make test` on 26.04 failed `grc_tests`, 2026-10-18). When it lands,
  remove the builder's `git clean` step and its doc bullet in a new tag.
- **#8239 (Thrift on `main`):** open. When fixed, `main` on 26.10 should
  give 42 components; consider adding the Thrift packages to Step 1 only if
  the developers keep ControlPort/Thrift (user, 2026-10-19). An existing
  `build/` keeps `ENABLE_CTRLPORT_THRIFT=OFF` cached.
- **#8253 (QT GUI Range slider with PyQt6, `event.x()`):** open, filed by
  the user 2026-10-24; watch it (user, 2026-10-31). Upstream, nothing for
  the scripts; drop it from the Known limitations of the Release notes
  once fixed.
- **Qt6 on 24.04 / 26.04:** `gr-qtgui` on `main` waits for Qwt for Qt6
  there; `gnuradio-companion --qt` on `main` doesn't work there (see Useful
  facts). Nothing for the scripts to do.
- **`v3.1-rc1` (user, 2026-10-30: "let's create a v3.1-rc1 but don't
  mark it Latest. include the changes we have planned for it such as the
  log-order fix"):** contents: the builder's `~/.profile` echo message
  (`d9197fa`); the log-order fix, `sys.stdout.reconfigure(line_buffering=True)`
  at the start of `main()` in **both** scripts (the builder's own `$ ...`
  lines before its unlogged steps had the same problem, my addition); the
  docs' leftover-library command with
  `~/gnuradio-pkg/bin/gnuradio-config-info` (README and wiki draft).
  Checked by me: Step 1 `--dry-run` output byte-identical to `v3.0`'s;
  builder `--dry-run` runs; a line-buffered print stays in order with a
  child's output in a pipe. To be a GitHub **pre-release, not Latest**
  (user's request), both scripts attached, so `releases/latest` stays
  `v3.0`.
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

- **Debian support (asked about by the user 2026-10-29; not decided; talk
  to the developers first, like Fedora). PAUSED (user, 2026-10-30: "With
  all of the differences involved with Debian, I want to save some notes
  and stop work on it").** **Code reverted** (user, 2026-10-30: "revert
  the code to before Debian"): both scripts restored to `6346964`, so
  Step 1 is identical to `v3.0` again and the builder differs from `v3.0`
  only by `d9197fa` (the `~/.profile` echo message). The Debian code stays
  in history: Step 1's Debian path and builder wording in `fa1db6b`, the
  builder's `UHD_IMAGES_DIR` line in `a8a93dc`; restore from there if
  Debian support is taken up again. Debian 13
  results: Step 1 and builder OK, 269/269, 42 components, GRC from the
  desktop, B200mini found and loopback OK (with `UHD_IMAGES_DIR`);
  RTL-SDR works (user, 2026-10-30); PlutoSDR not working yet. Differences found on
  Debian 13, each needing its own handling:
  1. no PPA (Debian's UHD 4.8), one-line `sources.list` (`deb-src`
     already on), possibly no `sudo` (root password set at install);
  2. UHD can't find its images (loaded through `/lib`, so `Package path:
     /lib`, empty images dir), fixed by `UHD_IMAGES_DIR`;
  3. **PlutoSDR over USB:** `lsusb` sees it (`0456:b673`) and the USB
     network interface `enx00e022e5fb58` appears, but NetworkManager
     leaves it `disconnected` with no address, so `ip:pluto.local` fails
     ("Avahi Resolver: Failed to resolve host 'pluto.local'", "Unable to
     create context") and `ping 192.168.3.1` gets nothing. (The user's
     Pluto is at `192.168.3.1`, not the factory `192.168.2.1`; resolved
     from the LENOVO with `avahi-resolve`.) `nmcli device connect
     enx00e022e5fb58` connected it, **but the GMKtec's Remote Desktop
     from the LENOVO stopped working** (user, 2026-10-30); cause not
     checked (my guess: the Pluto's DHCP gave a default route and/or DNS;
     untested fix: `nmcli connection modify <name> ipv4.never-default yes
     ipv4.ignore-auto-dns yes ipv6.method ignore`). The user unplugged the
     Pluto and rebooted: connectivity back. Whether the saved NM profile
     reconnects when the Pluto is plugged in again: not known (my note: it
     probably will, with the same effect). Workaround not tried: a `usb:`
     URI from `iio_info -s` in the PlutoSDR blocks, which needs no
     network;
  4. `qt.qpa.plugin: Could not find the Qt platform plugin "wayland"`
     when running a flowgraph: harmless, Qt5 falls back to XWayland;
     Debian's desktop lacks `qtwayland5`, which Ubuntu's has (my reading);
  5. the GNOME Settings Remote Desktop switch locks up; set up with
     `grdctl` instead (see Machines).
  - Debian's packages (Debian's package database, 2026-10-29): UHD 4.3.0.0
    (12 bookworm) / 4.8.0.0 (13 trixie) / 4.9.0.1 (forky); Debian's GNU
    Radio 3.10.5.1 / 3.10.12.0 / 3.10.12.0; Python 3.11 / 3.13; Qwt 6.1.4
    (Qt5 only) in 12 and 13, `libqwt-qt6-dev` (6.3.0) only in forky;
    `soapysdr0.8-module-all` in all three.
  - **A developer's report** (via the user, 2026-10-29): on Debian 13 he
    "had to manually install qwt but had to checkout version qwt-6.3 and
    not use the main git branch", and he didn't use the scripts but ran
    each command by hand. My reading: Qwt for Qt6 built from source, for
    `main`'s `gr-qtgui` (Debian 13 has no `libqwt-qt6-dev`); not known:
    which branch, results, whether `deb-src` / `sudo` needed setting up.
  - My proposal: Step 1 accepts `ID=debian`; no PPA (Debian's UHD, the
    26.10 path); enable `deb-src` in the one-line `sources.list` format as
    well as deb822 (what the Debian 13 installer writes not checked); a
    check and fix text for a user without `sudo` (root password set at
    install; not the case on the GMKtec, where no root password was set
    and `sudo` works, user 2026-10-29). The Qt6 step needs no change (keyed on `libqwt-qt6-dev`), so
    `main` on Debian 13 gets no `gr-qtgui`, as on Ubuntu 24.04 / 26.04;
    building Qwt from source is outside the apt-only scripts (at most a
    docs note). Builder: wording only. Docs: Debian notes. Target Debian 13
    (and later) only, my recommendation. Testing: clean Debian 13 on the
    GMKtec, both branches, the three SDRs; Ubuntu re-run.
  - **Debian 13 is a `maint-3.10` system** (user, 2026-10-29: "It seems
    to be a 'maint-3.10' oriented system"). In `gnuradio/gnuradio-docker`
    `ci/` (checked 2026-10-29), Debian 13 has only `ci-debian-13-3.10`
    (Qt5: `libqwt-qt5-dev`, `qtbase5-dev`, `python3-pyqt5`, Debian's
    `libuhd-dev`, `libsoapysdr-dev`, Thrift, `python3-pytest`), and
    `ci-debian-14-3.11` exists besides `ci-debian-14-3.10`. **Corrected
    2026-11-08:** I first read this as "`main` is paired with Debian 14,
    so Debian 13 support would mean `maint-3.10` only". Wrong: the image
    suffix is not the branch. `main`'s own
    `.github/workflows/make-test.yml` (checked by me) builds Debian 13 in
    `debian-13-3.10` and Ubuntu 24.04 in `ubuntu-24.04-3.10`, besides
    `ubuntu-26.10-3.11`, `fedora-44-3.11` (also for its "Fedora 45" job)
    and `debian-i386-14-3.11`. So `main` builds on Debian 13 too, without
    `gr-qtgui` presumably (no `libqwt-qt6-dev`; my reading), as on Ubuntu
    24.04 / 26.04. **How to read the CI images:** look up which image a
    branch's `make-test.yml` matrix pulls, not which image names exist.
    The `-4.0` images (`ubuntu-24.04-4.0`, `-4.0-emscripten`,
    `ubuntu-26.04-4.0`, `fedora-44-4.0`) are for GNU Radio 4.0
    (`gnuradio4`: `vir-simd`, `libboost-ext-ut-dev`, `libcpr-dev`, no
    Qt/UHD/Thrift), used by neither `main` nor `maint-3.10`; no 3.x CI
    tests Ubuntu 26.04.
  - **Debian 13 sources** (GMKtec, netinst 13.7.0 with firmware,
    `/home/barry/debian13-sources.txt`, 2026-10-29): only the one-line
    `/etc/apt/sources.list` (`sources.list.d/` empty, no deb822 file);
    **`deb-src` lines already enabled** for `trixie`, `trixie-security`,
    `trixie-updates`; components `main non-free-firmware` only (GNU Radio,
    UHD, SoapySDR are all in `main`). So `apt-get build-dep` needs no
    change on a fresh Debian 13; Step 1 would only check for `deb-src` (and
    add the matching lines if missing). Checked by me in Debian 13's
    packages: `libuhd-dev` 4.8.0.0 Recommends `gnuradio-dev` (so
    `--no-install-recommends` still needed) and has no Boost dependencies
    (Boost list still needed); `uhd-host` ships `uhd_images_downloader`.
  - **Debian changes drafted** (user, 2026-10-29: "yes, draft the Debian
    changes"; uncommitted in the working tree, not run on Debian yet). Step
    1: `ID` `ubuntu` or `debian` (`DISTRO_NAMES`); on Debian no PPA check
    and no `software-properties-common` (`DEBIAN_TOOL_PACKAGES = ["git"]`);
    sources file `debian.sources` (deb822) if present, else `sources.list`,
    where `enable_source_code_one_line()` adds a `deb-src` line after each
    `deb` line that has none (cdrom left alone; a second run adds nothing);
    `SUDO_HINT` (root password set at install: `su -`, `apt-get install
    sudo`, `usermod -aG sudo <user>`) when `sudo` is missing or `sudo -v`
    fails; messages name the distro. `--sources-path` now defaults per
    distro. Checked by me: Ubuntu `--dry-run` output byte-identical to
    `v3.0`'s on the LENOVO; Debian `--dry-run` with a fake os-release and
    the GMKtec's `sources.list` ("already enabled"), and with its `deb-src`
    lines removed (3 added, identical to the original). Builder: "Ubuntu's
    own" → "the system's own" in the conflict error and the **DON'T!**
    line. **Run on the clean Debian 13 GMKtec** (user, 2026-10-29),
    `maint-3.10`: UHD 4.8.0.0+ds1-2, 269/269, 3.10.12.0 in
    `~/gnuradio-pkg`, 42 components, and a flowgraph runs
    from the desktop (see Test results). **USRP images on Debian 13
    (user, 2026-10-30: "add UHD_IMAGES_DIR to setup_env.sh in the
    builder"):** Debian's UHD 4.8 reports no images directory although
    `uhd_images_downloader` filled `/usr/share/uhd/4.8.0/images`; the
    builder's `uhd_images_dir_to_set()` runs `uhd_config_info --version
    --images-dir` (with `UHD_IMAGES_DIR` removed from its environment), and
    if the images directory is empty and `/usr/share/uhd/<version>/images`
    has files, `setup_env.sh` gets `[ -n "$UHD_IMAGES_DIR" ] || export
    UHD_IMAGES_DIR=...`. Uncommitted. Checked by me: on the LENOVO (26.10,
    images dir `/usr/share/uhd/4.9.0/images`) nothing is added and
    `setup_env.sh` comes out identical; with a faked Debian answer the line
    is added. Committed in `a8a93dc`; **on the Debian 13 GMKtec the B200mini
    is found now** (user, 2026-10-30); **B200mini loopback works** (user,
    2026-10-30); **RTL-SDR works** (user, 2026-10-30). Paused before the
    PlutoSDR works (see the PAUSED
    note above).

## Drafts

### Fedora notes for the developers (drafted 2026-11-08; not sent)

For the user to send to the GNU Radio developers (user, 2026-11-08: "save
some notes on Fedora for the developers"). From the Fedora 44 trial
(2026-10-16) and the proposal under Open items. The size estimates are mine,
not measured.

~~~~markdown
## Fedora support for the build scripts: notes

The three scripts (Step 1 `gnuradio_dependencies_installer.py`, Step 2 `gnuradio_clone_builder.py`, and `gnuradio_uninstaller.py`) support Ubuntu only: 24.04 and 26.04, and 26.10 works too. Before adding Fedora, I'd like your views on the questions at the end.

### What I tried

On a clean **Fedora 44** (x86_64), I built **`maint-3.10`** by hand, the way the scripts would:

- Fedora's own UHD: `sudo dnf install uhd uhd-devel uhd-tools uhd-firmware` (4.9.0.1)
- `sudo dnf builddep gnuradio`
- cmake, make, make test, make install

`main` was not tried on Fedora.

**Results:**

- GNU Radio 3.10.12.0 installed and imports.
- **41 components**: Ubuntu's 42 minus Thrift. `gr-uhd` with RFNoC, `gr-iio` with `libad9361`, `gr-qtgui` and `gr-soapy` are all there.
- **269/269** after one test fix (see below).
- GNU Radio Companion works.
- Hardware: a USRP B200mini loopback (transmit and receive, 30 dB attenuator) and a PlutoSDR loopback both worked, and an RTL-SDR received broadcast FM in stereo. No udev changes were needed: Fedora's `uhd` package rules are enough.

### Problems found

1. **`qa_fastnoise` fails on `maint-3.10`.** It's the Laplacian variance check (`test_001_real_laplacian_moments`): the variance came out at 1.99293, against `places=2`. `main` fixed this tolerance in `aee9fd3f7` ("qa_fastnoise: Widen the Laplacian variance tolerance", `places=2` → `delta=0.05`). That commit doesn't cherry-pick onto `maint-3.10`, because `56d230fd3` changed the same lines on `main`, but the one-line change by hand works: 269/269. The builder stops on any failing test, so it would stop on Fedora `maint-3.10` builds whenever this test fails.
2. **No Thrift.** `dnf builddep gnuradio` doesn't bring `thrift-devel` or `python3-thrift`, though both are in Fedora 44. Adding them by name would fix it on `maint-3.10`. On `main`, Thrift is off anyway until #8239 is fixed.
3. **Python modules go to `lib64`:** `<prefix>/lib64/python3.14/site-packages`, not `lib/`. The builder's `setup_env.sh` and its stale-directory check, and the uninstaller's patterns, only look under `lib/` today.
4. **UHD is Fedora's 4.9.0.1,** not 4.11 as from the Ettus PPA on Ubuntu. There is no PPA equivalent, so the docs would just say so.

### What adding Fedora would take

- **Step 1:** the largest change. A second path chosen by `ID` in `/etc/os-release`, with the Ubuntu path unchanged:
  - `dnf builddep gnuradio`, plus `dnf install` of `uhd uhd-devel uhd-tools uhd-firmware python3-QtPy python3-pyqtgraph python3-matplotlib python3-pytest thrift-devel python3-thrift`
  - the SoapySDR modules from `dnf`'s list of `soapy-*` packages, since there's no metapackage. `soapy-uhd` can stay, as it uses the same UHD.
  - a conflict check with `rpm -q gnuradio gnuradio-devel python3-gnuradio`
  - no `deb-src`, PPA, or `uhd_images_downloader` steps: `uhd-firmware` brings the images.
- **Step 2 (builder):** small. `rpm -q uhd-devel` instead of `dpkg-query libuhd-dev`, and `lib64` paths in `setup_env.sh` and the install-directory patterns. Plus a decision on `qa_fastnoise` (see below).
- **Uninstaller:** moderate. It is apt-only today (`apt-get -s remove`, `dpkg -S`, PPA files), so it would need an `rpm` / `dnf` back end, COPR repositories in place of PPAs, and the `lib64` patterns.
- **Docs:** Fedora notes on the wiki page.
- **Testing:** a clean Fedora install for each change, and Ubuntu re-run to show nothing changed there.

My rough guess: Step 1 grows by about half, the builder by a few dozen lines, and the uninstaller needs a second package back end.

### Questions

1. **Is Fedora support wanted** in these scripts, and if so, for `maint-3.10`, `main`, or both? CI tests `main` on Fedora (`fedora-44-3.11`, and `fedora-45-3.11` exists) and `maint-3.10` on Fedora 42 and 43.
2. **`qa_fastnoise`:** could the tolerance change from `aee9fd3f7` be backported to `maint-3.10`? That's my preference. Otherwise, the builder could get an option to skip named tests, or the docs could describe the one-line edit.
3. **Thrift:** should Step 1 install it on Fedora, given that ControlPort/Thrift may be dropped?
4. **Where the scripts live:** if they move into `gnuradio/gnuradio-docker` (or elsewhere), should Fedora support wait until after the move?
~~~~

### Debian notes for the developers (drafted 2026-11-08; not sent)

For the user to send to the GNU Radio developers (user, 2026-11-08: "Let's
do the same for Debian"). From the Debian 13 runs (2026-10-29/30) and the
Debian items under Open items. Line counts from `git show --stat`; the
uninstaller estimate is mine.

~~~~markdown
## Debian support for the build scripts: notes

The three scripts (Step 1 `gnuradio_dependencies_installer.py`, Step 2 `gnuradio_clone_builder.py`, and `gnuradio_uninstaller.py`) support Ubuntu only: 24.04 and 26.04, and 26.10 works too. I tried them on Debian 13, and it went better than Fedora because Debian is apt-based too. The work is paused and the code reverted, but it's kept in the repository's history. I'd like your views on the questions at the end.

### What I tried

On a clean **Debian 13** (trixie, netinst 13.7.0, x86_64), I ran a Debian version of Step 1 and the builder on **`maint-3.10`**, installing into `~/gnuradio-pkg`. `main` was not tried.

**Results:**

- Debian's UHD **4.8.0.0+ds1-2**.
- **269/269**, GNU Radio 3.10.12.0, **42 components**, the same as on Ubuntu.
- A flowgraph runs from GRC started from the desktop.
- Hardware: a USRP B200mini loopback worked (after the images fix below), and an RTL-SDR received. The **PlutoSDR did not work** (see below).

### Problems found

1. **No PPA, so Debian's own UHD.** That's 4.8 on Debian 13 (4.9.0.1 in forky), not 4.11 as from the Ettus PPA on Ubuntu.
2. **UHD can't find its images.** `uhd_images_downloader` puts them in `/usr/share/uhd/4.8.0/images`, but `uhd_config_info` reports `Package path: /lib` and an empty images directory, so `uhd_find_devices` fails with "Could not find path for image: usrp_b200_fw.hex". My reading: Debian's UHD gets loaded through `/lib`, which is a link to `/usr/lib`, so it looks under `/share`. The fix was to have the builder add `export UHD_IMAGES_DIR=/usr/share/uhd/<version>/images` to `setup_env.sh`, but only when UHD reports an empty images directory. On Ubuntu nothing changes.
3. **PlutoSDR over USB.** `lsusb` sees it and its USB network interface appears, but NetworkManager leaves the interface disconnected with no address, so `ip:pluto.local` doesn't resolve. `nmcli device connect` brought it up, but it also broke the machine's other network access (Remote Desktop dropped) until the Pluto was unplugged and the machine rebooted. My guess is that the Pluto's DHCP took over the default route or DNS. Not tried: the connection settings `ipv4.never-default yes` and `ipv4.ignore-auto-dns yes`, or a `usb:` URI in the PlutoSDR blocks, which needs no network at all.
4. **The sources format differs.** Debian 13 uses the one-line `/etc/apt/sources.list`, not Ubuntu's deb822 `ubuntu.sources`. The netinst install already had its `deb-src` lines enabled, so `apt-get build-dep` needed no change there.
5. **There may be no `sudo`.** If a root password is set during the install, the user isn't put in the `sudo` group, and both scripts rely on `sudo`. On the test machine no root password was set, so `sudo` worked.
6. **`Could not find the Qt platform plugin "wayland"`** appears when a flowgraph runs. It's harmless: Qt5 falls back to XWayland. My reading is that Debian's desktop lacks `qtwayland5`, which Ubuntu's has.

Same as Ubuntu:

- Debian 13's `libuhd-dev` also Recommends `gnuradio-dev`, so `--no-install-recommends` is still needed.
- It also declares no Boost dependencies, so the explicit Boost list is still needed.
- `soapysdr0.8-module-all` exists, and gives 11 modules, the same set as Ubuntu 24.04. There's no PlutoSDR Soapy module, which doesn't matter, because `gr-iio` covers the Pluto.

### `main` on Debian 13

Debian 13 has no `libqwt-qt6-dev` (it's only in forky), so `main` would build without `gr-qtgui`, as on Ubuntu 24.04 and 26.04. That's my reading; I didn't try it. One developer reported building Qwt 6.3 from source on Debian 13 for this. That's outside what apt-only scripts can do, so at most it would be a note in the docs. GNU Radio's own CI builds `main` on Debian 13 (in the `debian-13-3.10` image).

### What adding Debian would take

Much less than Fedora, since the package tools are the same. It was drafted and run:

- **Step 1:** accept `ID=debian`. On Debian, skip the PPA check and `software-properties-common`. Enable `deb-src` in either the one-line or the deb822 format, adding lines only where they're missing. Print a hint when `sudo` is missing or fails. The draft changed about 180 lines of Step 1 (160 added, 48 removed), and its Ubuntu `--dry-run` output stayed byte-identical.
- **Builder:** the `UHD_IMAGES_DIR` line (about 50 lines) and "Ubuntu's" → "the system's" in two messages.
- **Uninstaller:** written after the Debian work, so not tried on Debian. It uses `apt-get` and `dpkg` like the other two, so I'd expect little to change apart from messages. That's my estimate.
- **Docs:** Debian notes on the wiki page: `sudo`, UHD 4.8, and the PlutoSDR network setting once it's understood.
- **Testing:** a clean Debian 13 with both branches and all three SDRs, and Ubuntu re-run.

### Questions

1. **Is Debian support wanted**, and for which branch? Debian 13 looks like a `maint-3.10` system: it has Qt5 Qwt only, and Debian's own GNU Radio is 3.10.12. Debian 14 would be the one where `main` gets `gr-qtgui`.
2. **The PlutoSDR network problem:** has anyone seen it on Debian, and is a `usb:` URI the better way to recommend?
3. **Where the scripts live:** if they move into `gnuradio/gnuradio-docker` (or elsewhere), should Debian support wait until after the move?
~~~~

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

### v3.2-rc1 test request for the other tester (drafted 2026-11-02; sent by the user 2026-11-02)

For the user to send to jesternofool. Part A runs on the tester's machine
as it is (my assumption: it still has a `v3.0`/`v3.1` install in
`~/gnuradio-pkg`); Part B is optional and puts the GNU Radio PPA's
packages on it (the PPA has a `noble` build), the one path not yet tested
with real PPA packages; Part C rebuilds from the clean state.

~~~~markdown
Hi! Thanks for all the testing so far. There's a release candidate for the next version, `v3.2-rc1`, and I'd like your help with it on Ubuntu 24.04.

**What's new:** a third script, `gnuradio_uninstaller.py`. It finds every GNU Radio installed on the machine, however it was installed, and removes it:

- Ubuntu's packages and GNU Radio PPAs
- installs in `~/gnuradio-pkg`, `/usr/local` or a PyBOMBS prefix
- GRC's menu entry
- build directories
- a UHD built from source in `/usr/local`
- the GNU Radio lines in `~/.profile` and friends (each file is backed up to `.bak` first)

It lists everything it found and changes nothing until you answer `y`. Step 1 and Step 2 now point to it when they find something in the way. Otherwise they are the same as v3.1.

This time you don't need a clean install to start with: the more GNU Radio your machine has on it, the better the test.

```bash
# Download the three rc1 scripts
mkdir -p ~/gr-v3.2 && cd ~/gr-v3.2
for f in gnuradio_dependencies_installer.py gnuradio_clone_builder.py gnuradio_uninstaller.py; do python3 -c "import sys, urllib.request; urllib.request.urlretrieve(sys.argv[1] + sys.argv[2], sys.argv[2])" https://raw.githubusercontent.com/duggabe/gr-wiki-revision/v3.2-rc1/ $f; done
```

**A. The uninstaller on your machine as it is now**

```bash
cd ~/gr-v3.2
python3 gnuradio_uninstaller.py --dry-run 2>&1 | tee uninst-dry.log
```

Please check the list before going on. Does it show everything you know is installed, and nothing that isn't GNU Radio's? If it looks right, run it for real, as yourself (NOT with sudo):

```bash
python3 gnuradio_uninstaller.py 2>&1 | tee uninst-run.log
python3 gnuradio_uninstaller.py --dry-run     # should find nothing now
```

**B. Optional: Ubuntu's GNU Radio from the GNU Radio PPA**

This puts the PPA's GNU Radio on the machine, so that Step 1 has something to stop on and the uninstaller has real PPA packages to remove:

```bash
sudo add-apt-repository -y ppa:gnuradio/gnuradio-releases
sudo apt-get install -y gnuradio
python3 gnuradio_dependencies_installer.py      # should stop and point to the uninstaller
python3 gnuradio_uninstaller.py 2>&1 | tee uninst-ppa.log
```

**C. A fresh build after the clean-up**

```bash
python3 gnuradio_dependencies_installer.py 2>&1 | tee step1.log
cd ~/gnuradio && git fetch upstream && git checkout maint-3.10
cd ~/gr-v3.2 && python3 gnuradio_clone_builder.py 2>&1 | tee step2.log
```

The uninstaller removed the `setup_env.sh` line from `~/.profile`, so at the end Step 2 prints the command to add it back. Run that command, then log out of the desktop and back in. After that, the usual checks:

```bash
uhd_config_info --version
gnuradio-config-info --version --prefix
gnuradio-config-info --enabled-components | tr ';' '\n' | wc -l
```

**Please report:**

1. **Part A:** what the dry run found (or just send `uninst-dry.log`). Did it miss anything, or list anything it shouldn't? Did the real run finish, and did the second dry run find nothing?
2. **Part B (if you did it):** did Step 1 stop with the uninstaller's command? Did the uninstaller remove the packages and the PPA? Send `uninst-ppa.log`.
3. **Part C:**
   - the UHD version (it should be 4.11 from the Ettus PPA)
   - the `make test` result (I expect 269/269)
   - the prefix (it should be `/home/<you>/gnuradio-pkg/`)
   - the component count (I expect 42)
   - whether GRC is back in Activities and runs a flowgraph
4. Your devices, if you have time, as before.
5. Anything odd in any of the logs.

Thanks!
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

### QT GUI Range slider issue for `gnuradio/gnuradio` (drafted 2026-10-20; posted by the user as #8253 on 2026-10-24)

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
