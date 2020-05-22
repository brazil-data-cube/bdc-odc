#!/bin/env python3
import stac
from collections import OrderedDict
import yaml
import click


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """

    def represent_dict_order(self, data): return self.represent_mapping(
        'tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


def convert_bdc_collection(collection, constants):

    product_type = "{}_{}_{}".format(
        collection['properties']['bdc:temporal_composition']['schema'],
        collection['properties']['bdc:temporal_composition']['step'],
        collection['properties']['bdc:temporal_composition']['unit'])

    odc_config = OrderedDict()
    odc_config['name'] = collection['id']
    odc_config['description'] = collection['description']
    odc_config['metadata_type'] = constants['metadata_type']

    odc_config['storage'] = OrderedDict()
    odc_config['storage']['crs'] = collection['properties']['bdc:crs']
    odc_config['storage']['resolution'] = OrderedDict()
    first_band = next(iter(collection['properties']['bdc:bands']))
    odc_config['storage']['resolution']['x'] = collection['properties']['bdc:bands'][first_band]['resolution_x']
    odc_config['storage']['resolution']['y'] = collection['properties']['bdc:bands'][first_band]['resolution_y']

    def measurements(data):
        m = OrderedDict()
        m['name'] = data['name']
        m['aliases'] = [data['name'], ]
        m['dtype'] = data['data_type']
        m['nodata'] = data['fill']
        m['units'] = constants['units']
        return m

    odc_config['metadata'] = OrderedDict()
    odc_config['metadata']['plataform'] = {'code': constants['plataform_code']}
    odc_config['metadata']['instrument'] = {'name': collection['id']}
    odc_config['metadata']['product_type'] = product_type
    odc_config['metadata']['format'] = {'name': constants['format_name']}
    odc_config['metadata']['measurements'] = [measurements(v)
                                              for k, v in collection['properties']['bdc:bands'].items()]
    return yaml.dump(odc_config)  # default_flow_style=None


@click.command()
@click.option('-c', '--collection', required=True, help='Collection name (Ex. C4_64_16D_MED).')
@click.option('-t', '--type', default='eo', help='Metadata type.')
@click.option('-p', '--code', default='BDC', help='Plataform code.')
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
def main(collection, type, code, format, units, url):
    constants = {
        'metadata_type': type,
        'plataform_code': code,
        'format_name': format,
        'units': units
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    yaml_content = convert_bdc_collection(c, constants)
    print(yaml_content)


if __name__ == '__main__':
    main()
