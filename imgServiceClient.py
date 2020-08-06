"""
FileName: imgServiceClient.py
Author: Shanmukesh Vankayala
The Python implementation of the GRPC image service client.
"""

from __future__ import print_function
import logging

import cv2
import grpc


import image_pb2
import image_pb2_grpc
from imgServiceMisc import *

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = image_pb2_grpc.NLImageServiceStub(channel)
    imgSrc = cv2.imread('sample_2005.png')
    imgBytes = imgToBytes(".png", imgSrc)
    response = stub.RotateImage(image_pb2.NLImageRotateRequest(image=image_pb2.NLImage(data=imgBytes)))
    imgDst = bytesToImg(response.data)
    cv2.imwrite('temp.jpg', imgDst)
    print("Success")

if __name__ == '__main__':
    logging.basicConfig()
    run()
