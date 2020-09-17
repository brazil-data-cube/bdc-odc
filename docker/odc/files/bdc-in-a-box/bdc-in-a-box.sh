#!/bin/bash

set -e

# Indexing
while IFS=, read -r COLLECTIONID PLATAFORM SENSOR MDTYPE LIMIT ADVANCEDFILTER
do
    COLLECTIONID_REPLACE=$(echo $COLLECTIONID | sed -e "s/-/"_"/g")

    {
    mkdir -p /data/products/${COLLECTIONID_REPLACE}/datasets/data
    stac2odc collection2product -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID_REPLACE}/${COLLECTIONID_REPLACE}.yaml --units m -p "${PLATFORM}" --instrument "${SENSOR}" --type "${MDTYPE}"
    datacube product add /data/products/${COLLECTIONID_REPLACE}/${COLLECTIONID_REPLACE}.yaml
    stac2odc item2dataset -c "${COLLECTIONID}" -o /data/products/${COLLECTIONID_REPLACE}/datasets/ --units m -p "${PLATFORM}" \
                  --instrument "${SENSOR}" -m "${LIMIT}" --download --download-out /data/products/${COLLECTIONID_REPLACE}/datasets/data \
                  --advanced-filter "${ADVANCEDFILTER}"

    find /data/products/${COLLECTIONID_REPLACE}/datasets/*.yaml -exec datacube -vvv dataset add -p ${COLLECTIONID_REPLACE} {} \;
    } || {
      echo "No Image found for ${COLLECTIONID}". Check your filter
    }
done <collections.list
