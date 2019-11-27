#!/usr/bin/env bash
export CUDA_VISIBLE_DEVICES='1'
GPUS='0'

CUDA_VISIBLE_DEVICES=$GPUS python3 tools/val.py -cfg='configs/softmax_triplet_resnext.yml' \
DATASETS.TEST_NAMES 'competition1910' \
MODEL.NAME 'aligned_resnext101_ibn' \
MODEL.BACKBONE 'aligned_resnext101' \
MODEL.WITH_IBN 'True' \
TEST.WEIGHT '/Volumes/Data/比赛/行人重识别2019/logs/competition1910/aligned_resnext101_ibn_bs63/ckpts/model_best.pth'
