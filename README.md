 # gRPC Image Service
 ## Author
 ### [Shanmukesh Vankayala](https://www.linkedin.com/in/shanmukesh-vankayala/)
 
 ## Description
 This is a simple gRPC image service server/client application with the server being deployed on Kubernetes and the client run using a docker image. There are two services: image rotation and image classification. The image rotation service is used to rotate an image in one of the [0, 90, 180, 270] angle. An open source computer vision library [OpenCV](https://opencv.org/) has been used for processing the images. The image classification service is used to classify whether an image is a cat or dog. A pretrained [Xception network](https://keras.io/examples/vision/image_classification_from_scratch/) has been used to perform inference and classify the input images.
 
 ## Prerequisites
 The application has been tested on a machine with following os/applications and versions
 - macOS Catalina v10.15.3
 - Python v3.7.3
 - Homebrew v2.4.9 (https://brew.sh/)
 - Docker v19.03.5 (https://docs.docker.com/docker-for-mac/install/)
 - kubectl v1.18.3 (https://kubernetes.io/docs/tasks/tools/install-kubectl/)
 - virtualbox v6.1.12 (https://www.virtualbox.org/wiki/Downloads)
 - minikube v1.12.2 (https://kubernetes.io/docs/tasks/tools/install-minikube/)
 
## Instructions on setting up the gRPC Image Service
1. Ensure the system have all the required prerequisites

2. Download the grpc Image Service sources
   ```sh
   git clone https://github.com/svankaya/image_service.git
   cd image_service
   ```
3. Start a local kubernetes cluster and check the status. By default Minikube only reserves 2 CPUs and 4GB RAM.
   ```sh
   minikube addons enable metrics-server
   minikube start --extra-config kubelet.EnableCustomMetrics=true --driver=virtualbox
   minikube status
   ```
4. Deploy the gRPC image service server on the local kubernetes cluster. 
   ```sh
   kubectl apply -f kubernetes/
   ```
   The Docker image required for the deployment are already pre-built and hosted on Docker Hub. This step takes time as it has to download the image and start the required services. The status of the deployment can be discovered by running:
   ```sh
   kubectl get deployments
   kubectl get pods
   ```
   When the deployments are ready, the output will be similar to:
   ```sh
   $ kubectl get deployments
   NAME                READY   UP-TO-DATE   AVAILABLE   AGE
   server-deployment   1/1     1            1           43s
   
   $ kubectl get pods
   NAME                                READY   STATUS    RESTARTS   AGE
   server-deployment-8b57bb766-twgj5   1/1     Running   0          37s
   ```
5. Enable horizontal auto-scaling of the server using:
   ```sh
   kubectl autoscale deployment server-deployment --cpu-percent=50 --min=5 --max=10
   ```
   This will spun up upto 10 instances of the server to keep up with user demand in an elastic way. When there is less traffic the number of instances of the server are scaled down.
   
6. Get the gRPC image service client by downloading the pre-built docker image
   ```sh
   docker pull shanmukesh55/imgserviceclient:latest
   ```

## Usage
Run the gRPC image service client using: 
```sh
docker run -v $(pwd)/data:/image_service/data shanmukesh55/imgserviceclient python3 src/imgServiceClient.py --host $(minikube ip) [Arguments]
```

### Arguments
|Name|Optional|Default |Description|
|-----|--------|--------|-----------|
|```--host```| No| |serving host|
|```--port```|Yes|30100|serving port|
|```--image```|Yes|/image_service/data/dog/dog1.jpg|path to image file|
|```--service``` {0,1,2}|Yes|0|request services: 1 for image rotation, 2 for image classification, 0 for both|
|```--rotation``` {NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG}|Yes|NINETY_DEG|image rotation angle|
|```-h```, ```--help```|Yes||Shows the help message and exits|

### Examples
#### Rotate an image by ninety degress:

The host gRPC Image Service source directory is mounted to the running docker image. ***So, it is important that the input images passed as arguments should be located in the ./data directory present in the gRPC Image Service source directory. The output will be saved to ./data/output/out.jpg in the gRPC Image Service source directory***
```sh
#Run the command from the gRPC Image Service source directory 
docker run -v $(pwd)/data:/image_service/data shanmukesh55/imgserviceclient python3 src/imgServiceClient.py --host $(minikube ip) --image ./data/cat/cat10.jpg --service 1 --rotation NINETY_DEG
```
The output will be similar to:
```sh
Welcome to imgService
Loaded the ./data/cat/cat10.jpg image file successfully
Image rotation: ./data/cat/cat10.jpg is rotated succesfully and saved as ./data/output/out.jpg.
Exiting! Thank you for using the service.
```

#### Classify an image:
```sh
#Run the command from the gRPC Image Service source directory 
docker run -v $(pwd)/data:/image_service/data shanmukesh55/imgserviceclient python3 src/imgServiceClient.py --host $(minikube ip) --image ./data/cat/cat10.jpg --service 2
```
The output will be similar to:
```sh
Welcome to imgService
Loaded the ./data/cat/cat10.jpg image file successfully
Image Classification: There is a chance of 0.00 percent  for the image ./data/cat/cat10.jpg to be dog and 100.00 percent for being cat.
Exiting! Thank you for using the service.
```
## Cleanup
Run the following commands to delete the minkube Kubernetes cluster
```sh
minikube delete
```

## Limitations and further improvements
- The code is tested only for png and jpeg image formats.
- The image classifier service can give incorrect output when the input image is other than a cat or dog.
- Since only 2 CPU cores and 4GB RAM is used by Minikube, there is limitation on scaling.
- Minikube used in this work is a lightweigth Kubernetes implementation that can only be deployed on single-node. For deploying the services on a multi-node cluster, other Kubernetes implementations like MicroK8s can be used. 
- Replace use of OpenCV library on the client side. Some simple file reading library can be used for this purpose. The client side can be made further lightweight by moving all of image processing to the server side.
- The performance of the services can be futher improved by processing the images on machines having GPU. Cuda programming and Nvidia Performance Primitives(NPP) library can be used for this purpose. The machine learning model can also be further optimized using TensorRT library.
- Currently, both the services are run on a single server. These services can be set up on different servers which can be accessed by a front-end server. This make both the services loosely coupled, independently deployable, highlt maintainable and testable. 
- While transfering images between client and server, the images can be encrypted for security, compressed for improved network performance.
- NodePort service has been used in the current work which can have only one service per port and directly exposes the service to external traffic from clients. This can be replaced by load balancer or ingress which don't directly expose the services.
- Write unit test cases to make sure the code is error free
