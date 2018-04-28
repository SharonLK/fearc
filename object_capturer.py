import cv2
import json
import numpy as np
import time

# define colors spectrums
lower_limits = {'green':np.array([90,0,0]),'blue':np.array([110,50,50]), 'orange':np.array([5, 50, 50],np.uint8)}
upper_limits = {'green':np.array([130,255,255]),'blue':np.array([130,255,255]),'orange':np.array([15, 255, 255],np.uint8)}

# get config's json
def get_json():
    with open('./config.json', 'r') as f2:
        data = f2.read()
    config = json.loads(str(data))
    return config

# split images to left and right
def split_image(image):
    width=image.shape[1]
    half_width = width // 2
    image1 = image[:,0:half_width]
    image2 = image[:,half_width:]
    return (image1 , image2)

# find color mask in frame
def find_mask(frame,color,lower_limits,upper_limits):
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
def find_largest_object(img,mask):
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
    img=cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 5)
    return img

# get video capture from config
config = get_json()
cap = cv2.VideoCapture(config['video_path'])

# read first frame
ret, frame = cap.read()

while frame is not None:

    # splitting images to left and right
    (left,right) = split_image(frame)

    # find mask of color
    left_mask = find_mask(left,'orange',lower_limits,upper_limits)
    right_mask = find_mask(right, 'orange', lower_limits, upper_limits)

    # find largest object bounding box in each half
    left_final = find_largest_object(left,left_mask)
    right_final = find_largest_object(right, right_mask)

    # putting images back together
    final_frame = np.concatenate((left_final , right_final ), axis=1)

    # show frame
    cv2.imshow('video', final_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capture next frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
