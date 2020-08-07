"""
FileName: imgServiceClient.py
Author: Shanmukesh Vankayala
The Python implementation of the GRPC image service client.
"""

from __future__ import print_function
import logging

import cv2
import grpc
import sys
import argparse
import image_pb2
import image_pb2_grpc
from imgServiceMisc import *
from imgServiceImageSpec import imageSpecs

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='0.0.0.0', help='serving host')
parser.add_argument('--port', default='9000', help='inception serving port')
parser.add_argument('--image', default='', help='path to image file')
parser.add_argument('--rotation', default='NONE', choices=['NONE', 'NINETY_DEG', 'ONE_EIGHTY_DEG', 'TWO_SEVENTY_DEG'], help='image rotation angle')
_args = parser.parse_args()

class imgServiceOperations:
    def rotateImage(self):
        response = self.stub.RotateImage(
                image_pb2.NLImageRotateRequest(
                    rotation = _args.rotation,
                    image=image_pb2.NLImage(
                        color=self.imgSpecs.color,
                        data=self.imgSpecs.imgBytes,
                        width=self.imgSpecs.width,
                        height=self.imgSpecs.height)))
        imgDst = bytesToImg(response.data)
        cv2.imwrite('temp.jpg', imgDst)

    def imageClassifier(self):
        response = self.stub.CustomImageEndpoint(
                image_pb2.NLCustomImageEndpointRequest(
                    image=image_pb2.NLImage(
                        color=self.imgSpecs.color,
                        data=self.imgSpecs.imgBytes,
                        width=self.imgSpecs.width,
                        height=self.imgSpecs.height)))
        print("This image is %.2f percent dog."% ( 100 * response.score))

    def __init__(self, stub, imgSpecs):
        self.stub = stub
        self.imgSpecs = imgSpecs
    

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = image_pb2_grpc.NLImageServiceStub(channel)
    
    imgSrc = cv2.imread(_args.image)
    try:
        if (imgSrc is None):
            raise Exception
    except:
        print("Error loading the image file")
        sys.exit(1)
    else:
        print("Loaded the image file successfully")

    imgSrcSpecs = imageSpecs(imgSrc)
    imgServices = imgServiceOperations(stub, imgSrcSpecs)
    imgServices.rotateImage();
    imgServices.imageClassifier();
    print("Success")

if __name__ == '__main__':
    logging.basicConfig()
    run()
