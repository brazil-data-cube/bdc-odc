..
    This file is part of Brazil Data Cube ODC Scripts & Tools.
    Copyright (C) 2019 INPE.

    Brazil Data Cube ODC Scripts & Tools is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


A Shareable Collection of Open Data Cube Scripts & Tools
=========================================================

.. image:: https://img.shields.io/github/license/brazil-data-cube/bdc-odc.svg
        :target: https://github.com/brazil-data-cube/bdc-odc/blob/master/LICENSE
        :alt: Software License


.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord

About
-----

The **O**\ pen **D**\ ata **C**\ ube (ODC) framework and all its tools ecosystem are currently being tested with **B**\ razil **D**\ ata **C**\ ube (BDC) data products. This integration aims to increase the set of access, visualization, and analysis tools available to the users of the various data cubes produced by the project. This repository presents the utilities and steps for using ODC tools in the BDC data ecosystem.

Generating the Documentation
----------------------------

The documentation contains details about each of the resources that are available in the repository. To access the documentation, generate it with the commands below.

**1.** Clone the documentation repository::

    git clone https://github.com/brazil-data-cube/bdc-odc.git


**2.** Go to the source code folder::

    cd bdc-odc


**3.** Install the required Python libraries::

    pip3 install -r requirements-docs.txt


or:


.. code-block:: shell

    pip3 install sphinx sphinx_rtd_theme sphinx-copybutton sphinx-tabs sphinx-click


or, if you prefer the ``Anaconda`` distribution::

    conda install sphinx sphinx_rtd_theme sphinx-copybutton sphinx-tabs sphinx-click


**4.** In order to build the HTML documentation, please, go to the ``docs`` folder::

    cd docs/sphinxs


**5.** Build the HTML documentation with the ``make html`` command::

    make html


The above command will generate the HTML documentation under the ``_build/html`` folder. You can open the ``index.html`` file in order to navigate in the documentation::

    firefox _build/html/index.html


.. note::

    In order to clean the sites directory, and remove staled files, you can use the following command::

        make clean

.. note::

    In addition to the steps presented, if your system has not been installed, it is necessary to install ``stac2odc``. See the `installation page <https://github.com/brazil-data-cube/bdc-odc/tree/master/stac2odc>`_.
