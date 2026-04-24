#!/usr/bin/env python3
"""Audio profiling: metadata, duration, VAD, language ID, clipping, SNR.

All checks are CPU-only. Whisper LID is the bottleneck (~30s/clip on CPU),
so it runs on a reduced sample controlled by --lid_sample_size.

Heavy optional dependencies (whisper, silero-vad) degrade gracefully.

Usage:
    python audio_stats.py \
        --repo_id google/fleurs --config sw_ke --split train \
        --column audio --sample_size 50 --lid_sample_size 20
"""

import argparse
import json
import os
import sys
import tempfile
import warnings
from collections import Counter

import io
import numpy as np
from datasets import load_dataset, Audio
from tqdm import tqdm

# === Optional heavy imports ===

try:
    import soundfile as sf
    HAS_SF = True
except ImportError:
    HAS_SF = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Silero VAD requires torch
HAS_VAD = False
if HAS_TORCH:
    try:
        _vad_model = None  # lazy-loaded
        HAS_VAD = True
    except Exception:
        pass

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False


def load_vad_model():
    """Lazy-load Silero VAD model."""
    global _vad_model
    if _vad_model is not None:
        return _vad_model
    _vad_model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-vad",
        model="silero_vad",
        trust_repo=True,
    )
    return _vad_model


def extract_audio_metadata(audio_value):
    """Extract audio array and metadata from an HF audio sample.

    Handles two formats:
    - Auto-decoded: {"array": np.ndarray, "sampling_rate": int}
    - Raw bytes (decode=False fallback): {"bytes": bytes, "path": str}
    """
    if isinstance(audio_value, dict):
        array = audio_value.get("array")
        sr = audio_value.get("sampling_rate", 16000)

        # === Raw bytes fallback (Audio(decode=False)) ===
        if array is None and audio_value.get("bytes") is not None and HAS_SF:
            try:
                array, sr = sf.read(io.BytesIO(audio_value["bytes"]))
                array = array.astype(np.float32)
                if array.ndim > 1:
                    array = array.mean(axis=1)  # stereo → mono
            except Exception:
                return None

        if array is not None:
            array = np.array(array, dtype=np.float32)
            duration = len(array) / sr
            return {
                "array": array,
                "sampling_rate": sr,
                "duration_s": round(duration, 2),
                "n_samples": len(array),
                "channels": 1,
            }
    return None


def compute_speech_ratio(vad_model, audio_array, sr):
    """Run Silero VAD and return speech-to-total duration ratio."""
    if not HAS_VAD:
        return None

    try:
        # Silero VAD expects 16kHz mono
        if sr != 16000:
            # Simple resampling via linear interpolation
            n_target = int(len(audio_array) * 16000 / sr)
            audio_16k = np.interp(
                np.linspace(0, len(audio_array) - 1, n_target),
                np.arange(len(audio_array)),
                audio_array,
            ).astype(np.float32)
            sr = 16000
        else:
            audio_16k = audio_array

        tensor = torch.from_numpy(audio_16k)

        # Get speech timestamps
        speech_timestamps = silero_get_speech_timestamps(
            vad_model, tensor, sampling_rate=sr,
            threshold=0.5, min_speech_duration_ms=250,
        )

        if not speech_timestamps:
            return 0.0

        speech_samples = sum(ts["end"] - ts["start"] for ts in speech_timestamps)
        return round(speech_samples / len(audio_16k), 3)

    except Exception:
        return None


