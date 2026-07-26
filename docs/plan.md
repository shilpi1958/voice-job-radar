# Build plan

## Scope, locked

One flow, built solid rather than four flows built thin:

speak query (any supported Indian language) → Sarvam STT → Sarvam translate
→ Claude + web search, ranked against a stated profile → results shown as
cards → Sarvam TTS reads the top results back in the original language.

No auth, no database, no persistence — session-only state. No code reused
from the original job radar; this is a fresh build that extends the idea.

**Provider note:** Claude is the documented, submitted path — called direct
from the browser, no backend. OpenAI was added as a second toggleable
provider purely because a Claude key wasn't on hand to test with during the
build; it requires the small local proxy in `server.js` since OpenAI's API
(unlike Claude's) blocks direct browser calls. The demo runs on Claude.

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
   OpenAI path (via `server.js`, since a Claude key wasn't available at
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

## Deferred, not abandoned

Two more barriers from the four-barrier framework (see main README) are
scoped but not built in this pass:

- **Comprehension barrier** — ask "what does this mean?" about a result, in
  your language, answered from that result's own content.
- **Trust barrier** — for any translation feeding something consequential
  (not a one-off search), verify independently: transcribe and translate
  separately, diff entities and numbers, check semantic intent, ask rather
  than guess on any mismatch.

Not building these now is a scope decision, not an oversight — depth on one
real loop beats partial coverage of four.
