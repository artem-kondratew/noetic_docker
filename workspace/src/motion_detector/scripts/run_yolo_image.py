#!/usr/bin/env python3


import numpy as np
import cv2 as cv
import time
import torch
import rospkg

import yolo
from yolo_classes import classes_list


def main():
    torch.set_num_threads(4)
    print('threads:', torch.get_num_threads())

    img_name = 'pcd.jpg'
    img_path = rospkg.RosPack().get_path('motion_detector') + '/images/' + img_name
    print(img_path)
    
    model = yolo.Yolo(classes=classes_list)

    frame = cv.imread(img_path)

    st = time.time()
    output = model.run(frame)
    success, masks = model.merge_masks(output.masks)
    if not success:
        return print('no masks')
    ft = time.time()
    print(ft - st)
    cv.imshow('frame', frame)
    cv.imshow('main_mask', masks)
    cv.waitKey(0)


if __name__ == '__main__':
    main()
