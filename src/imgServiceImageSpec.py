"""
FileName: imgServiceImageSpec.py
Author: Shanmukesh Vankayala
Description: Class file for the image.
"""

from __future__ import print_function
import logging
from imgServiceMisc import *
import sys

class imageSpecs:
    def getHeight(self):
        self.height = self.img.shape[0]

    def getWidth(self):
        self.width = self.img.shape[1]
    
    def getChannels(self):
        try:
            self.channels = self.img.shape[2]
        except:
            self.channels = 1

        try:
            if(self.channels !=1 and self.channels !=3):
                raise Exception
        except:
            print("Expecting only a single channel or a 3 channel RGB image. Exiting")
            sys.exit(1)
        
    def chkImgSize(self):
        try:
            maxMsgLength = 4096*4096*3
            if(self.channels*self.height*self.width > maxMsgLength):
                raise Exception
        except:
            print("Image size is beyond the limits of 4096*4096*3. Exiting")
            sys.exit(1)

    def getColor(self):
        if(self.channels == 3):
            self.color = True
        else:
            self.color = False
    
    def convertToBytes(self):
        self.imgBytes = imgToBytes(".jpg", self.img)

    def __init__(self, img):
        self.img = img
        self.getHeight()
        self.getWidth()
        self.getChannels()
        self.chkImgSize()
        self.getColor()
        self.convertToBytes()
