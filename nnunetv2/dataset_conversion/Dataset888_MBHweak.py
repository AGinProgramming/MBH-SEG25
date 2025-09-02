import os

data_root = "/root/autodl-tmp/MBH_Train_2025_case-label"
out_root = "/root/autodl-tmp/weak_raw/imagesTs"

os.makedirs(out_root, exist_ok=True)

for f in os.listdir(data_root):
    if f.endswith(".nii.gz"):
        case_id = f.replace(".nii.gz", "")
        new_name = f"{case_id}_0000.nii.gz"
        os.rename(os.path.join(data_root, f),
                  os.path.join(out_root, new_name))
print("All files renamed and moved to imagesTs/")
