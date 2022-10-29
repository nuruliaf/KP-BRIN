################## USING RASTERIO #####################
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

img = rasterio.open('clipped.tif')
show(img)
#X and Y are supposed to be latitude and longitude if you have the right metadata

full_img = img.read()  #Note the 3 bands and shape of image

# # result
# # clipped.tif
# # X=542; Y=326; Bands=3

#To find out number of bands in an image
num_bands = img.count
print("Number of bands in the image = ", num_bands)

#To find out x and y size in an image
img_x = img.width
img_y = img.height
print("X size:", img_x, "\nY size:", img_y)

img_band1 = img.read(1) #1 stands for 1st band. 
img_band2 = img.read(2) #2 stands for 2nd band. 
img_band3 = img.read(3) #3 stands for 3rd band. 

# #To get 'pink' from different band 
# fig = plt.figure(figsize=(10,10))
# ax1 = fig.add_subplot(2,2,1)
# ax1.imshow(img_band1, cmap='pink')
# ax2 = fig.add_subplot(2,2,2)
# ax2.imshow(img_band2, cmap='pink')
# ax3 = fig.add_subplot(2,2,3)
# ax3.imshow(img_band3, cmap='pink')

fig, (axr, axg, axb) = plt.subplots(1,3, figsize=(21,7))
show((img, 1), ax=axr, cmap='Reds', title='red channel')
show((img, 2), ax=axg, cmap='Greens', title='green channel')
show((img, 3), ax=axb, cmap='Blues', title='blue channel')
plt.show()

#To find out the coordinate reference system
print("Coordinate reference system:", img.crs)

#Read description, if any
desc = img.descriptions
print('Raster description: {desc}'.format(desc=desc))

# Read metadata
metadata = img.meta
print('Metadata:\n{metadata}'.format(metadata=metadata))

#To find out geo transform
print("Geotransform:\n",img.transform)

# Plot pixel value histogram in each band. 
rasterio.plot.show_hist(full_img, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histogram")
#Peak at 255 is pixels with no data, outside region of interest.

fig, (axrgb, axhist) = plt.subplots(1, 2, figsize=(14,7))
show(full_img, ax=axrgb)
rasterio.plot.show_hist(full_img, bins=50, histtype='stepfilled', lw=0.0, stacked=False, alpha=0.3, ax=axhist)
plt.show()

#format clipped_image = full_image[(all bands), (rasio xpixel), (rasio ypixel)]
clipped_img = full_img[:, 100:100, 100:100]
#get inside in the region of clipped_img
plt.imshow(clipped_img[0,:,:])
#get histogram from clipped_img
rasterio.plot.show_hist(clipped_img, bins=50, histtype='stepfilled', lw=0.0, stacked=False, alpha=0.3)
# Each band showing slightly different information

################ NDVI - normalized difference vegetation index ############
# NDVI = (NIR-Red)/(NIR+Red)

#Let us assume 1 is red and 2 is NIR
red_clipped = img[0].astype('f4')
nir_clipped = img[1].astype('f4')
ndvi_clipped = (nir_clipped - red_clipped) / (nir_clipped + red_clipped)

# Return Runtime warning about dividing by zero as we have some pixels with value 0.
# So let us use numpy to do this math and replace inf / nan with some value. 

import numpy as np
ndvi_clipped2 = np.divide(np.subtract(nir_clipped, red_clipped), np.add(nir_clipped, red_clipped))
ndvi_clipped3 = np.nan_to_num(ndvi_clipped2, nan=-1)
plt.imshow(ndvi_clipped3, cmap='viridis')
plt.colorbar()
#Some times each band is available as seperate images
#Data from here: https://landsatonaws.com/L8/042/034/LC08_L1TP_042034_20180619_20180703_01_T1
#Band 4 = Red, Band 5: NIR

red = rasterio.open('clipped.tif')
#Extract image as a smaller size... 
red_img = red.read(1, out_shape=(1, int(red.height // 2), int(red.width // 2)))
plt.imshow(red_img, cmap='viridis')
plt.colorbar()
#Extract smaller region, otherwise when we do NDVI math we divide by 0 where there is no data
red_img = red_img[100:300, 100:300]
plt.imshow(red_img, cmap='viridis')
plt.colorbar()

nir = rasterio.open('clipped.tif')
nir_img = nir.read(1, out_shape=(1, int(nir.height // 2), int(nir.width // 2)))
nir_img = nir_img[100:300, 100:300]

plt.imshow(nir_img, cmap='viridis')
plt.colorbar()

#Convert int to float as we will be doing math
red_img_float = red_img.astype('f4') #Float 32
nir_img_float = nir_img.astype('f4')

ndvi = (nir_img_float - red_img_float) / (nir_img_float + red_img_float)
plt.imshow(ndvi, cmap='viridis')
plt.colorbar()


##########################################################


############# USING GDAL ##############
# from osgeo import gdal
# import matplotlib.pyplot as plt

# input_file = "clipped.tif"
# ds = gdal.Open(input_file)

# #print basic raster info
# print("X size:", ds.RasterXSize,"\nY size:", ds.RasterYSize)
# print("Number of raster bands:", ds.RasterCount)
# print("Geo transform:", ds.GetGeoTransform())
# print("Projection info:", ds.GetProjection())

# #print raster band info
# band1 = ds.GetRasterBand(1)
# print("\nNo data value:", band1.GetNoDataValue())
# print("Min value:", band1.GetMinimum())
# print("Max value:", band1.GetMaximum())
# print("Data type:", band1.GetUnitType())