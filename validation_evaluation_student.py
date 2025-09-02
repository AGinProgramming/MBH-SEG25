import os
import glob
import numpy as np
import nibabel as nib
import pandas as pd
from itertools import combinations
from sklearn.metrics import jaccard_score

val_label_root = "/root/autodl-tmp/MBH_Val_2025_voxel-label"
pred_root = "/root/autodl-tmp/MBH_Validation_Preds_student"

val_labels_dict = {}
for case_dir in sorted(os.listdir(val_label_root)):
    case_path = os.path.join(val_label_root, case_dir)
    if os.path.isdir(case_path):
        label_paths = sorted(glob.glob(os.path.join(case_path, "label_annot_*.nii.gz")))
        if label_paths:  
            val_labels_dict[case_dir] = label_paths

print(f"find {len(val_labels_dict)}  cases : multi-rater labels")



pred_dict = {}
for case_id in val_labels_dict.keys():
    pred_path = os.path.join(pred_root, f"{case_id}.nii.gz")
    if os.path.exists(pred_path):
        pred_dict[case_id] = pred_path
    else:
        print(f"⚠️ 预测结果缺失: {case_id}")

print(f"find {len(pred_dict)}  cases : prediction")




def load_nii(path):
    return nib.load(path).get_fdata().astype(np.int32)

# def iou(a, b):
#     a = (a > 0).ravel()
#     b = (b > 0).ravel()
#     return jaccard_score(a, b)

def dice_coefficient(a, b):
    """Binary Dice"""
    a = (a > 0).astype(np.int32).ravel()
    b = (b > 0).astype(np.int32).ravel()
    inter = np.sum(a * b)
    return (2. * inter) / (np.sum(a) + np.sum(b) + 1e-8)

def dice_soft(pred, target):
    """Soft Dice (continuous maps)"""
    p = pred.astype(np.float32).ravel()
    g = target.astype(np.float32).ravel()
    inter = np.sum(p * g)
    return (2. * inter) / (np.sum(p) + np.sum(g) + 1e-8)

def dice_match(pred, raters):
    """Prediction vs each rater, take best match"""
    return max([dice_coefficient(pred, g) for g in raters])

def dice_max(preds, raters):
    """Max Dice over all preds × all raters (for multi-pred models, here single pred)"""
    return max([dice_coefficient(p, g) for p in preds for g in raters])

def generalized_energy_distance(preds, raters):
    """
    GED^2 = 2 E[d(P, G)] - E[d(P, P')] - E[d(G, G')]
    where d = 1 - Dice
    """
    # 1. E[d(P, G)] (prediction vs annotations)
    d_pg = np.mean([1 - dice_coefficient(p, g) for p in preds for g in raters])

    # 2. E[d(P, P')] (intra-pred diversity)
    if len(preds) > 1:
        d_pp = np.mean([1 - dice_coefficient(p1, p2) for p1, p2 in combinations(preds, 2)])
    else:
        d_pp = 0.0

    # 3. E[d(G, G')] (inter-rater diversity)
    if len(raters) > 1:
        d_gg = np.mean([1 - dice_coefficient(g1, g2) for g1, g2 in combinations(raters, 2)])
    else:
        d_gg = 0.0

    ged = 2 * d_pg - d_pp - d_gg
    return max(ged, 0.0)  # avoid negatives due to numerical errors

# def dice_from_iou(iou_val):
#     return 2 * iou_val / (1 + iou_val + 1e-8)

# def dice_score(pred, target):
#     intersection = np.sum((pred > 0) * (target > 0))
#     return 2.0 * intersection / (np.sum(pred > 0) + np.sum(target > 0) + 1e-8)

results = []

thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]

for case_id, raters in val_labels_dict.items():
    pred_path = pred_dict.get(case_id)
    if not pred_path or not os.path.exists(pred_path):
        continue

    pred = load_nii(pred_path)
    rater_masks = [load_nii(r) for r in raters]
    print("Case:", case_id)
    print("  pred sum:", np.sum(pred))
    print("  pred shape:", pred.shape)
    print("  raters sum:", [np.sum(m) for m in rater_masks])
    print("  raters shape:", [m.shape for m in rater_masks])


    # Personalized performance: Dice mean across raters
    dice_scores = [dice_coefficient(pred, m) for m in rater_masks]
    dice_mean = np.mean(dice_scores)
    dice_max_ind = max(dice_scores)

    # DiceSoft (soft agreement)
    stack = np.stack(rater_masks, axis=0)
    soft_gt = np.mean(stack, axis=0)  # average rater soft map
    soft_pred = (pred > 0).astype(np.float32)  # binary pred, could also support probabilistic
    dice_soft_val = dice_soft(soft_pred, soft_gt)

    # DiceMatch
    dice_match_val = dice_match(pred, rater_masks)

    # DiceMax (general definition, but here same as DiceMatch if only one pred)
    dice_max_val = dice_max([pred], rater_masks)

    # GED
    ged_val = generalized_energy_distance([pred], rater_masks)

    results.append({
        'case': case_id,
        'dice_mean': dice_mean,
        'dice_max_ind': dice_max_ind,
        'dice_soft': dice_soft_val,
        'dice_match': dice_match_val,
        'dice_max': dice_max_val,
        'ged': ged_val
    })


df = pd.DataFrame(results)
out_csv = os.path.join(pred_root, 'evaluation_summary_student.csv')
df.to_csv(out_csv, index=False)
print("Evaluation complete! Summary saved to:", out_csv)



