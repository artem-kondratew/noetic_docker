import cv2 as cv
import numpy as np
import time
import torch

from ultralytics import YOLO as _YOLO


class Yolo():

    def __init__(self, classes=None, model_path=None):
        self.model = _YOLO('yolov8n-seg.pt') if model_path == None else _YOLO(model_path)
        self.classes = classes if classes != None else [0]

    def ort_export(self):
        print('todo')
        return
        # if self.is_onnx:
        #     print('model is onnx: cannot export')
        #     exit(1)
        # self.model.export(format='onnx')

    def run(self, tensor : torch.Tensor):
        return self.model.predict(source=tensor, classes=self.classes, save=False)[0]
    
    def merge_masks(self, masks):
        if not masks:
            return False, None
        main_mask = masks[0].data[0].numpy() * np.uint8(255)
        for mask in masks:
            cv_mask = mask.data[0].numpy() * np.uint8(255)
            main_mask = cv.bitwise_or(main_mask, cv_mask)
        return True, main_mask


if __name__ == '__main__':
    model = Yolo(False)
    # model.ort_export()

    while True:
        st = time.time()
        result = model.run('https://ultralytics.com/images/bus.jpg')
        print(result)
        masks = result.masks
        cv_masks = []
        print(masks)
        main_mask = masks[0].data[0].numpy() * np.uint8(255)
        for mask in masks:
            cv_mask = mask.data[0].numpy() * np.uint8(255)
            main_mask = cv.bitwise_or(main_mask, cv_mask)
            # cv.imshow('img', cv_mask)
            # cv.imshow('main', main_mask)
            # cv.waitKey(500)
        ft = time.time()
        print(1 / (ft - st))
        cv.imshow('main', main_mask)
        cv.waitKey(20)
