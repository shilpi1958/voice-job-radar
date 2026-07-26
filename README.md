# voice job radar

A job search that works for someone who doesn't type or read English
confidently — not a translate button bolted onto an English-first app.

## The problem, stated precisely

Most job search tools assume you can type a query in English and read the
results. That assumption excludes a huge number of real job seekers —
especially tier-2/3 and blue-collar candidates — who search by voice, in
Hindi, Kannada, Tamil, and dozens of other languages, because typing in a
second language is the actual barrier, not intent or ability to do the job
itself.

"Add translation" undersells what's actually broken. Pulled apart, an
English-first product puts up **four distinct barriers**, and each one needs
its own fix — solving one doesn't solve the others.

## The four-barrier framework

**1. Input barrier** — can't type/read English well enough to search.
You know what job you want. You just can't type it in English.
→ **Speak your search, in your own language.**

**2. Comprehension barrier** — can't understand what the product hands back.
Correct English output is still opaque if you're not fluent in it —
technical or unfamiliar phrasing doesn't become clear just because the
words are spelled right.
→ **Ask "what does this mean?" in your language, get an answer grounded
in what was actually shown to you.**

**3. Trust barrier** — can't verify a translation is faithful enough to rely
on. Word-level correctness and meaning-level correctness aren't the same
thing — you can get every word "right" and still lose what someone meant,
especially on entities (names, numbers) and intent (a flipped negation, a
reversed direction).
→ **Wherever a translation feeds something consequential, verify it
independently instead of trusting it blindly.**

**4. Output barrier** — even correct, faithfully-translated text is still a
wall if you don't read fluently.
→ **Read results back out loud, in the language the person spoke in.**

## What this build demonstrates

All four barriers have a working version in this build — some deep, some
lightweight, but none are just a design doc anymore:

**Barrier #1 (input) — full depth.**
- **Speak a job search query**, in an Indian language — Sarvam
  speech-to-text transcribes it, Sarvam translation converts it to
  English, then one LLM cleanup pass fixes STT/translation artifacts
  (fillers, awkward literal phrasing) before it's used.
- Search terms are **chips** (role, company, keyword) — add by voice or
  by typing, remove any, combine as many as needed.
- A **profile/stance** field, buildable three ways: speak it freely,
  upload a CV (PDF or text, parsed client-side, never persisted), or
  answer a **guided 5-question spoken conversation** (strengths,
  coaching areas, a past-but-dropped skill, a proud highlight, current
  focus) that gets synthesized into a clean CV-style profile.

**Barrier #2 (comprehension) — built via "chat with a job."**
Each result card has an ask-a-question panel: speak a follow-up about
that specific job (e.g. "what does this requirement mean?"), and get an
answer grounded in that job's own details plus general knowledge — no
new web search per question, so it stays fast and doesn't reopen
fabrication risk on every turn. Multi-turn history is kept per card, and
every answer is translated back and read aloud in the language the
question was asked in.

**Barrier #3 (trust) — a lightweight, human-in-the-loop version, not the
full independent-verification pipeline.** After the spoken profile is
transcribed, translated, and cleaned up, it's read back to the user via
TTS in their own language before it's used — so they catch a
mistranslation themselves instead of the app silently trusting it. This
is not automated verification (no independent second translation or
entity diffing); it's "let the person confirm," which is cheaper and,
for a single-shot flow like this, arguably more trustworthy than an
automated check would be.

**Barrier #4 (output) — full depth.**
Every result can be read aloud individually, in the language the person
searched in, including the fit, any hard blocker, and — when a CV was
provided — exactly which skills are missing and what to do about it.

**Skill-gap analysis**, layered on top: when a CV is provided, each
result shows which required skills the candidate already has, which are
missing, and one concrete, job-specific next step to close the gap —
the thing translation alone never gives you, because it requires
actually reasoning about the candidate against the posting.

## Why job customization matters here

A query alone, translated and searched, is functionally a translated Google
search — it doesn't demonstrate anything beyond translation. The stated
profile ("what I'm looking for") is passed into the *same* search call and
directly changes which results come back and how they're ranked. That's
the difference between "translate and search" and an actual job search
product: the customization is structural, not decorative.

## Stack

- Sarvam AI — speech-to-text, translation, text-to-speech (Voice Experience)
- OpenAI — web search + ranking against the stated profile, in one call.
  This is the real, tested, demo-day path. OpenAI's API blocks direct
  browser calls, so this path runs through the small local proxy in
  `server.js` (~40 lines, no dependencies, BYOK — it relays the key from
  the browser per request and never stores one itself).
- Claude (Anthropic) — supported as an alternate provider (toggle in the
  UI), called directly from the browser with no backend needed. The code
  path exists and mirrors the OpenAI prompt exactly, but it has not been
  run against a live Claude key — no Anthropic key was available during
  the build. Untested, not the demo path.
- HTML/JS frontend, no auth, no database — session-only.

## Status

See [`docs/plan.md`](./docs/plan.md) for the build plan and current state.
