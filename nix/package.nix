{ lib, stdenvNoCC, python3, shellcheck }:

stdenvNoCC.mkDerivation {
  pname = "ulauncher-sway-plus";
  version = "0-unstable";

  src = lib.fileset.toSource {
    root = ../.;
    fileset = lib.fileset.unions [
      ../install.sh
      ../main.py
      ../manifest.json
      ../LICENSE
      (lib.fileset.fileFilter (file: file.hasExt "py") ../handlers)
      (lib.fileset.fileFilter (file: file.hasExt "py") ../sway)
      (lib.fileset.fileFilter (file: file.hasExt "py") ../utils)
      ../images/default.svg
      ../images/icon.png
      ../tests/test_install.py
    ];
  };

  dontBuild = true;
  doCheck = true;
  nativeCheckInputs = [ python3 shellcheck ];

  checkPhase = ''
    runHook preCheck
    shellcheck install.sh
    python -m unittest discover -s tests -p test_install.py
    runHook postCheck
  '';

  installPhase = ''
    runHook preInstall
    XDG_DATA_HOME="$out/share" bash ./install.sh
    runHook postInstall
  '';

  meta = {
    description = "Ulauncher extension for managing Sway windows, marks and workspaces";
    homepage = "https://github.com/cristianoliveira/ulauncher-sway-plus";
    license = lib.licenses.lgpl3Only;
    platforms = lib.platforms.linux;
  };
}
