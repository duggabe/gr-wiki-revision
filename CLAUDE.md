# gr-wiki-revision — Bare-Metal UHD / Volk / GNU Radio Build Tooling

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

**Two different Ubuntu versions are in play:** development/authoring happens
on **Ubuntu 24.04**, but the actual USRP hardware testing/build target is
**Ubuntu 26.04** (matching UHD's `uhd-builder-ubuntu2604.Dockerfile`). This
is exactly why `uhd_bare_metal_installer.py` auto-detects the host OS from
`/etc/os-release` and fetches the matching Dockerfile rather than hardcoding
one version — `install-uhd-build-deps.sh`, by contrast, only works correctly
on 26.04 since its package list is hardcoded from that Dockerfile. On a
24.04 host, expect `uhd_bare_metal_installer.py`'s auto-detect to fail (no
`uhd-builder-ubuntu2404.Dockerfile` upstream) unless `--dockerfile-url` /
`--dockerfile-path` is used to force the 26.04 Dockerfile explicitly.

## Files

- **`uhd_bare_metal_installer.py`** — the main tool. Fetches UHD's Dockerfile
  from GitHub (or a local path), auto-detects the host OS from
  `/etc/os-release` to pick the matching Dockerfile (e.g. Ubuntu 24.04 →
  `ubuntu2404`), parses out the `apt-get install` package list, and can:
  - `--list-only`: just print/save the parsed package list
  - `--dry-run`: show the commands that would run, no root needed
  - (default, run as root): actually `apt-get install` the dependencies
  - `--build`: additionally clone, `cmake`/`make`, install UHD from source,
    install udev rules, and run `uhd_find_devices` / `uhd_images_downloader`
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
  `uhd-ubuntu2604-dependencies.txt`. Re-run `--list-only` (and commit)
  whenever upstream's Dockerfile changes, or `volk_bare_metal_installer.py`'s
  content check will fail.

- **`volk_bare_metal_installer.py`** — builds/installs Volk from source
  after the UHD installer has installed deps. Imports parsing/build helpers
  from `uhd_bare_metal_installer.py` (incl. the shared `run_build_steps()`).
  Writes `volk-dependencies.txt` the same way as `--list-only`, aborts
  unless `uhd-dependencies.txt` exists, is older (by mtime — Linux has no
  reliable creation time), and has identical content (via the generic
  `check_dependency_lists()` over an ordered list of `DependencyList`s,
  shared with the GNU Radio installer), then runs `git clone
  --recursive` → cmake → make → `sudo make install` → `sudo ldconfig`.
  Installs no packages and doesn't need root; can run with or without sudo.
  Building is the default; `--build` is accepted and ignored, for
  consistency with the UHD installer.
  Both dependency-list filenames use hyphens, by the user's choice.

- **`gnuradio_bare_metal_installer.py`** — same shape as the Volk
  installer (imports from both earlier scripts). Writes
  `gnuradio-dependencies.txt`, aborts unless uhd → volk → gnuradio lists
  exist, are in that mtime order, and match, then runs `git clone` (not
  recursive) → cmake → make → `sudo make install` → `sudo ldconfig` into
  `~/gnuradio`. Adds `--volk-deps`; `--build` accepted and ignored.
  Caveat: git doesn't preserve mtimes, so on a fresh clone the committed
  uhd/volk lists may be out of order — refresh them in order with
  `--list-only` first (documented in README).

- **`volk-dependencies.txt`** — output of `volk_bare_metal_installer.py`
  (default `-o` filename), committed 2026-09-25 from a passing `--dry-run`.
  Rewritten on every run, so the Volk installer's own check survives a
  fresh clone; the GNU Radio installer's check may not (see its entry).

- **`gnuradio-dependencies.txt`** — output of
  `gnuradio_bare_metal_installer.py` (default `-o` filename), committed
  2026-09-25 from a passing `--dry-run`. Rewritten on every run.

- **`LICENSE`** — Creative Commons Attribution-ShareAlike 4.0
  International (CC BY-SA 4.0), added 2026-09-24. Note that Creative
  Commons advises against its licenses for software; kept as-is by choice.

- **`README.md`** — user-facing docs: project blurb, work-in-progress note,
  "Tested builds" table (UHD/Volk/GNU Radio versions), "Run the installers
  in order" (sudo requirements, the enforced order, refreshing in-between
  lists after re-running an earlier installer, removing `~/uhd` etc. before
  rebuilding), then a usage section per installer (options tables, build
  steps, examples, keeping the dependency lists current). Keep its options
  tables in sync with the scripts' argparse help.

- `AI_notes.txt` (running log incl. the machine-migration checklist) was
  removed from the repo on 2026-09-25; its content survives in git history
  (before commit `7472367`).

## What's been done

