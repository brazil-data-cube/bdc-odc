from ipyleaflet import WMSLayer, Map, basemaps, Polygon
from functools import partial
import pyproj
from shapely.ops import transform
import shapely
from datacube.api.core import get_bounds
from ipywidgets import Layout


def bdc_plot_datasets(datasets, zoom = 4, layout=Layout(width='600px', height='600px')):
    """Plot Dataset tiles
    """
    
    bbox = get_bounds(datasets, datasets[0].crs)
    bbox_pol = shapely.wkt.loads(bbox.wkt)

    project = partial(
        pyproj.transform,
        pyproj.Proj(datasets[0].crs.crs_str),
        pyproj.Proj(init='epsg:4674'))
    bbox_pol_wgs84 = transform(project, bbox_pol)
    bbox = bbox_pol_wgs84.bounds
    
    center = ((bbox[1] + bbox[3])/2, 
              (bbox[0] + bbox[2])/2)

    m = Map(basemap=basemaps.Esri.WorldImagery, center=center, zoom=zoom, layout=layout)
    grid = WMSLayer(url='http://brazildatacube.dpi.inpe.br/bdc/geoserver/grids/ows', 
                    layers='BDC_GRID', 
                    styles='tiles', 
                    format='image/png', 
                    transparent=True,
                    tile_size=512)
    m.add_layer(grid)
    
    if len(datasets):
        project = partial(
                pyproj.transform,
                pyproj.Proj(datasets[0].crs.crs_str),
                pyproj.Proj(init='epsg:4674'))

        plotted = []
        for ds in datasets:
            idt = "{},{};{},{}".format(ds.metadata.lon[0],ds.metadata.lat[0],ds.metadata.lon[1],ds.metadata.lat[1])
            if idt not in plotted:
                plotted.append(idt)
                # apply projection
                ds_pol = transform(project, shapely.wkt.loads(ds.extent.wkt))  
                x,y = ds_pol.exterior.xy
                points = [(y1,x1) for x1,y1 in zip(x,y)]
                polygon = Polygon(
                    locations=points,
                    color="#0033CC",
                    fill_color="#388b8b",
                    weight=2,
                    fill_opacity=.6
                )
                m.add_layer(polygon);
    return m
