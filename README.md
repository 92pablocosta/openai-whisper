# whisper-transcribe

Transcribe audio files, including WhatsApp `.opus` files, to `.txt` using the OpenAI API with the `gpt-4o-transcribe` model.

The script accepts either a single file or an entire folder. When processing a folder, it skips audio files that already have a matching `.txt` transcript.

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

```env
OPENAI_API_KEY=sk-...
```

## Troubleshooting

If the script gets stuck because the virtual environment or dependencies are in a bad state, rebuild them from the project root:

```bash
rm -rf .venv && uv sync && uv add openai python-dotenv
```

## Usage

```bash
# Transcribe one file
uv run main.py audio/message.opus

# Transcribe every supported audio file in a folder
uv run main.py audio/
```

Each `.txt` file is saved next to the original audio file with the same base name.

## Supported Formats

`.opus` · `.ogg` · `.mp3` · `.m4a` · `.wav` · `.mp4` · `.webm` · `.flac`

## Cost

The script uses `gpt-4o-transcribe` by default. To reduce transcription cost, change the `MODELO` constant in [main.py](main.py):

```python
MODELO = "gpt-4o-mini-transcribe"
```

## Language

Transcription is currently fixed to Portuguese with `language="pt"`. To use another language, update the `language` parameter in the `transcrever()` function in [main.py](main.py).
