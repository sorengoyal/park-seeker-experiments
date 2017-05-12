#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:10:54 2017

@author: soren
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import json
from osgeo import gdal
# our demo filter that filters by geometry, date and cloud cover
from filters import my_filter
import rasterio
import numpy as np
import matplotlib.pyplot as plt
API_KEY='3d42933f4c284a3b8dd2c5200e97da00'
session = requests.Session()
session.auth = (API_KEY, '')
#%%
search_request = {
  "interval": "day",
  "item_types": ['PSOrthoTile'], #["REOrthoTile"],
  "filter": my_filter
}
result = session.post('https://api.planet.com/data/v1/stats',json=search_request)
num_of_results = len(result.json()['buckets'])
if( num_of_results == 0):
    print('No results available')
    quit()

print('Found ' + str(num_of_results) + ' results')
#%%
res = session.post('https://api.planet.com/data/v1/quick-search',json=search_request)
#To download sometimes the permissions are not aviable. Permisions have to be checked
res_json = res.json()
for item in res_json['features']:
    if(len(item['_permissions']) != 0 ):
        result = item
thumb = session.get(result['_links']['thumbnail'])
thumb_file = result['id'] + '_thumb.png'
with open(thumb_file, 'wb') as file:
    file.write(thumb.content)
    print('Donwloaded Thumbnail:' + thumb_file)
asset_link = result['_links']['assets']
item_id = result['id']
#%%
item = session.get(asset_link)
response = session.post(item.json()['analytic']['_links']['activate'])
if(response.status_code == 202):
    print('Analytic asset activation request posted')
elif(response.status_code == 204):
    print('Analytic asset is ready for download')
response = session.post(item.json()['visual']['_links']['activate'])
if(response.status_code == 202):
    print('Visual asset activation request posted')
elif(response.status_code == 204):
    print('Visual asset is ready for download')
#%%
#Download the Area of Interest (AOI) from the analytic asset
asset_type = 'analytic'

# Request a new download URL
result = session.get(asset_link)
download_url = result.json()[asset_type]['location']
vsicurl_url = '/vsicurl/' + download_url
output_file = item_id + '_' + asset_type + '_subarea.tif'
# GDAL Warp crops the image by our AOI, and saves it
err = gdal.Warp(output_file, vsicurl_url, dstSRS = 'EPSG:4326', cutlineDSName = 'subarea.json', cropToCutline = True)
print("Downloaded image of subarea:" + output_file)

