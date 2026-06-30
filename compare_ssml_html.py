#!/usr/bin/env python3
"""
Compare each Lektion-N.html against its Lektion-N.ssml.
Lesson numbers are auto-detected from the files present in the directory.

Usage:
  python3 compare_ssml_html.py Menschen-A1.1
  python3 compare_ssml_html.py Menschen-A1.2
  python3 compare_ssml_html.py          # defaults to Menschen-A1.1
"""

import re
import sys
import unicodedata
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "Menschen-A1.1"
BASE = BASE.resolve()


# ---------------------------------------------------------------------------
# HTML extraction
# ---------------------------------------------------------------------------

def extract_html_vocab(html_path: Path):
    """
    Returns list of (display_word, first_sample_sentence).
    - For nouns: "der/die/das WORD" (text of .de excluding .plural and .pos spans)
    - For verbs/adj/adv: just the word text (excluding .pos spans)
    """
    text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    # Check if there is a vocab section
    wl = soup.find(class_="word-list")
    if not wl:
        return None  # No vocab section

    items = []
    for li in wl.find_all("li"):
        de_span = li.find(class_="de")
        if not de_span:
            continue

        # Remove .pos and .plural sub-spans to get clean word text
        de_clone = BeautifulSoup(str(de_span), "html.parser").find(class_="de")
        for rm in de_clone.find_all(class_=["pos", "plural"]):
            rm.decompose()
        word = de_clone.get_text(separator=" ").strip()
        # Collapse multiple spaces
        word = re.sub(r"\s+", " ", word)

        # First sample sentence (before " · " if multiple)
        sample_tag = li.find(class_="sample")
        if sample_tag:
            raw_sample = sample_tag.get_text().strip()
            first_sample = raw_sample.split(" · ")[0].strip()
        else:
            first_sample = ""

        items.append((word, first_sample))

    return items


# ---------------------------------------------------------------------------
# SSML extraction
# ---------------------------------------------------------------------------

def extract_ssml_entries(ssml_path: Path):
    """
    Returns list of (word, sentence).
    The word is the first <prosody rate="0.85"> content in each group.
    The sentence is the non-prosody voice line that follows the group.
    """
    text = ssml_path.read_text(encoding="utf-8")

    # We parse with BeautifulSoup (xml mode) or lxml-xml
    # The SSML uses <voice> elements and <prosody> elements
    # Pattern: 3 consecutive prosody elements (word repeated 3x) then a voice line (sentence)

    # Use regex to find all <prosody rate="0.85">...</prosody> and surrounding structure
    # Actually parse with BS4 html.parser (works fine for SSML-like XML)
    soup = BeautifulSoup(text, "html.parser")

    # Find all voice elements
    voices = soup.find_all("voice")

    entries = []
    i = 0
    while i < len(voices):
        v = voices[i]
        prosody = v.find("prosody")
        if prosody and prosody.get("rate") == "0.85":
            # This is the first repetition of a word
            word_raw = prosody.get_text().strip()
            # Remove trailing period if present (last of 3 repetitions has "word.")
            word = word_raw.rstrip(".")

            # Skip the next two prosody voice elements (repetitions 2 and 3)
            # Then find the sentence voice element
            # Count consecutive prosody voices starting from i
            prosody_count = 0
            j = i
            while j < len(voices) and voices[j].find("prosody"):
                prosody_count += 1
                j += 1

            # voices[j] should be the sentence voice (no prosody inside)
            if j < len(voices) and not voices[j].find("prosody"):
                sentence = voices[j].get_text().strip()
                entries.append((word, sentence))
                i = j + 1
            else:
                i += 1
        else:
            i += 1

    return entries


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def normalise(s: str) -> str:
    """Lowercase, collapse spaces, strip punctuation at edges."""
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def sentences_match(s1: str, s2: str) -> bool:
    """Return True if sentences are the same ignoring case/trailing punctuation/spaces."""
    def clean(s):
        s = s.strip().rstrip(".!?,;")
        s = re.sub(r"\s+", " ", s.lower())
        return s
    return clean(s1) == clean(s2)


