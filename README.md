# The Unofficial Guide

XinBao Chen , I picked city_guides as my corpus.

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.
 Milestone 5. -->


I picked the `city_guides` corpus: fourteen long travel guides to a fictional region — nine on individual towns and villages (Brightwater, Halden Bay, Kestrelford, Corry Vale and others), plus five that cut across all of them on eating, walking, transport, seasons and accessibility. My system answers practical trip-planning questions: how to reach a town, how to get around once you're there, where to eat and when kitchens stop serving, and which month to visit. I love trying new food wherever I travel, so a corpus built around where to eat and how to get there was the obvious one for me to learn on.




## Chunking Strategy

**Chunk size:** No fixed number — one `##` section per chunk. In practice that
comes out at 190 to 885 characters, 356 on average, across 84 chunks.

**Overlap:** 0

My documents are long sectioned guides, not short posts. Every guide is already
divided into labelled sections — "Getting there", "Eat and drink", "When to go"
— and when I read them in Milestone 1 I noticed that the answer to a question is
almost always the whole paragraph under one of those headings, not a single
sentence. So the section, not a character count, is the unit worth keeping
whole. I split on any line starting with `## ` instead of picking a number.

The starter's fixed 800-character windows showed me why that matters. Indexing
with `fallback_split` gave me 51 chunks with the longest at exactly 800
characters, which is the giveaway: it wasn't stopping where the text stopped, it
was stopping where it ran out of room. One chunk ended mid-word on "The station
is a 15-" and another on "bread made from the flour grou". It also left a
24-character chunk behind — the leftover tail of a document that didn't divide
evenly by 800. After switching to sections I get 84 chunks, longest 885, and
that 885 is set by how long one real section happens to be rather than by a
setting. 

Overlap is 0 because overlap exists to repair sentences a splitter broke, and
this one never breaks any.

One thing I added that isn't about size: every chunk keeps the document's
`# Title` line on top. Nine of my fourteen guides are towns using identical
section names, and the "Practical notes" paragraph is word-for-word the same in
all nine, so without the town name a chunk about Corry Vale is indistinguishable
from one about Marchwood.

**Where I changed my mind:** my first version split on headings and nothing
else, which left ten chunks that were intro paragraphs with no `##` heading at
all — the text sitting between a document's title and its first section. One of
them (`guide_accessibility.md#0`) was pure preamble: it announced that the guide
would be honest about difficult places and then stopped, so it could not answer
anything on its own.

My first instinct was to delete them by raising the minimum length from 60 to
200 characters. I'm glad I checked first, because when I ran my population
question the answer came back from `guide_halden_bay.md#0` — one of those intro
chunks. "A working fishing port of 8,000" is in the intro and nowhere else in
the corpus, and the same is true of Brightwater's 40,000. Raising the threshold
would have deleted the chunk that answered my own test question.

So instead of dropping the intros I merged each one into its document's first
section. That took the count from 94 chunks to 84, removed all ten headless
chunks, and lost nothing. It also pushed the longest chunk from 760 to 885
characters, which I decided was an acceptable price for keeping the facts.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

All five printed by `python app.py chunks -n 5` after the intro-merge change.

**Chunk 1 — mobility** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

This is the chunk that used to be the bare preamble. After the merge it carries
three towns' worth of real detail, and it is also my longest chunk at 885
characters — the cost of the change, visible in one place.

**Chunk 2 — Corry Vale** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3 — Givens Mill** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
Givens Mill

## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4 — Kestrelford** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
Kestrelford

## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.
```

**Chunk 5 — Pellew Sands** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
Pellew Sands

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

Chunk 5 is the paragraph that is word-for-word identical in all nine town
guides. The only thing telling it apart from the other eight is the `Pellew
Sands` line my chunker puts on top, which is what criterion 5 is testing.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** What is the population of Halden Bay?

**Answer:**

```
  (best distance 0.386, cutoff 0.6)

The population of Halden Bay is 8,000 (from guide_halden_bay.md).

Sources retrieved: guide_halden_bay.md
```

Produced by `python app.py ask "What is the population of Halden Bay?"` with the
response cache off. The gate line shows it passed at 0.386 against the 0.6
cutoff, and the answer names its file. The figure is correct — `guide_halden_bay.md`
opens with "a working fishing port of 8,000" — and it comes from the intro
paragraph, which is the chunk my first chunker would have thrown away.

**My relevance cutoff:**

**0.6** — the value `THRESHOLD` already had in `config.py`. I kept it, but I
only know it is right because I measured, and I would have moved it if the
numbers had said so.

The two groups came out cleanly separated, with no overlap at all:

```
in corpus       0.179 ─── 0.386
                          gap: 0.428 wide
