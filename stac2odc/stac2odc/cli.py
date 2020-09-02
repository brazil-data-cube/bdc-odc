#
# This file is part of BDC-ODC.
# Copyright (C) 2020 INPE.
#
# stac2odc is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import click
import stac
import yaml

import stac2odc.item
import stac2odc.collection
import stac2odc.mapper as mapper


@click.group()
def cli():
    """
    :return:
    """
    pass


@cli.command(name="item2dataset", help="Function to convert a STAC Collection JSON to ODC Dataset YAML")
@click.option('-c', '--collection', required=True, help='Collection name (Ex. CB4MOSBR_64_3M_STK).')
@click.option('-i', '--instrument', help='Instrument type.', required=True)
@click.option('-p', '--code', help='Plataform code.', required=True)
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
@click.option('--basepath', default='/gfs', help='Repository base path')
@click.option('-o', '--outpath', default='./', help='Output path')
@click.option('--ignore', default=['quality'], help='List of bands to ignore')
@click.option('-m', '--max-items', default=None, help='Max items', required=True)
@click.option('--pre-collection', default=False, is_flag=True,
              help="Defines whether the collection belongs to the pre-collection")
@click.option('--verbose', default=False, is_flag=True, help='Enable verbose mode')
@click.option('--download', default=False, is_flag=True, help="Enable download file")
@click.option('--download-out', default="./", help="Path to download dir")
def item2dataset_cli(collection, instrument, code, format, units, url, basepath, outpath, ignore, max_items,
                     pre_collection, verbose, download, download_out):
    constants = {
        'instrument_type': instrument,
        'plataform_code': code,
        'format_name': format,
        'units': units,
        'basepath': basepath,
        'ignore': ignore,
        'outpath': outpath,
        'max_items': int(max_items),
        "is_pre_collection": pre_collection,
        'verbose': verbose,
        "download": download,
        "download_out": download_out
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    stac2odc.item.item2dataset(c, mapper.Stac2ODCMapper08(), **constants)


@cli.command(name="collection2product", help="Function to convert a STAC Collection JSON to ODC Product YAML")
@click.option('-c', '--collection', required=True, help='Collection name (Ex. CB4MOSBR_64_3M_STK).')
@click.option('-i', '--instrument', help='Instrument type.', required=True)
@click.option('-t', '--type', help='Metadata type.', required=True)
@click.option('-p', '--code', help='Platform code.', required=True)
@click.option('-f', '--format', default='GeoTiff', help='Format name')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url')
@click.option('-o', '--outfile', default=None, help='Output file')
@click.option('--ignore', default=['quality'], help='List of bands to ignore', multiple=True)
@click.option('--pre-collection', default=False, is_flag=True,
              help="Defines whether the collection belongs to the pre-collection")
@click.option('--verbose', default=False, is_flag=True, help='Enable verbose mode')
def collection2product_cli(collection, instrument, type, code, format, units, url, outfile, ignore, pre_collection,
                           verbose):
    constants = {
        'instrument_type': instrument,
        'metadata_type': type,
        'platform_code': code,
        'format_name': format,
        'units': units,
        'ignore': ignore,
        "is_pre_collection": pre_collection,
        'verbose': verbose
    }

    s = stac.STAC(url, True)
    c = s.collection(collection)
    yaml_content = stac2odc.collection.collection2product(c, mapper.Stac2ODCMapper08(), **constants)
    if outfile is None:
        print(yaml.dump(yaml_content))
    else:
        with open(outfile, 'w') as f:
            yaml.dump(yaml_content, f)
