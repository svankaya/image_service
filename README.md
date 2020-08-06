1) export MY_INSTALL_DIR=$HOME/.local
export PATH="$PATH:$MY_INSTALL_DIR/bin"

python -m pip install grpcio
python -m pip install grpcio-tools