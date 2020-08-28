# Adapted from: https://github.com/opendatacube/datacube-core/blob/develop/Dockerfile
FROM ubuntu:18.04

###########################################################################
# Added by Vitor Gomes
ENV DATA_DIR=/datacube

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV ODC_USR=datacube
ENV ODC_PASS=datacube
ENV ROOT_PASS=datacube
ENV APPDIR=/tmp/code
ENV ODC_INSTALL=/opt/odc
###########################################################################

RUN groupadd $ODC_USR \
    # Adding user ODC_USER
    && useradd $ODC_USR -s /bin/bash -m -g $ODC_USR \
    && echo $ODC_USR:$ODC_PASS | chpasswd  \
    # Changing root password
    && echo root:$ROOT_PASS | chpasswd  \
    # Creating APPDIR
    && mkdir -p $APPDIR \
    && chown $ODC_USR:$ODC_USR $APPDIR \
    # Creating DATA_DIR
    && mkdir -p $DATA_DIR \
    && chown $ODC_USR:$ODC_USR $DATA_DIR

# First add the NextGIS repo
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:nextgis/ppa

# And now install apt dependencies, including a few of the heavy Python projects
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core requirements from travis.yml
    gdal-bin gdal-data libgdal-dev libgdal20 libudunits2-0 \
    # Extra python components, to speed things up
    python3 python3-setuptools python3-dev \
    python3-numpy python3-netcdf4 python3-gdal \
    # Need pip to install more python packages later.
    # The libdpkg-perl is needed to build pyproj
    python3-pip python3-wheel cython3 libdpkg-perl \
    # Git to work out the ODC version number
    git \
    # G++ because GDAL decided it needed compiling
    g++ \
    # numpy requires headers for cf_units
    libudunits2-dev \
    ###########################################################################
    # Added by Vitor Gomes
    vim \
    wget \
    sudo \
    git \
    postgresql-client\
    ###########################################################################
    && rm -rf /var/lib/apt/lists/*

###########################################################################
# Adapteded by Vitor Gomes
# Get the code, and put it in /code
RUN git clone https://github.com/opendatacube/datacube-core.git $APPDIR \
    && cd $APPDIR \
    && git checkout tags/datacube-1.7 \
    && sed -i 's/cligj==0\.4\.0/cligj==0\.5\.0/g' requirements-test.txt \
    && sed -i 's/botocore==1\.12\.117/botocore==1\.12\.195/g' requirements-test.txt \
    && sed -i 's/jsonschema==2\.6\.0/jsonschema==3\.0/g' requirements-test.txt
    
WORKDIR $APPDIR
###########################################################################

# Set the locale, this is required for some of the Python packages
ENV LC_ALL C.UTF-8

# Ensure pip is up to date
RUN pip3 install --upgrade pip \
    && rm -rf $HOME/.cache/pip

# Install psycopg2 as a special case to quiet the warning message 
# Make sure this version is the same as in the requirements-test.txt file
RUN pip3 install --no-cache --no-binary :all: psycopg2==2.7.7 \
    && rm -rf $HOME/.cache/pip

# Use the setup.py file to identify dependencies
RUN pip3 install -r requirements-test.txt \
    && rm -rf $HOME/.cache/pip

# Install ODC
RUN python3 setup.py install 

# Move docs and utils somewhere else, and remove the temp folder
RUN mkdir -p /opt/odc \
    && chmod +rwx /opt/odc \
    && mv $APPDIR/utils /opt/odc/ \
    && mv $APPDIR/docs /opt/odc/ \
    && mv $APPDIR/docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh \
    && rm -rf $APPDIR

# Fix an issue with libcurl...
RUN mkdir -p /etc/pki/tls/certs \
    && ln -s /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt;

###########################################################################
# Added by Vitor Gomes
RUN echo "$ODC_USR ALL=(ALL:ALL) NOPASSWD:ALL" | sudo EDITOR='tee -a' visudo

USER datacube
WORKDIR /home/datacube

COPY files/install_aws_cli.sh .
RUN sudo chown $ODC_USR:$ODC_USR install_aws_cli.sh\
    && chmod +x install_aws_cli.sh
    
COPY files/bdc-in-a-box .

#COPY files/docker-entrypoint.sh /usr/local/bin/
#RUN chmod +x /usr/local/bin/docker-entrypoint.sh.sh
###########################################################################

# Set up an entrypoint that drops environment variables into the config file
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["datacube","--help"]
