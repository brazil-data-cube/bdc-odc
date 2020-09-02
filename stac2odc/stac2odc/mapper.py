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

    def generate_product_type(self, collection):
        return "{}_{}_{}".format(
            collection['properties']['bdc:temporal_composition']['schema'],
            collection['properties']['bdc:temporal_composition']['step'],
            collection['properties']['bdc:temporal_composition']['unit'])

    def map_collection(self, collection, **kwargs) -> OrderedDict:
        def measurements(tag, data):
            m = OrderedDict()
            m['name'] = tag
            m['aliases'] = [data['name'], ]
            m['dtype'] = data['data_type'].lower()
            m['nodata'] = data['fill']
            m['units'] = kwargs['units']
            return m

        if kwargs['verbose']:
            logger.info("collection2product is running!")

        crs_proj4 = collection['properties']['bdc:crs']
        if kwargs['is_pre_collection']:
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

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

        odc_config['metadata'] = OrderedDict()
        odc_config['metadata']['platform'] = {'code': kwargs['platform_code']}
        odc_config['metadata']['instrument'] = {'name': kwargs['instrument_type']}
        odc_config['metadata']['product_type'] = self.generate_product_type(collection)
        odc_config['metadata']['format'] = {'name': kwargs['format_name']}
        odc_config['measurements'] = [measurements(k, v)
                                      for k, v in collection['properties']['bdc:bands'].items() if
                                      k not in kwargs['ignore']]

        if kwargs['verbose']:
            logger.info("Finished!")
        return odc_config

    def map_dataset(self, collection, dataset_items, **kwargs) -> OrderedDict:
        from osgeo import gdal
        from datetime import datetime
        import stac2odc.environment as environment

        if kwargs['verbose']:
            logger.info("item2dataset is running!")

        crs_proj4 = collection['properties']['bdc:crs']
        if kwargs['is_pre_collection']:
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

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
            feature['product_type'] = self.generate_product_type(collection)
            feature['platform'] = {'code': kwargs['plataform_code']}
            feature['instrument'] = {'name': kwargs['instrument_type']}
            feature['format'] = {'name': kwargs['format_name']}
            feature['lineage'] = {'source_datasets': {}}

            feature['extent'] = OrderedDict()
            feature['extent']['coord'] = OrderedDict()
            feature['extent']['coord'] = utils.geometry_coordinates(f)
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

            # build grid_spatial
            lrx, lry, ulx, uly = utils.raster_bounds(first_band_path)
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

            feature['grid_spatial']['projection']['spatial_reference'] = utils.to_wkt(crs_proj4)
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

    def generate_product_type(self, collectionobj):
        return "{}_{}_{}".format(
            collectionobj['bdc:temporal_composition']['schema'],
            collectionobj['bdc:temporal_composition']['step'],
            collectionobj['bdc:temporal_composition']['unit'])

    def map_collection(self, collection, **kwargs) -> OrderedDict:
        def measurements(data):
            m = OrderedDict()
            m['name'] = data['name']
            m['aliases'] = [data['name'], ]
            m['dtype'] = data['data_type'].lower()
            m['nodata'] = data['nodata']
            m['units'] = kwargs['units']
            return m

        if kwargs['verbose']:
            logger.info("collection2product is running!")

        crs_proj4 = collection['cube:dimensions']['x']['reference_system']
        if kwargs['is_pre_collection']: # fix gdal3 proj4 pattern error
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

        odc_config = OrderedDict()
        odc_config['name'] = collection['id']
        odc_config['description'] = collection['description']
        odc_config['metadata_type'] = kwargs['metadata_type']

        odc_config['storage'] = OrderedDict()
        odc_config['storage']['crs'] = crs_proj4
        odc_config['storage']['resolution'] = OrderedDict()
        odc_config['storage']['resolution']['x'] = int(collection['properties']['eo:gsd'])
        odc_config['storage']['resolution']['y'] = int(collection['properties']['eo:gsd']) * -1

        # Generate platform infos
        odc_config['metadata'] = OrderedDict()
        odc_config['metadata']['platform'] = {'code': kwargs['platform_code']}
        odc_config['metadata']['instrument'] = {'name': kwargs['instrument_type']}
        odc_config['metadata']['product_type'] = self.generate_product_type(collection)
        odc_config['metadata']['format'] = {'name': kwargs['format_name']}
        odc_config['measurements'] = [measurements(v)
                                      for v in collection['properties']['eo:bands'] if
                                      v['common_name'] not in kwargs['ignore']]

        if kwargs['verbose']:
            logger.info("Finished!")
        return odc_config

    def map_dataset(self, collection, dataset_items, **kwargs) -> OrderedDict:
        from datetime import datetime
        import stac2odc.environment as environment

        if kwargs['verbose']:
            logger.info("item2dataset is running!")

        crs_proj4 = collection['cube:dimensions']['x']['reference_system']
        if kwargs['is_pre_collection']:
            crs_proj4 = utils.fix_precollection_crs(crs_proj4)

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
            feature['product_type'] = self.generate_product_type(collection)
            feature['platform'] = {'code': kwargs['plataform_code']}
            feature['instrument'] = {'name': kwargs['instrument_type']}
            feature['format'] = {'name': kwargs['format_name']}
            feature['lineage'] = {'source_datasets': {}}

            feature['extent'] = OrderedDict()
            feature['extent']['coord'] = OrderedDict()
            feature['extent']['coord'] = utils.geometry_coordinates(f)
            feature['extent']['from_dt'] = _startdate
            feature['extent']['center_dt'] = _startdate # ToDo: Verify this
            feature['extent']['to_dt'] = _enddate

            # verify if necessary download data
            if kwargs['download']:
                logger.info(f"Downloading item: {_featureid}")
                environment.download_stac_tree(f, **kwargs)
                kwargs['basepath'] = kwargs['download_out']

            # Extract image bbox
            first_band = next(iter(collection['properties']['eo:bands']))
            first_band_path = utils.href_to_path(
                f['assets'][first_band]['href'], kwargs['basepath'])

            # build grid_spatial
            lrx, lry, ulx, uly = utils.raster_bounds(first_band_path)
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

            feature['grid_spatial']['projection']['spatial_reference'] = utils.to_wkt(crs_proj4)
            feature['image'] = OrderedDict()
            feature['image']['bands'] = OrderedDict()
            band_counter = 1
            for band in collection['properties']['eo:bands'].keys():
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
