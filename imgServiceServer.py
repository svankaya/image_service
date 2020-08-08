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
    
    def RotateImage(self, request, context):
        img = bytesToImg(request.image.data)
        img = rotateImg(img, request.rotation)
        imgBytes = imgToBytes(".jpg", img)
        return image_pb2.NLImage(data=imgBytes)
    
    def CustomImageEndpoint(self, request, context):
        tfServingHost= 'tf_serving_server'
        tfServingPort= '8500'
        inputTensor = 'input_1'
        outputTensor = 'dense'
        modelName = 'imgclassifier'
        
        channel = grpc.insecure_channel('{host}:{port}'.format(host=tfServingHost, port=tfServingPort))
        stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
        
        img = bytesToImg(request.image.data).astype(np.float32)
        img = cv2.resize(img, (180,180), interpolation = cv2.INTER_AREA)  
        tensor = tf.make_tensor_proto(img, shape=[1]+list(img.shape))
        
        # create request to pass to the image classifier server
        req = predict_pb2.PredictRequest()
        req.model_spec.name = modelName
        req.model_spec.signature_name = 'serving_default'
        req.inputs[inputTensor].CopyFrom(tensor)
        
        response = stub.Predict(req, 10.0)
        pred = response.outputs[outputTensor].float_val[0]
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
