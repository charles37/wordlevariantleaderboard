# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    pandas
    flask
    requests
    gunicorn
    datetime
    flask_sqlalchemy
    # other python packages
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env

