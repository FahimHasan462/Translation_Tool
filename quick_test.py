"""
Quick test: audio/video -> Whisper (speech to text) -> Gemma (translation)

This is NOT part of the final pipeline. It is only to see how well
transcription + translation work on a real file before building the layers.

Usage (from C:\\Projects\\translation_tool with .venv active):
    python quick_test.py test_videos\\test_audio.wav
    python quick_test.py test_videos\\test.mp4
    python quick_test.py test_videos\\test_audio.wav --model gemma4:12b
    python quick_test.py test_videos\\test_audio.wav --no-think

Output is printed on screen and saved to quick_test_output\\
"""

import argparse
import gc
import os
import sys
import time
from pathlib import Path

# On Windows, faster-whisper (CTranslate2) needs NVIDIA's cuBLAS and cuDNN DLLs.
# The GPU build of PyTorch already ships them in torch\lib. Importing torch first
# loads them into this process, so faster-whisper can find them.
import torch  # must be imported BEFORE faster_whisper

_torch_lib = Path(torch.__file__).parent / "lib"
if hasattr(os, "add_dll_directory") and _torch_lib.is_dir():
    os.add_dll_directory(str(_torch_lib))

import ollama
from faster_whisper import WhisperModel

OUT_DIR = Path(__file__).resolve().parent / "quick_test_output"

SYSTEM_PROMPT = """You are a professional translator working for an animation studio.
The text is a speech-recognition transcript of work meeting.

Rules:
- Translate every line into natural English.
- Use animation industry terminology where it fits, for example:
  タメ = hold / anticipation, ツメ = easing / spacing, 原画 = key animation,
  中割り = inbetweens, 作画 = animation drawing, リテイク = retake, カット = cut.
- The transcript comes from speech recognition and may contain mistakes
  (wrong kanji, misheard words). Use the surrounding lines to work out what was
  most likely meant.
- Keep the timestamp at the start of each line exactly as given.
- Output ONLY the translated lines. No explanations, no notes, no alternatives."""


def fmt(t: float) -> str:
    minutes, seconds = divmod(t, 60)
    return f"{int(minutes):02d}:{seconds:04.1f}"


def transcribe(path: Path):
    print("[1/2] Loading Whisper large-v3 on GPU ...")
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")

    print("      Transcribing ...")
    start = time.time()
    segments, info = model.transcribe(str(path), beam_size=5, vad_filter=True)

    lines = []
    for seg in segments:
        line = f"[{fmt(seg.start)} - {fmt(seg.end)}] {seg.text.strip()}"
        print("     ", line)
        lines.append(line)

    print(f"      Detected language: {info.language} "
          f"({info.language_probability:.0%} confident), took {time.time() - start:.1f}s")

    # Free GPU memory before Gemma loads
    del model
    gc.collect()
    return info.language, lines


def translate(language: str, lines: list[str], model_name: str, think: bool) -> str:
    print(f"\n[2/2] Translating with {model_name} (thinking {'on' if think else 'off'}) ...")
    start = time.time()

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Source language: {language}\n\nTranscript:\n" + "\n".join(lines)},
        ],
        think=think,
        options={"num_ctx": 16384, "temperature": 0.2},
    )

    print(f"      took {time.time() - start:.1f}s")
    return response.message.content.strip()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Quick Whisper + Gemma translation test")
    parser.add_argument("file", help="audio or video file to test")
    parser.add_argument("--model", default="gemma4:26b", help="Ollama model name (default: gemma4:26b)")
    parser.add_argument("--no-think", action="store_true", help="turn off Gemma's thinking step (faster)")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    if not path.is_file():
        sys.exit(f"ERROR: file not found: {path}")

    language, lines = transcribe(path)
    if not lines:
        sys.exit("No speech was found in this file.")

    translation = translate(language, lines, args.model, think=not args.no_think)

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "transcript.txt").write_text("\n".join(lines), encoding="utf-8")
    (OUT_DIR / "translation.txt").write_text(translation, encoding="utf-8")

    print("\n================ TRANSLATION ================\n")
    print(translation)
    print(f"\nSaved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
