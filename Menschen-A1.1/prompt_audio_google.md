# Google Text-to-Speech — Audio Script Prompt & Spec

## What this produces
An MP3 listen-and-repeat audio file for each lesson, generated from an SSML
script via Google Cloud Text-to-Speech. The learner hears each word 3 times
(time to repeat aloud), then a native-context sentence.

---

## Voice design

Two voices are used per lesson — one for words, one for sentences. This gives
a clear auditory cue separating "drill this word" from "hear it in context",
and provides talker variability which helps generalise pronunciation.

| Role | Voice | Why |
|------|-------|-----|
| **Word voice** (repeat after) | `de-DE-Chirp3-HD-Kore` | Clear female, 15% slower for drilling |
| **Sentence voice** (context) | `de-DE-Chirp3-HD-Charon` | Male contrast, normal speed |

### Why Chirp3 HD
| Tier | Naturalness | `<break>` SSML works | Free tier/month |
|------|-------------|----------------------|-----------------|
| Standard | robotic | yes | 4M chars |
| Neural2 | good | yes | 1M chars |
| **Chirp3 HD** | **most natural** | **yes** | **1M chars** |
| Studio | very natural | yes | none ($160/1M) |

One full lesson set (~12 lessons) uses ~50k chars — about 5% of the free tier.

### Other voice options
- Female word voice: `Leda` (neutral), `Aoede`, `Achernar`, `Callirrhoe`
- Male sentence voice: `Charon`, `Puck`, `Orus`, `Fenrir`

---

## Per-entry audio format

### All word types
1. Word spoken **3 times** by the word voice at 85% speed, 2.5s gap between reps
2. The **3rd repetition ends with a period** → falling "last one" intonation
3. The **first sample sentence** spoken once by the sentence voice at normal speed
4. 4s pause after the sentence

```xml
<voice name="de-DE-Chirp3-HD-Kore"><prosody rate="0.85">einsteigen</prosody></voice> <break time="2.5s"/>
<voice name="de-DE-Chirp3-HD-Kore"><prosody rate="0.85">einsteigen</prosody></voice> <break time="2.5s"/>
<voice name="de-DE-Chirp3-HD-Kore"><prosody rate="0.85">einsteigen.</prosody></voice> <break time="2.5s"/>
<voice name="de-DE-Chirp3-HD-Charon">Ich steige in den Bus ein.</voice> <break time="4s"/>
```

### Verbs — what to say
- **Word:** infinitive only (e.g. `einsteigen`) — no Perfekt form
- **Sentence:** the **present-tense sentence** (before ` · ` in the HTML sample)

### Nouns — what to say
- **Word:** article + noun (e.g. `der Zug`, `die U-Bahn`) — always include article
- **Sentence:** the **nominative sentence** (before ` · ` in the HTML sample)

### Other words (adverbs, adjectives, particles)
- **Word:** as-is
- **Sentence:** the single sample sentence

### Lesson title (spoken first by sentence voice)
```xml
<voice name="de-DE-Chirp3-HD-Charon">Menschen A1.1. Lektion 10. {TITLE}.</voice> <break time="4s"/>
```

---

## Source of content
Read vocabulary from `Lektion-N.html`:
- `.verb-reg` / `.verb-irr` span → verb infinitive
- `.perfekt` span → ignored for audio
- `<span class="der/die/das">` → noun with article
- `.sample` paragraph → split on ` · `, use **first part only**
- `.pos` span → ignored for audio

---

## Generating the audio — `tts.py`

`tts.py` contains the structured vocabulary data and generates the SSML +
renders the MP3. To add a new lesson:

1. Copy `tts.py`, update `LESSON`, `TITLE`, and `ITEMS` at the top.
2. Run `make` (creates `.venv`, installs deps, runs `tts.py`).

`tts.py` automatically:
- Builds the SSML and writes `Lektion-N.ssml` (the readable source of truth)
- Splits the SSML into chunks ≤ 4500 bytes (Google's 5000-byte per-request limit)
- Calls the API for each chunk and concatenates the MP3 output

### `ITEMS` format
```python
# Verbs:  (word,     None,  present_sentence,  None)
# Nouns:  (word,     None,  sentence,           None)
# Others: (word,     None,  sentence,           None)
("einsteigen",  None,  "Ich steige in den Bus ein.",  None),
("der Zug",     None,  "Der Zug kommt um zehn Uhr.",  None),
("gerade",      None,  "Der Bus kommt gerade.",        None),
```

---

## One-time setup
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
gcloud services enable texttospeech.googleapis.com --project=YOUR_PROJECT_ID
```

## Render a lesson
```bash
make
```
Output: `Lektion-N.ssml` (SSML source) and `Lektion-N.mp3` (final audio).
