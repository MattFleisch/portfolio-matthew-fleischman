from typing import List, Dict
from transformers import pipeline
import re

# Load BART once at import
_bart = pipeline("summarization", model="facebook/bart-large-cnn")


def _clean(text: str) -> str:
    """
    Cleans input text by:
      - removing zero-width characters
      - collapsing multiple spaces/newlines into a single space
      - trimming leading/trailing whitespace

    Args:
        text (str): The text to clean.

    Returns:
        str: Cleaned text.
    """
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)  # remove invisible chars
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _chunk(text: str, max_chars: int = 3000) -> list[str]:
    """
    Splits text into reasonably sized chunks based on sentence boundaries,
    so the summarizer can process long articles without hitting token limits.

    Args:
        text (str): The text to split.
        max_chars (int): Maximum number of characters per chunk.

    Returns:
        list[str]: List of text chunks.
    """
    text = _clean(text)
    if len(text) <= max_chars:
        return [text]

    chunks, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        cut = text.rfind(". ", start, end)  # cut at last sentence boundary
        if cut == -1 or cut <= start + int(0.6 * max_chars):
            cut = end
        chunks.append(text[start:cut].strip())
        start = cut + 1
    return chunks


def _lengths_for_chunk(chunk: str) -> tuple[int, int]:
    """
    Dynamically calculates max_length and min_length for summarization
    based on the length of a given chunk.

    Args:
        chunk (str): The chunk of text to summarize.

    Returns:
        tuple[int, int]: (max_length, min_length) for generation.
    """
    words = len(chunk.split())
    if words < 40:
        # For very short text, generate just 1–2 sentences
        max_len = min(60, max(24, int(words * 0.9)))
        min_len = min(30, max(12, int(words * 0.5)))
    else:
        # For typical news-length text
        max_len = min(150, max(60, int(words * 0.35)))
        min_len = min(80, max(40, int(words * 0.18)))

    if min_len >= max_len:
        min_len = max(10, max_len - 10)
    return max_len, min_len


def _summarize_chunk(chunk: str) -> str:
    """
    Summarizes a single chunk of text using BART.

    Args:
        chunk (str): The chunk of text.

    Returns:
        str: Summarized chunk.
    """
    max_len, min_len = _lengths_for_chunk(chunk)

    # If the chunk is too short, return it directly
    if len(chunk.split()) < 25:
        return chunk

    out = _bart(
        chunk,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        num_beams=4,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        early_stopping=True,
    )[0]["summary_text"]

    return _clean(out)


def _summarize_long_text(text: str) -> str:
    """
    Handles summarization for long text by:
      1. Splitting into chunks
      2. Summarizing each chunk
      3. Optionally re-summarizing all partial summaries into a final summary

    Args:
        text (str): The article text.

    Returns:
        str: Final summary.
    """
    chunks = _chunk(text)
    partials = [_summarize_chunk(c) for c in chunks]
    joined = " ".join(partials)

    if len(partials) == 1 or len(joined) < 1800:
        return joined

    max_len, min_len = _lengths_for_chunk(joined)
    final = _bart(
        joined,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        num_beams=4,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        early_stopping=True,
    )[0]["summary_text"]

    return _clean(final)


def summarize_articles(articles: List[Dict], *_args, **_kwargs) -> List[str]:
    """
    Summarizes a list of articles.

    Args:
        articles (list[dict]): Articles to summarize. Each dict should contain
                               a "text" key with article content.
        *_args (Any): Ignored, kept for API compatibility.
        **_kwargs (Any): Ignored, kept for API compatibility.

    Returns:
        list[str]: Summaries for each article.
    """
    summaries: List[str] = []
    for art in articles:
        text = _clean(art.get("text") or "")
        if not text:
            summaries.append("[No article text available]")
            continue
        try:
            summaries.append(_summarize_long_text(text))
        except Exception as e:
            summaries.append(f"[Error summarizing: {e}]")
    return summaries
