FROM tensorflow/tensorflow:1.12.0-gpu
  
WORKDIR /work
ADD lib lib
ADD model model
ADD scripts scripts
ADD dcrnn_train.py dcrnn_train.py

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip

RUN pip3 --no-cache-dir install --upgrade pip setuptools
RUN pip3 install numpy scipy tensorflow-gpu==1.12.0
RUN pip3 install pandas>=0.19.2 pyyaml statsmodels tables

ENTRYPOINT ["python3"]
