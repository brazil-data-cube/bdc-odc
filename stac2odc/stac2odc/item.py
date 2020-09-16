#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from loguru import logger
from stac2odc.mapper import Stac2ODCMapper

STAC_MAX_PAGE = 99999999
STAC_ITEM_PER_PAGE = 120


def item2dataset(stacservice, item_filter, mapper: Stac2ODCMapper, **kwargs) -> None:
    """Function to convert a STAC Collection JSON to ODC Dataset YAML

    Args:
        stacservice (stac.collection.Collection): An Collection
        item_filter (dict): A dict with behavior definitions
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
        if max_items is not None and max_items == total_items:
            break

        if limit > (max_items - total_items):
            limit = (max_items - total_items)

        collection = stacservice.collection(item_filter["collections"][0])
        features = stacservice.search({
            **item_filter, **{"page": page, "limit": limit}
        }).features

        if len(features) == 0:
            break

        # Multiple dataset is ignored!
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
    from stac2odc.mapper import Stac2ODCMapper09

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

    # stacservice, item_filter, mapper: Stac2ODCMapper, **kwargs
    s = stac.STAC('http://brazildatacube.dpi.inpe.br/stac/', False)
    item2dataset(s, {'collections': ['CB4_64_16D_STK-1']}, Stac2ODCMapper09(), **constants)
