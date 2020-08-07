1) export MY_INSTALL_DIR=$HOME/.local
export PATH="$PATH:$MY_INSTALL_DIR/bin"

python -m pip install grpcio
python -m pip install grpcio-tools
python -m pip install numpy
pip install opencv-python
Python pip install tensorflow tensorflow-serving-api tf-nightly

docker run -d -p 8500:8500 -v $(pwd)/saved_model:/models/imgclassifier -e MODEL_NAME=imgclassifier -t tensorflow/serving:latest
