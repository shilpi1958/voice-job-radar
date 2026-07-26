# Voice Job Radar — judging scorecard evidence

**Product one-liner:** A voice-first job search for Hindi and other Indian-language candidates — speak a profile, search roles, see skill gaps, and ask a job questions you can hear back.

**Sarvam scoring parameter selected:** **Voice Experience** only. We do **not** claim Document Intelligence or Dubbing.

**Live demo:** https://voice-job-radar.vercel.app · 3-min click path: [`docs/demo-3min.md`](demo-3min.md)

This doc maps each Voice-track parameter to **what exists in the repo today** (`index.html` + demo assets). It does not claim a final judge score.

---

## Suggested 3-minute demo path → parameters proven

Aligned with [`docs/demo-3min.md`](demo-3min.md). Narrate in English; product language = Hindi.

| Beat | What you show | Parameters |
|------|----------------|------------|
| Cold open + barriers | “Job search when English typing isn’t how you search” | **Impact**, **JTBD** |
| Language → Hindi | Profile language selector | **Voice Experience**, **JTBD** |
| Voice profile (1–2 answers) | Speak → Stop; follow-up question; progress | **Voice Experience**, **Memory**, **Delight**, **Creativity** |
| CV review → Update → dual pane | Upload sample PDF; Original \| Updated; download | **JTBD**, **Creativity**, **Delight** |
| Search roles/keywords | Speak or type; live ranked jobs | **JTBD**, **Creativity**, **Memory** (stance ranks) |
| Skill gap on one card | “you already have” / “skills to close the gap” | **JTBD**, **Impact**, **Creativity** |
| Job chat + Speak | Hindi question; Translate/Speak on answer | **JTBD**, **Voice Experience**, **Delight**, **Memory** (job + gap context) |
| Freeze | Gap + answer visible / TTS playing | Close — product outcome, not the stack |

**Personas:** Rahul (backend) or Arjun (robotics Hindi) — [`docs/sample-profile-robotics-hindi.md`](sample-profile-robotics-hindi.md).

---

## 1. JTBD (Jobs To Be Done)

**Bar (brief):** Does this solve a real, repeated job for the intended user — not a demo gimmick? Live outcomes beat mocked lists.

**What we built**
- Voice-first loop for Indian-language seekers: language select (Hindi default path) → **Voice profile** interviewer → optional **CV upload / review / update** → **Search** (Roles / Companies / Keywords by voice or type) → live web job results ranked with profile + CV → per-job **skill gap** → **Ask a question about this job**.
- Search is live (OpenAI web search via proxy is the tested path; Claude path exists as alternate). Results are not a hard-coded mock list.

**Where to see it**
- App: Profile → Search → result cards → job chat.
- Demo script: [`docs/demo-3min.md`](demo-3min.md) beats A–F.

**Evidence / demo beat**
- One continuous path: Hindi → 1–2 spoken profile answers → search `Backend Engineer` + `fintech` (or robotics + `ROS2`) → open a card → gap + one Hindi chat turn. Freeze on that outcome.

---

## 2. Memory and Context

**Bar (brief):** Does the system reuse what the user already said/uploaded so later steps feel continuous, not amnesiac?

**What we built**
- Guided interview Q&A is saved; answers (and LLM **summary** when done) sync into stance via `getStanceText()` / `syncStanceFromGuidedAnswers()` and are passed into the **same** job-search call that ranks results.
- Interviewer prompts include **CV excerpt** when a CV is uploaded (`cvExcerptForInterview`) and **ground the next question in the latest answer** (`lastGuidedAnswerMeta` + history) — not a fixed script of unrelated HR questions.
- Corrections keep history: re-speak/edit a turn or jump back to an earlier answer **without restarting from Q1**.
- Job chat is multi-turn **per card**, grounded in that job’s details including fit and (when CV was used) matched/missing skills. *Honest limit:* the chat prompt uses the job card context (profile-influenced fit + gap fields), not a second full paste of the raw stance string on every turn.

