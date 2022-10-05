#!/usr/bin/env bash

# -- copyright --

# install.sh
# Author: Nicolas Delgado
# Description: environment install script

# Setup start env function
if [ -v "$BASH" ]; then
    echo "st_$1() { source $HOME/.python_venvs/$1/bin/activate && . ./envars.sh }" >>$HOME/.bashrc
    . $HOME/.bashrc
else
    echo "st_$1() { source $HOME/.python_venvs/$1/bin/activate && . ./envars.sh }" >>$HOME/.zshrc
    . $HOME/.zshrc
fi

# Deactivate python venv if active
deactivate 2>/dev/null

# Create folders for python venv
mkdir -p $HOME/.python_venvs
mkdir -p $HOME/.python_cache

# Create and activate python venv
python3 -m venv $HOME/.python_venvs/$1
. $HOME/.python_venvs/$1/bin/activate

# Setup env vars
. ./envars.sh

# Upgrade pip
pip install -U pip

# Install seed project dependencies
pip install pybuilder
pyb install_dependencies
