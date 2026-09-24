# 03 · Decisions Log

Source of truth. Newest decisions go at the bottom. To change a decision, add a new entry that replaces it; don't edit old ones.

Format: **Decision** · Why · Date

---

## Direction

1. **Open-source, local only. No paid APIs.** · Cost, and client material stays in the studio. · 2026-09-23
2. **Quality and context first; speed/delay is not a priority.** · Feedback must be understood correctly. · 2026-09-23
3. **Cascade design (speech → text → LLM → voice), not end-to-end speech translation.** · Only a cascade lets us add glossary, context, and corrections. · 2026-09-23
4. **Recorded videos first, live meetings later.** · Most value, easiest to get right. · 2026-09-23
5. **Main output for feedback is text (retake list, subtitles, transcript); dubbing is on demand.** · Artists need actionable notes per cut. · 2026-09-23
6. **Work step by step: build one piece → test → next.** · Solo developer; avoids overload. · 2026-09-23

## Models

7. **Main translator: Gemma 4 26B-A4B (`gemma4:26b`).** · Best evidence for context-aware translation; MoE runs well with RAM offload; Apache 2.0. Passed a first test (タメ → hold/anticipation). · 2026-09-23
8. **Checker: Qwen 3.6 35B-A3B (`qwen3.6:35b`).** · A different model catches more errors than self-checking. · 2026-09-23
9. **Gemma 4 12B (`gemma4:12b`) for live mode and first fine-tuning.** · Fits fully on 12 GB; 26B likely too big to fine-tune locally. · 2026-09-23
10. **Speech to text: Whisper large-v3 for recorded videos, kotoba-whisper for live.** · large-v3 more accurate overall; kotoba ~6× faster. · 2026-09-23
11. **Speaker detection: pyannote `speaker-diarization-community-1`.** · 2026-09-23
12. **Voice: CosyVoice 3, installed in its own environment.** · Apache 2.0, voice cloning; its dependencies conflict with other packages. · 2026-09-23
13. **Bangla: subtitles only for now, no Bangla dub.** · No mature commercial-safe open-source Bangla voice. · 2026-09-23

## Technical

14. **Ollama context must be set explicitly (`num_ctx`), 32K–64K for translation.** · Default is 8,192 (~10–15 min of speech); too small. · 2026-09-23
15. **Ollama: flash attention on, KV cache `q8_0`.** · About doubles usable context on the GPU. · 2026-09-23
16. **Whisper runs on the original audio, not Demucs-separated audio.** · Separation artifacts can hurt recognition. · 2026-09-23
17. **Translate full sentences, not raw Whisper segments.** · Japanese puts the verb at the end; split sentences lose meaning. (Suspected cause of errors in the first quick test.) · 2026-09-23
18. **Import `torch` before `faster_whisper` in every script.** · On Windows, faster-whisper needs PyTorch's bundled cuBLAS/cuDNN DLLs. · 2026-09-23

## Setup

19. **Everything on C: (`C:\Projects\translation_tool`); NAS only for archiving finished jobs.** · Loading models over the network is too slow. · 2026-09-23
20. **Python 3.11 in a `.venv`; PyTorch 2.11 + CUDA 12.8.** · Compatibility with AI libraries and the RTX 5070. · 2026-09-23
21. **Code in a private GitHub repo, synced into the Claude Project.** · Reviews always see the latest code. Client media is never committed. · 2026-09-23
