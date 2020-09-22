..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installing
============

This section presents the ODC Explorer installation process. For this process, two main approaches can be followed. The first uses a local conda environment and another Docker container. Both are presented below

.. note::

    The use of the container-based approach is recommended. Working in a controlled Docker environment avoids problems with the installation of geospatial libraries such as GDAL and facilitates the reproducibility of the environment.

conda
----------

The first step for the installation is to download the ``datacube-explorer`` code. For this the `git <https://git-scm.com/>`_ command can be used::

    git clone https://github.com/brazil-data-cube/datacube-explorer.git

    cd datacube-explorer

In the first approach using conda, it is necessary first to create an environment with libraries ``fiona``, ``shapely``, and ``gunicorn``::

    conda create --name datacube-explorer python=3.8 fiona shapely gunicorn

.. note::

    The Python version is 3.8 because it presented the least amount of errors in the installation tests.

After configuring the conda base environment, it can be activated and then the installation of data-explorer::

    conda activate datacube-explorer

    pip install -e .

If the installation has been completed correctly, the following command must be executed without showing any error::

    cubedash-gen --help

The output of the ``cubedash-gen --help`` command should look like the following::

    Usage: cubedash-gen [OPTIONS] [PRODUCT_NAMES]...

      Generate summary files for the given products

    Options:
      -E, --env TEXT
      -C, --config, --config_file TEXT
      --all
      -v, --verbose
      -j, --jobs INTEGER              Number of worker processes to use
      -l, --event-log-file PATH       Output jsonl logs to file
      --refresh-stats / --no-refresh-stats
      --force-refresh / --no-force-refresh
      --force-concurrently
      --init-database, --init / --no-init-database
                                      Prepare the database for use by datacube
                                      explorer

      --custom-crs-definition-file PATH
                                      Output jsonl logs to file
      --help                          Show this message and exit.


It is necessary to generate the ``custom_crs.json`` and ``settings.env.py`` files. Both are presented in the `configuration files page <config_files.html>`_.

.. note::

    To use this version outside a container you will also need to add an ``.datacube.conf`` file to your user's home directory. It will be used by the datacube tools to access the database. An example of this file can be found in the `BDC-ODC repository <https://github.com/brazil-data-cube/docker/blob/master/jupyterhub/docker/odc/1.8/.datacube.conf-example>`_.

Docker
--------

The configuration of the ``datacube-explorer`` with the use of the Docker is done more simply, here, it is only necessary to define the configuration of the environment. The first step for the configuration is the creation of the ``custom_crs.json`` and ``settings.env.py`` files, these will be used to define the behavior of the datacube-explorer without the need for changes in its code.

.. note::

    For a complete description of each of the configuration files, see the `configuration files page <config_files.html>`_.

With both files created, it is necessary to configure the ``docker-compose`` options. In this one, change the options of connecting with the database according to what is necessary.

This is done within the ODC environment to enable the various grids defined by the project, each with its CRS, to be used without problems in the ``datacube-explorer``. Once this is done, build the image::

    docker-compose build --parallel --no-cache

Finally, run the containers::

    docker-compose up -d
