"""Turn an MP4 into a timestamped transcript + key screenshots.

Usage:
    .venv\\Scripts\\python tools\\video_to_notes.py                 # process every new video in videos/
    .venv\\Scripts\\python tools\\video_to_notes.py "path\\to\\file.mp4" [--model large-v3] [--device cuda] [--force]

Output goes to transcripts/<video name>/:
    transcript.md   transcript interleaved with screenshots (main file to read)
    transcript.txt  plain text, one timestamped line per segment
    transcript.srt  subtitles
    frames/*.jpg    screenshots taken on scene changes (slides, demos) and at regular intervals
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = ROOT / "videos"
OUT_ROOT = ROOT / "transcripts"
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".m4v", ".avi"}
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def add_cuda_dlls() -> None:
    """ctranslate2 needs cuBLAS/cuDNN DLLs from the pip nvidia-* packages on PATH."""
    nvidia = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    for bin_dir in nvidia.glob("*/bin"):
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{os.environ['PATH']}"
        os.add_dll_directory(str(bin_dir))


def pick_device(requested: str) -> str:
    if requested != "auto":
        return requested
    import ctranslate2

    return "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"


def ts(seconds: float, srt: bool = False) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}" if srt else f"{h:02}:{m:02}:{s:02}"


def extract_frames(video: Path, frames_dir: Path, scene: float, max_gap: float, min_gap: float) -> list[tuple[float, str]]:
    """Grab a frame on every scene change (at most one per min_gap s) and at least one every max_gap s."""
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("*.jpg"):
        old.unlink()
    select = (
        f"isnan(prev_selected_t)"
        f"+gte(t-prev_selected_t\\,{max_gap})"
        f"+gt(scene\\,{scene})*gte(t-prev_selected_t\\,{min_gap})"
    )
    cmd = [
        FFMPEG, "-hide_banner", "-i", str(video),
        "-vf", f"select='{select}',showinfo,scale='min(1280,iw)':-2",
        "-fps_mode", "vfr", "-q:v", "4",
        str(frames_dir / "frame_%04d.jpg"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        sys.exit(f"ffmpeg frame extraction failed:\n{proc.stderr[-2000:]}")
    times = [float(t) for t in re.findall(r"pts_time:([\d.]+)", proc.stderr)]
    files = sorted(frames_dir.glob("frame_*.jpg"))
    return [(t, f.name) for t, f in zip(times, files)]


def load_audio(video: Path):
    import numpy as np

    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(video),
           "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        sys.exit(f"ffmpeg audio extraction failed:\n{proc.stderr.decode(errors='replace')[-2000:]}")
    return np.frombuffer(proc.stdout, dtype=np.float32)


def run_whisper(audio, model_name: str, device: str, language: str | None):
    from faster_whisper import WhisperModel

    compute = "float16" if device == "cuda" else "int8"
    model = WhisperModel(model_name, device=device, compute_type=compute)
    segments, info = model.transcribe(audio, language=language, vad_filter=True, beam_size=5)
    print(f"  language: {info.language} ({info.language_probability:.0%}), duration {ts(info.duration)}")
    out = []
    for seg in segments:
        out.append((seg.start, seg.end, seg.text.strip()))
        print(f"  [{ts(seg.start)}] {seg.text.strip()}", flush=True)
    return out, info.duration


def transcribe(video: Path, model_name: str, device: str, language: str | None):
    audio = load_audio(video)
    if audio.size == 0:
        print("  no audio track found")
        return [], 0.0, model_name
    try:
        return (*run_whisper(audio, model_name, device, language), model_name)
    except Exception as e:
        if device != "cuda":
            raise
        print(f"  GPU failed ({e}); falling back to CPU with 'small'")
        return (*run_whisper(audio, "small", "cpu", language), "small")


def write_outputs(video: Path, out_dir: Path, segments, frames, duration: float, model_name: str):
    (out_dir / "transcript.txt").write_text(
        "\n".join(f"[{ts(s)}] {t}" for s, _, t in segments) + "\n", encoding="utf-8"
    )
    (out_dir / "transcript.srt").write_text(
        "\n".join(f"{i}\n{ts(s, True)} --> {ts(e, True)}\n{t}\n" for i, (s, e, t) in enumerate(segments, 1)),
        encoding="utf-8",
    )

    events = [(t, 0, ("frame", name)) for t, name in frames] + [(s, 1, ("text", txt)) for s, _, txt in segments]
    events.sort(key=lambda e: (e[0], e[1]))

    lines = [
        f"# Transcript: {video.name}",
        "",
        f"- Source: `{video}`",
        f"- Duration: {ts(duration)}",
        f"- Segments: {len(segments)}, screenshots: {len(frames)}",
        f"- Whisper model: `{model_name}` (auto-generated; may contain recognition errors)",
        "",
    ]
    paragraph: list[str] = []

    def flush():
        if paragraph:
            lines.append(" ".join(paragraph))
            lines.append("")
            paragraph.clear()

    for t, _, (kind, value) in events:
        if kind == "frame":
            flush()
            lines += [f"## [{ts(t)}]", "", f"![screenshot at {ts(t)}](frames/{value})", ""]
        else:
            paragraph.append(f"`[{ts(t)}]` {value}")
    flush()
    (out_dir / "transcript.md").write_text("\n".join(lines), encoding="utf-8")


def process(video: Path, args) -> None:
    out_dir = OUT_ROOT / video.stem
    if (out_dir / "transcript.md").exists() and not args.force:
        print(f"skip (already done): {video.name}  -> use --force to redo")
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== {video.name} ===")
    start = time.time()

    print("extracting screenshots...")
    frames = extract_frames(video, out_dir / "frames", args.scene, args.max_gap, args.min_gap)
    print(f"  {len(frames)} screenshots")

    device = pick_device(args.device)
    model = args.model if args.model != "auto" else ("large-v3" if device == "cuda" else "small")
    print(f"transcribing with whisper '{model}' on {device} (first run downloads the model)...")
    segments, duration, model = transcribe(video, model, device, args.language)

    write_outputs(video, out_dir, segments, frames, duration, model)
    print(f"done in {time.time() - start:.0f}s -> {out_dir / 'transcript.md'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("videos", nargs="*", type=Path, help="video files (default: everything in videos/)")
    p.add_argument("--model", default="auto", help="auto (large-v3 on GPU, small on CPU), tiny, base, small, medium, large-v3")
    p.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    p.add_argument("--language", default=None, help="force a language code, e.g. en")
    p.add_argument("--scene", type=float, default=0.25, help="scene-change sensitivity 0-1 (lower = more screenshots)")
    p.add_argument("--max-gap", type=float, default=45, help="take a screenshot at least every N seconds")
    p.add_argument("--min-gap", type=float, default=4, help="never take screenshots closer than N seconds")
    p.add_argument("--force", action="store_true", help="redo videos that already have a transcript")
    args = p.parse_args()
    add_cuda_dlls()

    videos = args.videos
    if not videos:
        VIDEOS_DIR.mkdir(exist_ok=True)
        videos = sorted(f for f in VIDEOS_DIR.iterdir() if f.suffix.lower() in VIDEO_EXTS)
        if not videos:
            print(f"No videos found. Drop .mp4 files into {VIDEOS_DIR} or pass a path.")
            return
    for v in videos:
        if not v.exists():
            print(f"not found: {v}")
            continue
        process(v.resolve(), args)


if __name__ == "__main__":
    main()
