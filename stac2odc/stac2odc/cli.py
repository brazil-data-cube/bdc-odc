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
@click.option('-c', '--collection', required=True, help='Collection name (Ex. C4_64_16D_MED).')
@click.option('-t', '--type', default='eo', help='Metadata type.')
@click.option('-p', '--code', default='BDC', help='Plataform code.')
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
@click.option('--basepath', default='/gfs', help='Repository base path')
@click.option('-o', '--outpath', default='./', help='Output path')
@click.option('-i', '--ignore', default=['quality'], help='List of bands to ignore')
@click.option('-m', '--max_items', default=None, help='Max items')
def item2dataset_cli(collection, type, code, format, units, url, basepath, outpath, ignore, max_items):
    constants = {
        'metadata_type': type,
        'plataform_code': code,
        'format_name': format,
        'units': units,
        'basepath': basepath,
        'ignore': ignore,
        'outpath': outpath,
        'max_items': int(max_items)
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    stac2odc.item.item2dataset(c, constants)


@cli.command(name = "collection2product", help = "Function to convert a STAC Collection JSON to ODC Product YAML")
@click.option('-c', '--collection', required=True, help='Collection name (Ex. C4_64_16D_MED).')
@click.option('-t', '--type', default='eo', help='Metadata type.')
@click.option('-p', '--code', default='BDC', help='Platform code.')
@click.option('-f', '--format', default='GeoTiff', help='Format name.')
@click.option('--units', default='1', help='Units.')
@click.option('--url', default='http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0/', help='BDC STAC url.')
@click.option('-o', '--outfile', default=None, help='Output file')
@click.option('-i', '--ignore', default=['quality'], help='List of bands to ignore')
def collection2product_cli(collection, type, code, format, units, url, outfile, ignore):
    constants = {
        'metadata_type': type,
        'platform_code': code,
        'format_name': format,
        'units': units,
        'ignore': ignore
    }
    s = stac.STAC(url, True)
    c = s.collection(collection)
    yaml_content = stac2odc.collection.collection2product(c, constants)
    if outfile is None:
        print(yaml.dump(yaml_content))
    else:
        with open(outfile, 'w') as f:
            yaml.dump(yaml_content, f)
