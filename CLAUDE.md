# AIwork — UHD Bare-Metal Build Tooling

## Project summary

Tooling to build and install Ettus Research's UHD (USRP Hardware Driver) —
plus Volk and GNU Radio — directly on bare metal (no Docker), by reusing the
dependency list from EttusResearch's own Docker build environment
(`.ci/docker/uhd-builder-ubuntu2604.Dockerfile` in the `EttusResearch/uhd`
repo on GitHub).

Pushed to **https://github.com/duggabe/gr-wiki-revision** (public). Note:
that repo was originally created for GNU Radio wiki scripts (its
description still says so) — it was reused for this UHD project by explicit
choice rather than creating a separate repo, so the name/description don't
match this project's actual content. The repo's original auto-generated
`README.md` was merged in (`--allow-unrelated-histories`) rather than
overwritten.

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
  `uhd_bare_metal_installer.py` run (default `-o` filename). Has a few extra
  packages (`clang-format-14`, `swig`) and two duplicate entries
  (`libgps-dev`, `python3-ruamel.yaml`) vs. `uhd-ubuntu2604-dependencies.txt`
  — likely because upstream's Dockerfile has been updated since the bash
  script was written. Not yet reconciled — see Next steps.

- **`LICENSE`** — Creative Commons Attribution-ShareAlike 4.0
  International (CC BY-SA 4.0), added 2026-09-24. Note that Creative
  Commons advises against its licenses for software; kept as-is by choice.

- **`AI_notes.txt`** — running log/notes, including the machine-migration
  checklist (git/gh setup, CLAUDE.md, `.gitignore`, transferring `.env` and
  `~/.claude/projects/` history) used to move this project between machines.

## What's been done

- 2026-09-22: Built `install-uhd-build-deps.sh` from UHD's Ubuntu 26.04
  Dockerfile. Used it plus the GNU Radio wiki's from-source build guide
  (Draft-AN-445) to successfully build, with no errors, on the original
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
  recorded in `AI_notes.txt`: initialized git in `~/AIwork`, added
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
- **`uhd_find_devices` failure is tolerated, not fatal**, during `--build`,
  since a non-zero exit there just means no USRP hardware is attached, not a
  build failure.
- **Reused the existing `gr-wiki-revision` repo instead of creating a new
  one**, on explicit instruction, even though its name/description are for
  GNU Radio wiki scripts, not this UHD tooling. Its original `README.md` was
  merged in rather than overwritten.

## Next steps

1. Reconcile the discrepancy between `uhd-dependencies.txt` (latest live
   fetch: has `clang-format-14`, `swig`, and two duplicate packages) and
   `uhd-ubuntu2604-dependencies.txt` / `install-uhd-build-deps.sh` (no
   duplicates, missing those two packages) — likely just needs
   `install-uhd-build-deps.sh` refreshed against the current upstream
   Dockerfile, or the duplicates are a parsing bug worth checking in
   `extract_apt_packages()`.
2. Confirm `uhd_bare_metal_installer.py`'s OS auto-detection actually works
   as intended given the 24.04-dev / 26.04-test split: on the 24.04 dev box
   it should either fail cleanly (no matching Dockerfile upstream) or be run
   with `--dockerfile-url`/`--dockerfile-path` forcing the 26.04 file; real
   dependency installs and `--build` runs should only happen on the 26.04
   test machine where the hardware is.
3. ~~Turn this directory into a git repo and push to GitHub~~ — done:
   pushed to https://github.com/duggabe/gr-wiki-revision (see note above on
   repo name mismatch).
4. **Finish migrating to LENOVO** (in progress as of 2026-09-24 — LENOVO will
   be the only machine used for future work; this machine's `~/AIwork` becomes
   historical only): install `git`, `gh`, Claude Code; `gh auth login`; set
   git identity (`duggabe` / `barry@dcsmail.net`); `gh repo clone
   duggabe/gr-wiki-revision` (clones to `~/gr-wiki-revision` by default —
   that's the working directory on LENOVO, not `AIwork`). Session-history
   continuity (`~/.claude/projects/`, see `AI_notes.txt` step 8) won't carry
   over automatically since the directory name is changing; rely on this
   file for context on LENOVO instead.
5. Run/validate `uhd_bare_metal_installer.py --build` end-to-end on the
   Ubuntu 26.04 test machine to confirm it reproduces the successful
   UHD/Volk/GNU Radio build from the original machine.
6. Repo naming/description/visibility: confirmed 2026-09-24 to leave public
   for now. Revisit later if the mismatch (still named/described for GNU
   Radio wiki scripts) becomes a problem.
