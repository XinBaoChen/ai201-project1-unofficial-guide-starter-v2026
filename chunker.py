"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

# A section shorter than this is a heading with nothing useful under it. The
# starter's chunker produced a 24-character chunk on this corpus; anything
# that small can't answer a question but still competes for a retrieval slot.
MIN_SECTION_CHARS = 60


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_on_headings(text: str) -> tuple[str, list[str]]:
    """
    Pull the `# Title` line off the top and split the rest on `## ` headings.

    Returns the title (without its `#`) and a list of sections, each one still
    carrying its own `## Heading` line.
    """
    title = ""
    body = text

    first_line, _, rest = text.partition("\n")
    if first_line.startswith("# ") and not first_line.startswith("## "):
        title = first_line[2:].strip()
        body = rest

    # Split before any line that begins with "## ". The lookahead keeps the
    # heading attached to the section it introduces instead of discarding it.
    parts = [p.strip() for p in re.split(r"\n(?=## )", body) if p.strip()]

    # The text above the first heading is an intro paragraph with no heading of
    # its own. Left alone it becomes a chunk that can't be attributed to a
    # section — and in one case (guide_accessibility.md) a pure preamble that
    # answers nothing. Dropping it isn't an option either: the populations of
    # Brightwater and Halden Bay appear nowhere else in the corpus. So it gets
    # merged into the first real section instead.
    if len(parts) > 1 and not parts[0].startswith("## "):
        intro = parts.pop(0)
        parts[0] = f"{intro}\n\n{parts[0]}"

    return title, parts


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?

    MY STRATEGY — one `##` section per chunk.

    Every guide in city_guides is already divided into labelled sections
    ("Getting there", "Eat and drink", "When to go"), and the answer to a
    question is the paragraph under one of those headings. So the section, not
    a character count, is the unit worth keeping whole. No overlap is needed:
    overlap exists to repair sentences a splitter broke, and this one never
    breaks any.

    Each chunk keeps the document's `# Title` line, because nine of the
    fourteen guides are towns using identical section names — a "When to go"
    paragraph on its own could belong to any of them.

    The intro paragraph above the first heading is merged into the first
    section rather than kept as a chunk of its own — see `_split_on_headings`.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        title, sections = _split_on_headings(doc.text)

        index = 0
        for section in sections:
            if len(section) < MIN_SECTION_CHARS:
                continue  # a heading with nothing useful under it

            text = f"{title}\n\n{section}" if title else section

            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
            index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
