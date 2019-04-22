
# Copyright 2018 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

""" Offline data generation for the KITTI dataset."""

import os
from absl import app
from absl import flags
from absl import logging
import numpy as np
import cv2
import os, glob

import alignment
from alignment import compute_overlap
from alignment import align


SEQ_LENGTH = 3
WIDTH = 416
HEIGHT = 128
STEPSIZE = 1
INPUT_DIR = '/home/ee401_2/ferdyan_train/data/kitti_raw/'
OUTPUT_DIR = '/home/ee401_2/ferdyan_train/data/coba/'


def run_all():
  img1 = cv2.imread('/home/ee401_2/ferdyan_train/data/kitti_raw/2011_09_26/2011_09_26_drive_0048_sync/image_02_new/data/0000000002.png')
  img2 = cv2.imread('/home/ee401_2/ferdyan_train/data/kitti_raw/2011_09_26/2011_09_26_drive_0048_sync/image_02_new/data/0000000003.png')
  img3 = cv2.imread('/home/ee401_2/ferdyan_train/data/kitti_raw/2011_09_26/2011_09_26_drive_0048_sync/image_02_new/data/0000000004.png')

  gbr1, gbr2, gbr3 = align(img1, img2, img3, threshold_same=0.1)

  cv2.imwrite(OUTPUT_DIR + 'gbr1.png', gbr1)
  cv2.imwrite(OUTPUT_DIR + 'gbr2.png', gbr2)
  cv2.imwrite(OUTPUT_DIR + 'gbr3.png', gbr3)

  print('done')

def main(_):
  run_all()


if __name__ == '__main__':
  app.run(main)
