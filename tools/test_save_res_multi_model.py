# encoding: utf-8
"""
@author:  l1aoxingyu
@contact: sherlockliao01@gmail.com
"""

import argparse
import os
import sys
import numpy as np
import h5py
import json
import time

sys.path.append('.')
from config import cfg
from data import get_test_dataloader
from utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(description="ReID Baseline Inference")
    parser.add_argument('-cfg',
        "--config_file", default="", help="path to config file", type=str
    )
    parser.add_argument('--test_phase', action='store_true', help="use cpu")
    parser.add_argument("opts", help="Modify config options using the command-line", default=None,
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()

    num_gpus = int(os.environ["WORLD_SIZE"]) if "WORLD_SIZE" in os.environ else 1

    if args.config_file != "":
        cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # set pretrian = False to avoid loading weight repeatedly
    cfg.MODEL.PRETRAIN = False
    cfg.freeze()

    logger = setup_logger("reid_baseline", False, 0)
    logger.info("Using {} GPUS".format(num_gpus))
    logger.info(args)

    if args.config_file != "":
        logger.info("Loaded configuration file {}".format(args.config_file))
    logger.info("Running with config:\n{}".format(cfg))

    test_dataloader, num_query, dataset = get_test_dataloader(cfg, test_phase=True)

    # 加载dist_mats
    dist_mats = []

    cnt = 0
    if os.path.isfile(cfg.TEST.DISTMAT1):
        f = h5py.File(cfg.TEST.DISTMAT1, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    if os.path.isfile(cfg.TEST.DISTMAT2):
        f = h5py.File(cfg.TEST.DISTMAT2, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    if os.path.isfile(cfg.TEST.DISTMAT3):
        f = h5py.File(cfg.TEST.DISTMAT3, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    if os.path.isfile(cfg.TEST.DISTMAT4):
        f = h5py.File(cfg.TEST.DISTMAT4, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    if os.path.isfile(cfg.TEST.DISTMAT5):
        f = h5py.File(cfg.TEST.DISTMAT5, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    if os.path.isfile(cfg.TEST.DISTMAT6):
        f = h5py.File(cfg.TEST.DISTMAT6, 'r')
        mat = f['dist_mat'][()]
        mat = mat[np.newaxis, ...]
        dist_mats.append(mat)
        f.close()
        cnt += 1

    dist_mat = np.concatenate(dist_mats, axis=0).mean(axis=0)
    score = dist_mat
    index = np.argsort(score, axis=1)  # from small to large

    logger.info(f'Average {cnt} results')
    # saving results
    if args.test_phase:
        query_path = [t[0] for t in dataset.query]
        gallery_path = [t[0] for t in dataset.gallery]
        logger.info("-------------Write resutls to json file----------")

        results = {}
        top_k = 200
        for i in range(len(query_path)):
            topk_res = []
            for j in range(top_k):
                img_path = gallery_path[index[i, j]]
                # print(img_path)
                topk_res.append(img_path.split('/')[-1].split('_')[-1])
            results[query_path[i].split('/')[-1].split('_')[-1]] = topk_res

        # 写入结果
        strtime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        json.dump(results, open('submit/ensemble_%s.json' % (strtime), 'w'))


if __name__ == '__main__':
    main()

