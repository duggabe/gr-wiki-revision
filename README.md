# gr-wiki-revision

Scripts and programs to support GNU Radio Wiki documents.

The main content is two Python scripts that build
[GNU Radio](https://github.com/gnuradio/gnuradio) from source on Ubuntu,
without Docker. They back the
[Building GNU Radio from Source Code](https://wiki.gnuradio.org/index.php?title=Building_GNU_Radio_from_Source_Code)
page on the GNU Radio Wiki.

The goals of these instructions are to:

- Use the Ettus PPA repository for UHD rather than building UHD from source.
- Use the `~/gnuradio` folder already cloned in the user's system so that
  developers/testers can build from their own fork.
- Install GNU Radio into a folder in the user's home directory
  (`~/gnuradio-pkg`), so that neither script has to be run with `sudo`.

This package is useful when a Developer of GNU Radio code needs to test
additions or revisions to the code, and needs to operate outside of a Docker
container. All others should follow the instructions in
[LinuxInstall#From_Binaries](https://wiki.gnuradio.org/index.php?title=LinuxInstall#From_Binaries).

**Note: Developing and running OOT (out-of-tree) modules does _not_ require
GNU Radio to be installed from source.**

---

There are two steps, each with its own script. Step 1 installs UHD from the
Ettus Research PPA and everything GNU Radio needs, using `apt-get`; nothing is
compiled. Step 2 builds, tests, and installs GNU Radio from your own fork,
which you clone into your home directory, so that you can work on an issue
and submit a pull request. GNU Radio is installed into `~/gnuradio-pkg`, and
one line in `~/.profile` makes it available in every terminal and from the
desktop.

## Instructions

The instructions, from downloading the scripts to checking the result, are on
the GNU Radio Wiki page
[Building GNU Radio from Source Code](https://wiki.gnuradio.org/index.php?title=Building_GNU_Radio_from_Source_Code).
They are kept there only, so that there is one copy to keep up to date.
Every script also has `--help` and `--dry-run`.

## Releases

The [Releases page](https://github.com/duggabe/gr-wiki-revision/releases)
lists the releases and what changed in each one. The Wiki page downloads the
scripts from the latest release. A tag is never moved, so a link to a tag
always gives the same scripts.

## License

[CC BY-SA 4.0](LICENSE).
