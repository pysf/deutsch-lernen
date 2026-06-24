You are a German A1.1 tutor and a front-end developer. Below is a plain block of
ttsmp3 commands for one lesson of "Menschen A1.1". Turn it into ONE minimal,
self-contained, mobile-friendly HTML vocabulary page.

LESSON:  Lektion {NUMBER} — "{TITLE}"   (use this for the page heading)

USE THE PASTED COMMANDS AS THE ONLY SOURCE OF CONTENT. Do not add or remove
German words, and do not change the German. Your only addition is English
translations.

How to read the commands:
- Ignore every  [speaker:...]  and  <break .../>  tag.
- The block has TWO parts, split by a line that contains ONLY a <break/> tag:
  * BEFORE the separator = vocabulary. Each of these lines repeats a word and
    uses 3-second breaks. The word is repeated — keep it ONCE. For a noun the
    line is "ARTICLE NOUN ... ARTICLE NOUN ... PLURAL": the singular is
    "ARTICLE NOUN" and the final token is the plural (no article).
  * AFTER the separator = the text. Each of these lines is one full German
    sentence (they use 4-second breaks). Together they form one paragraph.

Build the page with these requirements:
- A single standalone .html file. One <style> tag, no external libraries, fonts,
  scripts, or images. Must work offline.
- Include <meta name="viewport" content="width=device-width, initial-scale=1">.
- VERY MINIMAL design: white background, near-black text, clean system font
  stack, lots of whitespace, one column, no boxes/shadows/borders (a thin light
  divider between words at most). Comfortable font size for phone reading.
- NAVIGATION: immediately before the <h1>, add a small muted back-link:
    <a class="back-link" href="index.html">← Alle Lektionen</a>
  Style (.back-link): display:block; font-size:0.78rem; color:#bbb;
  text-decoration:none; margin-bottom:1.5rem. Hover: color:#888.
- Title at top: "Lektion {NUMBER} — {TITLE}".
- GENDER COLORS for nouns, and VERB COLORS for verbs — the only colors on the page.
  Noun gender: der -> blue (#1d4ed8),  die -> red (#db2777),  das -> green (#059669).
  Verb type: regular -> orange (#d97706),  irregular -> purple (#7c3aed).
  Add one small, quiet legend line under the title showing all five symbols. Legend margin-bottom: 0.5rem.
  Legend format: der (m) · die (f) · das (n) · reg. · irr. — each preceded by its colored ■ square.
- AUDIO DOWNLOAD: immediately after the legend </p>, add:
    <a class="mp3-link" href="Lektion-{NUMBER}.mp3" download>⬇ Audio herunterladen</a>
  Style (.mp3-link): display:block; font-size:0.78rem; color:#bbb;
  text-decoration:none; margin-bottom:2.5rem. Hover: color:#888.
- "Wortschatz" section: for each word, one simple row:
    * the German word (nouns: article + noun in the gender color; plural in small
      muted text after it, e.g. "Pl. Büros"; non-nouns in plain near-black)
    * for VERBS: wrap the infinitive in a colored span (verb-reg or verb-irr),
      then add the Perfekt form in small muted text after it, e.g.:
        regular: <span class="verb-reg">wohnen</span><span class="perfekt"> · hat gewohnt</span>
        irregular: <span class="verb-irr">kommen</span><span class="perfekt"> · ist gekommen</span>
      CSS: .verb-reg { color: #d97706; }  .verb-irr { color: #7c3aed; }
           .perfekt { font-size: 0.75rem; color: #bbb; font-weight: 400; margin-left: 0.4rem; }
    * its English translation in small muted text
- "Text" section: the German sentences as one paragraph, and under it the full
  English translation in small muted text.
- Good contrast, accessible, no Farsi or any language besides German and English.

OUTPUT: return only the full HTML document, starting with <!DOCTYPE html>.

AFTER SAVING Lektion-{NUMBER}.html: update index.html — add the following line
to the <ul class="lektion-list"> if this lektion is not already listed:
  <li><a href="Lektion-{NUMBER}.html"><span class="lektion-num">{NUMBER}</span>{TITLE}</a></li>

--- PASTE THE LESSON .txt BELOW THIS LINE ---

{PASTE THE FULL CONTENT OF Lektion-N.txt HERE}