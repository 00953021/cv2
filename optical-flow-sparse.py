# Blog: [OpenCV Optical Flow介紹](https://meetonfriday.com/posts/e2795e5a/)
import sys
import cv2
import numpy as np

# argv 
if len(sys.argv)>1:
    if sys.argv[1].isdigit():
        cap = cv2.VideoCapture(int(sys.argv[1]))
    else:
        cap = cv2.VideoCapture(sys.argv[1])
else:
    cap = cv2.VideoCapture('video/MOT16-03-raw.webm')
   
# Parameters for Shi-Tomasi corner detection
#feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
feature_params = dict(maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7)
# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0,255,(300,3)) # Create some random colors
ret, old_frame = cap.read()
prev_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
prev = cv2.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
mask = np.zeros_like(old_frame)

while(cap.isOpened()):
    ret, frame = cap.read() # capture a frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to Gray	
    next, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

    good_old = prev[status == 1] # Selects good feature points for previous position
    good_new = next[status == 1] # Selects good feature points for next position
    # Draws the optical flow tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel() # Returns a contiguous flattened array as (x, y) coordinates for new point
        c, d = old.ravel() # Returns a contiguous flattened array as (x, y) coordinates for old point
        mask  = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
    img = cv2.add(frame, mask)
    prev_gray = gray.copy()
    prev = good_new.reshape(-1, 1, 2)
    cv2.imshow("optical-flow sparse", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
