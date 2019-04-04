{ pkgs ? import <nixpkgs> {} }: let
siprefix = pkgs.python36Packages.callPackage ./build/si-prefix.nix { };
python = (pkgs.python36.withPackages (p: [ p.numpy p.networkx siprefix ]));
in pkgs.mkShell {
    buildInputs = [ python ];
}
