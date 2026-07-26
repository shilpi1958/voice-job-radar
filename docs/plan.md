# Build plan

## Scope, locked

One flow, built solid rather than four flows built thin:

speak query (any supported Indian language) → Sarvam STT → Sarvam translate
→ Claude + web search, ranked against a stated profile → results shown as
cards → Sarvam TTS reads the top results back in the original language.

No auth, no database, no persistence — session-only state. No code reused
from the original job radar; this is a fresh build that extends the idea.

**Provider note:** OpenAI is the real, tested, demo-day path, run through
the small local proxy in `local-server.js` (or Vercel `/api/openai-search`) since OpenAI's API blocks direct
browser calls (unlike Claude's). Claude is supported as a toggleable
alternate — same prompt, no backend needed — but has never been run
against a live key; no Anthropic key was available during the build.
The demo runs on OpenAI.

## Sarvam parameter declared: Voice Experience

Realistic target: **L3 (Working)** — decent turn-taking, domain-aware
results, not chasing L4/L5. Those levels require multi-turn conversational
robustness (barge-in, mid-call correction, emotional read, code-switching
under noise) that a single-shot speak-then-search flow doesn't attempt and
that 8 hours doesn't leave time to build *and* properly test. Honest scoping
beats overclaiming — the rubric rewards evidence, not ambition.

## Job-to-be-done is the priority

JTBD carries a 2.5x multiplier — the highest-weighted parameter — and is
graded on real, repeated success (90%+ across 3+ test cases = top band),
not a single lucky demo run. That's why:

- Results come from live Claude web search, not a mocked job list.
  Mocked/staged data caps out around L3 on the JTBD rubric; live results are
  what unlocks L4/L5.
- The majority of build time is reserved for making the core loop actually
  reliable across repeated, varied inputs — not for adding more features.

## Why the stated profile isn't cut, even under time pressure

A voice query alone, translated and searched, is a translated Google search
— it doesn't demonstrate a job search *product*, just a translation layer.
The profile field is folded into the *same* Claude call as the search
(one prompt, one API call — not a separate rubric-generation step like the
original job radar's two-step flow), so it directly changes ranking without
adding a second call to build, wire, and test under time pressure.

## Hour-by-hour

1. Sarvam auth working — translate call confirmed returning English from a
   Hindi input. STT itself not yet tested with real audio (no mic test run
   yet) — deferred since translate proves the same auth path.
2. Wired typed English text + stance into a job-search call, with the
   Claude and OpenAI paths both implemented. Verified end-to-end on the
   OpenAI path (via `local-server.js` / Vercel, since a Claude key wasn't available at
   test time) — 5 real, scored, sourced job results came back correctly.
   Claude path is written but not yet run live.
3–4. Build the actual UI (mic input, stance box, results cards) around the
   now-working pipeline. Test with 5+ different spoken queries, ideally
   across 2–3 languages.
5–6. Fix whatever breaks. Budgeted as the largest block on purpose — this
   is where JTBD reliability is actually won or lost, not in hour 1.
7. Add Sarvam TTS readback of the top results. Completes the input→output
   loop — this is what separates "voice input gimmick" from real Voice
   Experience credit.
8. Rehearse the live demo end to end, at least twice. Prep honest answers
   for judge questions about accents, code-switching, and noise — the
   rubric explicitly rewards teams who know and state their real limits
   over teams who claim robustness they haven't tested.

## Since the original 8-hour plan: what actually got built

The original plan scoped only barriers #1 and #4 and deferred #2 and #3.
Both have since been built, at a lighter weight than the original
deferred-scope description:

- **Comprehension barrier** — built as "chat with a job": a per-card
  spoken Q&A panel, answers grounded in that job's own data plus general
  knowledge, no new web search per question, multi-turn history kept per
  card, answers translated back and read aloud.
- **Trust barrier** — built as a lighter version than originally scoped.
  The original plan called for independent dual-translation and entity
  diffing; what's actually built is a human-in-the-loop confirmation
  instead: the spoken profile is read back via TTS in the user's own
  language before use, so *they* catch a mistranslation rather than an
  automated diff catching it. Cheaper to build, no second translation
  call per input, and arguably more trustworthy for a single-shot flow —
  but it is not the automated verification pipeline originally described,
  and that distinction should be stated plainly to judges if asked.

Also added, beyond the original four-barrier scope:
- Chip-based keyword search (roles/companies/keywords, add by voice or
  typing) instead of one free-text query string.
- CV upload (PDF or text, parsed client-side, session-only) plus
  per-job skill-gap analysis: matched skills, missing skills, and one
  concrete next step per result — this is the part translation alone
  never provides, since it requires reasoning about the candidate
  against the specific posting.
- A guided 5-question spoken conversation that synthesizes answers into
  a CV-style profile, for users with no CV to upload.
- Per-job TTS readback (previously one batch summary of the top 3
  results) — now the user picks which specific job to hear, read back
  in full detail including its skill gap.

## What's NOT yet done, with ~4 hours and ~$40 left

- **No real microphone test has been run.** Every test so far used either
  typed text or a JS-injected fake STT response — the actual
  speak-into-a-mic path (browser permissions, real accents, background
  noise, real Sarvam STT accuracy) is completely unverified. This is the
  single biggest risk before a live demo and the highest-priority item
  left.
- Real Claude-path test (currently untested, OpenAI is the verified path).
- Testing across multiple real spoken languages/queries, per the original
  hour 3-4 plan — not yet done with real audio.
- Demo rehearsal — not yet done at all.
