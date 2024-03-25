#!/usr/bin/env python3


import cv2 as cv
import numpy as np
import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from yolo import Yolo
from yolo_classes import classes_list


bridge = CvBridge()

model = Yolo(classes=classes_list)

mask_pub = rospy.Publisher('/mask', Image, queue_size=10)


def callback(msg):
    cv_frame = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    output = model.run(cv_frame)
    success, masks = model.merge_masks(output.masks)
    if not success:
        masks = np.zeros(cv_frame.shape, dtype='uint8')
        print('no masks')
    mask_msg = bridge.cv2_to_imgmsg(masks, encoding='passthrough')
    mask_pub.publish(mask_msg)
    
    cv.imshow('main_mask', masks)
    cv.imshow('frame', cv_frame)
    cv.waitKey(20)


def fake_callback(msg):
    cv_frame = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')   
    h, w = cv_frame.shape[:2]
    copy = np.copy(cv_frame)
    cv.circle(copy, (w // 2, h // 2), 20, (255, 0, 255), -1)
    mask_msg = bridge.cv2_to_imgmsg(copy, encoding='passthrough')
    mask_pub.publish(mask_msg)


def main():
    rospy.init_node('motion_detector')
    rospy.loginfo('Node has been started')

    # rospy.Subscriber('/image_raw', Image, callback)
    rospy.Subscriber('/image_raw', Image, fake_callback)

    rospy.spin()


if __name__ == '__main__':
    main()
