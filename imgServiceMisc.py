#Filename: imgServiceMisc.py
#Author: Shanmukesh Vankayala
#Description: Code contains helper or miscellaneous functions

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