def silero_get_speech_timestamps(model, audio, sampling_rate=16000,
                                  threshold=0.5, min_speech_duration_ms=250):
    """Extract speech timestamps using Silero VAD."""
    # Process in 512-sample windows (32ms at 16kHz)
    window_size = 512
    speech_probs = []

    model.reset_states()
    for i in range(0, len(audio), window_size):
        chunk = audio[i:i + window_size]
        if len(chunk) < window_size:
            chunk = torch.nn.functional.pad(chunk, (0, window_size - len(chunk)))
        prob = model(chunk.unsqueeze(0), sampling_rate).item()
        speech_probs.append(prob)

    # Convert to timestamps
    min_speech_windows = int(min_speech_duration_ms * sampling_rate / 1000 / window_size)
    timestamps = []
    current_start = None
    current_len = 0

    for i, prob in enumerate(speech_probs):
        if prob >= threshold:
            if current_start is None:
                current_start = i
            current_len += 1
        else:
            if current_start is not None and current_len >= min_speech_windows:
                timestamps.append({
                    "start": current_start * window_size,
                    "end": (current_start + current_len) * window_size,
                })
            current_start = None
            current_len = 0

    if current_start is not None and current_len >= min_speech_windows:
        timestamps.append({
            "start": current_start * window_size,
            "end": (current_start + current_len) * window_size,
        })

    return timestamps


def compute_clipping(audio_array, threshold=0.99):
    """Detect audio clipping (samples near +/- 1.0)."""
    n_clipped = int(np.sum(np.abs(audio_array) >= threshold))
    pct = round(100 * n_clipped / len(audio_array), 3) if len(audio_array) > 0 else 0
    return {"n_clipped_samples": n_clipped, "pct_clipped": pct}


def estimate_snr(audio_array, sr, frame_ms=25):
    """Simple energy-based SNR estimate.

    Splits audio into frames, computes energy per frame, estimates SNR as
    ratio of top-quartile energy (signal) to bottom-quartile (noise).
    """
    frame_size = int(sr * frame_ms / 1000)
    n_frames = len(audio_array) // frame_size
    if n_frames < 4:
        return None

    energies = []
    for i in range(n_frames):
        frame = audio_array[i * frame_size:(i + 1) * frame_size]
        energy = float(np.mean(frame ** 2))
        energies.append(energy)

    energies = np.array(energies)
    q25 = np.percentile(energies, 25)
    q75 = np.percentile(energies, 75)

    if q25 <= 0:
        return None

    snr_db = round(10 * np.log10(q75 / q25), 1)
    return snr_db


