# shell.nix
{ pkgs ? import <nixpkgs> {} }:

let
  signalbot = pkgs.python3Packages.buildPythonPackage rec {
    pname = "signalbot";
    version = "0.8.0";

    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "P/a45qBIh89kqzjtzvFUNr9VrsNT7E6lQM4xTFZtMyU=";
    };

    # Specify that this package uses pyproject.toml with Poetry
    format = "pyproject";

    # Add Poetry to nativeBuildInputs
    nativeBuildInputs = with pkgs.python3Packages; [ poetry-core ];

    propagatedBuildInputs = with pkgs.python3Packages; [ ];

    # Add any necessary configurations
    # doCheck = false;
  };

  my-python-packages = ps: with ps; [
    pandas
    flask
    requests
    gunicorn
    datetime
    signalbot
    flask_sqlalchemy
    apscheduler
    aiohttp
    websockets
    redis
    # other python packages
  ];

  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env

