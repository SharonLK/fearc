import cv2
import json
import numpy as np
def get_json():
    with open('./config.json', 'r') as f2:
        data = f2.read()
    config = json.loads(str(data))
    return config

lower_limits = {'green':np.array([90,0,0]),'blue':np.array([110,50,50]), 'orange':np.array([5, 50, 50],np.uint8)}
upper_limits = {'green':np.array([130,255,255]),'blue':np.array([130,255,255]),'orange':np.array([15, 255, 255],np.uint8)}

def find_mask(frame,color,lower_limits,upper_limits):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = lower_limits[color]
    upper = upper_limits[color]
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    return mask

def find_largest_object(img,mask):
    _, contours, hier = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    (x, y, w, h) = cv2.boundingRect(biggest_contour)
    img=cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 5)
    # for cnt in contours:
    #     if 500 < cv2.contourArea(cnt) < 5000000:
    #         (x, y, w, h) = cv2.boundingRect(cnt)

    cv2.imshow('IMG', img)

config = get_json()
cap = cv2.VideoCapture(config['video_path'])
ret, frame = cap.read()

while frame is not None:
    mask = find_mask(frame,'orange',lower_limits,upper_limits)
    find_largest_object(frame,mask)
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Capture frame-by-frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
