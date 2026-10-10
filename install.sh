#!/usr/bin/env bash
# Help and recovery commands deliberately show literal environment variables.
# shellcheck disable=SC2016
set -euo pipefail

if [[ $# -eq 1 && $1 == --help ]]; then
    printf '%s\n' \
        'Usage: ./install.sh' \
        'Install Sway+ for the current user. Run from a cloned repository.' \
        'Requires Ulauncher 5 (extension API 2), Sway, Python GI and PyXDG.' \
        'Destination: ${XDG_DATA_HOME:-$HOME/.local/share}/ulauncher/extensions/' \
        'Example: XDG_DATA_HOME="$HOME/.local/share" ./install.sh' \
        'Existing installations are never overwritten. Restart Ulauncher afterward.'
    exit 0
fi

if [[ $# -ne 0 ]]; then
    printf 'Unknown arguments. Run ./install.sh --help\n' >&2
    exit 1
fi

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
data_home=${XDG_DATA_HOME:-$HOME/.local/share}
if [[ $data_home != /* ]]; then
    printf 'Data directory must be absolute. Run XDG_DATA_HOME="$HOME/.local/share" ./install.sh\n' >&2
    exit 1
fi

target="$data_home/ulauncher/extensions/com.github.cristianoliveira.ulauncher-sway-plus"
mkdir -p -- "$(dirname -- "$target")"
# mkdir also refuses dangling symlinks and concurrent installations.
if ! mkdir -- "$target"; then
    printf 'Cannot create %s. Move any existing installation outside the extensions directory, then run ./install.sh again.\n' "$target" >&2
    exit 1
fi

cp -- "$source_dir/main.py" "$source_dir/manifest.json" "$source_dir/LICENSE" "$target/"
for module in handlers sway utils; do
    mkdir -- "$target/$module"
    cp -- "$source_dir/$module/"*.py "$target/$module/"
done
mkdir -- "$target/images"
cp -- "$source_dir/images/default.svg" "$source_dir/images/icon.png" "$target/images/"
printf 'Installed in %s\nRestart Ulauncher to load the extension.\n' "$target"
