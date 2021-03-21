..
    This file is part of bdc-odc
    Copyright 2020 INPE.

    bdc-odc is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Using Jupyter Environment with the ODC
=======================================

To access and manipulate the registered data, it is possible to use the ODC API in Python. This use is facilitated with the help of Jupyter Notebook. In this tutorial's installation stage, the Docker Image ``local/odc-jupyter`` was created. It will be used to access the data.


Use the command below to create an instance of the ODC container with support for Jupyter Notebook environment::

    docker run --detach \
               --name bdc-odc-jupyter \
               --hostname bdc-odc-jupyter \
               --network bdc-odc-net \
               --publish 8889:8889 \
               --volume $(pwd)/odc-data-repository:/data \
               --env DB_HOSTNAME=bdc-odc-pg \
               --env DB_DATABASE=opendatacube \
               --env DB_USERNAME=opendatacube \
               --env DB_PASSWORD=secreto \
               --env DB_PORT=5432 \
               local/odc-jupyter:1.7 jupyter notebook --ip=0.0.0.0 --port=8889


.. note::

    Remember to change the information about the location of stored data. The ``--volume`` parameter, in the above command, must point to the same location registered when creating the ``bdc-odc-core`` container


.. note::

    If you have changed the password of the database server, it will be necessary to include the same password in the parameter ``--env DB_PASSWORD``.


If your ``bdc-odc-jupyter`` container is running, use the following command to recover the ``access token`` needed to open the Jupyter Notebook environment on your browser screen::

    docker exec -it bdc-odc-jupyter jupyter notebook list


The Jupyter server should reply with a message similar to::

    Currently running servers:
    http://0.0.0.0:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363 :: /data


Use the ``access token`` shown on your server output to access the Jupyter environment in your browser at the host machine's local address. Example::

    firefox http://127.0.0.1:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363


.. note::

    If you have problems with the Jupyter server, see the log output of your container::

        docker logs -f bdc-odc-jupyter


    A container with functional status will display output, as shown below. It will show the ``access token`` needed to use the Jupyter environment in the browser::

        [I 21:46:46.140 NotebookApp] Writing notebook server cookie secret to /home/datacube/.local/share/jupyter/runtime/notebook_cookie_secret
        [I 21:46:47.391 NotebookApp] Serving notebooks from local directory: /data
        [I 21:46:47.391 NotebookApp] Jupyter Notebook 6.1.3 is running at:
        [I 21:46:47.392 NotebookApp] http://bdc-odc-jupyter:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363
        [I 21:46:47.392 NotebookApp]  or http://127.0.0.1:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363
        [I 21:46:47.392 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
        [W 21:46:47.409 NotebookApp] No web browser found: could not locate runnable browser.
        [C 21:46:47.409 NotebookApp]

            To access the notebook, open this file in a browser:
                file:///home/datacube/.local/share/jupyter/runtime/nbserver-1-open.html
            Or copy and paste one of these URLs:
                http://bdc-odc-jupyter:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363
             or http://127.0.0.1:8889/?token=d3e5ce2c0ae5e003cc5b606bdacc7e25a34ea23d36081363

That's it! Now the datacube API can be consumed to access the data, for examples, see the `ODC application library <https://www.opendatacube.org/dcal>`_.
