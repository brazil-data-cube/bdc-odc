#!/bin/bash

source env.sh

docker network create bdc-odc-net
docker run -it -d \
        --name bdc-odc-pg \
        --hostname bdc-odc-pg \
        --network bdc-odc-net \
        --restart unless-stopped \
        -v bdc-odc-pgdata_vol:/var/lib/postgresql/data \
        -e PGDATA=/var/lib/postgresql/data \
        -e POSTGRES_DB=${POSTGRES_DB} \
        -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
        -e POSTGRES_USER=${POSTGRES_USER} \
        kartoza/postgis:11.0-2.5

docker run -it -d \
        --name bdc-odc-core \
        --hostname bdc-odc-core \
        --network bdc-odc-net \
        --restart unless-stopped \
        -v ${DATADIR}:/data \
        -e DB_DATABASE=${POSTGRES_DB} \
        -e DB_HOSTNAME=bdc-odc-pg \
        -e DB_USERNAME=${POSTGRES_USER} \
        -e DB_PASSWORD=${POSTGRES_PASSWORD} \
        -e DB_PORT=5432 \
        local/bdc-in-a-box:1.7 /bin/bash
