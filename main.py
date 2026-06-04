"""
Transcreve audios (.opus do WhatsApp e outros) e salva cada transcricao num .txt.

Aceita um arquivo unico OU uma pasta inteira.

Pre-requisitos:
    uv add openai python-dotenv
    brew install ffmpeg
    .env com OPENAI_API_KEY=sk-...

Rodar:
    uv run main.py audio/audio1.opus      # um arquivo
    uv run main.py audio/                  # pasta inteira
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODELO = "gpt-4o-transcribe"  # troque por "gpt-4o-mini-transcribe" pra metade do custo
EXTENSOES_AUDIO = {".opus", ".ogg", ".mp3", ".m4a", ".wav", ".mp4", ".webm", ".flac"}


def converter_para_mp3(origem: Path) -> Path:
    """Converte qualquer audio (incl. .opus) pra .mp3 num arquivo temporario."""
    destino = Path(tempfile.mktemp(suffix=".mp3"))
    resultado = subprocess.run(
        ["ffmpeg", "-y", "-i", str(origem), str(destino)],
        capture_output=True,
        text=True,
    )
    if resultado.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou:\n{resultado.stderr}")
    return destino


def transcrever(caminho_audio: Path) -> str:
    client = OpenAI()
    with open(caminho_audio, "rb") as f:
        resp = client.audio.transcriptions.create(
            model=MODELO,
            file=f,
            language="pt",
        )
    return resp.text


def processar_um(audio: Path) -> Path:
    """Converte, transcreve e salva o .txt de um unico audio. Retorna o caminho do txt."""
    mp3 = converter_para_mp3(audio)
    try:
        texto = transcrever(mp3)
    finally:
        mp3.unlink(missing_ok=True)

    destino_txt = audio.with_suffix(".txt")
    destino_txt.write_text(texto, encoding="utf-8")
    return destino_txt


def coletar_audios(caminho: Path) -> list[Path]:
    """Se for arquivo, retorna ele. Se for pasta, retorna todos os audios dentro."""
    if caminho.is_file():
        return [caminho]
    # pasta: pega todos os arquivos com extensao de audio, ordenados
    return sorted(
        f for f in caminho.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSOES_AUDIO
    )


def main():
    if len(sys.argv) < 2:
        print("Uso: uv run main.py <arquivo.opus | pasta/>")
        sys.exit(1)

    alvo = Path(sys.argv[1])
    if not alvo.exists():
        print(f"Caminho nao encontrado: {alvo}")
        sys.exit(1)

    audios = coletar_audios(alvo)
    if not audios:
        print(f"Nenhum audio encontrado em: {alvo}")
        sys.exit(1)

    print(f"{len(audios)} audio(s) pra processar.\n")

    sucessos = 0
    falhas = []
    for i, audio in enumerate(audios, start=1):
        txt = audio.with_suffix(".txt")
        if txt.exists():
            print(f"[{i}/{len(audios)}] {audio.name} -> ja tem .txt, pulando")
            continue

        print(f"[{i}/{len(audios)}] {audio.name} -> transcrevendo ...")
        try:
            destino = processar_um(audio)
            print(f"           salvo em {destino.name}")
            sucessos += 1
        except Exception as e:
            # nao deixa um arquivo ruim derrubar o lote inteiro
            print(f"           FALHOU: {e}")
            falhas.append(audio.name)

    print(f"\nResumo: {sucessos} ok, {len(falhas)} falha(s).")
    if falhas:
        print("Falharam:", ", ".join(falhas))


if __name__ == "__main__":
    main()
