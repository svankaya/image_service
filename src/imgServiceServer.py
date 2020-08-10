'''
Filename: imgServiceServer.py
Author: Shanmukesh Vankayala
Description: The Python implementation of the GRPC image service server."""
'''

from concurrent import futures
import logging

import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

import image_pb2
import image_pb2_grpc
from imgServiceMisc import *



class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    
    def __init__(self):
        #Directory holding the machine learning model
        modelDir = "/image_service/saved_model"
        #Load the model for inference
        self.imageClassifierModel = tf.keras.models.load_model(modelDir)

    def RotateImage(self, request, context):
        #Convert byte data to image
        img = bytesToImg(request.image.data)
        #Call the rotate image function
        img = rotateImg(img, request.rotation)
        #Convert image data back to byte for transfer to client
        imgBytes = imgToBytes(".jpg", img)
        return image_pb2.NLImage(data=imgBytes)
    
    def CustomImageEndpoint(self, request, context):
        #Convert byte data to image
        img = bytesToImg(request.image.data).astype(np.float32)
        #Resize the image size to meet the input format of the machine learning model used
        img = cv2.resize(img, (180,180), interpolation = cv2.INTER_AREA)
        imgArray = tf.keras.preprocessing.image.img_to_array(img)
        #Resize the array to input tensor dimensions of the model
        imgArray = tf.expand_dims(imgArray, 0)
        #Perform inference
        prediction = self.imageClassifierModel.predict(imgArray)
        return image_pb2.NLCustomImageEndpointResponse(score=prediction[0])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    NLImageServiceObj = NLImageService()
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageServiceObj, server)
    server.add_insecure_port('[::]:80')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
