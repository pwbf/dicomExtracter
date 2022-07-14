import pydicom as di

from pydicom.data import get_testdata_files

import numpy as np
import cv2
import matplotlib.pyplot as plt


# 讀取 DICOM 檔案
PATH0 = '002221667H\\EXAM000\\IMG023'
#PATH0 = '002615637G\\EXAM000\\IMG001'
#PATH0 = '003028385D\\EXAM000\\'
ds = di.read_file(PATH0)

# 列出所有後設資料（metadata）
#ds.decompress('pillow')
print(ds)
print("Name: " + str((ds.PatientName).decode('big5')))
print("shape: " + str(ds.pixel_array.shape))
print("get_pixeldata: " + str(di.pixel_data_handlers.numpy_handler.get_pixeldata(ds, False)))
print("needs_to_convert_to_RGB: " + str(di.pixel_data_handlers.numpy_handler.needs_to_convert_to_RGB(ds)))
print("should_change_PhotometricInterpretation_to_RGB: " + str(di.pixel_data_handlers.numpy_handler.should_change_PhotometricInterpretation_to_RGB(ds)))
print("Photometric Interpretation: "+str(ds[0x28, 0x4].value))
#print(ds.pixel_array[0][0][0])

#for i in range(33):
set1 = ds.pixel_array
print(set1[0][0])
plt.imshow(set1)
plt.show()