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
parser.add_argument('--host', required='True', help='serving host')
parser.add_argument('--port', default='30100', help='inception serving port')
parser.add_argument('--image', default='/image_service/data/dog/dog1.jpg', 
        help='path to image file')
parser.add_argument('--service', default='0', choices=['0', '1', '2'], 
        help='request services: 1 for image rotation, 2 for image classification, 0 for both')
parser.add_argument('--rotation', default='NONE', 
        choices=['NONE', 'NINETY_DEG', 'ONE_EIGHTY_DEG', 'TWO_SEVENTY_DEG'], 
        help='image rotation angle')
_args = parser.parse_args()

class imgServiceOperations:
    def rotateImage(self):
        if(_args.service!='0' and _args.service!='1'):
                return
        response = self.stub.RotateImage(
                image_pb2.NLImageRotateRequest(
                    rotation = _args.rotation,
                    image=image_pb2.NLImage(
                        color=self.imgSpecs.color,
                        data=self.imgSpecs.imgBytes,
                        width=self.imgSpecs.width,
                        height=self.imgSpecs.height)))
        imgDst = bytesToImg(response.data)
        outputFile = '/image_service/data/output/out.jpg'
        cv2.imwrite(outputFile, imgDst)
        print("Image rotation: %s is rotated succesfully and saved as ./data/output/out.jpg." 
                %(_args.image))

    def imageClassifier(self):
        if(_args.service!='0' and _args.service!='2'):
                return
        response = self.stub.CustomImageEndpoint(
                image_pb2.NLCustomImageEndpointRequest(
                    image=image_pb2.NLImage(
                        color=self.imgSpecs.color,
                        data=self.imgSpecs.imgBytes,
                        width=self.imgSpecs.width,
                        height=self.imgSpecs.height)))
        print("Image Classification: There is a chance of %.2f percent " %(100*response.score) + 
                " for the image %s to be dog and %.2f percent for being cat."
         % (_args.image, 100 * (1-response.score)))

    def __init__(self, stub, imgSpecs):
        self.stub = stub
        self.imgSpecs = imgSpecs
    

def run():
    print("Welcome to imgService")
    channel = grpc.insecure_channel('{host}:{port}'.format(host=_args.host, port=_args.port))
    stub = image_pb2_grpc.NLImageServiceStub(channel)
    
    imgSrc = cv2.imread(_args.image)
    try:
        if (imgSrc is None):
            raise Exception
    except:
        print("Error loading the image file")
        sys.exit(1)
    else:
        print("Loaded the %s image file successfully" %_args.image)

    imgSrcSpecs = imageSpecs(imgSrc)
    imgServices = imgServiceOperations(stub, imgSrcSpecs)
    imgServices.rotateImage();
    imgServices.imageClassifier();
    print("Exiting! Thank you for using the service.")

if __name__ == '__main__':
    logging.basicConfig()
    run()
