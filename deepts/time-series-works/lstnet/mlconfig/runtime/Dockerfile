FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04


RUN apt-get update && apt-get install -y --no-install-recommends python wget
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

# https://pytorch.org/get-started/previous-versions/
# CUDA 9.0 build
RUN pip install torch==0.3.1 -f https://download.pytorch.org/whl/cu90/stable