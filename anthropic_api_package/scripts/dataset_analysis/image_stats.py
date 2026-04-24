#!/usr/bin/env python3
"""Image profiling: resolution, format, blur, duplicates, text detection, corruption.

All checks are CPU-only. Heavy optional dependencies (PaddleOCR, imagededup)
degrade gracefully — the script runs what it can and logs skipped checks.

Usage:
    python image_stats.py \
        --repo_id floschne/marvl --split id \
        --columns left_img right_img --sample_size 50
"""

import argparse
import io
import json
import os
import sys
from collections import Counter

import numpy as np
from datasets import load_dataset
from tqdm import tqdm

# === Optional heavy imports — degrade gracefully ===

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import exifread
    HAS_EXIF = True
except ImportError:
    HAS_EXIF = False

try:
    import reverse_geocoder as rg
    HAS_GEOCODER = True
except ImportError:
    HAS_GEOCODER = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from imagededup.methods import PHash
    HAS_DEDUP = True
except ImportError:
    HAS_DEDUP = False

try:
    from paddleocr import PaddleOCR
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def extract_pil_metadata(img):
    """Extract basic metadata from a PIL Image."""
    return {
        "format": img.format or "unknown",
        "mode": img.mode,
        "width": img.width,
        "height": img.height,
        "has_exif": bool(img.info.get("exif")),
    }


def extract_exif_gps(img_bytes):
    """Extract GPS coordinates from EXIF data using exifread."""
    if not HAS_EXIF:
        return None
    try:
        tags = exifread.process_file(io.BytesIO(img_bytes), details=False)
        lat_tag = tags.get("GPS GPSLatitude")
        lon_tag = tags.get("GPS GPSLongitude")
        if lat_tag and lon_tag:
            lat_ref = str(tags.get("GPS GPSLatitudeRef", "N"))
            lon_ref = str(tags.get("GPS GPSLongitudeRef", "E"))
            lat = _dms_to_decimal(lat_tag.values, lat_ref)
            lon = _dms_to_decimal(lon_tag.values, lon_ref)
            return {"lat": round(lat, 6), "lon": round(lon, 6)}
    except Exception:
        pass
    return None


def _dms_to_decimal(dms_values, ref):
    """Convert EXIF DMS (degrees, minutes, seconds) to decimal."""
    d = float(dms_values[0])
    m = float(dms_values[1])
    s = float(dms_values[2])
    decimal = d + m / 60.0 + s / 3600.0
    if ref in ("S", "W"):
        decimal = -decimal
    return decimal


def reverse_geocode(lat, lon):
    """Reverse geocode GPS coordinates to country."""
    if not HAS_GEOCODER:
        return None
    try:
        result = rg.search([(lat, lon)])[0]
        return result.get("cc", "unknown")
    except Exception:
        return None


def compute_blur_score(img_array):
    """Laplacian variance as blur metric. Higher = sharper."""
    if not HAS_CV2:
        return None
    try:
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        return round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2)
    except Exception:
        return None


def check_corruption(img_bytes):
    """Check if image bytes can be fully decoded without error."""
    if not HAS_PIL:
        return None
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()
        return False  # not corrupt
    except Exception:
        return True  # corrupt


def detect_text_in_image(ocr_engine, img_array):
    """Run PaddleOCR detection-only to check for text presence."""
    try:
        result = ocr_engine.ocr(img_array, det=True, rec=False, cls=False)
        if result and result[0]:
            return len(result[0])  # number of text regions detected
        return 0
    except Exception:
        return 0


def image_to_bytes(img_value):
    """Convert a HF image sample value to raw bytes and PIL Image.

    HF datasets return images in various forms:
    - PIL Image directly (when not streaming)
    - dict with 'bytes' key
    - dict with 'path' key
    """
    if HAS_PIL and isinstance(img_value, Image.Image):
        buf = io.BytesIO()
        img_value.save(buf, format=img_value.format or "PNG")
        return buf.getvalue(), img_value

    if isinstance(img_value, dict):
        raw = img_value.get("bytes")
        if raw:
            img = Image.open(io.BytesIO(raw)) if HAS_PIL else None
            return raw, img
        path = img_value.get("path")
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                raw = f.read()
            img = Image.open(io.BytesIO(raw)) if HAS_PIL else None
            return raw, img

    return None, None


