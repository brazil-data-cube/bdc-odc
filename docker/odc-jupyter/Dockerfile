FROM odc:1.7


USER root
# Get dependencies for Jupyter
RUN pip3 install \
    jupyter matplotlib folium geopandas seaborn descartes\
    && rm -rf $HOME/.cache/pip

USER $ODC_USR
WORKDIR /home/$ODC_USR
EXPOSE 8888
CMD ["jupyter","notebook", "--no-browser", "--ip=\"*\"", "--port=8888"]
