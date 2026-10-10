{
  description = "A flake for the Sway Windows Extension project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    {
      homeManagerModules.default = import ./nix/home-manager.nix;
    } // flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        packages.default = pkgs.callPackage ./nix/package.nix { };
        packages.ulauncher-sway-plus = self.packages.${system}.default;
        checks.install = self.packages.${system}.default;

        devShells.default = pkgs.mkShell {

          ULAUNCHER_WS_API="ws://127.0.0.1:5054/ulauncher-sway-plus";

          buildInputs = with pkgs; [
            python3
            python3Packages.virtualenv
            gtk3
            pkg-config
            gobject-introspection
            ulauncher

            # Tools
            black
            isort

            funzzy # watcher
          ];
        };
      });
}
