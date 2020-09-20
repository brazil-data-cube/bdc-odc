#!/bin/bash

echo "Installing OSGeo GDAL"
apt update -y && apt install build-essential git -y
apt-get install libgdal-dev -y && pip3 install --upgrade pip \
    && pip3 install GDAL==2.2.3

echo "Installing datacube..."
pip3 install datacube

echo "Installing digitalearthau..."
git clone https://github.com/GeoscienceAustralia/digitalearthau && cd digitalearthau
python3 setup.py install && rm -rf digitalearthau

echo "Installing odc-tools..."
pip3 install --extra-index-url="https://packages.dea.ga.gov.au" \
  odc-ui \
  odc-index \
  odc-geom \
  odc-algo \
  odc-io \
  odc-aws \
  odc-aio \
  odc-dscache \
  odc-dtools
pip3 install --extra-index-url="https://packages.dea.ga.gov.au" odc-apps-dc-tools

echo "Installing datacube-stats"
pip3 install git+https://github.com/opendatacube/datacube-stats/
