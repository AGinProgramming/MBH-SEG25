import os

imagesTr = "/root/autodl-tmp/nnUNet_raw/Dataset888_weak/imagesTr"

for f in os.listdir(imagesTr):
    if f.endswith(".nii") or f.endswith(".nii.gz"):
        # 如果文件名已经带有 _0000，就跳过
        if "_0000" not in f:
            old_path = os.path.join(imagesTr, f)
            # 去掉后缀
            if f.endswith(".nii.gz"):
                new_name = f.replace(".nii.gz", "_0000.nii.gz")
            else:  # 处理 .nii 的情况
                new_name = f.replace(".nii", "_0000.nii")
            new_path = os.path.join(imagesTr, new_name)

            print(f"重命名: {old_path} -> {new_path}")
            os.rename(old_path, new_path)

print("✅ 重命名完成！")
