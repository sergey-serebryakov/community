# Fast ES-RNN: A GPU Implementation of the ES-RNN Algorithm

__7 July 2019__. One of the time series forecasting models from [here](https://paperswithcode.com/task/time-series-forecasting). Implemented in `PyTorch`, requires tensorflow for TensorBoard support.

ES-RNN is a hybrid between classical state space forecasting models and modern RNNs that achieved a 9.4% sMAPE improvement in the M4 competition. Crucially, ES-RNN implementation requires per-time series parameters. By vectorizing the original implementation and porting the algorithm to a GPU, we achieve up to 322x training speedup depending on batch size with similar results as those reported in the original submission. Our code can be found [here](https://github.com/damitkwr/ESRNN-GPU). Paper is [here](https://arxiv.org/abs/1907.03329).


## Pre-requisites

Download M4 data:
```bash
mkdir ./m4_data && cd ./m4_data
wget https://www.m4.unic.ac.cy/wp-content/uploads/2017/12/M4DataSet.zip
wget https://www.m4.unic.ac.cy/wp-content/uploads/2018/07/M-test-set.zip
wget https://github.com/M4Competition/M4-methods/raw/master/Dataset/M4-info.csv
mkdir ./Train && cd ./Train && unzip ../M4DataSet.zip && cd ..
mkdir ./Test && cd ./Test && unzip ../M-test-set.zip && cd ..
cd ..
```

Clone ES-RNN project:
```bash
git clone https://github.com/damitkwr/ESRNN-GPU.git
cd ./ESRNN-GPU
```

Copy M4 data to ES-RNN (symlink will probably work, in this case M4-info.csv needs to be renamed):
```bash
mkdir ./data && cd ./data
mkdir ./Train && cp ../../m4_data/Train/* ./Train/
mkdir ./Test && cp ../../m4_data/Test/* ./Test/
cp ../../m4_data/M4-info.csv ./info.csv
cd ../..
``` 

Install required [dependencies](https://github.com/damitkwr/ESRNN-GPU#prerequisites). As an example here, I will use one of PyTorch NGC containers that I have on my machine. 

## Train model

Initialize runtime. I use  `nvcr.io/nvidia/pytorch:19.03-py3` NGC container that happens to be available on my machine:
```bash
nvidia-docker run --rm -ti --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v $(pwd)/ESRNN-GPU:/workspace nvcr.io/nvidia/pytorch:19.03-py3
cd /workspace && pip install --user tensorflow==1.14.0
```

Train model
```bash
export PYTHONPATH=$(pwd) CUDA_VISIBLE_DEVICES=0
cd ./es_rnn
python ./main.py
```

## Results

A model was trained with one P100 GPU using standard [configuration](https://github.com/damitkwr/ESRNN-GPU/blob/master/es_rnn/config.py). There are 35 batches in one epoch, default number of epochs is 15.

Total training time is `138.77 minutes` which is  `9.25 minutes per epoch` which is `0.26 minutes per batch`. To get more details, go to `logs/trainMonthlyprod1564625395` and run: `tensorboard --logdir=.`.

| Epoch    | Loss     | Demographic | Finance     | Industry    | Macro       | Micro       | Other       | Overall     | Hold-out Loss |
| -------- | -------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ------------- |
|  1       | 22.0722  | 11.5237     | 15.6731     | 16.7823     | 16.5961     | 14.8498     | 16.4327     | 15.3146     | 10.6034       |
|  2       |  6.0903  |  6.9036     | 12.1065     | 12.9082     | 12.8780     | 10.5395     | 12.7625     | 11.3409     |  7.4979       |
|  3       |  5.0121  |  6.3557     | 11.6723     | 12.4227     | 12.4946     | 10.0635     | 12.4010     | 10.8799     |  7.0544       |
|  4       |  4.7456  |  6.2945     | 11.5647     | 12.3815     | 12.4238     |  9.9067     | 12.4668     | 10.7955     |  6.9295       |
|  5       |  4.6295  |  6.2843     | 11.5602     | 12.3656     | 12.4211     |  9.9011     | 12.4780     | 10.7877     |  6.8824       |
|  6       |  4.5757  |  6.2901     | 11.5584     | 12.3684     | 12.4225     |  9.8943     | 12.4971     | 10.7882     |  6.8776       |
|  7       |  4.5516  |  6.2940     | 11.5606     | 12.3708     | 12.4247     |  9.8982     | 12.5043     | 10.7910     |  6.8746       |
|  8       |  4.5324  |  6.3026     | 11.5668     | 12.3703     | 12.4286     |  9.9058     | 12.5047     | 10.7958     |  6.8721       |
|  9       |  4.5144  |  6.3061     | 11.5632     | 12.3817     | 12.4307     |  9.8960     | 12.5320     | 10.7971     |  6.8768       |
| 10       |  4.4989  |  6.3090     | 11.5685     | 12.3790     | 12.4326     |  9.9032     | 12.5360     | 10.7998     |  6.8753       |
| 11       |  4.4859  |  6.3171     | 11.5786     | 12.3708     | 12.4387     |  9.9204     | 12.5231     | 10.8055     |  6.8730       |
| 12       |  4.4791  |  6.3161     | 11.5746     | 12.3788     | 12.4373     |  9.9105     | 12.5402     | 10.8044     |  6.8758       |
| 13       |  4.4728  |  6.3201     | 11.5749     | 12.3840     | 12.4372     |  9.9085     | 12.5480     | 10.8060     |  6.8778       |
| 14       |  4.4667  |  6.3280     | 11.5834     | 12.3781     | 12.4447     |  9.9222     | 12.5414     | 10.8116     |  6.8778       |
| 15       |  4.4610  |  6.3265     | 11.5792     | 12.3881     | 12.4420     |  9.9167     | 12.5600     | 10.8115     |  6.8812       |


