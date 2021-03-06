# MSBA: Multiple Scales, Branches and Attention Network with Bag of Tricks for Person Re-Identification
`Hanlin Tan ; Huaxin Xiao ; Xiaoyu Zhang ; Bin Dai ; Shiming Lai ; Yu Liu ; Maojun Zhang`

`National University of Defense Technology, China`

This repository contains code for our paper [MSBA: Multiple Scales, Branches and Attention Network with Bag of Tricks for Person Re-Identification](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9052718), in which we have achieved the state-of-the-art performance on Market1501, DukeMTMC-reid, CUHK03(Detected) and MSMT17 datasets as of Feb, 2020. Please note the "state-of-the-art" is under restriction of no inference tricks and no additional information other than image contents. Namely, the results in the paper is without re-ranking or flipping, and the model does not take advantage of temporal information. Besides, the computation complexity of the network backbone should not be greater than Resnet-50.

The model proposed by the paper is named MSBA (Multiple Scales, Branches and Attention) network. Details and tricks are available at [our paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9052718).

# Performance 

+ Performance of this repo:

| Datasets | Model | Image Size | mAP | R1 | Score | mAP (Re-rank+flip) | R1 (Re-rank+flip) | Score (Re-rank+flip) |
|--|--|--|--|--|--|--|--|--|
| market1501 | MSBA-a	| 384x128 | 89.0 |	95.8 |	92.4 |	92.5 |	95.7 |	94.7 |
| DukeMTMC-reID | MSBA-a | 384x128 |	~~79.8~~  80.2 | ~~89.7~~ 90.8	| ~~84.8~~ 85.5	| 86.2 | 91.1 | 88.7 |
| CUHK03(Detected) | MSBA-b | 384x128 |75.9 |	78.5 |	77.2 |	88.9 |	87.7 |	88.3 |
| MSMT17 | MSBA-a | 384x128 | 59.0    | 75.3	|  67.1  |   66.2  |    77.5  |  71.8 |
| MSMT17 | MSBA-a | 384x192 | 60.2    | 76.1	|  68.2  |   67.2  |    77.8 |  72.5  |

where score=(mAP+R1)/2.
	
+ Performance comparison with other works mainly in 2019.

