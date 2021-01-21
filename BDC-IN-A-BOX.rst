..
    This file is part of Brazil Data Cube ODC Scripts & Tools.
    Copyright (C) 2019 INPE.

    Brazil Data Cube ODC Scripts & Tools is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


bdc-in-a-box (bdcbox)
=====================================

This page presents the use of the bdc-in-a-box tool, a utility that allows rapid configuration and indexing of data, without the need for special access to the BDC project infrastructure. 

Requirements
------------

To use this tool, follow the steps in the running document. To use this tool, first follow the steps in the document RUNNING.rst. After doing this, the bdcbox utility can be started. 

The first step is to access the ODC-Core container, configured in the section indicated above.

.. code-block:: shell

    $ docker exec -it bdc-odc-core /bin/bash

Inside the container, when listing the contents of the current directory three files will be displayed

.. code-block:: shell

        $ ls

        bdc-in-a-box/  collections.list  install_aws_cli.sh

The bdcbox tool consists of the files that are inside the bdc-in-a-box directory. The ``bdc-in-a-box.sh`` file does all the settings while the ``collection.list`` has the definition of the collections to be downloaded.  Also available is the ``install_stac2odc.sh`` file with filter parameters, which can be changed according to the need of region that needs to be filtered.

In this example, some images from the BDC will be downloaded, considering the collections already present in the collections.list file. The change will be made in quantity, for this, access the file and change the column with the value 5000. Change this value for three. The filter file is also maintained in the ``collections.list``.

.. NOTE::

    You can edit these files, ``collections.list`` and ``advanced_filter.json`` according to your needs

.. code-block:: shell

        $ cat collections.list

        CB4_64_16D_STK_v1,CBERS4,AWFI,eo,3,advanced_filter.json
        LC8_30_16D_STK_v1,LC8,OLI,eo,3,advanced_filter.json
        S2_10_16D_STK_v1,S2,MSI,eo,3,advanced_filter.json


After this, you can run the bdc-in-a-box.sh script, it will record each of the downloaded collections in the ODC.

.. code-block:: shell

        $ ./bdc-in-a-box.sh


collections.list
------------------

This is a csv file created to facilitate the definition of which data should be considered in indexing. This section presents its structure.

The file is composed of 6 columns, being them:

- Collection Name (This name must be the same as the one made available in BDC-STAC)
    - e.g. CB4_64_16D_STK_v1
- Platform (Sensor platform that generated the data. User-defined name pattern)
    - e.g. CBERS4
- Sensor (Sensor that collected the data. User-defined name pattern)
    - e.g. AWFI
- ODC metadata type (Check ODC-Dataset_ documentation)
    - e.g. eo
- Number of images to be indexed
    - e.g. 5000
- File with filter for File with parameters for filtering the data to be downloaded in bdc-in-a-box. The parameters are the same as those offered in the stac.py_.
    - e.g. advanced_filter.json_

.. _stac.py: https://github.com/brazil-data-cube/stac.py
.. _advanced_filter.json: https://github.com/brazil-data-cube/bdc-odc/blob/master/docker/odc/files/bdc-in-a-box/advanced_filter.json
.. _ODC-Dataset: https://datacube-core.readthedocs.io/en/latest/ops/dataset_documents.html#metadata-type-definition
