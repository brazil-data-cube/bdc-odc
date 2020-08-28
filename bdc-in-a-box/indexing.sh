#!/bin/bash

git clone https://github.com/M3nin0/bdc-odc.git
cd bdc-odc && git checkout bdc-env && git branch bdc-env -u original/bdc-env

# install stac2odc
cd stac2odc && python setup.py install && cd ../.. && rm -rf bdc-odc

while IFS=, read -r COLLECTIONID PLATAFORM SENSOR MDTYPE LIMIT
do
    mkdir -p ~/products/${COLLECTIONID}/datasets/data
    stac2odc collection2product -c "${COLLECTIONID}" -o ~/products/${COLLECTIONID}/${COLLECTIONID}.yaml --units m -p "${PLATFORM}" --instrument "${SENSOR}" --type "${MDTYPE}"
    datacube product add ~/products/${COLLECTIONID}/${COLLECTIONID}.yaml
    stac2odc item2dataset -c "${COLLECTIONID}" -o ~/products/${COLLECTIONID}/datasets/ --units m -p "${PLATFORM}" --instrument "${SENSOR}" -m "${LIMIT}" --download --download-out ~/products/${COLLECTIONID}/datasets/data

    find ~/products/${COLLECTIONID}/datasets/*.yaml -exec datacube -vvv dataset add -p ${COLLECTIONID} {} \;
done <collections.list
