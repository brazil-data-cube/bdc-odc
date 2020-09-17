#!/bin/bash

echo "Installing OSGeo GDAL"
apt update -y && apt install build-essential -y
apt-get install libgdal-dev -y && pip install gdal==2.4

echo "Installing datacube..."
# conda install -c conda-forge datacube
pip install datacube

echo "Installing digitalearthau..."
git clone https://github.com/GeoscienceAustralia/digitalearthau && cd digitalearthau
python setup.py install && rm -rf digitalearthau

echo "Installing odc-tools..."
pip install --extra-index-url="https://packages.dea.ga.gov.au" \
  odc-ui \
  odc-index \
  odc-geom \
  odc-algo \
  odc-io \
  odc-aws \
  odc-aio \
  odc-dscache \
  odc-dtools
pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-apps-dc-tools

echo "Installing datacube-stats"
pip install git+https://github.com/opendatacube/datacube-stats/
