import os
import cv2
import numpy

os.system('sudo fswebcam -d /dev/video0 ~/photo1.jpg')
os.system('sudo fswebcam -d /dev/video1 ~/photo2.jpg')

image1 = cv2.imread('~/photo1.jpg')
image2 = cv2.imread('~/photo2.jpg')

#BGR colour values of cube faces
colorBoundaries = [
    ([], []), #red
    ([], []), #blue
    ([], []), #green
    ([], []), #white
    ([], []), #yellow
    ([], [])  #orange
]

for (lower, upper) in colorBoundaries:
    lower = numpy.array(lower, dtype = "uint8")
    upper = numpy.array(upper, dtype = "uint8")
    
    #use mask to extract colors
    mask1 = cv2.inRange(image1, lower, upper)
    mask2 = cv2.inRange(image2, lower, upper)
    
    output1 = cv2.bitwise_and(image1, image1, mask = mask1)
    output2 = cv2.bitwise_and(image2, image2, mask = mask2)
    
    cv2.imshow("images", numpy.hstack([image1, output1]))
    cv2.waitkey(0)
    
    cv2.imshow("images", numpy.hstack([image2, output2]))
