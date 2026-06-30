# HTML Vocabulary Page — Prompt & Spec

## What this produces
A self-contained offline HTML vocabulary page for one lesson of "Menschen A1.1"
(Hueber). One file per lesson: `Lektion-N.html`.

---

## Page structure

### Head / meta
```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lektion {N} — {TITLE}</title>
  <style>…</style>
</head>
```

### Required CSS (copy verbatim)
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  Helvetica, Arial, sans-serif; background: #fff; color: #1a1a1a;
  font-size: 18px; line-height: 1.6; padding: 2rem 1.25rem;
  max-width: 640px; margin: 0 auto; }
h1 { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.35rem; }
.legend { font-size: 0.78rem; color: #888; margin-bottom: 0.5rem; }
.legend span { margin-right: 1rem; }
.der { color: #1d4ed8; } .die { color: #db2477; } .das { color: #059669; }
h2 { font-size: 0.85rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.09em; color: #aaa; margin-bottom: 1.2rem; }
section { margin-bottom: 3rem; }
.word-list { list-style: none; }
.word-list li { padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; }
.word-list li:last-child { border-bottom: none; }
.word-row { display: flex; justify-content: space-between;
  align-items: baseline; gap: 1rem; }
.de { font-size: 1rem; font-weight: 500; }
.plural { font-size: 0.75rem; color: #bbb; font-weight: 400;
  margin-left: 0.35rem; }
.en { font-size: 0.85rem; color: #999; text-align: right; flex-shrink: 0; }
.sample { font-size: 0.82rem; color: #bbb; font-style: italic;
  margin-top: 0.1rem; }
.back-link { display: block; font-size: 0.78rem; color: #bbb;
  text-decoration: none; margin-bottom: 1.5rem; }
.back-link:hover { color: #888; }
.mp3-link { display: block; font-size: 0.78rem; color: #bbb;
  text-decoration: none; margin-bottom: 2.5rem; }
.mp3-link:hover { color: #888; }
.verb-reg { color: #d97706; }
.verb-irr { color: #7c3aed; }
.perfekt { font-size: 0.75rem; color: #bbb; font-weight: 400;
  margin-left: 0.4rem; }
.pos { font-style: italic; font-size: 0.72rem; color: #bbb;
  font-weight: 400; margin-left: 0.35rem; }
```

### Body order
1. Back-link
2. `<h1>` title
3. Legend `<p>`
4. MP3 download link
5. `<section>` Wortschatz

```html
<a class="back-link" href="index.html">← Alle Lektionen</a>
<h1>Lektion {N} — {TITLE}</h1>
<p class="legend">
  <span><span class="der">■</span> der (m)</span>
  <span><span class="die">■</span> die (f)</span>
  <span><span class="das">■</span> das (n)</span>
  <span><span class="verb-reg">■</span> reg.</span>
  <span><span class="verb-irr">■</span> irr.</span>
  <span><span class="pos">(t)</span> transitiv · <span class="pos">(i)</span> intransitiv · <span class="pos">(adj)</span> Adjektiv · <span class="pos">(adv)</span> Adverb</span>
</p>
<a class="mp3-link" href="Lektion-{N}.mp3" download>⬇ Audio herunterladen</a>
```

---

## Word entry patterns

### Verb (regular)
```html
<li>
  <div class="word-row">
    <span class="de">
      <span class="verb-reg">wohnen</span>
      <span class="perfekt"> · hat gewohnt</span>
      <span class="pos" title="intransitiv">(i)</span>
    </span>
    <span class="en">to live</span>
  </div>
  <p class="sample">Ich wohne in Berlin. · Ich habe in Berlin gewohnt.</p>
</li>
```

### Verb (irregular, transitive)
```html
<li>
  <div class="word-row">
    <span class="de">
      <span class="verb-irr">nehmen</span>
      <span class="perfekt"> · hat genommen</span>
      <span class="pos" title="transitiv (Akkusativobjekt)">(t)</span>
    </span>
    <span class="en">to take</span>
  </div>
  <p class="sample">Ich nehme die S-Bahn. · Ich habe die S-Bahn genommen.</p>
</li>
```

### Noun
```html
<li>
  <div class="word-row">
    <span class="de">
      <span class="der">der Zug</span>
      <span class="plural">Pl. Züge</span>
      <span class="pos" title="maskulin">(m)</span>
    </span>
    <span class="en">train</span>
  </div>
  <p class="sample">Der Zug kommt um zehn Uhr. · Ich nehme den Zug.</p>
</li>
```
For nouns with no plural (e.g. *das Gepäck*), omit the `.plural` span.

### Adjective
```html
<li>
  <div class="word-row">
    <span class="de">neu<span class="pos" title="Adjektiv">(adj)</span></span>
    <span class="en">new</span>
  </div>
  <p class="sample">Das Buch ist neu.</p>
</li>
```

### Adverb / particle / phrase
```html
<li>
  <div class="word-row">
    <span class="de">gerade<span class="pos" title="Adverb">(adv)</span></span>
    <span class="en">right now / just</span>
  </div>
  <p class="sample">Der Bus kommt gerade.</p>
</li>
```

---

## Sample sentence rules

| Word type | Sentences | Format |
|-----------|-----------|--------|
| Verb | 2 — present · Perfekt | `Ich esse Brot. · Ich habe Brot gegessen.` |
| Noun | 2 — nominative · accusative | `Der Zug kommt. · Ich nehme den Zug.` |
| Adj / adv / other | 1 | `Das Buch ist neu.` |

- Both sentences on **one line**, separated by ` · `
- A1.1 / A1.2 level only — present or Perfekt tense, short sentences
- Show the article change (der → den, die → die, das → das) in the accusative sentence

---

## POS marker scheme (`.pos` tag)

The `.pos` marker appears **after** the word (after the Perfekt span for verbs,
after the plural span for nouns). It is muted italic, small, and has a German
`title` tooltip.

| Word type | Marker | `title` attribute |
|-----------|--------|-------------------|
| Transitive verb | `(t)` | `transitiv (Akkusativobjekt)` |
| Intransitive verb | `(i)` | `intransitiv` |
| Adjective | `(adj)` | `Adjektiv` |
| Adverb | `(adv)` | `Adverb` |
| Noun — maskulin | `(m)` | `maskulin` |
| Noun — feminin | `(f)` | `feminin` |
| Noun — neutrum | `(n)` | `neutrum` |

---

## Color scheme

| Element | Color | Hex |
|---------|-------|-----|
| der (maskulin) | blue | `#1d4ed8` |
| die (feminin) | red/pink | `#db2477` |
| das (neutrum) | green | `#059669` |
| Regular verb | orange | `#d97706` |
| Irregular verb | purple | `#7c3aed` |
| Perfekt / plural / POS | muted grey | `#bbb` |

---

## After saving the HTML
Update `index.html` — add to `<ul class="lektion-list">` if not already listed:
```html
<li><a href="Lektion-{N}.html"><span class="lektion-num">{N}</span>{TITLE}</a></li>
```
