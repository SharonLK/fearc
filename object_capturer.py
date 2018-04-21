import cv2
import json

with open('./config.json', 'r') as f2:
    data = f2.read()
config = json.loads(str(data))

cap = cv2.VideoCapture(config['video_path'])
ret, frame = cap.read()

while frame is not None:

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capture frame-by-frame
    ret, frame = cap.read()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
