..
    This file is part of Brazil Data Cube ODC Scripts & Tools.
    Copyright (C) 2019 INPE.

    Brazil Data Cube ODC Scripts & Tools is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.



Adding Products and Indexing Datasets
=====================================

Requirements
------------

To import ODC Stac collections to the ODC instance is required to install some tools. 
First, execute the following command to get a `console` inside the ODC instance:


.. code-block:: shell

    $ docker exec -it bdc-odc-core /bin/bash

At the ODC terminal, run the following commands to download and install as required tools:

.. code-block:: shell

    $ git clone https://github.com/vconrado/bdc-odc.git
    $ pip install -r bdc-odc/scripts/collection2yaml/requirements.txt

The following steps are required for registration of a `Product` and indexing the `Datasets`:
    * Extract Product metadata
    * Add Product to ODC database
    * Extract Datasets metadata
    * Add Dataset to ODC database 


Extracting Product metadata
---------------------------

Initially, we will create a folder where the metadata will be saved:

.. code-block:: shell

    $ mkdir -p ~/products/C4_64_16D_MED/datasets

We provided a script for extracting the metadata from a `Collection` of BDC STAC to the format of an ODC `Product`.
To produce the methods for the `C4_64_16D_MED` `Collection`, use the following command:

.. code-block:: shell

    $ python3 bdc-odc/scripts/collection2yaml/collection2yaml.py -c C4_64_16D_MED -o ~/products/C4_64_16D_MED/C4_64_16D_MED.yaml

You can see the created file with the following command:

.. code-block:: shell

    $ cat ~/products/C4_64_16D_MED/C4_64_16D_MED.yaml

Add Product to ODC database
---------------------------

To register the new `Product` in the ODC database, use the following command:

.. code-block:: shell

    $ datacube product add ~/products/C4_64_16D_MED/C4_64_16D_MED.yaml


Extract Datasets metadata
--------------------------

We also provided a script for extracting the metadata from `Items` of a `Collection` of BDC STAC to the format of an ODC `Dataset`.
To create the metadata files from `C4_64_16D_MED` `Collection` use the following command:

.. code-block:: shell

    $ python3 bdc-odc/scripts/item2dataset/item2dataset.py -c C4_64_16D_MED -o ~/products/C4_64_16D_MED/datasets/

For each `Item` in the `Collection`, a YAML file will be created with the metadata to be inserted as a `Dataset` in the ODC.


Add Dataset to ODC database 
---------------------------

To register one `Dataset` in the ODC database, use the following command:

.. code-block:: shell

    datacube -v dataset add -p C4_64_16D_MED ~/products/C4_64_16D_MED/datasets/C4_64_16D_MED_083100_2016-09-13_2016-09-28.yaml

You can automate the indexing of `Datasets` using the following command:

.. code-block:: shell

    find ~/products/C4_64_16D_MED/datasets/*.yaml -exec datacube -vvv dataset add -p C4_64_16D_MED {} \;


Script for Product registration and Datasets indexing
=====================================================

We also provide a script to facilitate the process of extracting metadata and registering products and datasets. You can use the following command to perform the 4 tasks listed above:

.. code-block:: shell

    $ ./bdc-odc/scripts/index_collection.sh C4_64_16D_MED ~/products
