import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import pydicom as di
import copy
import cv2
from os import walk, mkdir, path
from tkinter import messagebox


root = tk.Tk()
root.title('DICOM Extractor v2 GUI')
root.geometry('350x350')
root.resizable(False, False)
try:
    root.iconbitmap('./LogoSolid64.ico')
except Exception as e:
    print(e)

folder_path = tk.StringVar()
same_folder = tk.StringVar()

pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=200
)

pb_sub = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=200
)

class guiText:
    def __init__(self):
        self.usageTitle = '使用方式: '
        self.usageS1 = '1. 選擇DICOM檔案存放路徑'
        self.usageS2 = '2. 選擇是否將結果集中於同一個資料夾'
        self.selBtn = '選擇路徑'
        self.fireBtn = '開始'
        self.pbLabel = '全部進度'
        self.pb_subLabel = '各項進度'
        self.sel2Rad1 = '是! 集中存放'
        self.sel2Rad2 = '否! 分開存放'
        self.emptyText = ''
    

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
        self.samefolder = True
        self.Files = []
        self.Frames = []
    

class dicomExtracter:
    def __init__(self):
        self.SINGLE_FRAME = False
        self.IMG_FRAME = [[]]
        self.FRAME_COUNT = 0
        self.DIR_PATH = ''
        
        
de = mainParameters()

def browse_button(fireBtn):
    global de
    global folder_path
    filename = tk.filedialog.askdirectory()
    folder_path.set(filename)
    de.path = filename
    
    if(de.path):
        fireBtn['state'] = tk.NORMAL
    else:
        fireBtn['state'] = tk.DISABLED
        
    
def select_Radio(fireBtn):
    global de
    global same_folder
    de.samefolder = same_folder.get()

    
def fetchFile(p):
    result = [path.join(dp, f) for dp, dn, filenames in walk(p) for f in filenames]
    return result
    #return next(walk(p), (None, None, []))[2]

def enumFiles(fname, fpath, sf):
    global pb_sub
    global root
    
    print('Processing file: '+str(fname))
    try:
        dsFile = di.read_file(fname)
        
    except Exception as e:
        #print(e)
        print('File \"'+fname+'\" is not a valid DICOM file type, skipped...')
        return
    
    dicomFile = dicomExtracter()
    
    additionalPath = fname.replace(fpath, '')
    
    if(sf == True):
        dicomFile.DIR_PATH = fpath+'\\Extract_'
    else:
        dirname = ''
        for apindex, ap in enumerate(additionalPath.split('/')):
            dirname += str(ap)+'_'
            
        dicomFile.DIR_PATH = fpath+'\\EX'+str(dirname)
    
    #create root folder
    dupIndex = 0
    while(path.exists(dicomFile.DIR_PATH) and not sf):
        dicomFile.DIR_PATH += '_'+str(dupIndex)
    
    #print(dicomFile.DIR_PATH)
    
    if(not path.exists(dicomFile.DIR_PATH)):
        mkdir(dicomFile.DIR_PATH)
    
    #Check if is single or multi frame
    try:
        #if(dsFile.pixel_array.shape[3] == 3):
        if(len(dsFile.pixel_array[0][0][0]) == 3):
            dicomFile.SINGLE_FRAME = False
            dicomFile.FRAME_COUNT = dsFile.pixel_array.shape[0]
            dicomFile.IMG_FRAME = copy.deepcopy(dsFile.pixel_array)
            
    except Exception as e:
        dicomFile.SINGLE_FRAME = True
        dicomFile.FRAME_COUNT = 1
        dicomFile.IMG_FRAME[0] = dsFile.pixel_array
        #return
    #Convert to RGB if is rgb
    pb_sub['value'] = 0
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
            fullFname = ''
            
            for apindex, ap in enumerate(additionalPath.split('/')):
                fullFname += str(ap)+'_'
            
            fullFname += str(idx)
            fullFname = dicomFile.DIR_PATH + '\\'+str(fullFname)
        else:
            fullFname = dicomFile.DIR_PATH + '\\frame_'+str(idx)
            
                
        cv2.imwrite(str(fullFname)+'.jpg', img)
        pb_sub['value'] = ((idx+1) / dicomFile.FRAME_COUNT * 100)
        root.update() 
        


def guiAction():
    global de
    global root
    global folder_path
    global same_folder
    global pb
    global pb_sub
    
    gt = guiText()
    
    
    pbLabel = tk.Label(master=root, text=gt.pbLabel)
    pbLabel.grid(row=6, column=0, sticky="W")
    pb.grid(row=7, column=0, sticky="W")
    
    pb_subLabel = tk.Label(master=root, text=gt.pb_subLabel)
    pb_subLabel.grid(row=8, column=0, sticky="W")
    pb_sub.grid(row=9, column=0, sticky="W")
    
    
    mainEmpty = tk.Label(master=root, text=gt.emptyText)
    mainEmpty.grid(row=10, column=0, sticky="W")
    
    fireBtn = tk.Button(text=gt.fireBtn, command=main, state=tk.DISABLED, width=20)
    fireBtn.grid(row=11, column=0, columnspan=2)

    usageTitle = tk.Label(master=root, text=gt.usageTitle)
    usageTitle.grid(row=0, column=0, sticky="W")
    usageS1 = tk.Label(master=root, text=gt.usageS1)
    usageS1.grid(row=1, column=0, sticky="W")

    selBtn = tk.Button(text=gt.selBtn, command=lambda: browse_button(fireBtn))
    selBtn.grid(row=1, column=1)
    selFolder = tk.Label(master=root, textvariable=folder_path, wraplength=300)
    selFolder.grid(row=2, column=0, columnspan=2)

    usageS2 = tk.Label(master=root, text=gt.usageS2)
    usageS2.grid(row=3, column=0, sticky="W")
    
    sel2Rad1 = tk.Radiobutton(master=root, text=gt.sel2Rad1, value=True, var=same_folder
                              , command=lambda: select_Radio(fireBtn))
    sel2Rad1.deselect()
    sel2Rad1.grid(row=4, column=0, sticky="W")
    
    sel2Rad2 = tk.Radiobutton(master=root, text=gt.sel2Rad2, value=False, var=same_folder
                              , command=lambda: select_Radio(fireBtn))
    sel2Rad2.select()
    sel2Rad2.grid(row=4, column=1, sticky="W")
    
    same_folder.set(True)
    
    root.mainloop()

def main():
    global de
    global folder_path
    global same_folder
    global pb
    global root
    
    
    if(not de.path):
        return
    
    ct = cliText()
    
    print(ct.parSet+'PATH= '+str(de.path)) 
    print(ct.parSet+'SAMEFOLDER= '+str(de.samefolder))
    
    de.Files = fetchFile(de.path)
    
    pb['value'] = 0
    for i,f in enumerate(de.Files):
        pb['value'] = (i+1) / len(de.Files) * 100
        root.update()
        
        f = f.replace("\\", "/")
        enumFiles(f, de.path, de.samefolder)
    cv2.destroyAllWindows()
    messagebox.showinfo("Message", "Process Finished")
    return

if __name__ == '__main__':
    print("Started")
    guiAction()
    print("Exited")
else:
    print(__name__)

