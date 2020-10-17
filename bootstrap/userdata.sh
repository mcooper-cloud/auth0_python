#!/bin/bash

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y nginx gunicorn3 python3-pip python3-flask git

git clone https://github.com/mcooper-cloud/auth0_flask

sudo pip3 install -r app/requirements.txt --upgrade
