# Ulauncher Sway+

An evolution of https://github.com/rdnetto/ulauncher-sway

This repo contains a [Ulauncher](https://ulauncher.io) extension for managing [Sway](https://swaywm.org).

## Sway + Windows

<p align="center">
  <img src="https://github.com/user-attachments/assets/bc16fcff-c8be-405a-ac76-e221b328a39a" alt="Sway Demo" width="720" />
</p>

## Sway + Marks

<p align="center">
  <img src="https://github.com/user-attachments/assets/a2d83e83-6273-4dfa-be84-d9cce6083649" alt="Sway Marks Demo" />
</p>

## Features of this fork

 - [x] Search and focus to window
 - [x] Sort by Most used/ Recently used / No sort

### Marks management

 - [x] Add a mark to the current windows
 - [x] Unmark the current windows
 - [x] List and focus by marked windows

### Future implementations

 - [ ] Move selected window to a workspace
 - [ ] List windows by workspace

## Installation

Requires **Ulauncher 5 (extension API 2)** running in a Sway session, with
`swaymsg` on its PATH. Ulauncher's Python must have PyGObject (`gi`) and PyXDG
(`xdg`). Install these through your distribution; this extension does not create
or use a virtual environment.

### Nix / Home Manager

Add this flake to your configuration inputs:

```nix
inputs.ulauncher-sway-plus.url = "github:cristianoliveira/ulauncher-sway-plus";
inputs.ulauncher-sway-plus.inputs.nixpkgs.follows = "nixpkgs";
```

Import its module in your **Home Manager** configuration:

```nix
{
  imports = [ inputs.ulauncher-sway-plus.homeManagerModules.default ];
  programs.ulauncher-sway-plus.enable = true;
}
```

Here `inputs` must be in scope (for example, passed through Home Manager's
`extraSpecialArgs`). Apply your configuration with `home-manager switch`, or
`sudo nixos-rebuild switch --flake .` if Home Manager is integrated into NixOS.
The module installs Ulauncher and links the extension into its discovery directory.
It does not configure Sway or start Ulauncher.

To build only the extension from a checkout:

```bash
nix build .#ulauncher-sway-plus
```

The extension is under
`result/share/ulauncher/extensions/com.github.cristianoliveira.ulauncher-sway-plus`.
`nix profile install` alone does **not** register an extension with Ulauncher;
use the Home Manager module or the standalone installer below.

### Other Linux systems

After installing the prerequisites:

```bash
git clone https://github.com/cristianoliveira/ulauncher-sway-plus.git
cd ulauncher-sway-plus
./install.sh
```

Alternatively, run `make install` from the repository root; it calls the same
installer and requires Make.

Run without `sudo`. The script copies runtime files to
`${XDG_DATA_HOME:-$HOME/.local/share}/ulauncher/extensions/com.github.cristianoliveira.ulauncher-sway-plus`.
It works from any current directory, leaves the checkout independent, and refuses
to overwrite an existing directory or symlink. Use `./install.sh --help` for help.

### Existing installations and updates

Quit Ulauncher before switching installations. Move any old copy or development
symlink **outside** its extensions directory before installing; check both
`com.github.cristianoliveira.ulauncher-sway-plus` and `ulauncher-sway-plus` to avoid
duplicate keywords. Keep that backup until the new installation works.

For script-based updates, run `git pull`, move the old installation out, and run
`./install.sh` again. For Home Manager, update your flake input and reapply your
configuration. Nix-managed files are read-only; do not update them through
Ulauncher's extension updater. Ulauncher preferences stay in its separate
configuration directory.

Restart Ulauncher directly (`ulauncher`), then type `w ` to list windows.

## Development

### Prerequisites

 - [Ulauncher](https://ulauncher.io)
 - [Sway](https://swaywm.org)
 - [gtk3](https://www.gtk.org/)

### CI tools

 - [black](https://github.com/psf/black) - Python code formatter
 - [isort](https://github.com/PyCQA/isort) - Python import sorter

### CI install

```bash
make ci-install
```

### Development link

For an editable checkout (instead of a copied or Nix-managed installation):

```bash
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/ulauncher/extensions"
ln -s "$PWD" "${XDG_DATA_HOME:-$HOME/.local/share}/ulauncher/extensions/ulauncher-sway-plus"
```

Remove other installations first to avoid duplicate keywords.

To start run
```bash
make start
```
It will kill any ulauncher instance and restart


### Test

To run the automated tests

```bash
make test
```
