import stac2odc.utils as utils

from collections import OrderedDict


def collection2product(collection, constants):
    """Function to convert a STAC Collection JSON to ODC Product YAML
    """

    product_type = utils.generate_product_type(collection)

    odc_config = OrderedDict()
    odc_config['name'] = collection['id']
    odc_config['description'] = collection['description']
    odc_config['metadata_type'] = constants['metadata_type']

    odc_config['storage'] = OrderedDict()
    odc_config['storage']['crs'] = collection['properties']['bdc:crs']
    odc_config['storage']['resolution'] = OrderedDict()
    first_band = next(iter(collection['properties']['bdc:bands']))
    odc_config['storage']['resolution']['x'] = int(
        collection['properties']['bdc:bands'][first_band]['resolution_x'])
    odc_config['storage']['resolution']['y'] = int(
        collection['properties']['bdc:bands'][first_band]['resolution_y']) * -1

    def measurements(tag, data):
        m = OrderedDict()
        m['name'] = tag # data['name']
        m['aliases'] = [data['name'], ]
        m['dtype'] = data['data_type'].lower()
        m['nodata'] = data['fill']
        m['units'] = constants['units']
        return m

    odc_config['metadata'] = OrderedDict()
    odc_config['metadata']['platform'] = {'code': constants['platform_code']}
    odc_config['metadata']['instrument'] = {'name': constants['instrument_type']}
    odc_config['metadata']['product_type'] = product_type
    odc_config['metadata']['format'] = {'name': constants['format_name']}
    odc_config['measurements'] = [measurements(k, v)
                                  for k, v in collection['properties']['bdc:bands'].items() if k not in constants['ignore']]
    return odc_config  # default_flow_style=None