def main():
    parser = argparse.ArgumentParser(description="Image profiling for DA module")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--columns", nargs="+", required=True, help="Image column names")
    parser.add_argument("--sample_size", type=int, default=50)
    parser.add_argument("--token", default=None)
    parser.add_argument("--skip_ocr", action="store_true", help="Skip PaddleOCR text detection")
    parser.add_argument("--skip_dedup", action="store_true", help="Skip duplicate detection")
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")

    # === Check critical dependency ===
    if not HAS_PIL:
        json.dump({
            "script": "image_stats",
            "error": "Pillow not installed. pip install Pillow",
        }, sys.stdout, indent=2)
        return

    # === Load dataset ===
    load_kwargs = {"path": args.repo_id, "split": args.split, "streaming": True}
    if args.config:
        load_kwargs["name"] = args.config
    if token:
        load_kwargs["token"] = token

    try:
        ds = load_dataset(**load_kwargs)
    except Exception as e:
        json.dump({"script": "image_stats", "error": str(e)}, sys.stdout, indent=2)
        return

    samples = list(tqdm(ds.take(args.sample_size), total=args.sample_size, desc="Streaming images"))

    # === Init optional engines ===
    ocr_engine = None
    if HAS_OCR and not args.skip_ocr:
        try:
            ocr_engine = PaddleOCR(use_angle_cls=False, lang="en", show_log=False,
                                   use_gpu=False, det=True, rec=False)
        except Exception:
            ocr_engine = None

    # === Profile each image column ===
    per_column = {}

    for col in args.columns:
        widths, heights, blur_scores = [], [], []
        formats = Counter()
        modes = Counter()
        n_corrupt = 0
        n_missing = 0
        n_with_exif = 0
        n_with_gps = 0
        gps_countries = Counter()
        text_region_counts = []
        image_hashes = []  # for dedup

        for sample in tqdm(samples, desc=f"Profiling '{col}'"):
            img_value = sample.get(col)
            if img_value is None:
                n_missing += 1
                continue

            raw_bytes, pil_img = image_to_bytes(img_value)

            if raw_bytes is None or pil_img is None:
                n_missing += 1
                continue

            # --- Corruption check ---
            if check_corruption(raw_bytes):
                n_corrupt += 1
                continue

            # --- Basic metadata ---
            meta = extract_pil_metadata(pil_img)
            widths.append(meta["width"])
            heights.append(meta["height"])
            formats[meta["format"]] += 1
            modes[meta["mode"]] += 1

            # --- EXIF / GPS ---
            if meta["has_exif"]:
                n_with_exif += 1
                gps = extract_exif_gps(raw_bytes)
                if gps:
                    n_with_gps += 1
                    country = reverse_geocode(gps["lat"], gps["lon"])
                    if country:
                        gps_countries[country] += 1

            # --- Blur score ---
            try:
                img_array = np.array(pil_img)
                blur = compute_blur_score(img_array)
                if blur is not None:
                    blur_scores.append(blur)
            except Exception:
                pass

            # --- OCR text detection ---
            if ocr_engine is not None:
                try:
                    img_array = np.array(pil_img.convert("RGB"))
                    n_regions = detect_text_in_image(ocr_engine, img_array)
                    text_region_counts.append(n_regions)
                except Exception:
                    pass

        # === Aggregate stats ===
        n_valid = len(widths)
        col_result = {
            "n_samples": len(samples),
            "n_valid": n_valid,
            "n_missing": n_missing,
            "n_corrupt": n_corrupt,
        }

        # Resolution distribution
        if widths:
            w_arr, h_arr = np.array(widths), np.array(heights)
            col_result["resolution"] = {
                "width": _percentile_stats(w_arr),
                "height": _percentile_stats(h_arr),
            }

        # Format and mode counts
        col_result["formats"] = dict(formats.most_common())
        col_result["modes"] = dict(modes.most_common())

        # EXIF/GPS
        col_result["exif"] = {
            "n_with_exif": n_with_exif,
            "pct_with_exif": round(100 * n_with_exif / n_valid, 1) if n_valid else 0,
            "n_with_gps": n_with_gps,
            "gps_countries": dict(gps_countries.most_common()) if gps_countries else {},
        }

        # Blur
        if blur_scores:
            b_arr = np.array(blur_scores)
            col_result["blur"] = _percentile_stats(b_arr)
            col_result["blur"]["n_very_blurry"] = int(np.sum(b_arr < 50))
        elif HAS_CV2:
            col_result["blur"] = {"skipped": False, "n_scores": 0}
        else:
            col_result["blur"] = {"skipped": True, "reason": "opencv not installed"}

        # OCR text detection
        if text_region_counts:
            col_result["text_in_image"] = {
                "n_checked": len(text_region_counts),
                "n_with_text": sum(1 for c in text_region_counts if c > 0),
                "pct_with_text": round(100 * sum(1 for c in text_region_counts if c > 0)
                                       / len(text_region_counts), 1),
                "avg_regions": round(np.mean(text_region_counts), 1),
            }
        elif not HAS_OCR or args.skip_ocr:
            col_result["text_in_image"] = {"skipped": True,
                                           "reason": "paddleocr not installed" if not HAS_OCR else "skip_ocr flag"}

        # Dedup (requires all images in memory — run separately)
        if HAS_DEDUP and not args.skip_dedup and n_valid > 1:
            col_result["duplicates"] = _run_dedup(samples, col)
        elif not HAS_DEDUP or args.skip_dedup:
            col_result["duplicates"] = {"skipped": True,
                                        "reason": "imagededup not installed" if not HAS_DEDUP else "skip_dedup flag"}

        # === Anomaly detection ===
        anomalies = []
        if n_corrupt > 0:
            anomalies.append(f"{n_corrupt} corrupt images ({round(100*n_corrupt/len(samples),1)}%)")
        if n_missing > 0:
            anomalies.append(f"{n_missing} missing/null images ({round(100*n_missing/len(samples),1)}%)")
        if widths:
            ratio = max(widths) / max(min(widths), 1)
            if ratio > 10:
                anomalies.append(f"Wide resolution range: {min(widths)}x{min(heights)} to "
                                 f"{max(widths)}x{max(heights)} (ratio {ratio:.0f}x)")
        if blur_scores and col_result.get("blur", {}).get("n_very_blurry", 0) > 0:
            n_blurry = col_result["blur"]["n_very_blurry"]
            anomalies.append(f"{n_blurry} very blurry images (Laplacian var < 50)")
        dup_info = col_result.get("duplicates", {})
        if isinstance(dup_info, dict) and dup_info.get("n_duplicate_clusters", 0) > 0:
            anomalies.append(f"{dup_info['n_duplicate_clusters']} duplicate clusters found")

        col_result["anomalies"] = anomalies
        per_column[col] = col_result

    # === Report which checks were available ===
    checks_available = {
        "pillow": HAS_PIL,
        "exifread": HAS_EXIF,
        "reverse_geocoder": HAS_GEOCODER,
        "opencv": HAS_CV2,
        "imagededup": HAS_DEDUP and not args.skip_dedup,
        "paddleocr": HAS_OCR and not args.skip_ocr,
    }

    result = {
        "script": "image_stats",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "sample_size": args.sample_size,
        "checks_available": checks_available,
        "columns": per_column,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


def _percentile_stats(arr):
    """Compute standard percentile stats for a numpy array."""
    return {
        "p5": int(np.percentile(arr, 5)),
        "p25": int(np.percentile(arr, 25)),
        "p50": int(np.percentile(arr, 50)),
        "p75": int(np.percentile(arr, 75)),
        "p95": int(np.percentile(arr, 95)),
        "mean": round(float(arr.mean()), 1),
        "min": int(arr.min()),
        "max": int(arr.max()),
    }


def _run_dedup(samples, col):
    """Run perceptual hash dedup across sampled images."""
    import tempfile
    import shutil

    tmpdir = tempfile.mkdtemp(prefix="image_dedup_")
    try:
        n_saved = 0
        for i, sample in enumerate(samples):
            img_value = sample.get(col)
            if img_value is None:
                continue
            _, pil_img = image_to_bytes(img_value)
            if pil_img is None:
                continue
            try:
                pil_img.convert("RGB").save(os.path.join(tmpdir, f"{i:05d}.png"))
                n_saved += 1
            except Exception:
                continue

        if n_saved < 2:
            return {"n_images": n_saved, "n_duplicate_clusters": 0}

        hasher = PHash()
        encodings = hasher.encode_images(image_dir=tmpdir)
        duplicates = hasher.find_duplicates(encoding_map=encodings, max_distance_threshold=10)

        # Count clusters (images that have at least one duplicate)
        seen = set()
        clusters = 0
        for img, dups in duplicates.items():
            if dups and img not in seen:
                clusters += 1
                seen.add(img)
                seen.update(dups)

        return {
            "n_images": n_saved,
            "n_duplicate_clusters": clusters,
            "n_images_in_clusters": len(seen),
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
