1) export MY_INSTALL_DIR=$HOME/.local
export PATH="$PATH:$MY_INSTALL_DIR/bin"

python -m pip install grpcio
python -m pip install grpcio-tools
python -m pip install numpy
pip install opencv-python
Python pip install tensorflow tensorflow-serving-api tf-nightly

docker pull tensorflow/serving
docker run -d -p 8500:8500 -v $(pwd)/saved_model:/models/imgclassifier -e MODEL_NAME=imgclassifier -t tensorflow/serving:latest

docker build -t img_service_server .
docker run --rm -p 50051:50051 --name img_service_server img_service_server

docker-compose up -d
