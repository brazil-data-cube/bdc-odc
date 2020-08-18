..
    This file is part of Brazil Data Cube ODC Scripts & Tools.
    Copyright (C) 2019 INPE.

    Brazil Data Cube ODC Scripts & Tools is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.



Building the Docker Images
==========================

On the command line use the `git clone` command to clone the software repository:

.. code-block:: shell

        $ git clone https://github.com/brazil-data-cube/bdc-odc.git

Then, go to the source code folder:

.. code-block:: shell

        $ cd bdc-odc

Run the script `./build-docker.sh` to create the docker images:


.. code-block:: shell

        $ ./build-docker.sh

The above command will create two Docker images named `odc:1.7` and `odc-jupyter:1.7`, as one can see with the `docker images` command:

.. code-block:: shell

        $ docker images

        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        local/odc-jupyter   1.7                 684c49022dd4        5 days ago          1.9GB
        local/odc           1.7                 72408270a63b        5 days ago          1.61GB


Running ODC Services
===========================

First you will need to create an docker network:

.. code-block:: shell

        $ docker network create bdc-odc-net


Now, you will need an instance of PostgreSQL up and running in order to launch the ODC services. In the console, enter the following command to start the PostgreSQL instance:

.. code-block:: shell

        $ docker run -it -d \
                --name bdc-odc-pg \
                --hostname bdc-odc-pg \
                --network bdc-odc-net \
                --restart unless-stopped \
                -v bdc-odc-pgdata_vol:/var/lib/postgresql/data \
                -e PGDATA=/var/lib/postgresql/data \
                -e POSTGRES_DB=opendatacube \
                -e POSTGRES_PASSWORD=change-me \
                -e POSTGRES_USER=opendatacube \
                kartoza/postgis:11.0-2.5

After that, you can initialize Open Data Cube instance with the following command:

.. code-block:: shell

        $ docker run -it -d \
                --name bdc-odc-core \
                --hostname bdc-odc-core \
                --network bdc-odc-net \
                --restart unless-stopped \
                -v /path/to/data-repository:/data \
                -e DB_DATABASE=opendatacube \
                -e DB_HOSTNAME=bdc-odc-pg \
                -e DB_USERNAME=opendatacube \
                -e DB_PASSWORD=change-me \
                -e DB_PORT=5432 \
                local/odc:1.7 /bin/bash

Configuring the ODC instance
----------------------------

Run the following command in order to initialize the ODC database:

.. code-block:: shell

        $ docker exec -it bdc-odc-core datacube system init

You can check if the ODC instance is ready with the following command:

.. code-block:: shell
        
        $ docker exec -it bdc-odc-core datacube product list


Starting an ODC Jupyter Notebook Instance
------------------------------------------

To start an ODC Jupyter Notebook instance, use the following command:

.. code-block:: shell

        $ docker run -it -d \
                --name bdc-odc-jupyter \
                --hostname bdc-odc-jupyter \
                --network bdc-odc-net \
                --restart unless-stopped \
                -p 8889:8889 \
                -v /path/to/data-repository:/data \
                -e DB_DATABASE=opendatacube \
                -e DB_HOSTNAME=bdc-odc-pg \
                -e DB_USERNAME=opendatacube \
                -e DB_PASSWORD=change-me \
                -e DB_PORT=5432 \
                local/odc-jupyter:1.7 /bin/bash

Run the following command to start the Jupyer Notebook service:

.. code-block:: shell

        $ docker exec -it bdc-odc-jupyter jupyter notebook --ip=0.0.0.0 --port=8889 --notebook-dir=/data

Starting an BDC-ODC OWS Instance
---------------------------------

To start an ODC WMS instance, use the following command:

.. code-block:: shell
        
        $ git clone https://github.com/brazil-data-cube/datacube-ows && cd datacube-ows

Now, update the .env file with your database settings. If necessary, get ows config files (OWS_CFG_FILE) in  `bdc-odc <https://github.com/brazil-data-cube/bdc-odc>`_. After this, run the build script

.. code-block:: shell

        $ ./build.sh

You will need to update the ODC ranges.

.. code-block:: shell

        $ docker exec -ti datacube-ows_ows_1 bash
        $ cd /code
        $ python3 update_ranges.py --schema  --role opendatacube
        $ python3 update_ranges.py

Use the URL below to test

.. code-block::

        http://127.0.0.1:8000/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-16.10877155100000024,-56.30364467999999789,-14.1582321009999994,-54.63602305900000289&CRS=EPSG:4326&WIDTH=229&HEIGHT=267&LAYERS=CB4_64_16D_STK_v1&STYLES=&FORMAT=image/png&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE


Starting an ODC Explorer Instance
----------------------------------

First download the code

To start an ODC WMS instance, use the following command:

.. code-block:: shell
        
        $ git clone https://github.com/brazil-data-cube/datacube-explorer && cd datacube-explorer

Inside the directory, modify the docker-compose settings, if necessary, and then run the build script

.. code-block:: shell

        $ ./build.sh

Now just access the container and update the datasets locations

.. code-block:: shell

        $ cubedash-gen --init --all

At the end of the process, go to address http://127.0.0.1:5000 and enjoy!
