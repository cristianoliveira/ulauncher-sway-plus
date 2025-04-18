{
  description = "A flake for the Sway Windows Extension project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {

          ULAUNCHER_WS_API="ws://127.0.0.1:5054/ulauncher-sway-plus";

          buildInputs = with pkgs; [
            python3
            python3Packages.virtualenv
            gtk3
            pkg-config
            gobject-introspection
            ulauncher
          ];
        };
      });
}
