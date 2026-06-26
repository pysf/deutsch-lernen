"""Render one sentence with several male Chirp3 HD voices for comparison."""
from google.cloud import texttospeech
import os

SENTENCE = "Der Zug fährt um acht Uhr vom Hauptbahnhof ab."

VOICES = [
    "de-DE-Chirp3-HD-Charon",
    "de-DE-Chirp3-HD-Puck",
    "de-DE-Chirp3-HD-Orus",
    "de-DE-Chirp3-HD-Fenrir",
]

os.makedirs("voice-samples", exist_ok=True)
client = texttospeech.TextToSpeechClient()

for voice in VOICES:
    name = voice.split("-")[-1].lower()
    path = f"voice-samples/{name}.mp3"
    r = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=SENTENCE),
        voice=texttospeech.VoiceSelectionParams(language_code="de-DE", name=voice),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3),
    )
    with open(path, "wb") as f:
        f.write(r.audio_content)
    print(f"{name:10}  →  {path}")

print(f'\nSentence: "{SENTENCE}"')
