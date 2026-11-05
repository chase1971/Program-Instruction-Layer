# Searchable Notes Project

> **Status: idea only, nothing built (written 2026-11-03).** Chase said: "let's start the
> searchable notes project" when he wants to begin. Start at "Build order" below.

## The problem

Chase writes class notes in Word and exports PDFs. Students fill in blank copies during the
lesson (paper, tablet, or nothing). When studying, or when a quiz problem trips them up, they
can't tell which section or page the idea came from.

Related issue: many students don't print the notes. Problems are pre-printed on the handouts to
save copying time, so non-printers fall behind.

## Constraints (from Chase)

- Must work for everyone: paper, tablet, phone only, no Word, no tablet, no computer.
- Notes are PDFs on Google Drive, linked from D2L. Source files are Word. Ink keys are flattened
  into the PDF.
- Wants eventually a chatbot in D2L. This project is the engine that chatbot would sit on.
- Possible separate fix for non-printers: bookstore course-pack bundle. Downsides: can't edit
  mid-term (use an errata sheet on the portal), needs department and bookstore approval, cost to
  students. Not part of the build.

## Design

**Home:** a "Find in notes" page in the student portal (Netlify). D2L links to it. Phone browser,
no login. PDFs hosted with the portal, because Google Drive links don't reliably jump to a page
on mobile. Open a result with `file.pdf#page=N`.

**Search runs against two things per page:** the real extracted PDF text, and an AI-written
**index card** for that page.

**Index card (written once offline, not per search):**
- Topics on the page in plain words
- Kinds of problems covered, including ones worded differently from the page
  ("at least 1 of something", "exactly k of something", "without replacement")
- Phrases a student might type that the page never says
- Formulas written out in words ("complement rule: 1 minus P(none)")

Chase spot-checks cards for a few pages, since AI summaries can drift.

**Result shows:** section, page number, short snippet of why it matched, tap to open the PDF at
that page.

**Matching levels:**
1. Exact phrase
2. Keyword with typo tolerance
3. Meaning match (embeddings or an AI call) using the index cards. Later.

**Photo of a problem (later):** phone OCR reads only the wording, not equations. Equations are
ignored; the sentence goes into the same search.

## Test case that already works

Student types "probability of exactly 2 clubs". Exact hit: 8.1 - 8.2 Class Notes, page 2,
problem 5 ("exactly 2 a..."). Related hits: 7.3 - 7.4 page 4 ("Exactly" Problems, clubs),
8.3 page 2 ("At Least").

## What was verified

Folder: `C:\Users\chase\My Drive\M1324\Unit 3\Class Notes`. Five PDFs, 23 pages: 7.1 (5 pages),
7.2 (3), 7.3 - 7.4 (4), 8.1 - 8.2 (6), 8.3 (5). Every page has real extractable text
(about 400 to 1,600 characters each), so no OCR is needed for the notes themselves.
Section number comes from the file name. PyMuPDF (`fitz`) is installed and reads them.
Handwritten keys were not checked. Ink is a picture, so search cannot see it. If a key matters
for search, add a short typed tag to the page.

## Build order

1. Generate index cards for the five Unit 3 PDFs into a scratch file. Chase reads a sample
   before anything goes into the portal.
2. Search page in the portal returning section and page.
3. Open the PDF at the right page from a result.
4. Photo input (OCR).
5. Chat box on the same engine, then embed in D2L.

Later: index homework and quiz problems too, and tag each with "Notes: 3.4, p. 27" so a missed
problem points back to the notes.

## Rules that apply when building

- Portal conventions: read `School Scrips/student-portal/AGENTS.md` first. Service layer for API
  calls, small buttons, no ephemeral "success" text, no em dashes in student-facing text.
- Never deploy to Netlify unless Chase says so in that message.
- Nothing visible on Chase's screen without asking. Verify headlessly and hand off with a
  statement.
- Grep the portal for an existing search or PDF-hosting mechanism before adding one.
