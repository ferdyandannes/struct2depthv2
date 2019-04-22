import os
import numpy as np
import cv2
import os, glob

import glob

#DIR1 = '/home/ee401_2/ferdyan_train/data/kitti_one_fix/2011_09_26_drive_0014_sync_02/'
#DIR1 = '/home/ee401_2/ferdyan_train/data/kitti_one_fix/2011_09_26_drive_0014_sync_03/'
#DIR1 = '/home/ee401_2/ferdyan_train/data/kitti_one_fix/2011_09_26_drive_0015_sync_02/'
#DIR1 = '/home/ee401_2/ferdyan_train/data/kitti_one_fix/2011_09_26_drive_0015_sync_03/'
DIR1 = '/home/ee401_2/ferdyan_train/data/he/2011_09_26_drive_0015_sync_03/'

for filename in glob.glob(DIR1 + "*-fseg.png"):
    input_image = cv2.imread(filename)
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    nama = os.path.basename(filename)
    print('filename = ', nama)

    img_size = gray_image.shape
    height = img_size[0]
    width = img_size[1]

    for i in range(height):
    	for j in range(width):
    		if gray_image[i,j] != 0 :
    			gray_image[i,j] = 175
    		else :
    			gray_image[i, j] = 0

    cv2.imwrite(DIR1 + nama, gray_image)
    #cv2.imwrite(OUTPUT_DIR + seqname2 + '/' + imgnum + '-fseg.png', big_img)

print('Done')
