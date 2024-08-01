{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
  ];

  shellHook = ''
    echo "Nix shell activated with Python3."
  '';
}
