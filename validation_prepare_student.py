import os
import shutil
from batchgenerators.utilities.file_and_folder_operations import *

if __name__ == '__main__':
    base = '/root/autodl-tmp/MBH_Val_2025_voxel-label'
    cases = subdirs(base, join=False)

    out_base = '/root/autodl-tmp/MBH_Validation_Inference'
    maybe_mkdir_p(out_base)

    for idx, case in enumerate(cases):
        case_dir = join(base, case)
        image_file = join(case_dir, 'image.nii.gz')

        if not os.path.exists(image_file):
            print(f"Warning: {image_file} not found, skipping...")
            continue

        new_case_id = case

        target_file = join(out_base, new_case_id + '_0000.nii.gz')
        shutil.copy(image_file, target_file)

        print(f"Copied {image_file} -> {target_file}")

    print(f"✅ Finished! Total {len(cases)} cases processed.")
    print(f"Inference input folder is ready: {out_base}")