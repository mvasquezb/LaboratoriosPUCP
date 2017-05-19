#!/usr/bin/env sh

sudo -u postgres psql -c "create user inf245 with \
                          createdb login password 'inf24520171'"
sudo -u postgres psql -c "create database labicpucp with \
                          owner = inf245 \
                          encoding = utf8"
