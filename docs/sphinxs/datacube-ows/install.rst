..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installing
============

The ``datacube-ows`` installation process is quite simple and straightforward, requiring only the definition of the configuration files. To start, the first step is to acquire the source code. The downloaded version will be the BDC-ODC, which contains improvements that avoid error running the code when the BDC data products are used.

.. note::

    In these steps, due to the number of settings and errors that may occur, only the installation via Docker will be displayed. If necessary, you can access the `datacube-ows repository <https://github.com/brazil-data-cube/datacube-ows>`_ and follow the manual installation steps.

Let's download the source code::

    git clone https://github.com/brazil-data-cube/datacube-ows

    cd datacube-ows

After downloading and accessing the downloaded directory, it will be necessary to configure the ``docker-compose.yaml`` and the ``ows_cfg.py`` file. For ``docker-compose.yaml``, configure the mappings and database instance information required for its use. In the ``ows_cfg.py`` file, specify how the ``datacube-ows`` will handle the data products that will be available.

With the files properly configured, edit the ``.env`` file, in it will be necessary the description of the access information to the database and also the location of the configuration file

.. note::

    For more information about the ``ows_cfg.py`` and ``.env`` files, see the `configuration files page <config_files.html>`_.

With the finalization of the configuration of each of these files, run the ``build.sh`` script::

    ./build.sh

After the build is finished, the service will already be running. To finish, run the ``update_ranges.py`` script inside the container; this script is responsible for creating the database schema and also for popularizing this schema with information that will be used by the ``datacube-ows``. First, we run the script to create the schema::

    docker-compose exec ows python3 /code/update_ranges.py --schema  --role opendatacube


Finally, we run the script for the database population::

    docker-compose exec ows python3 /code/update_ranges.py

The output should look like::

    Deriving extents from materialised views
    OWS Layer LC8_30_16D_STK_1 maps to ODC Product(s): ['LC8_30_16D_STK_1']
    OWS Layer CB4_64_16D_STK_1 maps to ODC Product(s): ['CB4_64_16D_STK_1']
    Updating range for ODC product LC8_30_16D_STK_1...
    Updating range for ODC product CB4_64_16D_STK_1...
