#!/usr/bin/env sh

port=${1:-8000}

cd laboratorios
./manage.py runserver $port
