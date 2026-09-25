# gr-wiki-revision
Scripts and programs to support GNU Radio Wiki documents

This is a work in progress.

## Install UHD in bare-metal environment

"uhd_bare_metal_installer.py" adapts the EttusResearch/uhd's .ci/docker build environment for bare-metal installation of UHD.

options:
  -h, --help            show this help message and exit
  --dockerfile-url DOCKERFILE_URL
                        URL of the Dockerfile to fetch. Default: auto-detect from /etc/os-release
                        and look up the matching file in EttusResearch/uhd's .ci/docker
                        directory.
  --dockerfile-path DOCKERFILE_PATH
                        Read the Dockerfile from a local path instead of fetching it.
  --list-only           Only parse and print/save the dependency list; do not install anything.
  -o, --output OUTPUT   Path to save the extracted package list (default: uhd-dependencies.txt).
  --dry-run             Print the apt/pip commands that would run, without executing or requiring
                        root.
  -y, --yes             Do not prompt for confirmation before installing.
  --skip-upgrade        Skip 'apt-get upgrade' (recommended on a machine you don't want fully
                        upgraded).
  --pip-index-url PIP_INDEX_URL
  --pip-index-host PIP_INDEX_HOST
  --os-release-path OS_RELEASE_PATH
                        Path to read NAME/VERSION_ID from for OS auto-detection (default:
                        /etc/os-release).
  --build               After dependencies install successfully, also clone and build UHD itself
                        into <home>/uhd (git clone, cmake, make -j(nproc-1), sudo make install,
                        sudo ldconfig, uhd_find_devices, sudo uhd_images_downloader, then
                        installs the udev rules and triggers udevadm so USRPs are usable without
                        root). Aborts with exit code 1 if any build step fails.
  --home HOME           Directory to clone/build UHD into (used with --build), overriding auto-
                        detection. Default: the invoking user's home when run via sudo
                        (SUDO_USER), else $HOME.

Examples
--------
  # Auto-detect the host OS and just print/save the dependency list (no install):
  python3 uhd_bare_metal_installer.py --list-only

  # Show exactly what would be run, without touching the system:
  python3 uhd_bare_metal_installer.py --dry-run

  # Actually install on a bare-metal host matching one of UHD's Dockerfiles (needs root):
  sudo python3 uhd_bare_metal_installer.py

  # Skip the "apt-get upgrade" step (safer on a machine you don't want fully upgraded):
  sudo python3 uhd_bare_metal_installer.py --skip-upgrade

  # Force a specific Dockerfile instead of auto-detecting from /etc/os-release:
  python3 uhd_bare_metal_installer.py --dockerfile-url https://raw.githubusercontent.com/EttusResearch/uhd/master/.ci/docker/uhd-builder-ubuntu2604.Dockerfile

  # Install dependencies AND then clone/build/install UHD itself into $HOME/uhd:
  sudo python3 uhd_bare_metal_installer.py --build
