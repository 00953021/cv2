import cv2
import numpy as np

filename = "balls-red-blue-yellow-green.jpg"

greenBGR = np.uint8([[[0,255,0]]])
print(cv2.cvtColor(greenBGR, cv2.COLOR_BGR2HSV))

image = cv2.imread(filename)
cv2.imshow('IMAGE', image)

frame = image.copy()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# lower & upper bound for Red color
lower_bound = np.array([  0,  90,  90])
upper_bound = np.array([ 10, 255, 255])

# lower & upper bound for Yellow color
#lower_bound = np.array([ 20,  90,  90])
#upper_bound = np.array([ 40, 255, 255])

# lower & upper bound for Green color
#lower_bound = np.array([ 50,  90,  90])
#upper_bound = np.array([100, 255, 255])

# lower & upper bound for Blue color
#lower_bound = np.array([100,  90,  90])
#upper_bound = np.array([120, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)
cv2.imshow('MASK', mask)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame, frame, mask=mask)
cv2.imshow('RESULT', res)

# Find Contours
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw All Contours
frame = image.copy()
cv2.drawContours(frame, contours, -1, (0,255,0), 3)
cv2.imshow('CONTOURS', frame)

# Finding The Largest Contour
contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
#frame = image.copy()
#cv2.drawContours(frame, biggest_contour, -1, (0,255,0), 3)
#cv2.imshow('OBJECT', frame)

# Bounding Rectangle
x,y,w,h = cv2.boundingRect(biggest_contour)
print(x,y,w,h)
frame = image.copy()
cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow('B-BOX', frame)


cv2.waitKey(0)
cv2.destroyAllWindows()
