..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installing
============

As with the other BDC-ODC tools, ``datacube-stats`` are being installed through a Docker container. In the structure presented, a dask cluster based on Docker containers is created, which allows the configuration of distributed execution of operations. The use of the distributed operation is optional, and all the execution can be done in parallel, in a single processor.

To begin with, the first step is to acquire the source code used to create the Docker images::

    git clone https://github.com/brazil-data-cube/bdc-odc.git

    cd bdc-odc/docker/odc-stats/

With the code downloaded and inside the odc-stats directory, it is necessary to create the `.datacube.conf <https://datacube-core.readthedocs.io/en/latest/ops/db_setup.html#create-configuration-file>`_ file. After creating this file in the current directory, access the ``dask-cluster`` directory, and create a ``.env`` file. This file will be used to configure the mapping of the container data directory

.. note::

    For more information about the possible values in the .env file, see the `datacube-stats configuration file page <config_files.html>`_.

After configuring these files, run the ``build.sh`` script. It will create the images and also run the containers::

    ./build.sh

To visualize the containers in execution, after finishing the script execution, use the command below::

    docker-compose ps

The output should look like the following::

    Name                        Command               State                       Ports
    ------------------------------------------------------------------------------------------------------------------
    dask-cluster_odc-stats_1   python3                          Up
    dask-cluster_scheduler_1   tini -g -- /usr/bin/prepar ...   Up      0.0.0.0:8786->8786/tcp, 0.0.0.0:8787->8787/tcp
    dask-cluster_worker_1      tini -g -- /usr/bin/prepar ...   Up

Make sure everything is correct by running the ``datacube-stats`` help command::

    docker-compose exec odc-stats datacube-stats --help

The output should look like::

    Usage: datacube-stats [OPTIONS] STATS_CONFIG_FILE

    Options:
      --save-tasks FILE
      --load-tasks PATH
      --tile-index INTEGER...         Override input_region specified in
                                      configuration with a single tile_index
                                      specified as [X] [Y]

      --tile-index-file FILE          A file consisting of tile indexes specified
                                      as [X] [Y] per line

      --output-location TEXT          Override output location in configuration
                                      file

      --year INTEGER                  Override time period in configuration file
      --task-slice SLICE              The subset of tasks to perform, using
                                      Python's slice syntax.

      --batch INTEGER                 The number of batch jobs to launch using PBS
                                      and the serial executor.

      --list-statistics
      --version
      -v, --verbose                   Use multiple times for more verbosity
      --log-file TEXT                 Specify log file
      -E, --env TEXT
      -C, --config, --config_file TEXT
      --log-queries                   Print database queries.
      --qsub OPTS                     Launch via qsub, supply comma or new-line
                                      separated list of parameters. Try
                                      --qsub=help.

      --workers-per-node INTEGER      For code that parallelizes over cores
      --queue-size INTEGER            Overwrite defaults for queue size
      --celery HOST:PORT              Use celery backend for parallel computation.
                                      Supply redis server address, or "pbs-launch"
                                      to launch redis server and workers when
                                      running under pbs.

      --dask HOST:PORT                Use dask.distributed backend for parallel
                                      computation. Supply address of dask
                                      scheduler.

      --parallel INTEGER              Run locally in parallel
      --version
      --help                          Show this message and exit.

