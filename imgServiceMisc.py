'''
Filename: imgServiceMisc.py
Author: Shanmukesh Vankayala
Description: Code contains helper or miscellaneous functions
'''

import cv2
import numpy as np 


#Code converts OpenCV images to bytes
def imgToBytes(imgFormat, img):
    isSuccess, imgBuffer = cv2.imencode(imgFormat, img)
    imgBytes = imgBuffer.tobytes()
    return imgBytes

def bytesToImg(imgBytes):
    npBuffer = np.frombuffer(imgBytes, np.uint8)
    img = cv2.imdecode(npBuffer, cv2.IMREAD_COLOR)
    return img

def rotateImg(img, rotationAngle):
    angle = [0, 90, 180, 270]
    (height, width) = img.shape[:2]           
    center = (width / 2, height / 2)
    rotationMatrix = cv2.getRotationMatrix2D(center, angle[rotationAngle], 1.0)
    img = cv2.warpAffine(img, rotationMatrix, (width, height))
    return img


