# 05 · Environment

## Machine

- Windows, PowerShell
- GPU: NVIDIA RTX 5070, 12 GB VRAM (about 1 GB used by Windows and apps). Driver CUDA version 13.3
- RAM: 64 GB
- Disk: C: (~160 GB free after models). NAS drives P: and Z: for archives only

## Project

- Folder: `C:\Projects\translation_tool`
- Start every session:
  ```
  cd C:\Projects\translation_tool
  .venv\Scripts\activate
  ```

```
translation_tool\
├── .venv\            Python 3.11 environment (not in git)
├── pipeline\         layer code
├── knowledge\        glossary, project profiles
├── jobs\             output of each run (not in git)
├── models\           CosyVoice files (not in git)
├── test_videos\      test media, confidential (not in git)
├── docs\             these knowledge documents
└── quick_test.py     Whisper → Gemma quick test
```

## Versions

- Python 3.11
- PyTorch 2.11.0 + cu128, torchaudio 2.11.0 + cu128, torchvision 0.26.0 + cu128
- faster-whisper 1.2.1 (CTranslate2 4.8.2)
- pyannote.audio 4.0.7
- ollama (Python client) 0.6.2
- FFmpeg 9.0.2 full build (includes Rubber Band)

## Models

| Model | Name / location | Size |
|---|---|---|
| Whisper large-v3 | `large-v3` (Hugging Face cache) | ~3 GB |
| kotoba-whisper | `kotoba-tech/kotoba-whisper-v2.0-faster` | ~1.5 GB |
| pyannote | `pyannote/speaker-diarization-community-1` | ~32 MB |
| Gemma 4 26B-A4B | `gemma4:26b` (Ollama) | 18 GB |
| Gemma 4 12B | `gemma4:12b` (Ollama) | 7.6 GB |
| Qwen 3.6 35B-A3B | `qwen3.6:35b` (Ollama) | 22 GB |
| CosyVoice 3 | `models\cosyvoice3` | 9.75 GB |

Caches: Hugging Face → `C:\Users\fahim\.cache\huggingface`, Ollama → `C:\Users\fahim\.ollama\models`

## Settings

- `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0` (user environment variables)
- Hugging Face login via `hf auth login`. **No token in environment variables or in code.**

## Known gotchas

1. **`cublas64_12.dll` not found** when Whisper runs → `import torch` before `faster_whisper`, and add `torch\lib` with `os.add_dll_directory`.
2. **Ollama default context is 8,192 tokens** → always pass `num_ctx` in options.
3. **`gemma4:26b` doesn't fit fully on the GPU** → about 27% runs on CPU. Larger `num_ctx` moves more to CPU (slower).
4. **Gemma thinks before answering by default** → use `think=False` for simple steps; keep thinking for hard ones.
5. **`torchcodec` version mismatch** (0.16 vs PyTorch 2.11) → load audio yourself and pass the waveform to pyannote.
6. **Installing packages can replace GPU PyTorch with a CPU build** → after any `pip install`, check:
   ```
   python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
   ```
   If it's not `+cu128 True`, reinstall PyTorch from the cu128 index.
7. **Windows console and Japanese text** → use `sys.stdout.reconfigure(encoding="utf-8")` and write files with `encoding="utf-8"`.
8. **Paths with spaces break tools** → keep folder names without spaces.
