import os
import numpy as np
import cv2
import os, glob

import glob

DIR1 = '/home/ee401_2/ferdyan_train/data/processedv4/2011_09_26_drive_0091_sync_02/'
DIR2 = '/home/ee401_2/ferdyan_train/data/processedv4/2011_09_26_drive_0001_sync_02/'

for filename in glob.glob(DIR2 + "*-fseg.png"):
    input_image = cv2.imread(filename)
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    nama = os.path.basename(filename)
    print('filename = ', nama)
    cv2.imwrite(DIR2 + nama, gray_image)
    #cv2.imwrite(OUTPUT_DIR + seqname2 + '/' + imgnum + '-fseg.png', big_img)

print('Done')
