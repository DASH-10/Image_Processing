# Image_Processing

This repository contains two small, focused image processing projects:
1) Prokudin-Gorskii RGB reconstruction from stacked grayscale plates.
2) Point operations and histogram processing on grayscale images.

## Why I made this
I built this repo as coursework and hands-on practice to understand core image processing ideas end to end, without relying on high-level library shortcuts.

## Repository structure
- `RGB coloring/` - Prokudin-Gorskii color reconstruction project.
- `Pic_Adjustment/odev_3/` - Point operations and histogram processing project.

## Project 1: Prokudin-Gorskii RGB reconstruction
**Use case:** Reconstruct color photos from historical stacked grayscale scans by aligning B, G, R channels.

**Code structure:**
- `RGB coloring/code/main.py` - CLI entry point and pipeline runner.
- `RGB coloring/code/alignment.py` - NCC/SSD alignment and pyramid alignment.
- `RGB coloring/code/enhancement.py` - Histogram equalization, gamma, unsharp mask.
- `RGB coloring/code/utils.py` - I/O helpers, split/compose, auto-crop.
- `RGB coloring/data/` - Sample stacked plates.
- `RGB coloring/results/` - Output images.
- `RGB coloring/requirements.txt` - Python dependencies.

**How it works:**
- Load a stacked grayscale plate and split it into B, G, R channels.
- Align G and R to B using NCC or SSD (optionally pyramid alignment).
- Compose the aligned RGB image.
- Enhance the image (histogram equalization, gamma correction, unsharp mask).
- Auto-crop dark borders and save outputs.

**How to run:**
```bash
pip install -r "RGB coloring/requirements.txt"
cd "RGB coloring/code"
python main.py --input ../data --output ../results --metric ncc --pyramid
```
Notes:
- `--input` accepts a single file or a folder.
- Defaults are `--input ../data` and `--output ../results`.

**Outputs:**
- `*_unaligned.jpg` - Direct BGR merge without alignment.
- `*_aligned.jpg` - Aligned RGB result.
- `*_enhanced.jpg` - Aligned + enhanced + cropped.

## Project 2: Point operations and histogram processing
**Use case:** Apply classic grayscale operations and histogram techniques from scratch, then save all results for analysis.

**Code structure:**
- `Pic_Adjustment/odev_3/main.py` - Orchestrates the full pipeline.
- `Pic_Adjustment/odev_3/point_operations.py` - Brightness, contrast, negative, threshold, gamma.
- `Pic_Adjustment/odev_3/histogram_processing.py` - Manual histogram, stats, stretch, equalization.
- `Pic_Adjustment/odev_3/test_images/` - Input images.
- `Pic_Adjustment/odev_3/results/` - Outputs (created automatically).

**How it works:**
- Load each test image in grayscale and resize to 256x256.
- Run point operations (brightness, contrast, negative, threshold).
- Compute histogram and statistics (mean, std, entropy, min, max).
- Apply contrast stretching and histogram equalization.
- Run gamma correction for multiple gamma values.
- Save all images and plots to `results/`.

**How to run:**
```bash
pip install numpy opencv-python matplotlib
cd "Pic_Adjustment/odev_3"
python main.py
```
Notes:
- The script expects the four test images already in `test_images/` with their exact filenames.

**Outputs:**
- Processed images like `*_bright_plus.jpg`, `*_contrast_1_5.jpg`, `*_negative.jpg`.
- Histograms like `*_orig_hist.png` and 2x2 comparison panels.
- Statistics in `*_stats.txt`.
