#!/bin/bash

configure_gunicorn(){
    cp gunicorn.service /etc/systemd/system/gunicorn.service
    systemctl start gunicorn
    systemctl enable gunicorn
}

configure_nginx(){
    rm /etc/nginx/sites-enabled/default
    cp flask-project.conf /etc/nginx/sites-available/flask-project.conf
    ln -s /etc/nginx/sites-available/flask-project.conf /etc/nginx/sites-enabled/
    systemctl start nginx
    systemctl enable nginx
}

reload_servers(){
    systemctl daemon-reload
    systemctl stop gunicorn
    systemctl stop nginx
    systemctl start gunicorn
    systemctl start nginx
}

configure_gunicorn
configure_nginx
reload_servers