import cv2
import json
import numpy as np
def get_json():
    with open('./config.json', 'r') as f2:
        data = f2.read()
    config = json.loads(str(data))
    return config

lower_limits = {'green':np.array([50,100,100]),'blue':np.array([110,50,50])}
upper_limits = {'green':np.array([70,255,255]),'blue':np.array([130,255,255])}

def find_color(color,lower_limits,upper_limits):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = lower_limits[color]
    upper = upper_limits[color]
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

config = get_json()
cap = cv2.VideoCapture(config['video_path'])
ret, frame = cap.read()

while frame is not None:
    find_color(frame,'green',lower_limits,upper_limits)
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Capture frame-by-frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
