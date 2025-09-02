import matplotlib.pyplot as plt

case_id = list(results.keys())[0]
pred = load_nii(pred_dict[case_id])
raters = [load_nii(lp) for lp in val_labels_dict[case_id]]

slice_idx = pred.shape[2] // 2 
plt.figure(figsize=(15, 3))
plt.subplot(1, len(raters) + 1, 1)
plt.imshow(pred[:, :, slice_idx], cmap="gray")
plt.title("Prediction")
for i, r in enumerate(raters):
    plt.subplot(1, len(raters) + 1, i + 2)
    plt.imshow(r[:, :, slice_idx], cmap="gray")
    plt.title(f"Rater {i+1}")
plt.show()
