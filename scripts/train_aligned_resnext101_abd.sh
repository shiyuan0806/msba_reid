#!/usr/bin/env bash
GPUS='0,1'

CUDA_VISIBLE_DEVICES=$GPUS python3 tools/train.py -cfg='configs/softmax_triplet.yml' \
DATASETS.NAMES '("competition1910",)'  \
DATASETS.TEST_NAMES 'competition1910' \
INPUT.SIZE_TRAIN '[256, 128]' \
INPUT.SIZE_TEST '[256, 128]' \
SOLVER.IMS_PER_BATCH '60' \
MODEL.NAME 'aligned_resnext101_ibn_abd' \
MODEL.WITH_IBN 'True' \
MODEL.BACKBONE 'aligned_resnext101_abd' \
MODEL.VERSION 'aligned_resnext101_ibn_abd_bs63' \
SOLVER.OPT 'adam' \
SOLVER.LOSSTYPE '("softmax", "triplet")' \
SOLVER.MARGIN '1.1' \
SOLVER.LABEL_SMOOTH 'True' \
SOLVER.BASE_LR '0.00035' \
MODEL.PRETRAIN_PATH '/Users/tomheaven/.cache/torch/checkpoints/resnext101_ibn_a.pth.tar' \

