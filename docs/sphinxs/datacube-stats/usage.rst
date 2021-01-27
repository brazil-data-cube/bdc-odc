..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Usage
=======

As mentioned earlier, the ``datacube-stats`` allows the user to worry only about the definition of the operation that will be carried out. The way the process will be done is up to the tool. The description of the operation is made using ``YAML`` files. This section will present an example of a ``YAML`` file describing a simple NDVI mean operation and how the ``datacube-stats`` consume and execute that operation.

To start, the mean operation in the NDVI "band" that is delivered in the BDC's datacubes is done based on the file presented below

.. code-block:: yaml
    :caption: ``CB4_64_16D_STK_1.temporal_mean.stats.yaml`` File with the description of the mean operation in NDVI

    sources:
      - product: CB4_64_16D_STK_1
        measurements: [NDVI]
        group_by: solar_day
        time: [2020-07-11, 2020-07-27]

    date_ranges:
      start_date: 2020-07-01
      end_date:  2020-08-01

    location: /data/stats/

    storage:
      driver: GeoTIFF

      crs: +proj=aea +lat_0=-12 +lon_0=-54 +lat_1=-2 +lat_2=-22 +x_0=5000000 +y_0=10000000 +ellps=GRS80 +units=m +no_defs
      tile_size:
        x: 100000.0
        y: 100000.0
      resolution:
        x: 64
        y: -64
      chunking:
        x: 256
        y: 256
        time: 1
      dimension_order: [time, x, y]

    computation:
      chunking:
        x: 1000
        y: 1000

    output_products:
      - name: CB4_64_16D_STK_1_simple_mean
        product_type: ndvi_simple_mean
        statistic: simple
        statistic_args:
          reduction_function: mean
        output_params:
          zlib: True
          fletcher32: True
        metadata:
          format:
            name: GeoTIFF
          platform:
            code: CBERS4
          instrument:
            name: AWFI
        file_path_template: 'CB4_64_16D_STK_1_NDVI_SIMPLE_MEAN/{name}_ndvi_{y}_{x}_{epoch_start:%Y-%m-%d}_{epoch_end:%Y-%m-%d}.tif'

Note that in the file presented above, the form of storage, transformations, and the statistical operation performed is described, but at no time does the user need to describe how the operation will be performed.

.. note::

    To learn more about the operations description file, consult the `datacube-stats repository <https://github.com/opendatacube/datacube-stats>`_.

After defining the file, it can be consumed using the CLI of ``datacube-stats``. This consumption can be done by passing several parameters, which can change how the operation is performed. For example, to run on a single processor, using 6 cores, the ``--parallel`` parameter can be used::

    datacube-stats --parallel 6 CB4_64_16D_STK_1.temporal_mean.stats.yaml

o execute with the dask, the operation can be done using the parameter ``--dask``, passing the scheduler's connection parameters::

    datacube-stats --dask scheduler:8786 CB4_64_16D_STK_1.temporal_mean.stats.yaml

.. note::

    To execute the operations above, you must connect to the client container, which was started with the others, use the command below::

        docker-compose exec odc-stats bash

.. note::

    For more files with descriptions of operations considering BDC data products, consult the `BDC-ODC repository <https://github.com/brazil-data-cube/bdc-odc>`_.
