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

Given the time available, this build goes deep on **barrier #1 (input)**
and closes the loop with a working version of **barrier #4 (output)** —
a complete, real, working slice rather than four shallow ones:

1. **Speak a job search query**, in an Indian language — Sarvam
   speech-to-text transcribes it, Sarvam translation converts it to English.
2. **Real jobs, not a mock list.** The translated query, combined with a
   short stated profile ("what I'm looking for"), goes to Claude with web
   search enabled — it finds and ranks actual live job postings against
   that profile, the same way a scan does in the original (English-only)
   job radar this project extends the idea from.
3. **Results are read back out loud**, in the language the person searched
   in, via Sarvam text-to-speech — so the loop never requires reading
   English at all.

Barriers #2 (comprehension) and #3 (trust) are scoped and designed —
see [`docs/`](./docs) — but not built in this pass. Depth on one working
loop beats breadth across four half-built ones.

## Why job customization matters here

A query alone, translated and searched, is functionally a translated Google
search — it doesn't demonstrate anything beyond translation. The stated
profile ("what I'm looking for") is passed into the *same* search call and
directly changes which results come back and how they're ranked. That's
the difference between "translate and search" and an actual job search
product: the customization is structural, not decorative.

## Stack

- Sarvam AI — speech-to-text, translation, text-to-speech (Voice Experience)
- Claude (Anthropic) — web search + ranking against the stated profile, in
  one call. This is the documented, primary path: called directly from the
  browser, no backend needed.
- OpenAI — supported as an alternate provider (toggle in the UI), added
  because Claude access wasn't available to test with during the build.
  Unlike Claude, OpenAI's API blocks direct browser calls, so this path
  requires running the small local proxy in `server.js`. Not the path this
  project is submitted/demoed on; kept because it's what got the pipeline
  actually verified end-to-end.
- HTML/JS frontend, no auth, no database — session-only. `server.js` is an
  optional ~40-line dev-only proxy for the OpenAI path; the Claude path
  needs no backend at all.

## Status

See [`docs/plan.md`](./docs/plan.md) for the build plan and current state.
