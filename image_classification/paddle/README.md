# 1. Problem
This benchmark uses [ResNet50](https://arxiv.org/abs/1512.03385) to classify [ILSVRC2012](http://image-net.org/challenges/LSVRC/2012/browse-synsets) images into 1000 classes.


# 2. Directions
### Steps to set up the Paddle environment
We provided PaddlePaddle v0.14.0 as a submodule so that users can compile PaddlePaddle from source. But since compiling takes quite some time (can take 1hr+ depending on the machine), we recommend using Docker image, which has a pre-compiled and stable PaddlePaddle environment.

A docker image can be pulled using:
```
docker pull paddlepaddle/paddle:0.14.0
```

To run the docker container, use:
```
nvidia-docker run -it -v `pwd`:/paddle -e CUDA_VISIBLE_DEVICES=0,1 paddlepaddle/paddle:0.14.0 /bin/bash
```

### Steps to download and verify data
PaddlePaddle's model library has a complete instruction on how to get the data, train, evaluate and infer [here](https://github.com/PaddlePaddle/models/tree/develop/fluid/image_classification)

You can use a [script](https://github.com/PaddlePaddle/models/blob/develop/fluid/image_classification/data/ILSVRC2012/download_imagenet2012.sh) to download the dataset [ILSVRC2012](http://image-net.org/challenges/LSVRC/2012/browse-synsets).

Inside the Docker container, you can git clone PaddlePaddle's model library and run the download script
```
cd /paddle
source env.sh
git clone https://github.com/PaddlePaddle/models.git
cd models/fluid/image_classification/
cd data/ILSVRC2012
./download.sh
cd ../..
```


### Steps to run and time

#### Train the model

Training can take a couple of days (9 days at max) due to the size of the training data (140 GB+). After you run the download script and downloaded the dataset, you can train a model as below:

```bash
python train.py \        
    --model=ResNet50 \
    --batch_size=256 \
    --total_images=1281167 \
    --class_dim=1000 \
    --image_shape=3,224,224 \        
    --model_save_dir=output/ \
    --with_mem_opt=True \
    --lr_strategy=piecewise_decay \
    --lr=0.1
```

Other than ResNet50, PaddlePaddle also provides other models:

```python
['AlexNet', 'DPN107', 'DPN131', 'DPN68', 'DPN92', 'DPN98', 'GoogleNet', 'InceptionV4', 'MobileNet', 'ResNet101', 'ResNet152', 'ResNet50', 'SE_ResNeXt101_32x4d', 'SE_ResNeXt152_32x4d', 'SE_ResNeXt50_32x4d', 'VGG11', 'VGG13', 'VGG16', 'VGG19', 'alexnet', 'dpn', 'googlenet', 'inception_v4', 'learning_rate', 'mobilenet', 'resnet', 'se_resnext', 'vgg']
```

#### Use a pre-trained model

Since training can take a long time, we also provide some [pre-trained models](https://github.com/PaddlePaddle/models/tree/develop/fluid/image_classification#supported-models-and-performances).

# 3. Dataset/Environment
### Publication/Attribution
[ImageNet Large Scale Visual Recognition Challenge](http://image-net.org/challenges/LSVRC/2012/index#introduction)

Citation:

```
@article{ILSVRC15,
Author = {Olga Russakovsky and Jia Deng and Hao Su and Jonathan Krause and Sanjeev Satheesh and Sean Ma and Zhiheng Huang and Andrej Karpathy and Aditya Khosla and Michael Bernstein and Alexander C. Berg and Li Fei-Fei},
Title = {{ImageNet Large Scale Visual Recognition Challenge}},
Year = {2015},
journal   = {International Journal of Computer Vision (IJCV)},
doi = {10.1007/s11263-015-0816-y},
volume={115},
number={3},
pages={211-252}
}
```

# 4. Model
### Publication/Attribution
```
@article{He2015,
	author = {Kaiming He and Xiangyu Zhang and Shaoqing Ren and Jian Sun},
	title = {Deep Residual Learning for Image Recognition},
	journal = {arXiv preprint arXiv:1512.03385},
	year = {2015}
}
```

# 5. Quality

### Quality metric
Average accuracy for all samples in the test set.

### Quality target
After 9 days of training, the top-1/top-5 accuracy are 76.63%/93.10%.

The error rate curves of AlexNet, ResNet50 and SE-ResNeXt-50 are shown in the figure below.
<p align="center">
<img src="assets/curve.jpg" height=480 width=640 hspace='10'/> <br />
Training and validation Curves
</p>

### Evaluation frequency
All test samples are evaluated once per epoch.

### Evaluation thoroughness
All test samples are evaluated once per epoch.