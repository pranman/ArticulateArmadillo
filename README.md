# Audio to SRT Subtitle Generator

This project transcribes audio files (MP3 or WAV) and generates SRT subtitle files. It can use either OpenAI's Whisper or the Faster-Whisper library as the transcription backend.

## Features

*   Supports MP3 and WAV audio formats.
*   Choice of transcription backend:
    *   OpenAI Whisper
    *   Faster-Whisper
*   Selectable model size for transcription quality and speed trade-off.
*   Option to run on CPU or CUDA-enabled GPU.
*   Test mode to quickly process only the first 3 minutes of an audio file.
*   Automatic sentence splitting for subtitle segments.
*   Subtitle line wrapping (max 80 characters, 2 lines).

## Setup

1.  **Clone the repository (if applicable) or download the project files.**
2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install FFmpeg:**
    This script requires FFmpeg to be installed and accessible in your system's PATH, or you need to specify the path to `ffmpeg.exe` in `main.py` (line 39). You can download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Place your audio file(s) (MP3 or WAV) into the `input` directory. The script will process the first audio file it finds.
2.  Run the script from the project's root directory:
    ```bash
    python main.py [OPTIONS]
    ```
3.  The generated SRT subtitle file will be saved in the `output` directory.

## Command-Line Arguments

| Argument        | Choices                    | Default   | Description                                                                      |
|-----------------|----------------------------|-----------|----------------------------------------------------------------------------------|
| `--test`        |                            |           | Process only the first 3 minutes of the audio.                                   |
| `--backend`     | `whisper`, `faster-whisper`| `whisper` | Backend model to use for transcription.                                          |
| `--model`       | (see note below)           | `large`   | Model size. Common options: `tiny`, `base`, `small`, `medium`, `large`, `large-v3`. |
| `--device`      | `cpu`, `cuda`              | `cpu`     | Device to run the model on.                                                      |

**Note on Models:** The available models depend on the chosen backend.
*   **Whisper:** `tiny`, `base`, `small`, `medium`, `large`, `large-v1`, `large-v2`, `large-v3`. Also language-specific models like `tiny.en`, `base.en`, etc.
*   **Faster-Whisper:** Compatible with OpenAI Whisper model names and can load CTranslate2-converted models. Refer to the [Faster-Whisper documentation](https://github.com/guillaumekln/faster-whisper) for more details on model conversion and usage.

## Requirements

The project dependencies are listed in `requirements.txt`:

```
certifi==2025.4.26
charset-normalizer==3.4.2
colorama==0.4.6
ffmpeg-python==0.2.0
filelock==3.16.1
fsspec==2025.3.0
future==1.0.0
idna==3.10
importlib-metadata==8.5.0
jinja2==3.1.6
llvmlite==0.41.1
MarkupSafe==2.1.5
more-itertools==10.5.0
mpmath==1.3.0
networkx==3.1
numba==0.58.1
numpy==1.24.4
openai-whisper @ git+https://github.com/openai/whisper.git@13907bed90989951b41ecb4448a258cd834ffbc6
regex==2024.11.6
requests==2.32.3
sympy==1.13.3
tiktoken==0.7.0
torch==2.4.1
tqdm==4.67.1
typing-extensions==4.13.2
urllib3==2.2.3
zipp==3.20.2
```

Additionally, **FFmpeg** must be installed on your system.

## How it Works

1.  The script takes an audio file from the `input` directory.
2.  If `--test` is specified, it creates a 3-minute clip of the audio using FFmpeg.
3.  It then uses the selected backend (`whisper` or `faster-whisper`) and model to transcribe the audio.
    *   For `whisper`, it uses the `openai-whisper` library.
    *   For `faster-whisper`, it uses the `faster-whisper` library, which is an optimized CTranslate2 implementation.
4.  The transcription results (segments with text and timestamps) are processed.
5.  Each segment's text is further split into sentences.
6.  An SRT file is generated where each sentence becomes a subtitle entry with appropriate timestamps. Lines are wrapped to a maximum of 80 characters and up to 2 lines per subtitle entry.
7.  The output SRT file is saved in the `output` directory.

## Troubleshooting

*   **Checksum failed (Whisper):** If you encounter a checksum error when Whisper tries to download a model, the script will attempt to clear the Whisper cache (`~/.cache/whisper`). You will need to rerun the script after the cache is cleared.
*   **FFmpeg not found:** Ensure FFmpeg is installed and added to your system's PATH, or modify the `cmd` path in `main.py` (around line 39) to point directly to your `ffmpeg.exe` (or `ffmpeg` on Linux/macOS).
*   **CUDA errors:** Ensure your Nvidia drivers and CUDA toolkit are correctly installed and compatible with the PyTorch version specified in `requirements.txt` if you are using `--device cuda`. 