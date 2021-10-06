{ lib, nixpkgs ? import <nixpkgs> {}, pythonPkgs ? nixpkgs.pkgs.python38Packages }:
pythonPkgs.buildPythonPackage rec {
  name   = "num2words-${version}";
  pname = "num2words";
  version = "0.6.0";

  src = ./.;

  propagatedBuildInputs = with pythonPkgs; [ docopt ];

  meta = with lib; {
    homepage    = "https://github.com/rhasspy/num2words";
    description = "Modules to convert numbers to words. Easily extensible.";
    license     = licenses.lgpl2;
  };

  doCheck = false;
}
