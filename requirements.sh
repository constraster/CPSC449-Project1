#!/bin/bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
sudo apt-install --yes gunicorn3
sudo gem install foreman