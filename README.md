# whisper-transcribe

Transcreve áudios (WhatsApp `.opus` e outros formatos) para `.txt` usando a API da OpenAI (modelo `gpt-4o-transcribe`).

Aceita um arquivo único ou uma pasta inteira. Pula arquivos que já têm `.txt` gerado.

## Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [ffmpeg](https://ffmpeg.org/) instalado (`brew install ffmpeg`)
- Chave de API da OpenAI

## Instalação

```bash
uv sync
```

Crie um arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sk-...
```

## Uso

```bash
# Transcrever um arquivo
uv run main.py audio/mensagem.opus

# Transcrever todos os áudios de uma pasta
uv run main.py audio/
```

O `.txt` é salvo no mesmo local do áudio original, com o mesmo nome.

## Formatos suportados

`.opus` · `.ogg` · `.mp3` · `.m4a` · `.wav` · `.mp4` · `.webm` · `.flac`

## Custo

O script usa `gpt-4o-transcribe` por padrão. Para reduzir custo pela metade, troque a constante `MODELO` em [main.py](main.py):

```python
MODELO = "gpt-4o-mini-transcribe"
```

## Idioma

Transcrição fixada em português (`language="pt"`). Para outros idiomas, altere o parâmetro `language` na função `transcrever()` em [main.py](main.py).
# openai-whisper
