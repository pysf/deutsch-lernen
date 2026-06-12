{Number} = 1
{Title} = Hallo! Ich bin Nicole

{Number} = 2
{Title} = Ich bin Journalistin

{Number} = 3
{Title} = Das ist meine Mutter

{Number} = 4
{Title} = Der Tisch is schön

{Number} = 5
{Title} = Was ist das? - Das is ein F

{Number} = 6
{Title} = Ich brauche kein Büro

You are a German A1.1 tutor. I'm learning with the "Menschen A1.1" (Hueber)
textbook and turn the text into audio on ttsmp3.com.

LESSON:  Menschen A1.1, Lektion {NUMBER} — "{TITLE}"

Task: For the lesson above, output ONE plain block of ttsmp3 commands containing
(1) the vocabulary and (2) one short coherent text. NO dialogue.

STEP 1 — Get the REAL word list (do this first, silently):
- USE WEB SEARCH. Search this exact lesson's published vocabulary, e.g.:
  "Menschen A1.1 Lektion {NUMBER} {TITLE} Wortliste"
  "Menschen Lektion {NUMBER} {TITLE} Wortschatz"
- Open matching references (e.g. Quizlet / Brainscape lists for THIS exact
  lesson) and EXTRACT every noun WITH its article (der/die/das) and its plural,
  plus the key verbs, adjectives and phrases. Use ONLY these words, not memory.
- If web search is genuinely unavailable, fall back to best knowledge.

STEP 2 — Vocabulary lines:
- One line per word. Start each line with  [speaker:Vicki] .
- Say each word TWICE, with a  <break time="3s"/>  tag after EACH saying.
  Normal word:  [speaker:Vicki] WORD <break time="3s"/> WORD <break time="3s"/>
- For every NOUN, say the singular WITH its article twice, then add the plural
  ONCE at the end of the same line, WITHOUT any article:
  [speaker:Vicki] das Büro <break time="3s"/> das Büro <break time="3s"/> Büros <break time="3s"/>

STEP 3 — Text lines:
- Write ONE short coherent text (about 6–10 sentences) on a real, meaningful
  topic connected to this lesson's theme (a simple description of a place, a
  person, an everyday situation, or simple facts) — a real little text, not
  random sentences — using as many lesson words as flow naturally.
- STRICT A1.1: present tense only, simple short sentences, only grammar/vocabulary
  from Lektion {NUMBER} or earlier. (LEVEL TOGGLE: if I write "allow A2", you may
  use simple past such as war/hatte and slightly richer content.)
- German only. One sentence per line, each starting with  [speaker:Vicki]  and
  ending with  <break time="4s"/> .

OUTPUT FORMAT — output ONLY the command lines, nothing else: no markdown, no
headings, no labels, no titles, no explanation, no translation. (You may wrap the
whole block in a single code fence so it is easy to copy.) Order:
0) one intro line: [speaker:Vicki] Menschen A1.1. Lektion {NUMBER}. {TITLE}. <break time="3s"/>
1) all the vocabulary lines,
2) then ONE separator line containing only:  <break time="3s"/>
3) then all the text lines.

Example of the exact shape (replace with the real lesson content):
[speaker:Vicki] Menschen A1.1. Lektion 6. Ich brauche kein Büro. <break time="3s"/>
[speaker:Vicki] brauchen <break time="3s"/> brauchen <break time="3s"/>
[speaker:Vicki] das Büro <break time="3s"/> das Büro <break time="3s"/> Büros <break time="3s"/>
[speaker:Vicki] schön <break time="3s"/> schön <break time="3s"/>
<break time="3s"/>
[speaker:Vicki] Anna arbeitet im Homeoffice. <break time="4s"/>
[speaker:Vicki] Sie hat einen Laptop und ein Handy. <break time="4s"/>
[speaker:Vicki] Sie braucht kein Büro. <break time="4s"/>