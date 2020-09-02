#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from urllib.parse import urlparse

import stac2odc.utils as utils


def __download_file(url: str, out: str) -> None:
    """Download files
    Args:
        url (str): File URL
        out (str): output file
    Returns:
        None
    """
    import tqdm
    import requests

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(out, "wb") as f:
            pbar = tqdm.tqdm(ncols=100, unit_scale=True, unit="B",
                                leave=None, total=(int(r.headers['Content-Length'])))
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    pbar.update(len(chunk))
                    f.write(chunk)


def download_stac_tree(stac_item, **args):
    """Download STAC item
    
    Args:
        stac_item (dict): dict with STAC item informations
        **args (dict): dict with user's definition.
    See:
        Check CLI definition to know possible args
    """

    # Generate stac tree in basepath
    _keys = list(stac_item['assets'].keys())
    basepath_repository = utils.href_to_path(os.path.dirname(stac_item['assets'][_keys[0]]['href']),
                                                                                                args['download_out'])
    os.makedirs(basepath_repository, exist_ok=True)

    for key in stac_item['assets']:
        asset = stac_item['assets'][key]
        assetpath = urlparse(asset['href']).path
        __download_file(asset['href'], os.path.join(basepath_repository, os.path.basename(assetpath)))