- 2026-09-22: Built `install-uhd-build-deps.sh` from UHD's Ubuntu 26.04
  Dockerfile. Used it plus the GNU Radio wiki's from-source build guide
  to successfully build, with no errors, on the original
  machine:
  - UHD 4.11.0.0-0-g0d7ed3b1
  - Volk 3.3.0
  - GNU Radio v3.11.0.0git-1174-gaee9fd3f
- 2026-09-24: Wrote `uhd_bare_metal_installer.py` to generalize the bash
  script — auto-detects host OS instead of hardcoding Ubuntu 26.04, fetches
  the Dockerfile live from GitHub instead of baking in the package list, and
  adds an end-to-end `--build` path (clone → cmake → make → install → udev
  rules) instead of just printing next-step instructions.
- Set this machine up for git/GitHub, following the migration checklist
  then recorded in `AI_notes.txt` (since removed): initialized git in `~/AIwork`, added
  `.gitignore`, committed, and pushed to the existing
  https://github.com/duggabe/gr-wiki-revision repo (merged with its
  pre-existing `README.md` via `--allow-unrelated-histories`).
- 2026-09-24: Now migrating to a new machine, **LENOVO**, which will be used
  for all future work going forward. On LENOVO the working directory will be
  the repo clone itself, `~/gr-wiki-revision` (not `~/AIwork` — that name
  only exists on this now-historical machine). Since the project is already
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
  machine's build).
- 2026-09-26: Made all three installers build as the normal user even when
  started with sudo, and chown the dependency lists back to the user (see
  Key decisions). Also: the UHD `--dry-run` "Build user" line now describes
  the required sudo run, and `/usr/local/lib` is only prepended to
  `LD_LIBRARY_PATH` if missing (no duplicate, no stray `:`). Chowned the
  existing root-owned `~/uhd` and `~/gnuradio`. Verified the full dry-run
  sequence in the repo: UHD `--dry-run --build` → Volk `--list-only` →
  GNU Radio `--dry-run` passes. Added the "Run the installers in order"
  section to `README.md`.

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
  runs as root via sudo, so `~/uhd`, `~/volk`, `~/gnuradio` aren't
  root-owned. `sudo` steps run as root. Real root (no `SUDO_USER`) builds as
  root. The dependency lists are written via the shared
  `write_package_list()`, which chowns them to `$SUDO_USER` under sudo (a
  newly created root-owned list would break a later non-sudo run). Still
  expected and harmless: `sudo make install` leaves a few root-owned files
  in each `build/` dir (`install_manifest.txt`, CMake `compiler_depend.*`),
  with or without starting the script via sudo. Real `sudo` runs of this
  code not yet tested (only simulated). `uhd_find_devices` now runs as the
  user *before* the udev rules are installed, so it couldn't see a USB USRP
  on a first build — irrelevant, since that call only checks that the
  freshly built UHD runs; no device is plugged in at that point (user
  confirmed 2026-09-26). Keep it where it is. `~/uhd` and `~/gnuradio` on
  the 26.04 machine were root-owned from builds before this change; fixed
  2026-09-26 with `sudo chown -R barry:barry ~/uhd ~/gnuradio`.
- **Re-running an earlier installer breaks the later order checks** — every
  run (even `--dry-run`/`--list-only`) rewrites that installer's list. Fix:
  refresh the in-between lists in order with `--list-only` (e.g. Volk's
  before GNU Radio's after a UHD re-run); the installer being run rewrites
  its own list first. Documented in README; accepted as the workflow rather
  than changing the check.
- **`uhd_find_devices` failure is tolerated, not fatal**, during `--build`,
  since a non-zero exit there just means no USRP hardware is attached, not a
  build failure.
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
2. Confirm `uhd_bare_metal_installer.py`'s OS auto-detection actually works
   as intended given the 24.04-dev / 26.04-test split: on the 24.04 dev box
   it should either fail cleanly (no matching Dockerfile upstream) or be run
   with `--dockerfile-url`/`--dockerfile-path` forcing the 26.04 file; real
   dependency installs and `--build` runs should only happen on the 26.04
   test machine where the hardware is. (2026-09-25: auto-detection
   confirmed working on an Ubuntu 26.04 host; 24.04 behaviour still
   untested.)
3. ~~Turn this directory into a git repo and push to GitHub~~ — done:
   pushed to https://github.com/duggabe/gr-wiki-revision.
4. **Finish migrating to LENOVO** (in progress as of 2026-09-24 — LENOVO will
   be the only machine used for future work; this machine's `~/AIwork` becomes
   historical only): install `git`, `gh`, Claude Code; `gh auth login`; set
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
7. Repo visibility: confirmed 2026-09-24 to leave public. (The name and
   description aren't a mismatch — see Key decisions.)
