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
        imgBytes = imgToBytes(".jpg", img)
        return image_pb2.NLImage(data=imgBytes)
    
    def CustomImageEndpoint(self, request, context):
        # create prediction service client stub
        #channel = gprc.insecure_channel(FLAGS.host, int(FLAGS.port))
        GRPC_MAX_RECEIVE_MESSAGE_LENGTH = 4096 * 4096 * 3
        channel = grpc.insecure_channel('localhost:8500', options=[('grpc.max_receive_message_length', GRPC_MAX_RECEIVE_MESSAGE_LENGTH)])
        stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
        
        # create request
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'imgclassifier'
        request.model_spec.signature_name = 'serving_default'
        
        # read image into numpy array
        img = cv2.imread('1211.jpg').astype(np.float32)
        img = cv2.resize(img, (180,180), interpolation = cv2.INTER_AREA)  
        # convert to tensor proto and make request
        # shape is in NHWC (num_samples x height x width x channels) format
        tensor = tf.make_tensor_proto(img, shape=[1]+list(img.shape))
        request.inputs['input_1'].CopyFrom(tensor)
        result = stub.Predict(request, 30.0)
        pred = result.outputs['dense'].float_val[0]
        return image_pb2.NLCustomImageEndpointResponse(score=pred)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
