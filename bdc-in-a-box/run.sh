#!/bin/bash

git clone https://github.com/M3nin0/bdc-odc.git
cd bdc-odc && git checkout bdc-env && git branch bdc-env -u original/bdc-env

# build images
./build-docker.sh
cd bdc-in-a-box

./bdc-in-a-box.sh
./docker.sh
