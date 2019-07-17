#!/bin/sh

# change runtime where applicable
RUNTIME=nvidia-docker

NOW=$(date "+%y%m%d%H%M%S")
CONFIG_FILE=$1

$RUNTIME run -it \
  -v $(realpath $(dirname $0)/DCRNN/data):/work/data \
  -v $(realpath $(dirname $CONFIG_FILE)):/config \
  mlperf-deepts-dcrnn:latest \
  dcrnn_train.py --config_filename=/config/$(basename $CONFIG_FILE) | tee run-$NOW.log
