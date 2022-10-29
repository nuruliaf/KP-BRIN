from osgeo import gdal
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
from numpy import genfromtxt
import tifffile

input_file = "clipped.tif"
output_file = "op"

ds = gdal.Open(input_file, gdal.GA_ReadOnly)
img_width,img_height=ds.RasterXSize,ds.RasterYSize
print(img_width)
print(img_height)

#Convert GeoTIFF to CSV with GDAL
# xyz = gdal.Translate("S1A_IW.xyz", ds)
# xyz = None

# df = pd.read_csv("S1A_IW.xyz", sep = " ", header = None)
# df.columns = ["x", "y", "value"]
# df.to_csv("S1A_IW.csv", index = False)

#CSV to GeoTIFF
ar1 = ds.GetRasterBand(1).ReadAsArray()
flat1 = ar1.flatten()
ar2 = ds.GetRasterBand(2).ReadAsArray()
flat2 = ar2.flatten()
ar3 = ds.GetRasterBand(3).ReadAsArray()
flat3 = ar3.flatten()
gt = ds.GetGeoTransform()
res = gt[1]
xmin = gt[0]
ymax = gt[3]
xsize = ds.RasterXSize
ysize = ds.RasterYSize
xstart = xmin +res/2
ystart = ymax - res/2
ds = None

x = np.arange(xstart, xstart+xsize*res, res)
y = np.arange(ystart, ystart-ysize*res, -res)
x = np.tile(x, ysize)
y = np.repeat(y, xsize)

#dfn = pd.DataFrame({"x": x, "y": y, "nilai_r": flat1, "nilai_g": flat1, "nilai_b": flat3})
dfn = pd.DataFrame({"nilai_r": flat1, "nilai_g": flat2, "nilai_b": flat3})

dfn.to_csv(output_file + ".csv", index = False, header = None, sep = " ")
#demn = gdal.Translate("demn.tif", "S1A_IW.xyz", outputSRS = "EPSG:32719")
#demn = None

#def toTIFF(dfn, name):
#    dfn.to_csv(name+".xyz", index = False, header = None, sep = " ")
#    demn = gdal.Translate(name+".tif", name+".xyz", outputSRS = "EPSG:32719", xRes = res, yRes = -res, bandList=(1,2,3))
#    demn = None
    
#shuffle = dfn.sample(frac = 1)
#shuffle = shuffle.sort_values(by = ["y", "x"], ascending = [False, True])
#toTIFF(shuffle, "shuffle")

#sample = dfn.sample(frac = 0.1)
#sample = sample.sort_values(by = ["y", "x"], ascending = [False, True])
#toTIFF(sample, "sample")

#uneven = sample.copy()
#uneven.x = uneven.x + np.random.randint(6, size = len(uneven))
#uneven.y = uneven.y + np.random.randint(6, size = len(uneven))

#silakan edit dimensi H, W disini
#disini H = 263, W=200, sedang isinya 3 nilai R, G dan B
image = np.zeros((img_height,img_width,3), np.float64)
#ingin W dan H tanpa perlu input nilai manual
#image = np.zeros((ysize,xsize,3), np.uint8) 
#tapi masih menemukan error 'index 643 is out of bounds for axis 0 with size 643'
ctrx = 0
ctry = 0
f = open(output_file + '.csv','r')
for row in f:
    #print(row)
    row1 = row.split(' ')
    r = float(row1[0])
    g = float(row1[1])
    b = float(row1[2])
    #RGBint = (r<<16) + (g<<8) + b
    image[ctry, ctrx] = [r, g, b]
    #print(RGBint)
    #image[ctrx, ctry] = RGBint
    ctrx = ctrx + 1
    if ctrx == img_width:
        ctrx = 0
        ctry = ctry +1
#image1 = Image.fromarray(image).convert('RGB')
#Image.fromarray(image).save(output_file + '.tif')
tifffile.imwrite(output_file + '.tif', image)