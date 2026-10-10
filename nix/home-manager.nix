{ config, lib, pkgs, ... }:

let
  cfg = config.programs.ulauncher-sway-plus;
  extensionId = "com.github.cristianoliveira.ulauncher-sway-plus";
in
{
  options.programs.ulauncher-sway-plus = {
    enable = lib.mkEnableOption "the Sway+ extension for Ulauncher";
    package = lib.mkOption {
      type = lib.types.package;
      default = pkgs.callPackage ./package.nix { };
      description = "Sway+ extension package to install.";
    };
  };

  config = lib.mkIf cfg.enable {
    home.packages = [ pkgs.ulauncher ];
    xdg.dataFile."ulauncher/extensions/${extensionId}".source =
      "${cfg.package}/share/ulauncher/extensions/${extensionId}";
  };
}
