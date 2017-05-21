#!/usr/bin/env sh

psql -U postgres -c "create user inf245 with \
                     createdb login password 'inf24520171'"

psql -U postgres -c "create database labicpucp with \
                     owner = inf245 \
                     encoding = utf8"
