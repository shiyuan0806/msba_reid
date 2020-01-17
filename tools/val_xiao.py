# encoding: utf-8
"""
@author:  l1aoxingyu
@contact: sherlockliao01@gmail.com
"""

import argparse
import os
import sys

import torch
from torch.backends import cudnn

sys.path.append('.')
from config import cfg
from data import get_test_dataloader
from engine.inference import inference, inference_aligned_flipped, inference_no_rerank
from modeling_xiao import build_model
from utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(description="ReID Baseline Inference")
    parser.add_argument('-cfg',
        "--config_file", default="", help="path to config file", type=str
    )
    parser.add_argument("opts", help="Modify config options using the command-line", default=None,
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()

    num_gpus = int(os.environ["WORLD_SIZE"]) if "WORLD_SIZE" in os.environ else 1

    if args.config_file != "":
        cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # set pretrian = False to avoid loading weight repeatedly
    cfg.MODEL.PRETRAIN = False
    cfg.DATASETS.PRELOAD_IMAGE = False
    cfg.freeze()

    logger = setup_logger("reid_baseline", False, 0)
    logger.info("Using {} GPUS".format(num_gpus))
    logger.info(args)

    if args.config_file != "":
        logger.info("Loaded configuration file {}".format(args.config_file))
    logger.info("Running with config:\n{}".format(cfg))

    cudnn.benchmark = True

    model = build_model(cfg, 0)
    #print('model', model)
    model = model.cuda()
    model.load_params_wo_fc(torch.load(cfg.TEST.WEIGHT))

    test_dataloader, num_query, _ = get_test_dataloader(cfg, test_phase=False)

    #inference_no_rerank(cfg, model, test_dataloader, num_query)
    #inference(cfg, model, test_dataloader, num_query)
    #inference_aligned(cfg, model, test_dataloader, num_query) # using flipped image

    inference_aligned_flipped(cfg, model, test_dataloader, num_query,  use_local_feature=False, use_rerank=True,
                              use_cross_feature=True)


if __name__ == '__main__':
    main()

