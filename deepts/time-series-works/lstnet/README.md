# Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks

* [Paper](https://arxiv.org/pdf/1703.07015.pdf)
* [GitGub](https://github.com/laiguokun/LSTNet)
* [Papers with code](https://paperswithcode.com/paper/modeling-long-and-short-term-temporal)

## Datasets
Four datasets used in the project are described [here](https://github.com/laiguokun/multivariate-time-series-data):
 1. [Electricity consumption](https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014).
 2. [Traffic usage](http://pems.dot.ca.gov/).
 3. [Solar energy](http://www.nrel.gov/grid/solar-power-data.html). 
 4. Exchange rate.

## Train models in standard environment
```bash
# Build training package 
../build .

# Run training for all or one of the below pre-configured models
./mlbox/run exchange-rate
./mlbox/run traffic
./mlbox/run electricity
./mlbox/run solar-energy

```

## Train models in custom environment

1. __Download datasets__
   ```bash
   mkdir ./lstnet && cd ./lstnet 
   git clone https://github.com/laiguokun/multivariate-time-series-data.git
   ```

2. __Clone project and extract data__  
   ```bash
   git clone https://github.com/laiguokun/LSTNet.git
   cd ./LSTNet && mkdir ./data

   gunzip -c ../multivariate-time-series-data/traffic/traffic.txt.gz > ./data/traffic.txt
   gunzip -c ../multivariate-time-series-data/electricity/electricity.txt.gz > ./data/electricity.txt
   gunzip -c ../multivariate-time-series-data/solar-energy/solar_AL.txt.gz > ./data/solar_AL.txt
   gunzip -c ../multivariate-time-series-data/exchange_rate/exchange_rate.txt.gz > ./data/exchange_rate.txt
   
   cd ..
   ```

3. __Train models__  
   Initialize runtime. The project requires python2.7 and PyTorch 0.3.0 but seems to work OK with 0.3.1:
   ```bash
   docker pull nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04
   nvidia-docker run --rm -ti --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v $(pwd)/LSTNet:/workspace nvidia/9.0-cudnn7-runtime-ubuntu16.04
   apt-get update && apt-get install -y --no-install-recommends python wget
   wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

   # https://pytorch.org/get-started/previous-versions/
   # CUDA 9.0 build
   pip install torch==0.3.1 -f https://download.pytorch.org/whl/cu90/stable


   cd /workspace
   mkdir ./save
   ```

   One NVIDIA P100 GPU was used. 

   1. __Train Traffic model__  
      Epoch time `~ 4.65 s`, default number of epochs is `100`. Total training time `~ 8 minutes`.

      ```bash
      python main.py --gpu 0 --data data/traffic.txt --save save/traffic.pt --hidSkip 10
 
      # ... 
      # test rse 0.5088 | test rae 0.3429 | test corr 0.8570
      ```
  
   2. __Train Electricity model__    
      Epoch time `~ 3.4 s`, default number of epochs is `100`. Total training time `~ 5.7 minutes`.
  
      ```bash
      python main.py --gpu 0 --horizon 24 --data data/electricity.txt --save save/elec.pt --output_fun Linear

      # ...
      # test rse 0.0984 | test rae 0.0533 | test corr 0.9119
      ```

   3. __Train Solar-Energy model__    
      Epoch time `~ 4.8 s`, default number of epochs is `100`. Total training time `~ 8 minutes`.

      ```bash
      python main.py --gpu 0 --data data/solar_AL.txt --save save/solar_AL.pt --hidSkip 10 --output_fun Linear

      # ...
      # test rse 0.3669 | test rae 0.2250 | test corr 0.9305
      ```

   4. __Train Exchange-Rate model__    
      Epoch time `~ 0.64 s`, default number of epochs is `100`. Total training time `~ 64 seconds`.
      ```bash
      python main.py --gpu 0 --data data/exchange_rate.txt --save save/exchange_rate.pt --hidCNN 50 --hidRNN 50 --L1Loss False --output_fun None

      # ...
      # test rse 0.0360 | test rae 0.0298 | test corr 0.9538
      ``` 
