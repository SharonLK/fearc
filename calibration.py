import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
import time


# get config's json
def get_json():
    with open('./config.json', 'r') as f2:
        data = f2.read()
    config = json.loads(str(data))
    return config


# get video capture from config
config = get_json()
cap = cv2.VideoCapture(config['video_path'])

# read first frame
ret, frame = cap.read()
height , width ,_ = frame.shape
plt.figure(0)
plt.axis("off")
plt.imshow(frame)
dt=np.dtype('float32')
destination_points = np.array([[0, 0],[width - 1, 0],[width - 1, height - 1],[0, height - 1]], dt)
input_points = plt.ginput(4)
print(destination_points)
print(input_points)
source_points = np.array(input_points,dtype=dt)
print(source_points)
tform = cv2.getPerspectiveTransform(source_points ,destination_points )
print(tform)
warped = cv2.warpPerspective(frame, tform, (width , height ))
plt.figure(1)
plt.imshow(warped)
plt.show()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
