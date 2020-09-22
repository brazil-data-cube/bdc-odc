# Adapted from: https://github.com/thinkWhere/GDAL-Docker/blob/develop/3.6-ubuntu/Dockerfile
#### Use latest Ubuntu LTS release as the base
FROM ubuntu:bionic

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# Install GDAL dependencies
RUN apt-get install -y python3.8 python3-pip libgdal-dev locales vim git

# Ensure locales configured correctly
RUN locale-gen en_US.UTF-8
ENV LC_ALL='en_US.utf8'

# Set python aliases for python3
RUN echo 'alias python=python3' >> ~/.bashrc
RUN echo 'alias pip=pip3' >> ~/.bashrc

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# This will install latest version of GDAL
RUN pip3 install --upgrade pip && pip3 install GDAL==2.2.3

COPY datacube-stats.sh .
COPY .datacube.conf /root/.datacube.conf
RUN ./datacube-stats.sh
