..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Creating the Datasets Metadata
===============================

The records of datasets in the ``ODC-Core`` catalog are made in the same way as the products: given a definition in ``YAML`` file, it is possible to make the addition. In this case, ``stac2odc`` offers a utility to map BDC-STAC items in datasets.


.. note::

    Before executing the utility, it is necessary to understand that this process requires the BDC data repository; this is because the path to the data files is required during the datasets' description. With this in mind, ``stac2odc`` offers the option ``--download``, which allows you to download the data and then make its description. For this tutorial, this facility will be used.


To extract the metadata from the datasets, it is necessary to define the collection, the amount of data considered, and the options of ``unit`` and ``instrument`` presented previously::

    sudo stac2odc item2dataset -c CB4_64_16D_STK-1 \
                               -o ~/products/CB4_64_16D_STK_1/datasets/ \
                               --units m \
                               -p CBERS4 \
                               --instrument AWFI \
                               -m 3 \
                               --download \
                               --download-out /data


The above command will download 03 items from the data cube ``CB4_64_16D_STK-1``, saved in the ``/data`` directory. The descriptions of these items will be placed in the directory ``~/products/CB4_64_16D_STK_1/datasets/``. The directory tree created in the ``/data`` folder follows the same organization used in the BDC.
