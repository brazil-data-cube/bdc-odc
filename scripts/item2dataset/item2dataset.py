import stac
from collections import OrderedDict
import yaml
import click
from urllib.parse import urlparse
from osgeo import osr


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """

    def represent_dict_order(self, data): return self.represent_mapping(
        'tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


def href_to_path(href, basepath):
    url = urlparse(href)
    return "{}{}".format(basepath, url.path)


def lon_lat_2_y_x(geo_ref_points):
    def transform(p):
        return {'x': p['lon'], 'y': p['lat']}

    return {key: transform(p) for key, p in geo_ref_points.items()}


def convert_bdc_item(collection, constants):
    datasets = []
    features = collection.get_items().features
    crs_proj4 = collection['properties']['bdc:crs']
    sr = osr.SpatialReference()
    sr.ImportFromProj4(crs_proj4)
    crs_wkt = sr.ExportToWkt()

    for f in features:
        feature = OrderedDict()
        feature['id'] = f['id']
        feature['creation_dt'] = f['properties']['datetime']
        feature['product_type'] = ''
        feature['platform'] = {'code': constants['plataform_code']}
        feature['instrument'] = {'name': collection['id']}
        feature['format'] = {'name': constants['format_name']}
        feature['lineage'] = {'source_datasets:': {}}

        feature['extent'] = OrderedDict()
        feature['extent']['coord'] = OrderedDict()
        feature['extent']['coord']['ll'] = {'lat': f['geometry']['coordinates'][0][1][1],
                                            'lon': f['geometry']['coordinates'][0][1][0]}
        feature['extent']['coord']['lr'] = {'lat': f['geometry']['coordinates'][0][2][1],
                                            'lon': f['geometry']['coordinates'][0][2][0]}
        feature['extent']['coord']['ul'] = {'lat': f['geometry']['coordinates'][0][0][1],
                                            'lon': f['geometry']['coordinates'][0][0][0]}
        feature['extent']['coord']['ur'] = {'lat': f['geometry']['coordinates'][0][3][1],
                                            'lon': f['geometry']['coordinates'][0][3][0]}
        feature['extent']['from_dt'] = f['properties']['datetime']
        feature['extent']['center_dt'] = f['properties']['datetime']
        feature['extent']['to_dt'] = f['properties']['datetime']

        feature['grid_spatial'] = OrderedDict()
        feature['grid_spatial']['projection'] = OrderedDict()
        feature['grid_spatial']['projection']['geo_ref_points'] = lon_lat_2_y_x(
            feature['extent']['coord'])
        feature['grid_spatial']['projection']['spatial_reference'] = crs_wkt
        feature['image'] = OrderedDict()
        feature['image']['bands'] = OrderedDict()
        band_counter = 1
        for band in collection['properties']['bdc:bands'].keys():
            if band in f['assets']:
                feature['image']['bands'][band] = OrderedDict()
                feature['image']['bands'][band]['path'] = href_to_path(
                    f['assets'][band]['href'], constants['basepath'])
                # feature['image']['bands'][band]['type'] = ''
                feature['image']['bands'][band]['label'] = band
                feature['image']['bands'][band]['number'] = band_counter
                feature['image']['bands'][band]['cell_size'] = collection['properties']['bdc:bands'][band]['resolution_x']
                feature['image']['bands'][band]['layer'] = '1'
                band_counter += 1
            else:
                print("Band '{}' was not found in asset '{}'".format(
                    band, f['id']))
        datasets.append(yaml.dump(feature))
    return datasets


@click.command()
@click.option('-c', '--collection', required=True, help='Collection name (Ex. C4_64_16D_MED).')
@click.option('-t', '--type', default='eo', help='Metadata type.')
@click.option('-p', '--code', default='BDC', help='Plataform code.')
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
@click.option('--basepath', default='/gfs', help='Repository base path')
def main(collection, type, code, format, units, url, basepath):
    constants = {
        'metadata_type': type,
        'plataform_code': code,
        'format_name': format,
        'units': units,
        'basepath': basepath
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    yaml_content = convert_bdc_item(c, constants)
    for y in yaml_content:
        print(y)


if __name__ == '__main__':
    main()
