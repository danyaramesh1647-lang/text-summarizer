"""Extractive text summarizer using NLTK.
Pipeline: sentence split -> preprocessing -> word frequencies ->
sentence scoring -> top sentences (kept in original order)."""
import re
from collections import Counter

import nltk

for pkg in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.data.find(("corpora/" if pkg == "stopwords" else "tokenizers/") + pkg)
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

STOP_WORDS = set(stopwords.words("english"))
RATIOS = {"short": 0.2, "medium": 0.35, "long": 0.5}


def _clean_words(sentence):
    """Lowercase, keep alphabetic words, drop stop words."""
    return [w for w in (t.lower() for t in word_tokenize(sentence))
            if w.isalpha() and w not in STOP_WORDS]


def summarize(text, length="medium"):
    text = re.sub(r"\s+", " ", text).strip()
    sentences = sent_tokenize(text)
    total = len(sentences)
    all_words = [w for w in word_tokenize(text) if w.isalpha()]

    stats = {"words": len(all_words), "sentences": total}
    if total <= 2:
        return {"summary": text, "sentences": sentences,
                "selected": list(range(total)), "keywords": [],
                "stats": {**stats, "summary_words": len(all_words),
                          "summary_sentences": total, "reduction": 0}}

    # 1. word frequencies (normalised by the most frequent word)
    freq = Counter(w for s in sentences for w in _clean_words(s))
    top = max(freq.values()) if freq else 1
    weights = {w: c / top for w, c in freq.items()}

    # 2. sentence scores (average word weight + bonus for the first sentence)
    scores = []
    for i, s in enumerate(sentences):
        words = _clean_words(s)
        score = sum(weights[w] for w in words) / len(words) if len(words) >= 3 else 0
        if i == 0:
            score *= 1.5
        scores.append(score)

    # 3. pick top N sentences, then restore original order
    n = max(1, round(total * RATIOS.get(length, 0.35)))
    best = sorted(range(total), key=lambda i: scores[i], reverse=True)[:n]
    selected = sorted(best)
    summary = " ".join(sentences[i] for i in selected)
    summary_words = len([w for w in word_tokenize(summary) if w.isalpha()])

    return {
        "summary": summary,
        "sentences": sentences,
        "selected": selected,
        "keywords": [w for w, _ in freq.most_common(5)],
        "stats": {**stats, "summary_words": summary_words,
                  "summary_sentences": len(selected),
                  "reduction": round((1 - summary_words / max(1, len(all_words))) * 100)},
    }