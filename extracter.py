import pydicom as di

from pydicom.data import get_testdata_files

import numpy as np
import cv2
import matplotlib.pyplot as plt


# 讀取 DICOM 檔案
PATH0 = '002221667H\\EXAM000\\IMG001'
#PATH0 = '002615637G\\EXAM000\\'
#PATH0 = '003028385D\\EXAM000\\'
ds = di.read_file(PATH0)

# 列出所有後設資料（metadata）
#ds.decompress('pillow')
#print(ds)
print((ds.PatientName).decode('big5'))
print(ds.pixel_array.shape)
#print(ds.pixel_array[0][0][0])

try:
    if(ds.pixel_array[3]):
        print('multi frame')
        img = ds.pixel_array[0]
except:
    print('Error')
#for i in range(33):
set1 = ds.pixel_array[0]
print(set1[0][0])
set2 = cv2.cvtColor(set1, cv2.COLOR_YCR_CB2BGR)
plt.imshow(set2)
plt.show()