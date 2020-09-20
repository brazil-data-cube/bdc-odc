..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Data Ingestion
===============

With the products and their cataloged datasets, it is possible to perform a data ingestion process. In this process, transformations such as ``reprojection`` and ``tiling`` can be applied to the data to be simpler to be loaded by the ODC and become more usual for different user analyses.

As in all other steps presented in this tutorial, the completion of the ingestion process requires a YAML file. For this case, ``stac2odc`` has no utilities available yet

To get around this issue and make the ingestion process easy, use the file `CB4_64_16D_STK_1.ingest.yaml <https://raw.githubusercontent.com/brazil-data-cube/bdc-odc/master/config/datacube-core/ingest/CB4_64_16D_STK-1.ingest.yaml>`_ is shown below, which contains the description of this operation.

.. code-block:: yaml
    :caption: File with the description of the ingestion process of the product ``CB4_64_16D_STK_1``.

    source_type: CB4_64_16D_STK_1
    output_type: CB4_64_16D_STK_1_ingested

    description: CBERS-4 ingested data

    location: '/data/ingested/'
    file_path_template: 'CB4_64_16D_STK_1_ingested/CB4_64_16D_STK_1_ingested_{tile_index[0]}_{tile_index[1]}_{start_time}.nc'

    global_attributes:
        title: CBERS 4 ingested
        summary: CBERS-4 data product
        source: CBERS 4 version 1
        institution: INPE
        instrument: AWFI
        cdm_data_type: Grid
        keywords: REFLECTANCE,CBERS,EARTH SCIENCE
        platform: CBERS-4
        processing_level: L2
        product_version: '1.0'
        product_suite: INPE CBERS4
        project: BDC
        naming_authority: bdc.inpe
        acknowledgment: CBERS4 is provided by the National Institute for Space Research (INPE).

    storage:
        driver: NetCDF CF

        crs: +proj=aea +lat_0=-12 +lon_0=-54 +lat_1=-2 +lat_2=-22 +x_0=5000000 +y_0=10000000 +ellps=GRS80 +units=m +no_defs
        tile_size:
                x: 100000.0
                y: 100000.0
        resolution:
                x: 64
                y: -64
        chunking:
            x: 200
            y: 200
            time: 1
        dimension_order: ['time', 'y', 'x']

    measurements:
        - name: blue
          dtype: int16
          nodata: -9999
          resampling_method: nearest
          src_varname: 'blue'
          zlib: True
          attrs:
            long_name: "BAND13"
            alias: "BAND13"

        - name: evi
          dtype: int16
          nodata: -9999
          resampling_method: nearest
          src_varname: 'evi'
          zlib: True
          attrs:
            long_name: "EVI"
            alias: "EVI"

        - name: green
          dtype: int16
          nodata: -9999
          resampling_method: nearest
          src_varname: 'evi'
          zlib: True
          attrs:
            long_name: "BAND14"
            alias: "BAND14"

        - name: ndvi
          dtype: int16
          nodata: -9999
          resampling_method: nearest
          src_varname: 'ndvi'
          zlib: True
          attrs:
            long_name: "BAND16"
            alias: "BAND16"

        - name: red
          dtype: int16
          nodata: -9999
          resampling_method: nearest
          src_varname: 'red'
          zlib: True
          attrs:
            long_name: "BAND15"
            alias: "BAND15"


.. note::

    More YAML for ingestion is available in `bdc-odc repository <https://github.com/brazil-data-cube/bdc-odc>`_.

The ingestion process present in the file ``CB4_64_16D_STK-1.ingest.yaml`` performs the data's ``compression`` and applies ``tiling`` so that the data's recovery is made faster. The generation of the ingestion is presented below::

    sudo datacube -v ingest \
                  -c CB4_64_16D_STK_v1.ingest.yaml \
                  --executor multiproc 2


Besides the option ``--executor``, applied in the above command, several others can be used to accelerate the ingestion process and guarantee its reproducibility. For more information, consult the `ODC documentation <https://datacube-core.readthedocs.io/en/latest/ops/ingest.html>`_.
