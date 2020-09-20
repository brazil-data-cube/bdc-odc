..
    This file is part of Brazil Data Cube ODC Scripts & Tools.
    Copyright (C) 2019 INPE.

    Brazil Data Cube ODC Scripts & Tools is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.



Adding Products and Indexing Datasets
=====================================

> The execution of the scripts below requires the BDC image collection. If you do not have access to BDC infrastructure use the bdc-in-a-box tool.

Requirements
------------

To import ODC Stac collections to the ODC instance is required to install some tools. 
First, execute the following command to get a `console` inside the ODC instance:


.. code-block:: shell

    $ docker exec -it bdc-odc-core /bin/bash

At the ODC terminal, run the following commands to download and install as required tools:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/bdc-odc.git
    $ cd bdc-odc/stac2odc
    $ sudo pip3 install -e .[all]

The following steps are required for registration of a `Product` and indexing the `Datasets`:
    * Extract Product metadata
    * Add Product to ODC database
    * Extract Datasets metadata
    * Add Dataset to ODC database 


Extracting Product metadata
---------------------------

Initially, we will create a folder where the metadata will be saved:

.. code-block:: shell

    $ mkdir -p ~/products/CB4_64_16D_STK_v1/datasets

We provided a script for extracting the metadata from a `Collection` of BDC STAC to the format of an ODC `Product`.
To produce the methods for the `CB4_64_16D_STK_v1` `Collection`, use the following command:

.. code-block:: shell

    $ stac2odc collection2product -c CB4_64_16D_STK_v1 -o ~/products/CB4_64_16D_STK_v1/CB4_64_16D_STK_v1.yaml --units m -p CBERS4 --instrument AWFI --type eo

You can see the created file with the following command:

.. code-block:: shell

    $ cat ~/products/CB4_64_16D_STK_v1/CB4_64_16D_STK_v1.yaml

Add Product to ODC database
---------------------------

To register the new `Product` in the ODC database, use the following command:

.. code-block:: shell

    $ datacube product add ~/products/CB4_64_16D_STK_v1/CB4_64_16D_STK_v1.yaml


Extract Datasets metadata
--------------------------

We also provided a script for extracting the metadata from `Items` of a `Collection` of BDC STAC to the format of an ODC `Dataset`.
To create the metadata files from `CB4_64_16D_STK_v1` `Collection` use the following command:

.. code-block:: shell

    $ stac2odc item2dataset -c CB4_64_16D_STK_v1 -o ~/products/CB4_64_16D_STK_v1/datasets/ --units m -p CBERS4 --instrument AWFI -m 5

For each `Item` in the `Collection`, a YAML file will be created with the metadata to be inserted as a `Dataset` in the ODC. 5 elements will be converted

Add Dataset to ODC database 
---------------------------

To register one `Dataset` in the ODC database, use the following command (The file name shown in the example below may change according to the date when you made the indexing. To avoid problems, check the files in the directory).

.. code-block:: shell

    $ datacube -v dataset add -p CB4_64_16D_STK_v1 ~/products/CB4_64_16D_STK_v1/datasets/CB4_64_16D_STK_v1_020024_2020-07-11_2020-07-26.yaml

You can automate the indexing of `Datasets` using the following command:

.. code-block:: shell

    $ find ~/products/CB4_64_16D_STK_v1/datasets/*.yaml -exec datacube -vvv dataset add -p CB4_64_16D_STK_v1 {} \;


Script for Product registration and Datasets indexing
=====================================================

We also provide a script to facilitate the process of extracting metadata and registering products and datasets. You can use the following command to perform the 4 tasks listed above:

.. code-block:: shell

    $ bdc-odc/stac2odc/index_collection.sh CB4_64_16D_STK_v1 ~/products m CBERS4 AWFI 500
