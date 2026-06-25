from google.cloud import texttospeech
import os, glob

WORD_VOICE = "de-DE-Chirp3-HD-Kore"
MAX_BYTES  = 4500

def synthesize_ssml_file(ssml_path, mp3_path):
    with open(ssml_path) as f:
        ssml_full = f.read()

    inner = ssml_full.strip()[len("<speak>"):-len("</speak>")]
    chunks, current = [], ""
    for block in inner.strip().split("\n\n"):
        block = block.strip()
        if not block:
            continue
        candidate = (current + "\n\n" + block) if current else block
        if len(f"<speak>\n{candidate}\n</speak>".encode("utf-8")) > MAX_BYTES and current:
            chunks.append(current)
            current = block
        else:
            current = candidate
    if current:
        chunks.append(current)

    client = texttospeech.TextToSpeechClient()
    audio  = b""
    for i, chunk in enumerate(chunks, 1):
        r = client.synthesize_speech(
            input=texttospeech.SynthesisInput(ssml=f"<speak>\n{chunk}\n</speak>"),
            voice=texttospeech.VoiceSelectionParams(language_code="de-DE", name=WORD_VOICE),
            audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3),
        )
        audio += r.audio_content
        print(f"  chunk {i}/{len(chunks)} ok")

    with open(mp3_path, "wb") as f:
        f.write(audio)
    print(f"  saved {mp3_path}  ({len(chunks)} chunks)")

ssml_files = sorted(glob.glob("Lektion-*.ssml"))
if not ssml_files:
    print("No .ssml files found. Generate them first.")
else:
    for ssml_path in ssml_files:
        lesson = ssml_path.replace(".ssml", "")
        mp3_path = f"{lesson}.mp3"
        if os.path.exists(mp3_path):
            print(f"skip  {mp3_path}  (already exists)")
        else:
            print(f"render {ssml_path} ...")
            synthesize_ssml_file(ssml_path, mp3_path)
