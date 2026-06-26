from google.cloud import texttospeech
import os, glob

WORD_VOICE = "de-DE-Chirp3-HD-Charon"
SENT_VOICE = "de-DE-Chirp3-HD-Charon"
RATE       = "0.85"
GAP        = "2.5s"   # gap between word repetitions
PERF_GAP   = "3.5s"   # slightly longer gap after Perfekt
MAX_BYTES  = 4500

# ── Config for bulk mode ───────────────────────────────────────────────────────
# Set SINGLE_LESSON to a name (e.g. "Lektion-10") to render only that lesson.
# Set to None to render all lessons that don't have an MP3 yet.
SINGLE_LESSON = "Lektion-10"

# ── Lektion-10 vocabulary ─────────────────────────────────────────────────────
# (word, perfekt_or_None, first_sample_sentence)
ITEMS_10 = [
    ("einsteigen",       "ist eingestiegen",  "Ich steige in den Bus ein."),
    ("aussteigen",       "ist ausgestiegen",  "Ich steige am Bahnhof aus."),
    ("abfahren",         "ist abgefahren",    "Der Zug fährt um acht Uhr ab."),
    ("ankommen",         "ist angekommen",    "Wir kommen um zehn Uhr an."),
    ("umsteigen",        "ist umgestiegen",   "In München steige ich um."),
    ("einfahren",        "ist eingefahren",   "Der Zug fährt gerade ein."),
    ("abholen",          "hat abgeholt",      "Mein Freund holt mich ab."),
    ("anrufen",          "hat angerufen",     "Ich rufe meine Mutter an."),
    ("nehmen",           "hat genommen",      "Ich nehme die S-Bahn."),
    ("gerade",           None,                "Der Bus kommt gerade."),
    ("die U-Bahn",       None,                "Die U-Bahn kommt."),
    ("der Bus",          None,                "Der Bus kommt in fünf Minuten."),
    ("die S-Bahn",       None,                "Die S-Bahn fährt nach München."),
    ("die Straßenbahn",  None,                "Die Straßenbahn hält hier."),
    ("der Zug",          None,                "Der Zug kommt um zehn Uhr."),
    ("das Taxi",         None,                "Das Taxi ist teuer."),
    ("das Flugzeug",     None,                "Das Flugzeug fliegt nach Berlin."),
    ("der Bahnhof",      None,                "Der Bahnhof ist groß."),
    ("der Hauptbahnhof", None,                "Der Hauptbahnhof ist sehr groß."),
    ("der Flughafen",    None,                "Der Flughafen ist weit weg."),
    ("der Bahnsteig",    None,                "Der Bahnsteig ist hier."),
    ("das Gleis",        None,                "Das Gleis ist Nummer fünf."),
    ("die Haltestelle",  None,                "Die Haltestelle ist hier."),
    ("der Koffer",       None,                "Der Koffer ist schwer."),
    ("das Gepäck",       None,                "Das Gepäck ist schwer."),
    ("die Reise",        None,                "Die Reise dauert zwei Stunden."),
    ("die Minute",       None,                "Eine Minute ist kurz."),
    ("die Durchsage",    None,                "Die Durchsage ist laut."),
    ("das Verkehrsmittel", None,              "Das Verkehrsmittel ist gut."),
]

LESSONS = {
    "Lektion-10": ("Menschen A1.1. Lektion 10. Ich steige jetzt in die U-Bahn ein.", ITEMS_10),
}

# ── SSML builder ──────────────────────────────────────────────────────────────
def w(text, last=False):
    t = text + "." if last else text
    return f'<voice name="{WORD_VOICE}"><prosody rate="{RATE}">{t}</prosody></voice>'

def build_block(word, perfekt, sentence):
    reps = (f'{w(word)} <break time="{GAP}"/> '
            f'{w(word)} <break time="{GAP}"/> '
            f'{w(word, last=True)} <break time="{GAP}"/>')
    perf = (f'\n  {w(perfekt, last=True)} <break time="{PERF_GAP}"/>'
            if perfekt else "")
    sent = f'  <voice name="{SENT_VOICE}">{sentence}</voice> <break time="4s"/>'
    return f'  {reps}{perf}\n  {sent}'

# ── Synthesize ─────────────────────────────────────────────────────────────────
def synthesize(lesson, title, items):
    mp3_path  = f"{lesson}.mp3"
    ssml_path = f"{lesson}.ssml"

    blocks  = [f'  <voice name="{SENT_VOICE}">{title}</voice> <break time="4s"/>']
    blocks += [build_block(w, p, s) for w, p, s in items]
    ssml_full = "<speak>\n" + "\n\n".join(blocks) + "\n</speak>\n"

    with open(ssml_path, "w") as f:
        f.write(ssml_full)
    print(f"Wrote {ssml_path}  ({len(ssml_full)} chars)")

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
    print(f"Saved {mp3_path}  ({len(chunks)} chunks)")

# ── Main ───────────────────────────────────────────────────────────────────────
if SINGLE_LESSON:
    if SINGLE_LESSON not in LESSONS:
        print(f"Unknown lesson: {SINGLE_LESSON}. Available: {list(LESSONS)}")
    else:
        title, items = LESSONS[SINGLE_LESSON]
        print(f"render {SINGLE_LESSON} ...")
        synthesize(SINGLE_LESSON, title, items)
else:
    for lesson, (title, items) in LESSONS.items():
        mp3_path = f"{lesson}.mp3"
        if os.path.exists(mp3_path):
            print(f"skip  {mp3_path}  (already exists)")
        else:
            print(f"render {lesson} ...")
            synthesize(lesson, title, items)