**Where to see it**
- Profile → Voice profile (progress, “Your answers”, Done for now).
- Search after interview — ranking/fit sentences change with stance.
- Job card → Ask a question… → follow-up turns keep history.

**Evidence / demo beat**
- Answer one strength aloud → Next → show the follow-up referencing that answer (or CV project). Search → point at fit. Chat → second question still about *this* posting.

---

## 3. Creativity

**Bar (brief):** Is the solution a thoughtful product composition, not “translate button + Google”?

**What we built**
- **Sarvam** STT → translate → TTS, plus an LLM **cleanup** pass so English-after-STT keeps meaning (titles, companies, numbers) while fixing fillers/awkward literals.
- **LLM interviewer** (not a static 5-question form) synthesizing a job-search profile.
- Search pipeline: Roles cleaned to English; **Companies / Keywords keep spoken wording** (`appendSearchDictation` / `keepAsSpoken`) so names and skill phrases aren’t over-translated away.
- CV **dual-pane** update (Original \| Updated) with download **PDF** and **.txt**.
- Per-job skill gap: **you already have** / **skills to close the gap** / **what to do next**.
- Demo assets: Hindi robotics persona + sample CV ([`sample-profile-robotics-hindi.md`](sample-profile-robotics-hindi.md), `sample-cv-robotics.pdf`).

**Where to see it**
- Mic path on Profile and Search; dual pane under Upload CV; gap block on cards; robotics sheet for a non-generic JTBD story.

**Evidence / demo beat**
- Narrate: “Not translate-and-pray — profile ranks, gap is honest, chat is about *this* job.” Show dual pane once, then gap labels.

---

## 4. Impact

**Bar (brief):** Who benefits, and why does this matter beyond a cool demo?

**What we built / claim**
- **Who:** Job seekers fluent in work but not in English keyboard/job-board UX — Hindi and other Indian languages supported in the language picker (Kannada, Tamil, Telugu, Marathi, Bengali, Gujarati, Malayalam, Punjabi, English, auto-detect).
- **Why voice matters:** Four barriers (input, comprehension, trust, output) — speak to search; ask what a requirement means; hear answers back; confirm meaning via Translate/Speak rather than silent mistranslation.
- **LinkedIn-style match narrative:** When a CV is present, each card surfaces matched vs missing skills and one concrete next step for *this* role — the “do I fit?” story boards usually leave to the seeker.

**Where to see it**
- README four-barrier framing; demo cold open + pain narration; skill-gap UI on cards.

**Evidence / demo beat**
- 30s business context from the demo script, then prove it with gap + Hindi chat — not with architecture slides.

**Honest limit:** Impact is demonstrated as a working product loop and personas, not as measured deployment metrics or A/B lift.

---

## 5. Delight

**Bar (brief):** Are polish and interaction details intentional — mic UX, feedback, controls that reduce friction?

**What we built (including mid-flight polish already in the working tree)**
- **Speak / Stop** mic labeling with recording pulse; elapsed “Recording…” clock; hint “Tap Speak, then Stop when you’re done” on job chat.
- Interview **progress** status (“thinking of next question…”, question counts); Skip / Next / **Done for now**.
- Per-block **Translate** and **Speak** (toggle to **Stop** while TTS plays); native-language peek on profile answers.
- Search progress stages while web search runs; single-flight TTS (one Speak at a time).
- Mic **stops TTS** when the user starts recording so the product doesn’t talk over them.

**Where to see it**
- Guided mic + Speak question; Translate/Speak on answers and job cards; search status spinner copy.

**Evidence / demo beat**
- Start TTS on a question or answer, then tap Speak — audio stops. Point at progress while the interviewer thinks.

**Honest limit:** Delight is UX polish around a serious loop, not gamification or flashy motion. Some interviewer/memory polish is recent; demo what’s on screen.

---

## 6. Voice Experience *(selected Sarvam parameter)*

