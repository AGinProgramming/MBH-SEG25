# MBH-SEG25 solution
## Summary
MICCAI - MBHSEG 2025 Multi-class Brain Hemorrhage Segmentation in Non-contrast CT Challenge solution

### Model

The newest version of nnUNetv2 is utilized as the baseline model. 

1. **Input:**
   - NIFTI(.nii.gz) files with the same size.
   - Annotations from different raters should be noted with their ID instead of being the only ground truth.

2. **Output:**
   - Multiclass segmentation of the Brain Hemorrhage Segmentation CT images:
     "background": 0,  
     "epidural": 1,  
     "intraparenchymal": 2,  
     "intraventricular": 3,  
     "subarachnoid": 4,  
     "subdural": 5, 

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

### Download model structure
Model can be downloaded by:
```bash
git clone git@github.com:MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
 ```

### Download model weights
Download model weights from:
https://drive.google.com/drive/folders/1yM6iR6KDjj-VsbuGHAIkv4l0ip2VLUeb?usp=sharing

### Run Inference
after install and activate the environment, form the test dataset into the proper data form
```bash
python /path_to_data_form.py/data_form.py
```
where 'data_root' and  'out_root' should be replaced by the real path of the raw data and the folder which stored the reformed data in.
The input files should be renamed as:
```bash
input_folder/caseid_0000.nii.gz
```
The output will be NIFTI(.nii.gz) files formed as:
```bash
output_folder/caseid.nii.gz
```

### Run prediction
```bash
python test_inference.py \
  --model_folder /absolute_path_to_submission/submission/model_inputs/Dataset888_weak/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_all \
  --input_folder /absolute_path_to_input_files \
  --output_folder /absolute_path_to_output_files \
  --folds all \
  --checkpoint /absolute_path_to_checkpoint_best.pth

```

### Evaluations
Simply run:
```bash
python competition_evaluation.py --pred_path /path/to/predictions(output files path) --gt_path /path/to/annotations
```

## Reference
-This work uses the nnUNet framework developed by Isensee et al. [1]. The official repository is available at: [https://github.com/MIC-DKFZ/nnUNet](https://github.com/MIC-DKFZ/nnUNet)

-Wu, Y., Luo, X., Xu, Z., Guo, X., Ju, L., Ge, Z., Liao, W., Cai, J.: Diversified and personalized multi-rater medical image segmentation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 11470–11479 (June 2024).
