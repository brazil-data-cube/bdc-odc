#!/bin/bash

# Install stac2odc
git clone https://github.com/brazil-data-cube/bdc-odc.git && cd bdc-odc
pip3 install  git+https://github.com/brazil-data-cube/stac.py
cd stac2odc && python3 setup.py install && cd ../.. && rm -rf bdc-odc

# Indexing
while IFS=, read -r COLLECTIONID PLATAFORM SENSOR MDTYPE LIMIT
do
    mkdir -p /data/products/${COLLECTIONID}/datasets/data
    stac2odc collection2product -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID}/${COLLECTIONID}.yaml --units m -p "${PLATFORM}" --instrument "${SENSOR}" --type "${MDTYPE}"
    datacube product add /data/products/${COLLECTIONID}/${COLLECTIONID}.yaml
    stac2odc item2dataset -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID}/datasets/ --units m -p "${PLATFORM}" --instrument "${SENSOR}" -m "${LIMIT}" --download --download-out /data/products/${COLLECTIONID}/datasets/data

    find /data/products/${COLLECTIONID}/datasets/*.yaml -exec datacube -vvv dataset add -p ${COLLECTIONID} {} \;
done <collections.list
