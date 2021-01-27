#!/bin/bash

set -e
docker-compose stop && docker-compose rm -f && docker-compose build --no-cache --parallel --force-rm && docker-compose up -d
