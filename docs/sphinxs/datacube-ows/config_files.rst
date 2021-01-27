..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Configuration files
====================

This section presents some configuration files that can be used in the installation steps of ``datacube-ows``.

ows_cfg.py
------------

The ``ows_cfg.py`` file was created in order to give configuration flexibility to users of ODC-OWS services. With this file, all styles, metadata of the OGC services, and pre-processing applied to the data can be described through a Python dictionary. There are many options available for use. An example of this file created for BDC consumption is available in the `BDC-ODC repository <https://github.com/brazil-data-cube/bdc-odc/blob/master/config/datacube-ows/ows_cfg.py>`_.

.. note::

    To learn about all the available parameters, consult the official documentation of the `ODC-OWS <https://datacube-ows.readthedocs.io/en/latest/configuration.html>`_.

.env
------

The ``.env`` file, available at the root of the ``datacube-ows`` project, helps in the configuration of the services. This file specifies environment variables to be used by the service for connection to the database, recovery from the ``ows_cfg.py`` configuration file, and several other options such as permission to recover data from AWS. An example of this file is presented below.

.. code-block:: text
    :caption: .env file example

    # Set some default vars, you can overwrite these by creating env vars
    AWS_REGION=ap-southeast-2
    DB_HOSTNAME=postgres
    DB_PORT=5432
    DB_USERNAME=opendatacubeusername
    DB_PASSWORD=opendatacubepassword
    DB_DATABASE=opendatacube
    OWS_CFG_FILE=./ows_test_cfg.py
    AWS_NO_SIGN_REQUEST=yes
    # If you want to use pydev for interactive debugging
    PYDEV_DEBUG=
    # Will not work with pydev
    FLASK_ENV=development
    prometheus_multiproc_dir=/tmp

.. warning::

    It should be noted that the variable ``OWS_CFG_FILE`` indicates where the configuration file ``ows_cfg.py`` is located. It is recommended to keep it inside the project directory because it will be copied into the container during the build