def main():
    parser = argparse.ArgumentParser(description="Audio profiling for DA module")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--column", required=True, help="Audio column name")
    parser.add_argument("--sample_size", type=int, default=50,
                        help="Samples for structural checks (metadata, VAD, clipping)")
    parser.add_argument("--lid_sample_size", type=int, default=20,
                        help="Samples for Whisper LID (expensive; subset of sample_size)")
    parser.add_argument("--token", default=None)
    parser.add_argument("--skip_vad", action="store_true", help="Skip Silero VAD")
    parser.add_argument("--skip_lid", action="store_true", help="Skip Whisper LID")
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")

    # === Load dataset ===
    load_kwargs = {"path": args.repo_id, "split": args.split, "streaming": True}
    if args.config:
        load_kwargs["name"] = args.config
    if token:
        load_kwargs["token"] = token

    try:
        ds = load_dataset(**load_kwargs)
    except Exception as e:
        json.dump({"script": "audio_stats", "error": str(e)}, sys.stdout, indent=2)
        return

    # Try streaming first sample — if auto-decode fails (e.g. missing torchcodec),
    # fall back to raw bytes + soundfile decoding
    decode_mode = "auto"
    try:
        test_iter = iter(ds.take(1))
        test_sample = next(test_iter)
        _ = test_sample[args.column]
    except Exception:
        if HAS_SF:
            ds = ds.cast_column(args.column, Audio(decode=False))
            decode_mode = "soundfile_fallback"
        else:
            json.dump({"script": "audio_stats",
                        "error": "Audio auto-decode failed and soundfile not installed"},
                       sys.stdout, indent=2)
            return

    # Re-stream from start (take consumed the iterator head)
    ds_fresh = load_dataset(**load_kwargs)
    if decode_mode == "soundfile_fallback":
        ds_fresh = ds_fresh.cast_column(args.column, Audio(decode=False))

    samples = list(tqdm(ds_fresh.take(args.sample_size), total=args.sample_size,
                        desc="Streaming audio"))

    # === Lazy-load models ===
    vad_model = None
    if HAS_VAD and not args.skip_vad:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                vad_model = load_vad_model()
        except Exception:
            vad_model = None

    # === Structural profiling (all samples) ===
    durations = []
    sample_rates = Counter()
    speech_ratios = []
    clipping_pcts = []
    snr_values = []
    n_missing = 0
    n_errors = 0

    # Keep audio arrays for LID pass later
    audio_arrays_for_lid = []

    for sample in tqdm(samples, desc="Audio profiling"):
        audio_value = sample.get(args.column)
        if audio_value is None:
            n_missing += 1
            continue

        meta = extract_audio_metadata(audio_value)
        if meta is None:
            n_errors += 1
            continue

        durations.append(meta["duration_s"])
        sample_rates[meta["sampling_rate"]] += 1

        audio_array = meta["array"]
        sr = meta["sampling_rate"]

        # --- Clipping ---
        clip = compute_clipping(audio_array)
        clipping_pcts.append(clip["pct_clipped"])

        # --- SNR ---
        snr = estimate_snr(audio_array, sr)
        if snr is not None:
            snr_values.append(snr)

        # --- VAD ---
        if vad_model is not None:
            ratio = compute_speech_ratio(vad_model, audio_array, sr)
            if ratio is not None:
                speech_ratios.append(ratio)

        # Save for LID (up to lid_sample_size)
        if len(audio_arrays_for_lid) < args.lid_sample_size:
            audio_arrays_for_lid.append((audio_array, sr))

    # === Whisper LID pass (reduced sample) ===
    lid_results = []
    if HAS_WHISPER and not args.skip_lid and audio_arrays_for_lid:
        # Load whisper model once
        try:
            whisper_model = whisper.load_model("tiny", device="cpu")
        except Exception:
            whisper_model = None

        if whisper_model is not None:
            for audio_array, sr in tqdm(audio_arrays_for_lid, desc="Whisper LID"):
                try:
                    if sr != 16000:
                        n_target = int(len(audio_array) * 16000 / sr)
                        audio_16k = np.interp(
                            np.linspace(0, len(audio_array) - 1, n_target),
                            np.arange(len(audio_array)),
                            audio_array,
                        ).astype(np.float32)
                    else:
                        audio_16k = audio_array

                    audio_padded = whisper.pad_or_trim(audio_16k)
                    mel = whisper.log_mel_spectrogram(audio_padded).to("cpu")
                    _, probs = whisper_model.detect_language(mel)
                    top_lang = max(probs, key=probs.get)
                    lid_results.append({
                        "language": top_lang,
                        "confidence": round(probs[top_lang], 3),
                    })
                except Exception:
                    lid_results.append({"error": "detection_failed"})

    # === Aggregate results ===
    n_valid = len(durations)
    col_result = {
        "n_samples": len(samples),
        "n_valid": n_valid,
        "n_missing": n_missing,
        "n_errors": n_errors,
    }

    # Duration distribution
    if durations:
        d_arr = np.array(durations)
        col_result["duration_s"] = {
            "p5": round(float(np.percentile(d_arr, 5)), 2),
            "p25": round(float(np.percentile(d_arr, 25)), 2),
            "p50": round(float(np.percentile(d_arr, 50)), 2),
            "p75": round(float(np.percentile(d_arr, 75)), 2),
            "p95": round(float(np.percentile(d_arr, 95)), 2),
            "mean": round(float(d_arr.mean()), 2),
            "total_minutes": round(float(d_arr.sum() / 60), 1),
        }

    # Sample rate consistency
    col_result["sample_rates"] = dict(sample_rates.most_common())
    col_result["sample_rate_consistent"] = len(sample_rates) == 1

    # VAD speech ratios
    if speech_ratios:
        sr_arr = np.array(speech_ratios)
        col_result["vad"] = {
            "n_analyzed": len(speech_ratios),
            "speech_ratio_mean": round(float(sr_arr.mean()), 3),
            "speech_ratio_p25": round(float(np.percentile(sr_arr, 25)), 3),
            "speech_ratio_p50": round(float(np.percentile(sr_arr, 50)), 3),
            "n_low_speech": int(np.sum(sr_arr < 0.5)),
        }
    elif args.skip_vad:
        col_result["vad"] = {"skipped": True, "reason": "skip_vad flag"}
    elif not HAS_VAD:
        col_result["vad"] = {"skipped": True, "reason": "silero-vad not installed (requires torch)"}

    # Clipping
    if clipping_pcts:
        c_arr = np.array(clipping_pcts)
        col_result["clipping"] = {
            "mean_pct": round(float(c_arr.mean()), 3),
            "max_pct": round(float(c_arr.max()), 3),
            "n_clips_with_clipping": int(np.sum(c_arr > 1.0)),
        }

    # SNR
    if snr_values:
        snr_arr = np.array(snr_values)
        col_result["snr_db"] = {
            "p25": round(float(np.percentile(snr_arr, 25)), 1),
            "p50": round(float(np.percentile(snr_arr, 50)), 1),
            "p75": round(float(np.percentile(snr_arr, 75)), 1),
            "n_low_snr": int(np.sum(snr_arr < 10)),
        }

    # Whisper LID
    if lid_results:
        lang_counts = Counter()
        confidences = []
        for r in lid_results:
            if "language" in r:
                lang_counts[r["language"]] += 1
                confidences.append(r["confidence"])

        n_lid = len([r for r in lid_results if "language" in r])
        lang_distribution = {}
        for lang, count in lang_counts.most_common():
            lang_distribution[lang] = {
                "count": count,
                "pct": round(100 * count / n_lid, 1) if n_lid else 0,
            }

        col_result["whisper_lid"] = {
            "n_analyzed": len(lid_results),
            "n_successful": n_lid,
            "language_distribution": lang_distribution,
            "mean_confidence": round(float(np.mean(confidences)), 3) if confidences else 0,
        }
    elif args.skip_lid:
        col_result["whisper_lid"] = {"skipped": True, "reason": "skip_lid flag"}
    elif not HAS_WHISPER:
        col_result["whisper_lid"] = {"skipped": True, "reason": "openai-whisper not installed"}

    # === Anomaly detection ===
    anomalies = []
    if n_missing > 0:
        anomalies.append(f"{n_missing} missing/null audio clips ({round(100*n_missing/len(samples),1)}%)")
    if not col_result.get("sample_rate_consistent", True):
        anomalies.append(f"Inconsistent sample rates: {dict(sample_rates)}")
    if speech_ratios:
        n_low = col_result.get("vad", {}).get("n_low_speech", 0)
        if n_low > 0:
            anomalies.append(f"{n_low} clips with < 50% speech (mostly silence/noise)")
    if clipping_pcts:
        n_clip = col_result.get("clipping", {}).get("n_clips_with_clipping", 0)
        if n_clip > 0:
            anomalies.append(f"{n_clip} clips with audio clipping (> 1% samples at ceiling)")
    if snr_values:
        n_low_snr = col_result.get("snr_db", {}).get("n_low_snr", 0)
        if n_low_snr > 0:
            anomalies.append(f"{n_low_snr} clips with low SNR (< 10 dB)")
    if lid_results:
        lid_info = col_result.get("whisper_lid", {})
        lang_dist = lid_info.get("language_distribution", {})
        if lang_dist:
            top_lang = list(lang_dist.keys())[0]
            top_pct = lang_dist[top_lang]["pct"]
            if top_pct < 70:
                anomalies.append(
                    f"No dominant language: top detected '{top_lang}' at only {top_pct}%"
                )

    col_result["anomalies"] = anomalies

    # === Final output ===
    checks_available = {
        "soundfile": HAS_SF,
        "silero_vad": HAS_VAD and not args.skip_vad,
        "whisper": HAS_WHISPER and not args.skip_lid,
    }

    result = {
        "script": "audio_stats",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "sample_size": args.sample_size,
        "lid_sample_size": min(args.lid_sample_size, args.sample_size),
        "checks_available": checks_available,
        "column": col_result,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
