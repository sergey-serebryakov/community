DATADIR=$(dirname $0)/DCRNN/data

# Create data directories
mkdir -p $DATADIR/{METR-LA,PEMS-BAY}

# METR-LA
docker run -it \
  -v $(realpath $DATADIR):/work/data \
  mlperf-deepts-dcrnn:latest \
  -m scripts.generate_training_data --output_dir=data/METR-LA --traffic_df_filename=data/metr-la.h5

# PEMS-BAY
docker run -it \
  -v $(realpath $DATADIR):/work/data \
  mlperf-deepts-dcrnn:latest \
  -m scripts.generate_training_data --output_dir=data/PEMS-BAY --traffic_df_filename=data/pems-bay.h5
