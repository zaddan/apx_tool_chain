import numpy as np
from PIL import Image
from PIL import ImageFile
import math 
ImageFile.LOAD_TRUNCATED_IMAGES = True
import itertools
#imageName = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/lena_cropped.bmp"
#imageName = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/roki_320_240.ppm"
imageName = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/west_1_bu.ppm"


im = Image.open(imageName)
print im.size[0]
print im.size[1]


#list2d =[[23,6,7], [3,5], [6,7], [8]]
#b = list(itertools.chain(*list2d))
#print b
