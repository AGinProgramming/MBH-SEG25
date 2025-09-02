# MBH-SEG25 solution
## Summary
MICCAI - MBHSEG 2025 Multi-class Brain Hemorrhage Segmentation in Non-contrast CT Challenge solution

### Model - nnUNetv2

Using the newest nnUNetv2 as the baseline of the model to train on the voxel-level training dataset. 
   - The input and preprocessing steps follow the nnUNet rules so that the nnUNetv2 model can read and process the data.
   - The 3d_fullres configuration was selected.

Model can be downloaded by:
```bash
git clone git@github.com:MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
 ```

### Data processing

The voxel-level dataset was used for the baseline model pre-training. The case-level dataset was selected and joined to the voxel-level training dataset for self-training steps.

### Multi-Rater Evaluation

   - During the training with the voxel-level training dataset, each annotation from different raters in the same case was considered as a ground truth, noted with the rater's ID number.
   - During the self-training phase, the predictions of the case-level cases were considered as pseudo labels instead of a single ground truth. They were treated as an external annotation source and served as auxiliary annotations during the self-training.

## Inference

### Environment and installations:
you can use either conda --> environment.yml to create the emvironment
```bash
conda env create -f environment.yml
conda activate nnunet_env
 ```
or pip --> requirements.txt to install the requirements
```bash
pip install -r requirements.txt
```

### Download model weights
Download model weights from:
https://drive.google.com/drive/folders/1yM6iR6KDjj-VsbuGHAIkv4l0ip2VLUeb?usp=drive_link

### Run Inference
after install and activate the environment, form the test dataset into the proper data form
```bash
python /path_to_data_form.py/data_form.py
```
where 'base' and  'out_base' should be replaced by the real path of the raw data and the folder which stored the reformed data in.

### Run prediction
```bash
nnUNet_predict \
    -i /path/to/raw/data/ \
    -o /path/to/save_predictions/ \
    -t 888 \
    -m 3d_fullres
    -tr nnUNetTrainerV2  # trainer class used for training
    -f all  # use all folds for prediction
```
The outcome will be NIFTI(.nii.gz) files.

### Evaluations
Simply run:
```bash
python competition_evaluation.py --pred_path /path/to/predictions --gt_path /path/to/annotations
```

## Reference
-This work uses the nnUNet framework developed by Isensee et al. [1]. The official repository is available at: [https://github.com/MIC-DKFZ/nnUNet](https://github.com/MIC-DKFZ/nnUNet)

-Wu, Y., Luo, X., Xu, Z., Guo, X., Ju, L., Ge, Z., Liao, W., Cai, J.: Diversified and personalized multi-rater medical image segmentation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 11470–11479 (June 2024).
