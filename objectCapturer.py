import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\Chen\PycharmProjects\fearc\video\vid1.mp4')
ret, frame = cap.read()

while frame is not None:

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capture frame-by-frame
    ret, frame = cap.read()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()