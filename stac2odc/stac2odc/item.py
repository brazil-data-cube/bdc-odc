#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
import yaml

from loguru import logger
from stac.collection import Collection
from stac2odc.mapper import Stac2ODCMapper

STAC_MAX_PAGE = 99999999
STAC_ITEM_PER_PAGE = 120


def item2dataset(collection: Collection, mapper: Stac2ODCMapper, **kwargs) -> None:
    """Function to convert a STAC Collection JSON to ODC Dataset YAML

    Args:
        collection (stac.collection.Collection): An Collection
        constants (dict): A dict with behavior definitions
        mapper (stac2odc.mapper.Stac2ODCMapper): An mapper to convert STAC collection to ODC Datasets
    See:
        See the BDC STAC catalog for more information on the collections available
        (http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/)
    """

    if kwargs['verbose']:
        logger.info("item2dataset is running!")

    total_items = 0
    limit = STAC_ITEM_PER_PAGE
    max_items = kwargs['max_items']

    if kwargs['verbose']:
        logger.info("Collecting information from STAC...")

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

        odc_items = mapper.map_dataset(collection, features, **kwargs)
        total_items += len(odc_items)

        if kwargs['verbose']:
            logger.info('Saving page {}'.format(page))

        for odc_item in odc_items:
            with open('{}.yaml'.format(os.path.join(kwargs['outpath'], odc_item['id'])), 'w') as _file:
                yaml.dump(odc_item, _file)

    if kwargs['verbose']:
        logger.info("Finished!")


if __name__ == '__main__':
    import stac
    import yaml

    import stac2odc.item
    import stac2odc.collection
    from stac2odc.mapper import Stac2ODCMapper08

    constants = {
        'instrument_type': 'AWFI',
        'plataform_code': 'CBERS4',
        'format_name': 'GeoTIFF',
        'units': 'm',
        'basepath': './',
        'ignore': ['quality'],
        'outpath': './',
        'max_items': 1,
        "is_pre_collection": False,
        'verbose': True,
        "download": True,
        "download_out": './'
    }

    s = stac.STAC('http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', True)
    c = s.collection('CB4_64_16D_STK_v1')
    item2dataset(c, Stac2ODCMapper08(), **constants)
