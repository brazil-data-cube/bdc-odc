#!/bin/bash

echo "Installing datacube..."

# During the configuration of the odc-dask certain problems related
# to the dask version were identified. To get around this problem, the way the
# command line parameters are passed to the dask.distributed API is replaced.
# This makes the use of dask possible even in the most recent versions.
git clone https://github.com/opendatacube/datacube-core.git && cd datacube-core
sed -i 's/DistributedExecutor(distributed.Client(scheduler))/DistributedExecutor(distributed.Client(":".join(map(str, scheduler))))/g' \
  datacube/executor.py
pip install --upgrade -e .

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
