..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Configuration files
====================

This section presents some configuration files that can be used in the installation steps of ``datacube-explorer``.

custom_crs.json
----------------

The ``custom_crs.json`` file is used in the ``BDC-ODC`` version of ``datacube-explorer`` to enable the support of different types of CRS without the need for reprojections in the data. With this file multiple, CRS can be defined, which allows data, such as those of the BDC, that have multiple CRS to be easily treated in the ``datacube-explorer``.

The file with the custom CRS definitions is a JSON file, where the key represents the custom EPSG code and the value of the CRS string definition.

.. code-block:: json
    :caption: custom_crs.json file example

    {
        "epsg:100001": "+proj=aea +lat_0=-12 +lon_0=-54 +lat_1=-2 +lat_2=-22 +x_0=5000000 +y_0=10000000 +ellps=GRS80 +units=m +no_defs"
    }

settings.env.py
----------------

The ``settings.env.py`` file is used by ``datacube-explorer`` to configure the deployment options. All the options available in this file are described in its `documentation <https://github.com/brazil-data-cube/datacube-explorer#how-can-i-configure-the-deployment>`_. For the BDC-ODC an example of this file is presented below.

.. code-block:: python
    :caption: settings.env.py file example

    URL_PREFIX = "/bdc/odc/"
    CUBEDASH_DEFAULT_PRODUCTS = ('CB4_64_16D_STK_1', 'LC8_30_16D_STK_1')
    CUSTOM_CRS_CONFIG_FILE = "custom-crs-file.json"
