#!/usr/bin/env sh

php-fpm -D
nginx -g 'daemon off;'
