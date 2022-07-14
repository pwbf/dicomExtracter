import pydicom as di
import numpy as np
import cv2
from pydicom.data import get_testdata_files
from os import walk, mkdir, path


class cliText:
    def __init__(self):
        self.askPath = '輸入存放DICOM的資料夾路徑: '
        self.askSamefolder = '是否要將輸出結果集合於同一資料夾 (y,n)? '
        self.askPathEr = '路徑無效或是目錄不存在'
        self.askSamefolderEr = '無效輸入，Y or N?'
        self.parSet = '變數已設定-> '
    
class mainParameters:
    def __init__(self):
        self.path = ''
        self.samefolder = False
        self.Files = []
        self.Frames = []
    

class dicomExtracter:
    def __init__(self):
        self.SINGLE_FRAME = False
        self.IMG_FRAME = [np.ndarray([])]
        self.FRAME_COUNT = 0
        self.DIR_PATH = ''
        
        
def fetchFile(path):
    return next(walk(path), (None, None, []))[2]

def enumFiles(fname, fpath, sf):
    print('Processing file: '+str(fname))
    dsFile = di.read_file(fpath+'\\'+fname)
    dicomFile = dicomExtracter()

    if(sf):
        dicomFile.DIR_PATH = fpath+'\\Extract_'
    else:
        dicomFile.DIR_PATH = fpath+'\\EX_'+str(fname.split('.')[0])
    
    #create root folder
    dupIndex = 0
    while(path.exists(dicomFile.DIR_PATH) and not sf):
        dicomFile.DIR_PATH += '_'+str(dupIndex)
    
    #print(dicomFile.DIR_PATH)
    
    if(not path.exists(dicomFile.DIR_PATH)):
        mkdir(dicomFile.DIR_PATH)
    
        
    #Check if is single or multi frame
    try:
        if(dsFile.pixel_array.shape[3] == 3):
            #print('multi frame')
            dicomFile.SINGLE_FRAME = False
            dicomFile.FRAME_COUNT = dsFile.pixel_array.shape[0]
            dicomFile.IMG_FRAME = np.copy(dsFile.pixel_array)
            
    except Exception as e:
        #if(dsFile.pixel_array.shape[2] == 3):
        #print('single frame')
        dicomFile.SINGLE_FRAME = True
        dicomFile.FRAME_COUNT = 1
        dicomFile.IMG_FRAME[0] = np.copy(dsFile.pixel_array)
        #print('Error: '+str(e))
        
    #Convert to RGB if is rgb
    for idx in range(dicomFile.FRAME_COUNT):
        #Check file is RGB
        if(dsFile[0x28,0x04].value == 'RGB'):
            img = dicomFile.IMG_FRAME[idx]
        elif(dsFile[0x28,0x04].value == 'YBR_FULL_422'):
            img = cv2.cvtColor(dicomFile.IMG_FRAME[idx], cv2.COLOR_YCR_CB2BGR)
        else:
            img = cv2.cvtColor(dicomFile.IMG_FRAME[idx], cv2.COLOR_GRAY2RGB)
        
        cv2.imshow('Processing Frame', img)
        cv2.waitKey(10)
        
        if(sf):
            fullFname = dicomFile.DIR_PATH + '\\'+fname+'_'+str(idx)+'.jpg'
        else:
            fullFname = dicomFile.DIR_PATH + '\\frame'+str(idx)+'.jpg'
            
        cv2.imwrite(fullFname, img)
        



def main():
    ct = cliText()
    de = mainParameters()
    
    de.path = input(ct.askPath)
    
    while(not path.exists(de.path)):
        print(ct.askPathEr)
        de.path = input(ct.askPath)
    
    print(ct.parSet+'PATH= '+str(de.path))
    
    sf = input(ct.askSamefolder)
    while( sf.upper() != 'Y' and sf.upper() != 'N' ):
        print(ct.askSamefolderEr)
        sf = input(ct.askSamefolder)
        
        
    if(sf.upper() == 'Y'):
        de.sf = True  
    else:
        de.sf = False  
        
    print(ct.parSet+'SAMEFOLDER= '+str(de.sf))
    
    de.Files = fetchFile(de.path)
    
    for f in de.Files:
        #try:
            enumFiles(f, de.path, de.sf)
        #except Exception as e:
            #print(e)
           # print('File \"'+f+'\" is not a valid DICOM file type, skipped...')
            #continue
        #cv2.destroyAllWindows()
    return 0

if __name__ == '__main__':
    main()
    print("Finished")
else:
    print(__name__)