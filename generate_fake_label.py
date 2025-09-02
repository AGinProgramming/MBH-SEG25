import os
import shutil
import pandas as pd
import nibabel as nib
import numpy as np

weak_pred_root = "/root/autodl-tmp/weak_predict"
accurate_csv = "/root/autodl-tmp/weak_predict/accurate_cases.csv"

# 输出目录
student_data_root = "/root/autodl-tmp/nnUNet_raw_1/Datasetweak"
imagesTr_out = os.path.join(student_data_root, "imagesTr")
labelsTr_out = os.path.join(student_data_root, "labelsTr")
os.makedirs(imagesTr_out, exist_ok=True)
os.makedirs(labelsTr_out, exist_ok=True)

# 读取 accurate cases
df_acc = pd.read_csv(accurate_csv)
accurate_ids = df_acc['patientID_studyID'].tolist()

skipped_ids = []

# 将 weak dataset images 和 pseudo-labels 复制到 Student 数据集
for case_id in accurate_ids:
    img_src = os.path.join("/root/autodl-tmp/weak_raw/imagesTs", case_id + "_0000.nii.gz")
    label_src = os.path.join(weak_pred_root, case_id + ".nii.gz")
    # print(img_src)
    # print(label_src)
    # img_src2 = os.path.join("/root/autodl-tmp/MBH_Train_2025_case-label", case_id + ".nii.gz")

    

    shutil.copy(img_src, os.path.join(imagesTr_out, case_id + ".nii.gz"))
    shutil.copy(label_src, os.path.join(labelsTr_out, case_id + ".nii.gz"))

