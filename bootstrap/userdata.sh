#!/bin/bash

APP_PATH="/home/ubuntu/app"
REQS_PATH="${APP_PATH}/requirements.txt"
GIT_URL="https://github.com/mcooper-cloud/auth0_python"

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y nginx gunicorn3 python3-pip python3-flask git

git clone ${GIT_URL} ${APP_PATH}
sudo pip3 install -r ${REQS_PATH} --upgrade