# ---------------------------------------------------------------------------
# Main comparison
# ---------------------------------------------------------------------------

def compare_lesson(n: int):
    html_path = BASE / f"Lektion-{n}.html"
    ssml_path = BASE / f"Lektion-{n}.ssml"

    issues = []

    if not html_path.exists():
        return [f"  [MISSING] {html_path.name}"]
    if not ssml_path.exists():
        return [f"  [MISSING] {ssml_path.name}"]

    html_items = extract_html_vocab(html_path)
    ssml_entries = extract_ssml_entries(ssml_path)

    if html_items is None:
        issues.append("  [INFO] No .word-list in HTML (skipping HTML vocab check)")
        html_items = []

    html_count = len(html_items)
    ssml_count = len(ssml_entries)

    # Build lookup: normalised word -> list of (original_word, sentence) for SSML
    ssml_word_map = {}
    for word, sentence in ssml_entries:
        key = normalise(word)
        ssml_word_map.setdefault(key, []).append((word, sentence))

    # Build lookup for HTML
    html_word_map = {}
    for word, sentence in html_items:
        key = normalise(word)
        html_word_map.setdefault(key, []).append((word, sentence))

    # 1. Words in HTML but missing from SSML
    missing_from_ssml = []
    for key, vals in html_word_map.items():
        if key not in ssml_word_map:
            for word, _ in vals:
                missing_from_ssml.append(word)

    # 2. Words in SSML but not in HTML (skip header voice line if present)
    extra_in_ssml = []
    for key, vals in ssml_word_map.items():
        if key not in html_word_map:
            for word, _ in vals:
                extra_in_ssml.append(word)

    # 3. Sentence mismatches for matching words
    sentence_mismatches = []
    for key in html_word_map:
        if key in ssml_word_map:
            html_word, html_sentence = html_word_map[key][0]
            ssml_word, ssml_sentence = ssml_word_map[key][0]
            if not sentences_match(html_sentence, ssml_sentence):
                sentence_mismatches.append(
                    (html_word, html_sentence, ssml_sentence)
                )

    # Collect report lines
    lines = []
    lines.append(f"  HTML vocab items : {html_count}")
    lines.append(f"  SSML entries     : {ssml_count}")

    if missing_from_ssml:
        lines.append(f"  Words in HTML but MISSING from SSML ({len(missing_from_ssml)}):")
        for w in missing_from_ssml:
            lines.append(f"    - {w!r}")

    if extra_in_ssml:
        lines.append(f"  Words in SSML but NOT in HTML ({len(extra_in_ssml)}):")
        for w in extra_in_ssml:
            lines.append(f"    + {w!r}")

    if sentence_mismatches:
        lines.append(f"  Sentence mismatches ({len(sentence_mismatches)}):")
        for word, html_s, ssml_s in sentence_mismatches:
            lines.append(f"    Word: {word!r}")
            lines.append(f"      HTML : {html_s!r}")
            lines.append(f"      SSML : {ssml_s!r}")

    if not missing_from_ssml and not extra_in_ssml and not sentence_mismatches:
        lines.append("  [OK] No issues found.")

    total_issues = len(missing_from_ssml) + len(extra_in_ssml) + len(sentence_mismatches)
    return lines, total_issues


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    grand_total = 0

    lesson_nums = sorted(
        int(p.stem.split("-")[1])
        for p in BASE.glob("Lektion-*.html")
    )
    for n in lesson_nums:
        print(f"\n{'='*60}")
        print(f"Lektion {n}")
        print(f"{'='*60}")

        result = compare_lesson(n)
        if isinstance(result, list):
            # Error path (list of strings)
            for line in result:
                print(line)
        else:
            lines, issues = result
            for line in lines:
                print(line)
            grand_total += issues

    print(f"\n{'='*60}")
    print(f"SUMMARY: Total issues across all lessons: {grand_total}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
