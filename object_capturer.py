import cv2
import json
import numpy as np
import time
import os.path
import pickle

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
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        # read first frame
        ret, self.frame = self.cap.read()
        self.fgmask = self.fgbg.apply(self.frame)
        
        self.height , self.width ,_ = self.frame.shape
        self.is_calibrated = os.path.exists("calibrationCache.pkl")
        if self.is_calibrated:
            with open(r"calibrationCache.pkl", "rb") as calibration_file:
                self.tform = pickle.load(calibration_file)

    def get_locations(self):
        if self.is_calibrated:
            self.frame = cv2.warpPerspective(self.frame, self.tform, (self.width, self.height))

        # splitting images to left and right
        # (left, right) = self.split_image(self.frame)

        # find mask of color
        # left_mask = self.find_mask(left, 'orange', lower_limits, upper_limits)
        # right_mask = self.find_mask(right, 'orange', lower_limits, upper_limits)
        left_mask, right_mask = self.split_image(self.fgmask)

        # find largest object bounding box in each half
        point_left , left_final = self.find_largest_object(left, left_mask)
        point_right , right_final = self.find_largest_object(right, right_mask)
        point_right = (point_right[0] , point_right[1] + self.width/2 )
        # putting images back together
        final_frame = np.concatenate((left_final, right_final), axis=1)

        # show frame
        cv2.imshow('video', final_frame)
        cv2.waitKey(1)
        ret, self.frame = self.cap.read()
        self.fgmask = self.fgbg.apply(self.fgmask)

        self.is_video_done = self.frame is None
        return point_left , point_right

    def close_capturer(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    objectCapturer = objectCapturer()
    while not objectCapturer.is_video_done:
        pointL , pointR = objectCapturer.get_locations()



    # When everything done, release the capture