![market1501](https://github.com/TomHeaven/reid2019/blob/paper/readme/market1501.png "Comparison on Market1501")
![duke](https://github.com/TomHeaven/reid2019/blob/paper/readme/dukeMTMC.png "Comparison on DukeMTMC-reID")
![cuhk03](https://github.com/TomHeaven/reid2019/blob/paper/readme/CUHK03_Detected.png "Comparison on CUHK03(Detected)")
![msmt17](https://github.com/TomHeaven/reid2019/blob/paper/readme/MSMT17.png "Comparison on MSMT1501")

# Training
+ Clone the repo:
```shell
git clone --depth 1 https://github.com/TomHeaven/msba_reid
cd msba_reid
```
+ Compile Cython codes:
```shell
cd csrc/eval_cylib; make
```
+ Prepare the datasets at `../data` folder and set the path by updating `_C.DATASETS.ROOT_DIR` of `config/defaults.py` .
+ Prepare pretrained IBN-resnet50 weights from this [repo](https://github.com/XingangPan/IBN-Net) and place it at `~/.torch/checkpoints/resnet50-ibn-a.pth`.
+ Run 
```shell
sh scripts/train_resnet50_market1501.sh
```
to train and evaluate on market1501 dataset at resolution 384x128. Scripts for other datasets are available at `scripts`. The trained weights and logs are available at `logs` by default. 



# Inference using Pretrained Weights
+ Download pretrained weights from [GoogleDrive](https://drive.google.com/open?id=1C_Gzrv1zHMxqRkX371RcA1vEXchBz27q) or [BaiduYun (password:gizs)](https://pan.baidu.com/s/1scchUfCX5rUBausHX4FqBA) and place them at `logs` folder.
+ Inference on Market1501 dataset using MSBA-a under resolution 384x128
```shell
python3 tools/val.py -cfg='configs/softmax_triplet.yml' \
DATASETS.TEST_NAMES 'market1501' \
MODEL.NAME 'resnet50_ibn' \
MODEL.BACKBONE 'resnet50' \
MODEL.WITH_IBN 'True' \
TEST.WEIGHT 'logs/384x128_MSBA-a/cuhk03/resnet50_ibn_bs64/ckpts/model_best.pth' \
TEST.IMS_PER_BATCH '128' \
INPUT.SIZE_TRAIN '[384, 128]' \
INPUT.SIZE_TEST '[384, 128]' 
```

+ Inference on DukeMTMC-reID dataset using MSBA-a under resolution 384x128
```shell
python3 tools/val.py -cfg='configs/softmax_triplet.yml' \
DATASETS.TEST_NAMES 'dukemtmc' \
MODEL.NAME 'resnet50_ibn' \
MODEL.BACKBONE 'resnet50' \
MODEL.WITH_IBN 'True' \
TEST.WEIGHT 'logs/384x128_MSBA-a/dukemtmc/resnet50_ibn_bs64/ckpts/model_best.pth' \
TEST.IMS_PER_BATCH '128' \
INPUT.SIZE_TRAIN '[384, 128]' \
INPUT.SIZE_TEST '[384, 128]' 
```

+ Inference on CUHK03(Detected) dataset using MSBA-b under resolution 384x128
```shell
python3 tools/val.py -cfg='configs/softmax_triplet.yml' \
DATASETS.TEST_NAMES 'cuhk03' \
MODEL.NAME 'resnet50_ibn' \
MODEL.BACKBONE 'resnet50' \
MODEL.WITH_IBN 'True' \
TEST.WEIGHT 'logs/384x128_MSBA-b/cuhk03/resnet50_ibn_bs64/ckpts/model_best.pth' \
TEST.IMS_PER_BATCH '128' \
INPUT.SIZE_TRAIN '[384, 128]' \
INPUT.SIZE_TEST '[384, 128]' 
```

+ Inference on MSMT17 dataset using MSBA-a under resolution 384x128
```shell
python3 tools/val.py -cfg='configs/softmax_triplet.yml' \
DATASETS.TEST_NAMES 'msmt17' \
MODEL.NAME 'resnet50_ibn' \
MODEL.BACKBONE 'resnet50' \
MODEL.WITH_IBN 'True' \
TEST.WEIGHT 'logs/384x128_MSBA-a/msmt17/resnet50_ibn_bs64/ckpts/model_best.pth' \
TEST.IMS_PER_BATCH '128' \
INPUT.SIZE_TRAIN '[384, 128]' \
INPUT.SIZE_TEST '[384, 128]' 
```
The parameter TEST.WEIGHT specifies path of the pretrained weight. The parameter `INPUT.SIZE_TEST` controls the image size for inference. The file ` tools/val.py` will also report performance results with re-ranking and flipping inference, which generally improves performance metrics by a large margin.

# Switch between MSBA-a and MSBA-b
MSBA-b achieves better performance on CUHK03(Detected) dataset. Switch to MSBA-b by
```
cp modeling/baseline_parts_b.py  modeling/baseline_parts.py 
```
and back to MSBA-a by
```
cp modeling/baseline_parts_a.py  modeling/baseline_parts.py 
```
The difference is only in construction of loss function and affects training only. That is to say, you don't have to do this if you do inference only.

# Optimized Re-ranking Implementation

+ Optimized re-ranking. `utils/re-ranking.py` contains a heavily optimized re-ranking implementation: The distance matrix computation is done on GPU and the memory usage is heavily optimized compared with the original version. This is done when we join in a person ReID competition.

# Reference

If you find our paper or repo helpful to your work, please consider cite our paper
```
@ARTICLE{tan2020msba, 
author={H. {Tan} and H. {Xiao} and X. {Zhang} and B. {Dai} and S. {Lai} and Y. {Liu} and M. {Zhang}
journal={IEEE Access}, 
title={MSBA: Multiple Scales, Branches and Attention Network With Bag of Tricks for Person Re-Identification}, year={2020}, volume={8}, 
pages={63632-63642},
}
```
