{ lib
, buildPythonPackage
, fetchPypi
, nose
, decorator
}:

buildPythonPackage rec {
  pname = "si-prefix";
  version = "1.2.2";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0xq02zb49mc4wjxgz5qqhc0jw8wmc4spm90pd9hdlkj1v9jjfbnd";
  };

  checkInputs = [ nose ];
  propagatedBuildInputs = [ decorator ];

  meta = {
    homepage = "https://github.com/cfobel/si-prefix";
    description = "Functions for formatting numbers according to SI standards.";
    license = lib.licenses.bsd3;
  };
}
