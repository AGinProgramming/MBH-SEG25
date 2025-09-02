import os
import numpy as np
import nibabel as nib
import pandas as pd
from tqdm import tqdm

# --- settings ---
data_root = "/root/autodl-tmp/weak_predict"
csv_path = "/root/autodl-tmp/MBH_Train_2025_case-label/case-wise_annotation.csv"
pred_root = "/root/autodl-tmp/weak_predict"
output_csv = "/root/autodl-tmp/weak_predict/accurate_cases.csv"

# --- read weak labels ---
df_labels = pd.read_csv(csv_path)
df_labels.set_index('patientID_studyID', inplace=True)
label_cols = ['epidural', 'intraparenchymal', 'intraventricular', 'subarachnoid', 'subdural']
df_labels = df_labels[label_cols]
 
# --- prepare output ---
accurate_cases = []

# --- go through NIfTI files ---
for nii_file in tqdm(os.listdir(data_root)):
    if not nii_file.endswith(".nii.gz"):
        continue
    case_id = nii_file.replace(".nii.gz","")
    # nii_path = os.path.join(data_root, nii_file)
    
    # # load NIfTI
    # img = nib.load(nii_path).get_fdata()
    
    pred_path = os.path.join("/root/autodl-tmp/weak_predict", case_id + ".nii.gz")
    if not os.path.exists(pred_path):
        print(f"⚠️ Missing prediction for {case_id}")
        continue
    
    pred = nib.load(pred_path).get_fdata().astype(int)
    case_pred = [(pred == i).any() for i in range(1, 6)]
    case_pred = np.array(case_pred, dtype=int)

    
    # get weak label
    if case_id in df_labels.index:
        weak_label = df_labels.loc[case_id].values.astype(int)
    else:
        print(f"⚠️ {case_id} not found in CSV, assigning zero label.")
        weak_label = np.zeros(5, dtype=int)
    
    # keep cases same as weak label
    if np.all((case_pred == weak_label) | (weak_label == 0)):
        accurate_cases.append([case_id] + case_pred.tolist())

# --- save accurate case ---
df_out = pd.DataFrame(accurate_cases, columns=['patientID_studyID', 'epidural', 'intra', 'intraven', 'subara', 'subdural'])
df_out.to_csv(output_csv, index=False)
print(f"Saved {len(accurate_cases)} accurate cases to {output_csv}")
