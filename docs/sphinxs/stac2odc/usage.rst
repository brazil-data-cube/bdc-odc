..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


stac2odc operations
====================

Essentially, ``stac2odc`` offers two operations, each responsible for transforming STAC data into ODC objects. The functions are presented below.

STAC-Collection to ODC-Product
---------------------------------

The first operation available on ``stac2odc`` is the ``collection2product`` that enables the conversion of STAC-Collections into ODC-Products. The CLI can be seen below.

.. click:: stac2odc.cli:collection2product_cli
    :prog: stac2odc collection2product

STAC-Item to ODC-Dataset
--------------------------

The second possible operation with ``stac2odc`` is ``item2dataset``, which allows the conversion from STAC-Item to ODC-Dataset.

.. click:: stac2odc.cli:item2dataset_cli
    :prog: stac2odc item2dataset
