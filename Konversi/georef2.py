################## USING GDAL #####################
import shutil
from osgeo import gdal, osr

orig_fn = 'clipped.tif'
output_fn = 'ini.tif'

# Create a copy of the original file and save it as the output filename:
shutil.copy(orig_fn, output_fn)
# Open the output file for writing for writing:
ds = gdal.Open(output_fn, gdal.GA_Update)
# Set spatial reference:
sr = osr.SpatialReference()
sr.ImportFromEPSG(4326) #4326 refers to the clipped.tif, but can use any desired projection

# Enter the GCPs (Ground Control Point)
#   Format: [map x-coordinate(longitude)], [map y-coordinate (latitude)], [elevation],
#   [image column index(x)], [image row index (y)]
gcps = [gdal.GCP(108.267000, -6.425000, 0),
gdal.GCP(108.254300, -6423000, 0),
gdal.GCP(108.294000, -6.420000,0)]

# Apply the GCPs to the open output file:
ds.SetGCPs(gcps, sr.ExportToWkt())

# Close the output file in order to be able to work with it in other programs:
ds = None