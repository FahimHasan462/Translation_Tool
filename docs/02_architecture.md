# 02 · Architecture (planned)

This is the plan. It will change as we build and test. If this file and `03_decisions_log.md` disagree, the decisions log wins.

## Recorded video pipeline

| # | Layer | Input | What it does | Output | Fine-tunable? |
|---|---|---|---|---|---|
| 1 | Input | Video file (+ retake sheets, if any) | Extracts audio and saves frames; records video info | `audio_16k.wav`, `audio_original.wav`, `frames/`, `job.json` | No (FFmpeg code) |
| 2 | Speech to text | Japanese audio | Transcribes with timestamps and word confidence; detects language and speakers | Japanese lines with times and speakers | **Yes**: Whisper LoRA |
| 3 | Japanese cleanup | Raw transcript + glossary | Fixes misheard words and wrong kanji (homophones) | Clean Japanese transcript | **Yes**: same Gemma as layer 5 |
| 4 | Context builder | Clean transcript, frames, glossary, translation memory | Collects the context the translator needs: frames for lines that point at the screen, OCR of cut numbers, similar past corrections | Context package | No (code; improves as data grows) |
| 5 | Translation | Context package | Writes a context brief, then translates in parts; duration-aware for dubbing | English lines (+ emotion, notes) | **Yes**: most important one |
| 6 | Checking | Japanese + English lines | A second model (Qwen) checks the translation and flags doubtful lines; it doesn't auto-fix | English with flags | Possible, not needed early |
| 7 | Human review | Flagged lines | The Japanese-speaking colleague fixes flagged lines; each fix is saved | Corrected translation + training data | No (human) |
| 8 | Output | Final English | Creates the files the team uses | Retake list, bilingual subtitles, transcript, optional dub | Voice model possible, not worth it now |

## Models and tools per layer

| Layer | Tool | Where it runs |
|---|---|---|
| 1 | FFmpeg | CPU |
| 2 | Whisper large-v3 (faster-whisper), pyannote | GPU |
| 3, 5 | Gemma 4 26B-A4B via Ollama | GPU + RAM |
| 6 | Qwen 3.6 35B-A3B via Ollama | GPU + RAM |
| 8 | CosyVoice 3 (own environment), Demucs, Rubber Band, FFmpeg | GPU |

Rule: **one model on the GPU at a time.** Load, run the stage, unload.

## Knowledge base

- **Glossary** (`knowledge/glossary.yaml`): studio terms and their correct translations. Used by layers 2, 3, 5, 6.
- **Project profiles** (`knowledge/projects/*.yaml`): show, characters (JP + EN names), episode, staff roles.
- **Translation memory:** past corrected lines, stored with embeddings. The most similar ones are added to each translation prompt, so the tool learns from corrections right away.

## Learning loop

1. The tool translates → the colleague corrects flagged lines → corrections are saved.
2. Corrections improve results immediately through the translation memory and glossary.
3. Every few months, with 500–1,000+ corrections, fine-tune with **Unsloth** (Gemma) and PEFT/Unsloth (Whisper).
4. Test the fine-tuned model on the **gold set**. Only switch if it scores better.

## Measuring quality

- **Gold set:** 10–20 short clips with correct translations from the Japanese-speaking colleague.
- Every change to models or prompts is scored on the gold set before it's accepted.

## Live meeting mode (later)

- Audio in/out through VB-Audio Virtual Cable.
- Silero VAD waits for the end of each sentence → kotoba-whisper → Gemma (with the last 10–15 minutes as context) → subtitles first, voice (Kokoro) optional.
- Two directions: JP → EN (listening) and EN → JP (speaking).
- Live mode pauses batch jobs, since both need the GPU.
- After the meeting, the recording goes through the full batch pipeline for an accurate transcript.

## Build order

1. Gold set (with the Japanese-speaking colleague)
2. Text pipeline: layers 1, 2, 3, 5 → subtitles + transcript. Score on the gold set.
3. Screen context: layer 4 (frames, OCR)
4. Review UI + translation memory (layer 7)
5. Checking with a second model (layer 6)
6. Retake list + HR_Local integration
7. Dubbing on demand (layer 8)
8. Live mode (subtitles first)
9. Fine-tuning, only if the gold set shows it's needed
