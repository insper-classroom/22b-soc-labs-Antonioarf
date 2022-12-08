import os 
print('antes')
#os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save frame.jpg') # uses Fswebcam to take picture
import cv2
cam = cv2.VideoCapture(0)
s, f = cam.read()
cv2.imwrite('frame.jpeg',f)
print('passou')