**Bar (brief):** Accents / Indian-language speech, natural turn-taking, recovery from unclear audio, no talk-over, corrections without full restart, short spoken questions, meaning preserved after English STT/translate. *(Rubric rewards honest limits over unverified L4/L5 claims.)*

**What we built — mapped to the rubric**

| Rubric idea | Concrete behavior in product |
|-------------|------------------------------|
| Accents / Indian languages / code-switching | Sarvam STT with language select (incl. Hindi, auto-detect); interviewer prompt treats Hindi–English **code-switch** meaning after English transcripts, not surface wording. |
| Follow-ups not a fixed script | LLM interviewer: next question **must** cite latest answer and/or CV; bans generic openers when already covered. |
| Unclear STT → clarification | `isUnclearSpeechTranscript` + `requireClearSpeech` on guided mic: rejects empty/filler/garble with “didn’t catch that clearly — please say it again” instead of saving garbage. |
| Mic stops TTS (no talk-over) | `beginRecordSession` calls `stopTtsPlayback()` before recording. |
| Corrections without restart | `appendDictatedText`; edit/re-answer current turn; jump to a prior turn keeping full Q&A; does not wipe back to Q1. |
| Short natural questions | Prompt prefers one short spoken sentence (TTS-friendly); pacing hint shortens follow-ups after long answers. |
| English-after-STT meaning preserved | Translate + `cleanupTranslatedText` instructed to keep titles, companies, numbers, constraints; companies/keywords fields keep **spoken** text. |

**Where to see it**
- Profile Voice profile (Speak/Stop, Speak question, unclear rejection, follow-ups).
- Search mic + Companies/Keywords keepAsSpoken.
- Any Speak control + mic interaction for no talk-over.

**Evidence / demo beat**
- Hindi answer with a tool name (e.g. ROS2) → follow-up references it.
- Optional: mumble/empty take → clarification status.
- Speak question TTS → tap mic → TTS stops.

**Honest limits (say if asked):** We aim to **demonstrate** a strong working Voice Experience loop. Full barge-in under noise, multi-language stress tests, and verified L4/L5 emotional/code-switch robustness are **not** claimed as proven. Prefer showing the working loop over overclaiming.

---

## Appendix — official weighting (example arithmetic)

Judges use weighted levels. The numbers below illustrate the **formula**, not our awarded score. Do **not** claim we scored 35.5.

| Parameter | Example level | Weight | Example points |
|-----------|---------------|--------|----------------|
| JTBD | L4 | × 2.5 | 10 |
| Memory and Context | L3 | × 1 | 3 |
| Creativity | L4 | × 1.5 | 6 |
| Impact | L3 | × 1.5 | 4.5 |
| Delight | L2 | × 1 | 2 |
| Voice Experience *(selected Sarvam)* | L4 | × 2.5 | 10 |
| **Example total** | | | **35.5 / 50** |

**Targets we aim to demonstrate in demo (aspirational, evidence-based):**
- **JTBD:** L4-style live loop (profile → search → gap → chat) with real postings.
- **Voice Experience:** strong working conversational loop (honest L3+ demonstration; do not invent barge-in/noise proofs).
- **Memory / Creativity / Impact / Delight:** show the concrete behaviors above; let judges assign levels from evidence.

---

## Quick reference — one line per parameter

| Parameter | One-liner |
|-----------|-----------|
| **JTBD** | Full voice-first Hindi job loop: profile, CV help, live search, skill gap, job chat. |
| **Memory and Context** | Interview + CV stance ranks search; follow-ups and chat stay grounded in prior answers/job. |
| **Creativity** | Sarvam + LLM interviewer, English cleanup, spoken companies/keywords, dual-pane CV, have/missing gap. |
| **Impact** | Removes English-board barriers for Indian-language seekers; honest fit/gap narrative per posting. |
| **Delight** | Speak/Stop mic, interview progress, Translate/Speak, TTS yields when mic starts. |
| **Voice Experience** | Sarvam STT/TTS path with adaptive follow-ups, unclear-speech retry, no talk-over, meaning-preserving cleanup. |
