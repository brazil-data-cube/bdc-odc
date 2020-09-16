#!/bin/bash

# Indexing
while IFS=, read -r COLLECTIONID PLATAFORM SENSOR MDTYPE LIMIT ADVANCEDFILTER
do
    mkdir -p /data/products/${COLLECTIONID}/datasets/data
    stac2odc collection2product -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID}/${COLLECTIONID}.yaml --units m -p "${PLATFORM}" --instrument "${SENSOR}" --type "${MDTYPE}"
    datacube product add /data/products/${COLLECTIONID}/${COLLECTIONID}.yaml
    stac2odc item2dataset -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID}/datasets/ --units m -p "${PLATFORM}"
                  --instrument "${SENSOR}" -m "${LIMIT}" --download --download-out /data/products/${COLLECTIONID}/datasets/data \
                  --advanced-filter "${ADVANCEDFILTER}"

    find /data/products/${COLLECTIONID}/datasets/*.yaml -exec datacube -vvv dataset add -p ${COLLECTIONID} {} \;
done <collections.list
