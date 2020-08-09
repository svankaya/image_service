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
3. Start a local kubernetes cluster and check the status
   ```sh
   minikube start --driver=virtualbox
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
5. Get the gRPC image service client by downloading the pre-built docker image
   ```sh
   docker pull shanmukesh55/imgserviceclient:latest
   ```

## Usage
Run the gRPC image service client using: 
```sh
docker run -v $(pwd)/data:/image_service/data img_service_client python3 src/imgServiceClient.py --host $(minikube ip) [Arguments]
```

#### Arguments:
|Name|Optional|Default |Description|
|-----|--------|--------|-----------|
|```--host```| No| |serving host|
|```--port```|Yes|30100|serving port|
|```--image```|Yes|/image_service/data/dog/dog1.jpg|path to image file|
|```--service``` {0,1,2}|Yes|0|request services: 1 for image rotation, 2 for image classification, 0 for both|
|```--rotation``` {NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG}|Yes|NINETY_DEG|image rotation angle|
|```-h```, ```--help```|Yes||Shows the help message and exits|

#### Examples
Rotate an image by ninety degress:

The host gRPC Image Service source directory is mounted to the running docker image. ***So, it is important that the input images passed as arguments should be located in the ./data directory present in the gRPC Image Service source directory. The output will be saved to ./data/output/out.jpg in the gRPC Image Service source directory***
```sh
#Run the command from the gRPC Image Service source directory 
docker run -v $(pwd)/data:/image_service/data img_service_client python3 src/imgServiceClient.py --host $(minikube ip) --image ./data/cat/cat10.jpg --service 1 --rotation NINETY_DEG
```
The output will be similar to:
```sh
Welcome to imgService
Loaded the ./data/cat/cat10.jpg image file successfully
Image rotation: ./data/cat/cat10.jpg is rotated succesfully and saved as /image_service/data/output/out.jpg.
Exiting! Thank you for using the service.
```

Classify an image:
```sh
docker run -v $(pwd)/data:/image_service/data img_service_client python3 src/imgServiceClient.py --host $(minikube ip) --image ./data/cat/cat10.jpg --service 2
```
The output will be similar to:
```sh
Welcome to imgService
Loaded the ./data/cat/cat10.jpg image file successfully
Image Classification: There is a chance of 0.00 percent  for the image ./data/cat/cat10.jpg to be dog and 100.00 percent for being cat.
Exiting! Thank you for using the service.
```







Running the gRPC Image service server



python -m grpc_tools.protoc -I./proto/ --python_out=. --grpc_python_out=. ./proto/image.proto

microk8s kubectl create deployment imageserver --image=shanmukesh55/imgserviceserver
microk8s kubectl expose deployment imageserver --type=NodePort --port=50051
microk8s kubectl get services
microk8s  kubectl get deployments

kubectl apply -f kubernetes/

docker build -t img_service_client -f Dockerfile-client .
docker build -t img_service_server -f Dockerfile-server .

docker run -v $(pwd)/data:/image_service/data img_service_client python3 src/imgServiceClient.py --host $(minikube ip) --image ./data/dog/dog1.jpg

minikube start --driver=virtualbox
