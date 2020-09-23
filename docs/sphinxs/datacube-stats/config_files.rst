..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Configuration files
====================

This section lists the configuration files that are used in the ``datacube-stats`` configuration

.env
-------

The ``.env`` file is used to describe the mapping of directories within the container. This way, only two configuration keys are available

- **DATA_DIR_SOURCE**: Indicates the directory on the host machine that will be mapped
- **DATA_DIR_TARGET**: Where the machine directory will be mapped inside the container

It is essential to configure this file correctly since it must be by the way your data is stored. This mapping will eventually be used by the ODC to search for data, but this may vary according to the way your data is stored and configured in the ODC catalog.
