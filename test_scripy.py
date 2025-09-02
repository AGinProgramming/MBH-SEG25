import os
import sys
import argparse
import nibabel as nib
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor

def run_inference(model_folder, input_folder, output_folder, folds="all", checkpoint="checkpoint_best.pth"):
    """
    Run nnUNetv2 inference and save results in NIfTI format.
    """

    # create output path
    os.makedirs(output_folder, exist_ok=True)

    # initiate predictor
    predictor = nnUNetPredictor(
        tile_step_size=0.5,
        use_gaussian=True,
        use_mirroring=True,
        perform_everything_on_device=True,
        device="cuda" if torch.cuda.is_available() else "cpu",
        verbose=True,
        verbose_preprocessing=True,
        allow_tqdm=True
    )

    # load model
    predictor.initialize_from_trained_model_folder(
        model_folder,
        use_folds=folds,
        checkpoint_name=checkpoint
    )

    # run inference
    predictor.predict_from_files(
        list_of_lists_or_source_folder=input_folder,
        output_folder=output_folder,
        save_probabilities=False,      # 只保存 segmentation mask
        overwrite=True,
        num_processes_preprocessing=2,
        num_processes_segmentation_export=2,
        folder_with_segs_from_prev_stage=None,
        num_parts=1,
        part_id=0
    )

    print(f"✅ Inference finished. Results are saved to: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run nnUNetv2 inference and save NIfTI results.")
    parser.add_argument("--model_folder", type=str, required=True, help="Path to trained nnUNetv2 model folder")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to input images (NIfTI files)")
    parser.add_argument("--output_folder", type=str, required=True, help="Where to save segmentation results")
    parser.add_argument("--folds", type=str, default="all", help="Which folds to use (default: all)")
    parser.add_argument("--checkpoint", type=str, default="checkpoint_best.pth", help="Checkpoint file name")

    args = parser.parse_args()
    run_inference(args.model_folder, args.input_folder, args.output_folder, args.folds, args.checkpoint)
