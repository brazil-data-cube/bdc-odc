import click
import stac
import yaml

import stac2odc.item
import stac2odc.collection


@click.group()
def cli():
    """
    :return:
    """
    pass


@cli.command(name = "item2dataset", help = "Function to convert a STAC Collection JSON to ODC Dataset YAML")
@click.option('-c', '--collection', required=True, help='Collection name (Ex. CB4MOSBR_64_3M_STK).')
@click.option('-i', '--instrument', help='Instrument type.', required=True)
@click.option('-p', '--code', help='Plataform code.', required=True)
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
@click.option('--basepath', default='/gfs', help='Repository base path')
@click.option('-o', '--outpath', default='./', help='Output path')
@click.option('-q', '--quality-ignore', default=['quality'], help='List of bands to ignore')
@click.option('-m', '--max-items', default=None, help='Max items')
def item2dataset_cli(collection, instrument, code, format, units, url, basepath, outpath, quality_ignore, max_items):
    constants = {
        'instrument_type': instrument,
        'plataform_code': code,
        'format_name': format,
        'units': units,
        'basepath': basepath,
        'ignore': quality_ignore,
        'outpath': outpath,
        'max_items': int(max_items)
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    stac2odc.item.item2dataset(c, constants)


@cli.command(name = "collection2product", help = "Function to convert a STAC Collection JSON to ODC Product YAML")
@click.option('-c', '--collection', required=True, help='Collection name (Ex. CB4MOSBR_64_3M_STK).')
@click.option('-i', '--instrument', help='Instrument type.', required=True)
@click.option('-t', '--type', help='Metadata type.', required = True)
@click.option('-p', '--code', help='Platform code.', required = True)
@click.option('-f', '--format', default='GeoTiff', help='Format name')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url')
@click.option('-o', '--outfile', default=None, help='Output file')
@click.option('-q', '--quality-ignore', default=['quality'], help='List of bands to ignore')
def collection2product_cli(collection, instrument, type, code, format, units, url, outfile, quality_ignore):
    constants = {
        'instrument_type': instrument,
        'metadata_type': type,
        'platform_code': code,
        'format_name': format,
        'units': units,
        'ignore': quality_ignore
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    yaml_content = stac2odc.collection.collection2product(c, constants)
    if outfile is None:
        print(yaml.dump(yaml_content))
    else:
        with open(outfile, 'w') as f:
            yaml.dump(yaml_content, f)
