..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Configuration files
====================

The use of a bdc-in-a-box is done with a script and two auxiliary files. In this section, we will briefly present the characteristics and possibilities with each of these files.

bdc-in-a-box.sh
-----------------

``bdc-in-a-box.sh`` is the script that reads the auxiliary files and uses the information in each one to download the data and register in the ODC. Essentially this script automates the operations of ``stac2odc``, which brings the user the ease of not working directly with the parameters of ``stac2odc``.

collections.list
------------------

``collections.list`` is a ``CSV`` file created to facilitate the definition of which data should be considered in indexing. This section presents its structure.

The file is composed of 6 columns (in order), being them:

- **Collection Name** (This name must be the same as the one made available in BDC-STAC)

    - e.g. CB4_64_16D_STK_v1
- **Platform** (Sensor platform that generated the data. User-defined name pattern)

    - e.g. CBERS4
- **Sensor** (Sensor that collected the data. User-defined name pattern)

    - e.g. AWFI
- **ODC metadata type** (Check ODC-Dataset_ documentation)

    - e.g. eo
- **Number of images to be indexed**

    - e.g. 5000

- **File with parameters for filtering** the data to be downloaded in ``bdc-in-a-box``. The parameters are the same as those offered in the stac.py_. The file may be blank, but must be declared in the lines of the collections.list file

    - e.g. advanced_filter.json_

.. _stac.py: https://github.com/brazil-data-cube/stac.py
.. _advanced_filter.json: https://github.com/M3nin0/brazil-data-cube/blob/master/docker/odc/files/bdc-in-a-box/advanced_filter.json
.. _ODC-Dataset: https://datacube-core.readthedocs.io/en/latest/ops/dataset_documents.html#metadata-type-definition

advanced_filter.json
---------------------

The file ``advanced_filter.json`` allows the filter functionalities implemented in stac.py_ to be used by bdc-in-a-box users. This way, the same parameters that stac.py accepts can be inserted in this ``JSON`` file. Internally, the content of ``advanced_filter.json`` is passed to the search method of stac.py_.

For example, consider the file ``advanced_filter.json`` presented below.

.. code-block:: json
    :caption: An example filter file used by bdc-in-a-box.

    {
        "datetime": "2016-09-13/2017-12-31",
        "intersects": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -44.78027343749999,
                  -14.434680215297268
                ],
                [
                  -41.9677734375,
                  -14.434680215297268
                ],
                [
                  -41.9677734375,
                  -11.480024648555816
                ],
                [
                  -44.78027343749999,
                  -11.480024648555816
                ],
                [
                  -44.78027343749999,
                  -14.434680215297268
                ]
              ]
            ]
        }
    }

Internally, the contents of this file will be passed as follows to stac.py::

    items = stac.search({
        "datetime": "2016-09-13/2017-12-31",
        "intersects": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -44.78027343749999,
                  -14.434680215297268
                ],
                [
                  -41.9677734375,
                  -14.434680215297268
                ],
                [
                  -41.9677734375,
                  -11.480024648555816
                ],
                [
                  -44.78027343749999,
                  -11.480024648555816
                ],
                [
                  -44.78027343749999,
                  -14.434680215297268
                ]
              ]
            ]
        }
    })
