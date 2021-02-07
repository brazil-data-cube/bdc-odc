..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Analyzing large volumes of data with ODC Stats
=================================================

To facilitate the process of statistical analysis of large volumes of data, the ODC ecosystem makes available available ``datacube-stats``. This tool allows the user to declare the operations that need to be done without worrying about implementation. In BDC-ODC, the ``datacube-stats`` is also configured, able to work with both distributed and parallel operations. This section shows the steps for tool configuration.

All configuration files presented in this step by step are available in the `BDC-ODC repository <https://github.com/brazil-data-cube/bdc-odc/tree/master/docker/odc-stats>`_.

.. toctree::
    :maxdepth: 1
    :caption: Topics:
    :titlesonly:

    ./datacube-stats/install
    ./datacube-stats/usage
    ./datacube-stats/config_files
