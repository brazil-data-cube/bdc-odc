FROM local/odc:1.7

USER root
# Get dependencies for Jupyter
RUN pip3 install \
    jupyter matplotlib folium geopandas seaborn descartes ipyleaflet \
    && jupyter nbextension enable --py --sys-prefix ipyleaflet \
    && rm -rf $HOME/.cache/pip

USER $ODC_USR
WORKDIR /home/$ODC_USR
EXPOSE 8889
