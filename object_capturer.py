import sys
from pong.game_better import Pong
import cv2
import json
import numpy as np
import time
import os.path
import pickle
import pygame
import random

DEBUG = False

# define colors spectrums
lower_limits = {'green':np.array([90,0,0]),'blue':np.array([110,50,50]), 'orange':np.array([5, 50, 50],np.uint8)}
upper_limits = {'green':np.array([130,255,255]),'blue':np.array([130,255,255]),'orange':np.array([15, 255, 255],np.uint8)}
class objectCapturer:


    # get config's json
    def get_json(self):
        with open('./config.json', 'r') as f2:
            data = f2.read()
        config = json.loads(str(data))
        return config

    # split images to left and right
    @staticmethod
    def split_image(image):
        width=image.shape[1]
        half_width = width // 2
        image1 = image[:,0:half_width]
        image2 = image[:,half_width:]
        return (image1 , image2)

    @staticmethod
    def get_hue(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue = hsv[:, :, 0]
        return hue

    @staticmethod
    def get_hue_mask(image1,image2):
        hue1 = objectCapturer.get_hue(image1)
        hue2 = objectCapturer.get_hue(image2)
        hue_diff = cv2.absdiff(hue1, hue2)
        _, mask = cv2.threshold(hue_diff, 30, 255, cv2.THRESH_BINARY)
        return mask

    # find color mask in frame
    def find_mask(self,frame,color,lower_limits,upper_limits):
        # t0 = time.time()

        # convert color to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define lower and upper limits
        lower = lower_limits[color]
        upper = upper_limits[color]

        # create mask by limits
        mask = cv2.inRange(hsv, lower, upper)

        # t1 = time.time()
        # print(t1-t0)

        # old unused code
        # res = cv2.bitwise_and(frame, frame, mask=mask)
        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        return mask

    # find largest object in image, currently shows it above img
    def find_largest_object(self,img,mask):
        # t0 = time.time()

        # find all objects in mask
        _, contours, hier = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # create list of tuples of sizes and objects
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

        # choose biggest counter
        if len(contour_sizes) == 0:
            return None, img
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # find bounding box
        (x, y, w, h) = cv2.boundingRect(biggest_contour)

        # t1 = time.time()
        # print(t1-t0)

        # add rectabgle above image

        point = int(x + w/2) , int(y + h/2)
        img=cv2.line(img, point, point, (0,255,0), 5)
        return point , img

    def __init__(self):
        # get video capture from config
        config = self.get_json()
        self.cap = cv2.VideoCapture(config['video_path'])
        self.is_video_done = False
        # read first frame
        ret, self.frame = self.cap.read()
        self.full_first_frame = self.frame
        
        self.height , self.width ,_ = self.frame.shape
        self.is_calibrated = os.path.exists("calibrationCache.pkl")
        if self.is_calibrated:
            with open(r"calibrationCache.pkl", "rb") as calibration_file:
                self.tform = pickle.load(calibration_file)

        self.first_frame = self.frame
        self.calibrated_width, self.calibrated_height = 0, 0

    def get_locations(self):
        mask_full = objectCapturer.get_hue_mask(self.full_first_frame,self.frame)
        if self.is_calibrated:
            self.frame = cv2.warpPerspective(self.frame, self.tform, (self.width, self.height))
            self.calibrated_height, self.calibrated_width, _ = self.frame.shape
            mask_calibrated = cv2.warpPerspective(mask_full, self.tform, (self.width, self.height))
            if DEBUG:
                cv2.imshow('mask_calibrated', mask_calibrated)
                cv2.waitKey(1)
        else:
            mask_calibrated = mask_full
        (left_mask, right_mask) = self.split_image(mask_calibrated)

        # # splitting images to left and right
        (left, right) = self.split_image(self.frame)
        #
        # # find mask of color
        # # left_mask = self.find_mask(left, 'orange', lower_limits, upper_limits)
        # # right_mask = self.find_mask(right, 'orange', lower_limits, upper_limits)
        # mask = objectCapturer.get_hue_mask(self.first_frame,self.frame)
        # (left_mask,right_mask) = self.split_image(mask)
        # cv2.imshow('maskleft', mask)
        # cv2.waitKey(1)
        #
        # # find largest object bounding box in each half
        point_left, left_final = self.find_largest_object(left, left_mask)
        point_right, right_final = self.find_largest_object(right, right_mask)
        if point_right is not None:
            point_right = (point_right[0] + self.width/2, point_right[1])
        # putting images back together
        final_frame = np.concatenate((left_final, right_final), axis=1)

        # show frame
        if DEBUG:
            cv2.imshow('video', final_frame)
            cv2.waitKey(1)
        ret, self.frame = self.cap.read()
        self.is_video_done = self.frame is None
        return point_left , point_right

    def close_capturer(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    objectCapturer = objectCapturer()

    pong = Pong()

    while not objectCapturer.is_video_done:
        pointL , pointR = objectCapturer.get_locations()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if pointL is not None:
            pong.pad1_pos.center = (pong.pad1_pos.center[0], pointL[1])
        if pointR is not None:
            pong.pad2_pos.center = (pong.pad2_pos.center[0], pointR[1])

        pong.update()
        pong.draw()
        pygame.display.update()

        # pong.FPS_CLOCK.tick(60)
