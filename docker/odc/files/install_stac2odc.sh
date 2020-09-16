#!/bin/bash

echo "Installing stac2odc"

# Install stac2odc
git clone https://github.com/brazil-data-cube/bdc-odc.git && cd bdc-odc
cd stac2odc && python3 setup.py install && cd ../.. && rm -rf bdc-odc
