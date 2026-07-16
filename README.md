# whisper-transcribe

Transcribe audio files, including WhatsApp `.opus` files, to `.txt` using the OpenAI API with the `gpt-4o-transcribe` model.

The script accepts either a single file or a folder. When a matching `.txt` transcript already exists next to an audio file, that file is skipped.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [ffmpeg](https://ffmpeg.org/) installed (`brew install ffmpeg`)
- An OpenAI API key

## Installation

```bash
uv sync
```

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```env
OPENAI_API_KEY=sk-...
```

## Troubleshooting

If the script gets stuck because the virtual environment or dependencies are in a bad state, rebuild them from the project root:

```bash
rm -rf .venv
uv sync
```

## Usage

```bash
# Transcribe one file
uv run python main.py audio/message.opus

# Transcribe every supported audio file directly inside a folder
uv run python main.py audio/
```

Each `.txt` file is saved next to the original audio file with the same base name. Folder processing is not recursive.

## Supported Formats

`.opus` · `.ogg` · `.mp3` · `.m4a` · `.wav` · `.mp4` · `.webm` · `.flac`

## Cost

The script uses `gpt-4o-transcribe` by default. To reduce transcription cost, change the `MODELO` constant in [main.py](main.py):

```python
MODELO = "gpt-4o-mini-transcribe"
```

## Language

Transcription is currently fixed to Portuguese with `language="pt"`. To use another language, update the `language` parameter in the `transcrever()` function in [main.py](main.py).
