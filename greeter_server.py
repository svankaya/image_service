# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
import cv2
import numpy as np

def rotate_image(image):
    (h, w) = image.shape[:2]           
    center = (w / 2, h / 2)
 
    M = cv2.getRotationMatrix2D(center, 150, 1.0)
    image = cv2.warpAffine(image, M, (w, h))
    return image


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
    
    def SayHelloAgain(self, request, context):
        #image = cv2.imread(request.name)
        nparr = np.fromstring(request.data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #image = cv2.resize(shm_image, (640, 540), interpolation=cv2.INTER_AREA)
        image = rotate_image(image)
        is_success, im_buf_arr = cv2.imencode(".png", image)
        byte_im = im_buf_arr.tobytes()
        #cv2.imwrite('temp.jpg', image)
        return helloworld_pb2.ImgReply(data=byte_im)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
