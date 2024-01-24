import ee
from ee_jupyter.ipyleaflet import Map
import ipyleaflet as ipyl
from ipywidgets import Layout
import json
import os

# Authenticate and Initialize
def ee_initialize():
    print("Authenticating using Notebook auth...")
    if os.path.exists(ee.oauth.get_credentials_path()) is False:
        ee.Authenticate()
    else:
        print('\N{check mark} '
                'Previously created authentication credentials were found.')
        ee.Initialize()

def create_map(image,visparams,name,center=[40,110],zoom=4,basemap=ipyl.basemaps.OpenStreetMap):
    map0=Map(center=center,zoom=zoom,basemap=basemap)
    map0.addLayer(image,visparams,name)
    map0.layout=Layout(width='100%',height='600px')
    return map0

def read_china_shp():
    with open(r'../shp/china.json') as f:
        data = json.load(f)
    china=ee.FeatureCollection(data)
    return china

def print_bands(imageCollection):
    bands=imageCollection.first().bandNames().getInfo()
    for i in bands:
        print(i)

def print_size(imageCollection):
    size=imageCollection.size().getInfo()
    print(size)

def print_info(imageCollection):
    print_bands(imageCollection)
    print_size(imageCollection)