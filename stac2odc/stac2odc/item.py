import yaml
from osgeo import osr
from osgeo import gdal

import stac2odc.utils as utils

from datetime import datetime
from collections import OrderedDict


STAC_MAX_PAGE = 99999999


def item2dataset(collection, constants):
    """Function to convert a STAC Collection JSON to ODC Dataset YAML
    :param collection:
    :param constants:
    :return:
    """

    crs_proj4 = collection['properties']['bdc:crs']
    sr = osr.SpatialReference()
    sr.ImportFromProj4(crs_proj4)
    crs_wkt = sr.ExportToWkt()

    out_spatial_ref = osr.SpatialReference()
    out_spatial_ref.ImportFromProj4(crs_proj4)

    in_spatial_ref = osr.SpatialReference()
    in_spatial_ref.ImportFromEPSG(4326)  # (?)
    product_type = utils.generate_product_type(collection)

    limit = 120
    total_items = 0
    max_items = constants['max_items']

    for page in range(1, STAC_MAX_PAGE + 1):
        if max_items is not None:
            if max_items == total_items:
                break

        if limit > (max_items - total_items):
            limit = (max_items - total_items)

        features = collection.get_items(
            filter={'page': page, 'limit': limit}).features

        if len(features) == 0:
            break

        for f in features:
            _startdate, _enddate = utils.stacdate_to_odcdate(f['id'])

            feature = OrderedDict()
            feature['id'] = utils.generate_id(f)
            feature['creation_dt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%fZ")
            feature['product_type'] = product_type
            feature['platform'] = {'code': constants['plataform_code']}
            feature['instrument'] = {'name': constants['instrument_type']}
            feature['format'] = {'name': constants['format_name']}
            feature['lineage'] = {'source_datasets': {}}

            feature['extent'] = OrderedDict()
            feature['extent']['coord'] = OrderedDict()
            feature['extent']['coord']['ul'] = {'lat': f['geometry']['coordinates'][0][0][0],
                                                'lon': f['geometry']['coordinates'][0][0][1]}
            feature['extent']['coord']['ur'] = {'lat': f['geometry']['coordinates'][0][1][0],
                                                'lon': f['geometry']['coordinates'][0][1][1]}
            feature['extent']['coord']['lr'] = {'lat': f['geometry']['coordinates'][0][2][0],
                                                'lon': f['geometry']['coordinates'][0][2][1]}
            feature['extent']['coord']['ll'] = {'lat': f['geometry']['coordinates'][0][3][0],
                                                'lon': f['geometry']['coordinates'][0][3][1]}

            # :TODO: Change this
            feature['extent']['from_dt'] = _startdate
            feature['extent']['center_dt'] = _startdate  # (?)
            feature['extent']['to_dt'] = _enddate

            # Extract image bbox
            first_band = next(iter(collection['properties']['bdc:bands']))
            first_band_path = utils.href_to_path(
                f['assets'][first_band]['href'], constants['basepath'])

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
                if band not in constants['ignore']:
                    if band in f['assets']:
                        feature['image']['bands'][band] = OrderedDict()
                        feature['image']['bands'][band]['path'] = utils.href_to_path(
                            f['assets'][band]['href'], constants['basepath'])
                        feature['image']['bands'][band]['layer'] = 1
                        band_counter += 1
                    else:
                        print("Band '{}' was not found in asset '{}'".format(
                            band, f['id']))
            file_name = "{}{}.yaml".format(constants['outpath'], f['id'])
            with open(file_name, 'w') as f:
                yaml.dump(feature, f)
            total_items += 1
