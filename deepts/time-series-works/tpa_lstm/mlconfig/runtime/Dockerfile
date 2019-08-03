FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

# Mount datafolder to /tpa_lstm/data

RUN apt-get update && apt-get install -y --no-install-recommends wget software-properties-common libgomp1 git
RUN add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && apt-get install -y --no-install-recommends python3.6
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py


# Do not change benchmark dir, or change that in `run` script as well.
ENV BENCHMARK_DIR /tpa_lstm
ARG BENCHMARK_COMMIT="598cfc90f778856084f0ca80b463894e7ea26481"
RUN git clone https://github.com/gantheory/TPA-LSTM.git ${BENCHMARK_DIR} && \
    cd ${BENCHMARK_DIR} && git reset --hard ${BENCHMARK_COMMIT} && \
    sed -i 's/tensorflow/tensorflow-gpu/g' ./requirements.txt && \
    pip3 install -r ./requirements.txt

ENV PYTHONPATH ${BENCHMARK_DIR}
WORKDIR ${BENCHMARK_DIR}
