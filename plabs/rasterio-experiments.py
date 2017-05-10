import rasterio
import numpy as np
import matplotlib.pyplot as plt
#%%
image_file = "1056318_2017-04-15_RE3_3A.tif"

# Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
with rasterio.open(image_file) as src:
    band_red = src.read(3)
    band_green = src.read(2)
    band_blue = src.read(1)
    band_nir = src.read(4)
#%%
with rasterio.open(image_file) as src:
    band_nir = src.read(4)
#%%
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

kwargs = src.meta
kwargs.update(
    dtype=rasterio.float32,
    count = 1)

# Create the file
with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))

plt.imsave("ndvi_cmap.png", ndvi, cmap=plt.cm.summer)

#%%

plt.imsave("band_red.png", band_red.astype(float), cmap=plt.cm.summer)

#%%
scale = pow(2,8) - 1
band_red = scale*(band_red/(band_red.max() - band_red.min()))
band_green = scale*(band_green/(band_green.max() - band_green.min()))
band_blue = scale*(band_blue/(band_blue.max() - band_blue.min()))
shape = band_red.shape
rgbArray = np.zeros((l[0],l[1],3), 'uint8')
rgbArray[:,:,2] = band_red.astype('uint8')
rgbArray[:,:,1] = band_green.astype('uint8')
rgbArray[:,:,0] = band_blue.astype('uint8')
plt.imshow(rgbArray)