"""Small, auditable scorer for the five committed evaluation questions.

The expected phrases live in ``questions.py`` and were written before the
evaluation results.  This scorer deliberately does one narrow thing: it checks
whether the generated answer contains that expected phrase after harmless
case, punctuation, and whitespace normalization.
"""

import re
import unicodedata


def _normalize(text: str) -> str:
    """Make formatting differences irrelevant without changing word order."""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"(?<=\d)\s*[-–—]\s*(?=\d)", " to ", text)
    text = re.sub(r"\b([ap])\.?\s*m\.?\b", r"\1m", text)
    text = re.sub(r"(?<=\d)(?=[a-z])", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Return whether the answer contains the pre-committed expected phrase."""
    del question, results  # Part of run_eval.py's scorer interface.
    expected = _normalize(expects)
    return bool(expected) and expected in _normalize(answer)
