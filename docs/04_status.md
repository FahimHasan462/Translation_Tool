# 04 · Status

_Last updated: 2026-09-23_

The PM role keeps this file current. Paste each **Status update** block here.

## Current phase

Setup done. First quick test done. Next: collect translation error examples, then build Layer 1.

## Done

- [x] Environment: Python 3.11 `.venv`, PyTorch 2.11 + CUDA 12.8 (GPU working), FFmpeg 9.0.2
- [x] Whisper large-v3 and kotoba-whisper downloaded and working on GPU
- [x] pyannote speaker detection model downloaded (Hugging Face login working)
- [x] Ollama models: `gemma4:26b`, `gemma4:12b`, `qwen3.6:35b`
- [x] CosyVoice 3 model files in `models\cosyvoice3` (not installed yet)
- [x] Test files: `test_videos\test.mp4` (89 s), `test_videos\test_audio.wav` (92 s)
- [x] Quick test script `quick_test.py`: Whisper → Gemma, whole transcript at once

## Quick test findings

- **Whisper:** about 90% correct according to the Japanese-speaking colleague. It drops fillers like あと and えっと, which is fine.
- **Translation:** many errors. Suspected causes, most likely first:
  1. Whisper segments split sentences mid-way (Japanese verb comes at the end), and the test translated line by line
  2. No real context (project, characters, what's on screen)
  3. Missing subjects guessed wrong
  4. Whisper's ~10% errors carried into translation
- **Gemma single-sentence test:** correctly translated タメ as hold/anticipation with a one-line context hint.

## Next task

Collect **3–5 translation error examples** from the Japanese-speaking colleague, each with:
1. Japanese line
2. Gemma's English
3. Correct English
4. Type of mistake (wrong meaning / wrong term / wrong subject / unnatural)

These show which cause is real and become the start of the gold set.

## After that

Build Layer 1 (input: audio extraction, frames, `job.json`).

## Blockers

None.

## Open questions

- How often to save frames in Layer 1 (plan: every 1 second)?
- Which clips go into the gold set?

## Known issues to watch

- `torchcodec` 0.16 was installed for a newer PyTorch; may error when pyannote processes audio. Plan: load audio in memory to avoid it.
- Ollama default context is 8,192. Always set `num_ctx`.
