{ lib, nixpkgs ? import <nixpkgs> {}, pythonPkgs ? nixpkgs.pkgs.python38Packages }:
pythonPkgs.buildPythonPackage rec {
  name   = "num2words-${version}";
  pname = "num2words";
  version = "0.6.0";

  src = fetchTarball {
    url = "https://github.com/rhasspy/num2words/archive/refs/tags/v0.6.0.tar.gz";
    sha256 = "1qnibxix5jxl94kyfvksa386hhvp4xl86961pjz6pybm0jz131l9";
  };

  propagatedBuildInputs = with pythonPkgs; [ docopt ];

  meta = with lib; {
    homepage    = "https://github.com/rhasspy/num2words";
    description = "Modules to convert numbers to words. Easily extensible.";
    license     = licenses.lgpl2;
  };

  doCheck = false;
}