out of scope                        0.814 ─── 0.992
```

The gap runs from 0.386 to 0.814 and its midpoint is 0.600, which is where the
default already sat. Anything from roughly 0.45 to 0.75 would give the same
verdict on all ten questions, so the cutoff has a wide margin on both sides
rather than being balanced on an edge. I read that as the embeddings separating
travel-guide language from everything else very easily — my out-of-scope
questions are about Mongolia, diesel engines, the World Cup, ibuprofen and Rust,
and none of them share real vocabulary with a guide about where to eat.

All ten distances, from `python app.py retrieve "..."`:

| Question | In corpus? | Best distance |
|---|---|---|
| What time does the local bus service at Brightwater stop? | Yes | 0.281 |
| What time do kitchens in Brightwater stop serving? | Yes | 0.343 |
| What are some good months to visit Halden Bay? | Yes | 0.179 |
| What is the population of Halden Bay? | Yes | 0.386 |
| What is the nearest hospital to Halden Bay? | Yes | 0.347 |
| What is the capital of Mongolia? | No | 0.848 |
| How do I change the oil in a diesel engine? | No | 0.908 |
| Who won the 1994 World Cup? | No | 0.992 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.818 |
| How do I write a for loop in Rust? | No | 0.814 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I asked Claude to help me justify criterion 3's target, and it pointed out that my five out-of-scope questions share no vocabulary at all with travel guides, so their distances should land well clear of the cutoff — I reworded that into my own explanation. When I later ran the criteria self-check past it, it told me not to change criterion 3 because there's nothing in it to interpret: the gate is a number comparison and the refusal is a fixed string. The one thing it flagged was that the word "clearly" only holds because my five out-of-scope questions are fixed, so I'm leaving them alone rather than swapping in borderline ones.

**2.**
I asked Claude to construct the chunking code from my notes, keeping the town name at the top and creating one chunk for each `##` part. It worked, but when I performed the "what question could this chunk answer" exercise on the output, I discovered ten chunks that were simply headless intro paragraphs, and one of them (`guide_accessibility.md#0`) was just a preamble with no answers in it. Claude's version had a 60-character minimum that was too low to catch them, and its suggestion was to either raise that to 200 or leave them and call it a known limitation. I didn't like either: raising it would have deleted `guide_halden_bay.md#0`, which is the only chunk holding the population figure one of my own test questions asks for. So I had it merge each intro into the document's first section instead. That took me from 94 chunks to 84, removed all ten headless chunks, and cost me nothing except a longer maximum chunk (760 to 885 characters). I re-indexed and re-measured my distances afterwards, which is why the numbers above differ from my first run.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

Evidence: `results/run_2026-09-23_1439_before.md`, produced by
`run_eval.py::main`. Three passes per question, caching off. `scorer.py` does
not exist yet, so the per-question cells came out blank and I judged each
criterion myself by reading the fifteen answers.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks hold one complete section | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Sources name the town I asked about | 2 of 3 | pass | pass | pass | MET |

Criteria 1, 3 and 4 give the same number in all three columns, and that is
correct rather than lazy: retrieval is deterministic, the gate is a comparison
against a fixed number, and chunking is a pure function of the documents.
Criterion 2 is the one that could have moved between runs, because it depends
on the model following an instruction — it didn't move.

### Real output — criterion 1

Every question's answer text appears in the chunks that came back. This is the
clearest case, from `store.py::search` via `run_eval.py::main`:

```
### What is the population of Halden Bay? — run 1

- Best distance: 0.3864 (passed the gate)
- Sources retrieved: guide_halden_bay.md

The population of Halden Bay is 8,000.

Source: guide_halden_bay.md
```

`guide_halden_bay.md` opens with "a working fishing port of 8,000", so the
retrieved chunk genuinely contained the answer rather than the model supplying
it from elsewhere.

### Real output — criterion 2

All fifteen answers named a file. Three consecutive runs of the same question,
showing the citation format drifting while the citation itself never
disappeared — produced by `generate.py::answer_from_chunks`:

```
run 1: The local bus service at Brightwater runs until 7 pm and stops entirely on Sundays (guide_brightwater.md).

run 2: The local bus service at Brightwater runs until 7pm and stops entirely on Sundays.

       Source: guide_brightwater.md

run 3: The local bus service at Brightwater runs until 7pm and stops entirely on Sundays (*guide_brightwater.md*).
```

