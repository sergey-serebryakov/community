FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

# Mount datafolder to /tpa_lstm/data

RUN apt-get update && apt-get install -y --no-install-recommends wget software-properties-common libgomp1 git
RUN add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && apt-get install -y --no-install-recommends python3.6
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

RUN pip3 install tensorflow==1.14.0 torch==1.1.0
RUN pip3 install pandas

# Do not change benchmark dir, or change that in `run` script as well.
ENV BENCHMARK_DIR /esrnn_gpu
ARG BENCHMARK_COMMIT="003bafbbce907268b5f72da51e7d64ad2f846ace"
RUN git clone https://github.com/damitkwr/ESRNN-GPU.git ${BENCHMARK_DIR} && \
    cd ${BENCHMARK_DIR} && git reset --hard ${BENCHMARK_COMMIT}

ENV PYTHONPATH ${BENCHMARK_DIR}
WORKDIR ${BENCHMARK_DIR}/es_rnn
