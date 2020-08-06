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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import cv2
import numpy as np
import grpc


import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    #response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='sample_2005.png'))
    #print("Greeter client received: " + response.message)
    image = cv2.imread('sample_2005.png')
    is_success, im_buf_arr = cv2.imencode(".png", image)
    byte_im = im_buf_arr.tobytes()
    response = stub.SayHelloAgain(helloworld_pb2.ImgRequest(data=byte_im))
    nparr = np.fromstring(response.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('temp.jpg', image)
    print("Sucess")

if __name__ == '__main__':
    logging.basicConfig()
    run()
