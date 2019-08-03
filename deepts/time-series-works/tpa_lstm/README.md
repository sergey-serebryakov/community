# Temporal Pattern Attention for Multivariate Time Series Forecasting

* [Paper](https://arxiv.org/pdf/1809.04206v2.pdf)
* [GitGub](https://github.com/gantheory/TPA-LSTM)
* [Papers with code](https://paperswithcode.com/paper/temporal-pattern-attention-for-multivariate)

## Datasets
__Multivariate Time Series datasets__  
Four datasets used in the project are described [here](https://github.com/laiguokun/multivariate-time-series-data):
 1. [Electricity consumption](https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014).
 2. [Traffic usage](http://pems.dot.ca.gov/).
 3. [Solar energy](http://www.nrel.gov/grid/solar-power-data.html). 
 4. Exchange rate.
 
 __Polyphonic Music Datasets__  
 
 1. MuseData: a collection of musical pieces from various classical music composers in MIDI format
 2. LPD-5-Cleansed: 21, 425 multi-track piano-rolls that contain drums, piano, guitar, bass, and strings
 
 
 ## Train models in standard environment
```bash
# Build training package 
../build .

# Run training for all or one of the below pre-configured models
./mlbox/run muse        # Will take some time

```
 
## Train models in custom environment
 
1. __Clone project (data will be downloaded automatically)__
    ```bash
   git clone https://github.com/gantheory/TPA-LSTM.git
   cd ./TPA-LSTM && sed -i 's/tensorflow/tensorflow-gpu/g' ./requirements.txt && cd ..
   ```

2. __Build runtime__ 
   TensorFlow 1.9.0 requires CUDA 9 and cudnn 7.
   ```bash
   docker pull nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04
   nvidia-docker run --rm -ti --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v $(pwd)/TPA-LSTM:/workspace nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04
   apt-get update && apt-get install -y --no-install-recommends wget software-properties-common libgomp1
   add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && apt-get install -y --no-install-recommends python3.6
   wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py
   ```

   ```bash
   cd /workspace && export PYTHONPATH=$(pwd) CUDA_VISIBLE_DEVICES=0
   pip3 install -r ./requirements.txt
   ```

3. __Train models__
   ```bash
   python3.6 main.py --mode train --attention_len 16 --batch_size 32 --data_set muse --dropout 0.2 --learning_rate 1e-5 --model_dir ./models/muse --num_epochs 40 --num_layers 3 --num_units 338
   ```
