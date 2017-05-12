import os
import requests
from requests.auth import HTTPBasicAuth
import json
from osgeo import gdal
# our demo filter that filters by geometry, date and cloud cover
from demo_filters import redding_reservoir

API_KEY='3d42933f4c284a3b8dd2c5200e97da00'
#%%
# Stats API request object
stats_endpoint_request = {
  "interval": "day",
  "item_types": ['REOrthoTile'], #["REOrthoTile"],
  "filter": redding_reservoir
}
# fire off the POST request
result = \
  requests.post(
    'https://api.planet.com/data/v1/stats',
    auth=HTTPBasicAuth(API_KEY, ''),
    json=stats_endpoint_request)

print(result.text)
#%%
search_endpoint_request = {
  "item_types": ["PSOrthoTile"], #REOrthoTile
  "filter": redding_reservoir
}

result = \
  requests.post(
    'https://api.planet.com/data/v1/quick-search',
    auth=HTTPBasicAuth(API_KEY, ''),
    json=search_endpoint_request)
#To download sometimes the permissions are not aviable. Permisions have to be checked
results = json.loads(result.text)
link = results['features'][5]['_links']['thumbnail']
print(link)

#%%
#Downloads the entire image
asset_path = results['features'][5]['_links']['assets']

# setup auth
session = requests.Session()
session.auth = (API_KEY, '')

# request an item
item = session.get(asset_path)#("https://api.planet.com/data/v1/item-types/{}/items/{}/assets/").format(item_type, item_id))

# extract the activation url from the item for the desired asset
item_activation_url = item.json()['analytic']["_links"]["activate"]

# request activation
response = session.post(item_activation_url)

print(response.status_code)
#%%
#Download the Area of Interest (AOI)
item_id = results['features'][5]['id']
asset_type = 'visual'
asset_path = results['features'][5]['_links']['assets']

# Request a new download URL
result = requests.get(asset_path, auth=HTTPBasicAuth(API_KEY, ''))
download_url = result.json()[asset_type]['location']
vsicurl_url = '/vsicurl/' + download_url
output_file = item_id + '_' + asset_type + '_subarea.tif'

# GDAL Warp crops the image by our AOI, and saves it
err = gdal.Warp(output_file, vsicurl_url, dstSRS = 'EPSG:4326', cutlineDSName = 'subarea.json', cropToCutline = True)