Three different formats — inline parentheses, a separate Source line, and
italics — for the same fact. Worth noting because a scorer that looks for one
exact format would mark two of these wrong.

### Real output — criterion 3

Produced by `run_eval.py::check_out_of_scope` against `gate.py::check`, cutoff
0.6. Refused 5 of 5, and no refused question reached the model:

```
| Out-of-scope question                                       | Best distance | Gate    |
| What is the capital of Mongolia?                            | 0.848         | refused |
| How do I change the oil in a diesel engine?                 | 0.908         | refused |
| Who won the 1994 World Cup?                                 | 0.992         | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.818         | refused |
| How do I write a for loop in Rust?                          | 0.814         | refused |
```

The closest of the five was 0.814 against a 0.6 cutoff — not one of them came
near passing.

### Real output — criterion 4

Sampled five chunks across the corpus from `chunker.py::split_documents`:

```
guide_accessibility.md#0     heading=True title=True ends_clean=True
guide_eating.md#2            heading=True title=True ends_clean=True
guide_halden_bay.md#4        heading=True title=True ends_clean=True
guide_pellew_sands.md#4      heading=True title=True ends_clean=True
guide_walking.md#3           heading=True title=True ends_clean=True
```

5 of 5 against a target of 4 of 5. I also checked all 84 rather than just the
sample: no chunk ends mid-sentence and none is missing its heading.

### Real output — criterion 5

"What is the nearest hospital to Halden Bay?" is the test for this, because the
answer lives in the `## Practical notes` paragraph that is word-for-word
identical in all nine town guides. Three runs, from
`run_eval.py::main`:

```
run 1  Sources retrieved: guide_accessibility.md, guide_halden_bay.md
       The nearest full hospital to Halden Bay is in Brightwater (guide_halden_bay.md).

run 2  Sources retrieved: guide_accessibility.md, guide_halden_bay.md
       The nearest full hospital to Halden Bay is in Brightwater (guide_halden_bay.md).

run 3  Sources retrieved: guide_accessibility.md, guide_halden_bay.md
       The nearest full hospital to Halden Bay is in Brightwater (guide_halden_bay.md).
```

`guide_halden_bay.md` is in the sources every time, and the answer cites it
rather than one of the other eight towns carrying the same sentence. 3 of 3
against a target of 2 of 3.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | I read all fifteen answers and checked each fact against its source file. Every one was present in a chunk that came back, so 5 of 5 against a target of 4 of 5. Nothing was close enough to argue about. |
| 2 | Every answer names a source | MET | I counted filenames in all fifteen answers and every one named at least one. I scored the citation written inside the answer text, not the `Sources retrieved:` line the program prints by itself — that line appears no matter what, and counting it would have made this criterion impossible to fail. |
| 3 | Gate stops out-of-corpus questions | MET | `run_eval.py::check_out_of_scope` refused 5 of 5. The closest out-of-scope question scored 0.814 against a 0.6 cutoff, so none of them were near the line. |
| 4 | Chunks hold one complete section | MET | I sampled five chunks and checked each for a `##` heading, a title line, and an ending on real punctuation. 5 of 5. I then checked all 84 rather than trust a sample of five, and none of them ends mid-sentence. |
| 5 | Sources name the town I asked about | MET | The hospital question is the test for this, because its answer is the paragraph repeated word-for-word across all nine town guides. `guide_halden_bay.md` was in the sources and cited in the answer on all three runs, so 3 of 3 against a target of 2 of 3. |

**The number that surprised me** was criterion 5 going 3 for 3. I wrote that
criterion expecting it to fail — nine chunks carrying an identical paragraph,
and the system has to pick the right one. It never got it wrong. Reading the
output, the reason is the town name my chunker puts at the top of every chunk:
the question asks about Halden Bay and only one of the nine copies has
`Halden Bay` on it.

**Where I nearly read the numbers generously:** criterion 2. My first instinct
was to look at the `Sources retrieved:` line, which is right there in the output
and present on every single answer. Scored that way this criterion is a
formality — it passes even if the model says nothing about where its answer came
from. I scored the in-answer citation instead, which is the thing the criterion
was actually meant to be about. It still passed 15 out of 15, but it passed for
a reason rather than by construction.

I am not revising any criterion. All five were measurable as written, and I
checked each one the same way three times. The one I would have considered
revising is criterion 2, since "names at least one source document" doesn't say
*which* of the two source lines counts — but I was able to resolve that by
choosing the stricter reading and applying it consistently, which makes it an
ambiguity I worked around rather than a criterion I couldn't measure.

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
