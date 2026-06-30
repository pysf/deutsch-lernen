from google.cloud import texttospeech
import argparse, os, glob

VOICE     = "de-DE-Chirp3-HD-Puck"
MAX_BYTES = 4500

parser = argparse.ArgumentParser(description="Render SSML files to MP3 via Google TTS.")
parser.add_argument("--dir", default=".", help="Book directory containing Lektion-*.ssml files (default: cwd)")
parser.add_argument("--lesson", default=None, help="Render a single lesson, e.g. Lektion-10 (default: all missing)")
args = parser.parse_args()

BOOK_DIR      = os.path.abspath(args.dir)
SINGLE_LESSON = args.lesson


def synthesize_ssml(ssml_path, mp3_path):
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
            voice=texttospeech.VoiceSelectionParams(language_code="de-DE", name=VOICE),
            audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3),
        )
        audio += r.audio_content
        print(f"  chunk {i}/{len(chunks)} ok")

    with open(mp3_path, "wb") as f:
        f.write(audio)
    print(f"  saved {mp3_path}")


if SINGLE_LESSON:
    ssml = os.path.join(BOOK_DIR, f"{SINGLE_LESSON}.ssml")
    mp3  = os.path.join(BOOK_DIR, f"{SINGLE_LESSON}.mp3")
    if not os.path.exists(ssml):
        print(f"Not found: {ssml}")
    else:
        print(f"render {ssml} ...")
        synthesize_ssml(ssml, mp3)
else:
    for ssml in sorted(glob.glob(os.path.join(BOOK_DIR, "Lektion-*.ssml"))):
        mp3 = ssml.replace(".ssml", ".mp3")
        if os.path.exists(mp3):
            print(f"skip  {os.path.basename(mp3)}  (already exists)")
        else:
            print(f"render {os.path.basename(ssml)} ...")
            synthesize_ssml(ssml, mp3)
