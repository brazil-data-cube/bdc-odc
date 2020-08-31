#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from abc import ABC, abstractmethod

from loguru import logger
import stac2odc.utils as utils
from collections import OrderedDict


class Stac2ODCMapper(ABC):
    @abstractmethod
    def map_collection(self, collection, **kwargs) -> OrderedDict:
        pass

    @abstractmethod
    def map_dataset(self, collection, dataset_items, **kwargs) -> OrderedDict:
        pass


class Stac2ODCMapper08(Stac2ODCMapper):
    def map_collection(self, collection, **kwargs) -> OrderedDict:
        if kwargs['verbose']:
            logger.info("collection2product is running!")

        crs_proj4 = collection['properties']['bdc:crs']
        if kwargs['is_pre_collection']:
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

        product_type = utils.generate_product_type(collection)

        odc_config = OrderedDict()
        odc_config['name'] = collection['id']
        odc_config['description'] = collection['description']
        odc_config['metadata_type'] = kwargs['metadata_type']

        odc_config['storage'] = OrderedDict()
        odc_config['storage']['crs'] = crs_proj4
        odc_config['storage']['resolution'] = OrderedDict()
        first_band = next(iter(collection['properties']['bdc:bands']))
        odc_config['storage']['resolution']['x'] = int(
            collection['properties']['bdc:bands'][first_band]['resolution_x'])
        odc_config['storage']['resolution']['y'] = int(
            collection['properties']['bdc:bands'][first_band]['resolution_y']) * -1

        def measurements(tag, data):
            m = OrderedDict()
            m['name'] = tag  # data['name']
            m['aliases'] = [data['name'], ]
            m['dtype'] = data['data_type'].lower()
            m['nodata'] = data['fill']
            m['units'] = kwargs['units']
            return m

        odc_config['metadata'] = OrderedDict()
        odc_config['metadata']['platform'] = {'code': kwargs['platform_code']}
        odc_config['metadata']['instrument'] = {'name': kwargs['instrument_type']}
        odc_config['metadata']['product_type'] = product_type
        odc_config['metadata']['format'] = {'name': kwargs['format_name']}
        odc_config['measurements'] = [measurements(k, v)
                                      for k, v in collection['properties']['bdc:bands'].items() if
                                      k not in kwargs['ignore']]

        if kwargs['verbose']:
            logger.info("Finished!")
        return odc_config

    def map_dataset(self, collection, dataset_items, **kwargs) -> OrderedDict:
        from osgeo import osr
        from osgeo import gdal
        from datetime import datetime
        import stac2odc.environment as environment

        if kwargs['verbose']:
            logger.info("item2dataset is running!")

        crs_proj4 = collection['properties']['bdc:crs']
        if kwargs['is_pre_collection']:
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

        sr = osr.SpatialReference()
        sr.ImportFromProj4(crs_proj4)
        crs_wkt = sr.ExportToWkt()

        odc_items = []
        for f in dataset_items:
            try:
                _startdate, _enddate = utils.stacdate_to_odcdate(f['id'])
            except:
                _tmp = f['properties']['datetime']
                _startdate, _enddate = _tmp, _tmp

            _featureid = utils.generate_id(f)
            if kwargs['verbose']:
                logger.info(f"New item found: {_featureid}")

            feature = OrderedDict()
            feature['id'] = _featureid
            feature['creation_dt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%fZ")
            feature['product_type'] = utils.generate_product_type(collection)
            feature['platform'] = {'code': kwargs['plataform_code']}
            feature['instrument'] = {'name': kwargs['instrument_type']}
            feature['format'] = {'name': kwargs['format_name']}
            feature['lineage'] = {'source_datasets': {}}

            feature['extent'] = OrderedDict()
            feature['extent']['coord'] = OrderedDict()
            feature['extent']['coord']['ul'] = {'lon': f['geometry']['coordinates'][0][0][0],
                                                'lat': f['geometry']['coordinates'][0][0][1]}
            feature['extent']['coord']['ur'] = {'lon': f['geometry']['coordinates'][0][1][0],
                                                'lat': f['geometry']['coordinates'][0][1][1]}
            feature['extent']['coord']['lr'] = {'lon': f['geometry']['coordinates'][0][2][0],
                                                'lat': f['geometry']['coordinates'][0][2][1]}
            feature['extent']['coord']['ll'] = {'lon': f['geometry']['coordinates'][0][3][0],
                                                'lat': f['geometry']['coordinates'][0][3][1]}

            feature['extent']['from_dt'] = _startdate
            feature['extent']['center_dt'] = _startdate  # ToDo: Verify this
            feature['extent']['to_dt'] = _enddate

            # verify if necessary download data
            if kwargs['download']:
                logger.info(f"Downloading item: {_featureid}")
                environment.download_stac_tree(f, **kwargs)
                kwargs['basepath'] = kwargs['download_out']

            # Extract image bbox
            first_band = next(iter(collection['properties']['bdc:bands']))
            first_band_path = utils.href_to_path(
                f['assets'][first_band]['href'], kwargs['basepath'])

            src = gdal.Open(first_band_path)
            ulx, xres, _, uly, _, yres = src.GetGeoTransform()
            lrx = ulx + (src.RasterXSize * xres)
            lry = uly + (src.RasterYSize * yres)

            feature['grid_spatial'] = OrderedDict()
            feature['grid_spatial']['projection'] = OrderedDict()
            feature['grid_spatial']['projection']['geo_ref_points'] = OrderedDict()
            feature['grid_spatial']['projection']['geo_ref_points']['ul'] = {
                'x': ulx, 'y': uly}
            feature['grid_spatial']['projection']['geo_ref_points']['ur'] = {
                'x': lrx, 'y': uly}
            feature['grid_spatial']['projection']['geo_ref_points']['lr'] = {
                'x': lrx, 'y': lry}
            feature['grid_spatial']['projection']['geo_ref_points']['ll'] = {
                'x': ulx, 'y': lry}

            feature['grid_spatial']['projection']['spatial_reference'] = crs_wkt
            feature['image'] = OrderedDict()
            feature['image']['bands'] = OrderedDict()
            band_counter = 1
            for band in collection['properties']['bdc:bands'].keys():
                if band not in kwargs['ignore']:
                    if band in f['assets']:
                        feature['image']['bands'][band] = OrderedDict()
                        feature['image']['bands'][band]['path'] = utils.href_to_path(
                            f['assets'][band]['href'], kwargs['basepath'])
                        feature['image']['bands'][band]['layer'] = 1
                        band_counter += 1
                    else:
                        logger.info("Band '{}' was not found in asset '{}'".format(
                            band, f['id']))
            odc_items.append(feature)
        return odc_items


class Stac2ODCMapper09(Stac2ODCMapper):
    def map_collection(self, collection, **kwargs) -> OrderedDict:
        pass

    def map_dataset(self, collection, dataset_items, **kwargs) -> OrderedDict:
        pass
