#!/bin/bash

APP_PATH="/home/ubuntu/app"
REQS_PATH="${APP_PATH}/requirements.txt"
GIT_URL="https://github.com/mcooper-cloud/auth0_python"

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-venv python3-pip python3-flask git nginx 

python3 -m venv .flycatcher
source .flycatcher/bin/activate

python3 -m pip install --upgrade pip

git clone ${GIT_URL} ${APP_PATH}
pip3 install -r ${REQS_PATH} --no-cache-dir --upgrade
