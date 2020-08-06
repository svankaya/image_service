'''
Filename: imgServiceServer.py
Author: Shanmukesh Vankayala
Description: The Python implementation of the GRPC image service server."""
'''

from concurrent import futures
import logging

import grpc

import image_pb2
import image_pb2_grpc
from imgServiceMisc import *

def rotate_image(image):
    (h, w) = image.shape[:2]           
    center = (w / 2, h / 2)
 
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    image = cv2.warpAffine(image, M, (w, h))
    return image


class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    
    def RotateImage(self, request, context):
        img = bytesToImg(request.image.data)
        img = rotate_image(img)
        imgBytes = imgToBytes(".png", img)
        return image_pb2.NLImage(data=imgBytes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
