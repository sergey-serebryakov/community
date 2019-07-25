# DCRNN

Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting

- [Paper link](https://openreview.net/pdf?id=SJiHXGWAZ)
- [Code link](https://github.com/liyaguang/DCRNN)

## Experiment Instructions

### Download this repository

```sh
git clone https://github.com/mlperf/community.git
```

### Download model code

```sh
cd community/deepts/time-series-works/dcrnn
git clone https://github.com/liyaguang/DCRNN.git src/DCRNN
```

### Download data

[Google Drive](https://drive.google.com/open?id=10FOTa6HXPqX8Pf5WRoRwcFnW9BrNZEIX) or [Baidu Cloud](https://pan.baidu.com/s/14Yy9isAIZYdU__OYEQGa_g)

Place the data under `src/DCRNN/data` directory where `DCRNN` corresponds to the repository downloaded above.

### Build Docker image

```sh
docker build -t mlperf-deepts-dcrnn:latest -f build/Dockerfile src/DCRNN
```

### Run preprocessing

```sh
src/run_preprocess.sh
```

### Run training

```sh
src/run_training.sh src/DCRNN/data/model/dcrnn_la.yaml
```
The arguement is the config file, you may modify it or use a different config file. The command will output a log file in current directory.
