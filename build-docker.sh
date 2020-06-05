#/bin/bash

repo=local
tag=1.7
docker build docker/odc/ --tag ${repo}/odc:${tag} $@
docker build docker/odc-jupyter/ --tag ${repo}/odc-jupyter:${tag} $@

