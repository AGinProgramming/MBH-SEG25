import os
import shutil
import nibabel as nib
import numpy as np
from batchgenerators.utilities.file_and_folder_operations import *
from nnunetv21.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv21.paths import nnUNet_raw

if __name__ == '__main__':
    base = '/autodl-tmp/MBH_Train_2025_voxel-label'
    cases = subdirs(base, join=False)

    target_dataset_id = 666
    target_dataset_name = f'Dataset{target_dataset_id:03d}_MBHSeg25'
    out_base = join(nnUNet_raw, target_dataset_name)

    imagesTr = join(out_base, 'imagesTr')
    labelsTr = join(out_base, 'labelsTr')
    maybe_mkdir_p(imagesTr)
    maybe_mkdir_p(labelsTr)

    new_case_list = []
    for case in cases:
        case_dir = join(base, case)
        image_file = join(case_dir, 'image.nii.gz')

        label_files = [f for f in os.listdir(case_dir) if f.startswith('label_annot')]

        for lbl in label_files:
            annot_id = lbl.split('_')[-1].replace('.nii.gz', '')  # corresponding to different annotators e.g. 1, 2, 3, 4
            new_case_id = f"{case}_annot{annot_id}"

            shutil.copy(image_file, join(imagesTr, new_case_id + '_0000.nii.gz'))

            shutil.copy(join(case_dir, lbl), join(labelsTr, new_case_id + '.nii.gz'))

            new_case_list.append(new_case_id)

    generate_dataset_json(
        out_base,
        channel_names={0: "CT"},
        labels={
            "background": 0,
            "EDH": 1,
            "IPH": 2,
            "IVH": 3,
            "SAH": 4,
            "SDH": 5
        },
        num_training_cases=len(new_case_list),
        file_ending='.nii.gz',
        dataset_name=target_dataset_name,
        reference="MBH-Seg25 challenge dataset",
        release="2025.01"
    )
