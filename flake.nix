{
  description = "A flake for the Sway Windows Extension project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python3
          pkgs.python3Packages.pip
          pkgs.python3Packages.setuptools
          pkgs.python3Packages.wheel
        ];
      };
    };
}
