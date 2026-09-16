# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

Most of my questions are about a certain town, and the answer is usually in the section of that town's guide that matches the question. Therefore, I expect that at least 4 of my 5 test questions will have a chunk that contains the answer.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

The model is designed to provide accurate and reliable information from the corpus, so it's important that every answer includes a real reference to the source document. This ensures that users can verify the information and understand where it comes from.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

For the out-of-scope inquiries, the distances between the query and the documents are far as none of them have any actual terminology in common with a travel guides. This indicates that the relevance threshold needs to be carefully established in order to differentiate between relevant and irrelevant items.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

When I look at 5 chunks, at least 4 of them should start and stop at a section break, nothing should be cut off mid-sentence, and each one should still carry both its `##` section heading and the town name from the top of the document.

**Why this target:**

Each guide in my corpus is already divided into sections such as "Getting there" and "When to go," and the entire paragraph under one of those topics typically provides the answer to a question. Therefore, rather than chunks that end at a certain character count, I want chunks that match the sections. I said 4 of 5 rather than all 5 because a few sections in my corpus are long enough that they may still have to be cut somewhere, and I would rather allow for one imperfect chunk than claim a perfect result I cannot guarantee. I want the town name kept as well as the section heading because nine of my guides use the exact same section names, so a "When to go" paragraph on its own could belong to any of them.


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

When I ask a question about something that appears exactly the same in multiple guides, the place I asked about must be included in the list of sources. I'll give it three tries, and at least two of them should be successful.

**Why this target:**

The identical phrases about money, phone signal, and the hospital may be found in the "Practical notes" section at the conclusion of each of my city guides. Because there are nine pieces that match about evenly, the algorithm may easily cite the incorrect town when I ask "do I need cash in Kestrelford," even if it sounds accurate. Because those sections are word-for-word identical by purpose, I assigned a score of two out of three instead of three. I anticipate that this will be the most difficult of my five criteria to meet.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
