#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from collections import OrderedDict
from stac.collection import Collection
from stac2odc.mapper import Stac2ODCMapper


def collection2product(collection: Collection, mapper: Stac2ODCMapper, **kwargs) -> OrderedDict:
    """Function to convert a STAC Collection JSON to ODC Product YAML

    Args:
        collection (stac.collection.Collection): An Collection
        constants (dict): A dict with behavior definitions
        mapper (stac2odc.mapper.Stac2ODCMapper): An mapper to convert STAC collection to ODC Products
    See:
        See the BDC STAC catalog for more information on the collections available
        (http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/)
    """

    # ToDo: Add validators
    return mapper.map_collection(collection, **kwargs)


if __name__ == '__main__':
    import stac
    import yaml

    import stac2odc.item
    import stac2odc.collection
    from stac2odc.mapper import Stac2ODCMapper08

    constants = {
        'instrument_type': 'AWFI',
        'metadata_type': 'eo',
        'platform_code': 'CBERS04',
        'format_name': 'GeoTiff',
        'units': 'm',
        'ignore': ['quality'],
        "is_pre_collection": False,
        'verbose': True
    }
    outfile = 'test.yaml'

    s = stac.STAC('http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', True)
    c = s.collection('CB4_64_16D_STK_v1')
    yaml_content = stac2odc.collection.collection2product(c, Stac2ODCMapper08(), **constants)
    if outfile is None:
        print(yaml.dump(yaml_content))
    else:
        with open(outfile, 'w') as f:
            yaml.dump(yaml_content, f)
