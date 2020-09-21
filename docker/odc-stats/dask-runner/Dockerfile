FROM daskdev/dask

COPY .datacube.conf /root/.datacube.conf
COPY datacube-stats.sh .

RUN apt update -y && apt install build-essential git -y \
    && apt-get install libgdal-dev -y && pip install --upgrade pip \
    && pip install gdal==2.4

RUN ./datacube-stats.sh && rm datacube-stats.sh
