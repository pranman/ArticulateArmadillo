# Articulate Armadillo: Audio to SRT Subtitle Generator

Generates SRT subtitles from MP3/WAV audio using Whisper or Faster-Whisper backends. Optimized for developer use.

## Core Features

*   **Backends & Models:** `--backend whisper` (OpenAI) or `faster-whisper`. Supports various model sizes (e.g., `tiny` to `large-v3`).
*   **Performance:** `--device cpu` or `cuda`. `--test` mode for 3-min audio clips (auto-creates if non-existent).
*   **Output Quality:** Segments split to sentences, proportional timing, 80-char/2-line SRT formatting.
*   **Efficiency:** Caches models, skips redundant test clip creation. `faster-whisper` shows duration-based progress.

## Setup

1.  **Prerequisites:** Python 3.x, FFmpeg (in PATH or update `main.py`).
2.  **Environment:** `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows).
3.  **Dependencies:** `pip install -r requirements.txt`.

## Usage

1.  Audio files (MP3/WAV) in `input/`.
2.  `python main.py [OPTIONS]`
3.  Subtitles in `output/`.

## CLI Options

| Argument    | Choices                    | Default   | Description                                         |
|-------------|----------------------------|-----------|-----------------------------------------------------|
| `--test`    |                            |           | Use 3-min test clip.                                |
| `--backend` | `whisper`, `faster-whisper`| `whisper` | Transcription backend.                              |
| `--model`   | (backend-dependent)        | `large`   | Model size (e.g., `tiny`, `large`, `large-v3`).    |
| `--device`  | `cpu`, `cuda`              | `cpu`     | Execution device.                                   |

Refer to backend docs for specific model availability.

## Notes

*   For full dependency list, see `requirements.txt`.
*   Handles Whisper model checksum errors by offering cache clearing.
*   Ensure CUDA environment is correctly configured if using `--device cuda`. 