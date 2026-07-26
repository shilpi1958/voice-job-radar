# Voice Job Radar — 3-minute judge demo

Glance sheet. Speak the narration lines. Click the path. Freeze on the product.

**Scorecard evidence (per judging parameter):** [`docs/judging-parameters.md`](judging-parameters.md)

**Live URL:** https://voice-job-radar.vercel.app  
**Sample CVs:** `docs/sample-cv-backend.pdf` (Rahul Sharma, backend) · `docs/sample-cv-robotics.pdf` (Arjun Mehra, robotics / Hindi; also `.txt`)  
**Robotics Hindi persona (full Q&A):** `docs/sample-profile-robotics-hindi.md`

---

## 1. Cold open (one breath)

> Job search that works when English typing isn’t the way you search.

---

## 2. 0:00–0:30 — Business context

**Say:**
> Hundreds of millions of job seekers in India are fluent in work — not in typing English job boards. They know the role. The product still assumes English keyboard + English reading. That isn’t a translation bug. It’s four barriers: input, understanding results, trusting what came back, and hearing the answer out loud.

**Metric (pick one, keep it plain):**
> If someone can’t type the query or read the posting, they never apply — ability isn’t the bottleneck; the interface is.

---

## 3. 0:30–1:00 — Workflow today (manual pain)

**Say:**
> Today that person asks a friend to translate, pastes English into Naukri or LinkedIn, squints at requirements they don’t fully get, and guesses whether their CV fits. No skill gap. No “what does this mean?” in their language. Lots of drop-off before apply.

**Point at the screen (app open, idle):**
> We’re going to do that loop voice-first — profile, CV help, search, gap, ask the job — in Hindi.

---

## 4. 1:00–3:00 — Live demo script

### Pre-flight (before judges sit / while muted)

1. Open https://voice-job-radar.vercel.app  
2. **Setup** (if keys not already in this browser):
   - Sarvam key
   - Prefer **OpenAI** (tested demo path) *or* Claude if that’s what’s loaded
   - Save → Start searching  
3. Mic allowed. Quiet room. Sample PDF on Desktop / Downloads.  
4. Optional warm-up: one Speak take on Profile so STT is warm.

### Click path (tight — ~2 minutes)

| Beat | Click | Do | Narration |
|------|--------|-----|-----------|
| **A. Language** | **Profile** → Language | Set **Hindi** | “Same person. Their language.” |
| **B. Voice profile** | **Voice profile** → **Start** | Answer **1–2** questions out loud (Speak → Stop). Skip the rest with **Skip** / **Done for now** if clock is tight. | “AI interviewer — speak answers; profile ranks jobs, not just keywords.” |
| **C. CV** | **Upload CV** → Choose file | Upload `sample-cv-backend.pdf` *or* robotics path: `sample-cv-robotics.pdf` → **Review my CV** → wait for **2-sentence** review → **Update CV** → show dual pane (Original \| Updated) → **Download CV-updated.txt** | “Upload → short review → update beside the original → take it with you.” |
| **D. Search** | **Search** | Backend: `Backend Engineer` + `fintech` · **or robotics:** `Robotics Engineer` + `ROS2` → **Search jobs** | “Search in their words — live jobs, ranked with the profile.” |
| **E. One job** | Open **first solid card** | Point at **you already have** / **skills to close the gap** | “Not translate-and-pray — have vs missing, for *this* posting.” |
| **F. Chat** | **Ask a question about this job** | Speak (or type) one Hindi question → get answer (+ Speak if time) | “Comprehension barrier: ask the job, in Hindi.” |

**If time is melting:** skip B after one answer, or skip Download — still show dual pane. Never skip skill gap + one chat turn.

---

## 5. Narration lines (short, speakable)

Copy-paste into your mouth:

| Beat | Line |
|------|------|
| Cold open | “Job search that works when English typing isn’t how you search.” |
| Context | “They can do the job. The board still demands English keyboard and English reading.” |
| Pain | “Friend translates. Paste. Guess. Drop off. No skill gap, no Q&A in their language.” |
| Language | “Hindi. One setting.” |
| Voice profile | “Interviewer asks; they speak. That profile changes ranking.” |
| CV | “Two-sentence review. Update next to the original. Download.” |
| Search | “Live search — roles and keywords, voice or type.” |
| Skill gap | “Green: already have. Red: close the gap. One next step for this role.” |
| Chat | “What does this requirement mean? — answered for *this* job, spoken back.” |
| Close | “That’s the product: voice in → ranked fit → gap → ask → hear it back.” |

---

## 6. One outcome close

**Freeze on:** one job card with skill gap visible + chat answer on screen (or TTS playing).

**Say (and stop):**
> Same seeker. Spoke Hindi. Got ranked jobs, an honest gap, and an answer they can hear. That’s the win — not the stack.

Do **not** list Sarvam / OpenAI / Claude / Vercel unless a judge asks.

---

## 7. Fallback recording checklist (if live fails)

Prep **before** demo day. One continuous screen recording (~2–2.5 min) of the happy path above.

- [ ] Recording file on laptop + phone backup; open in a player, paused at cold open  
- [ ] Keys worked in the recorded session (don’t demo a red Setup badge)  
- [ ] Hindi language selected on screen  
- [ ] At least one voice profile answer captured  
- [ ] CV review → Update → dual pane visible  
- [ ] Search returned ≥1 real job  
- [ ] Skill gap (“you already have” / “skills to close the gap”) readable  
- [ ] One job-chat Q&A completed  
- [ ] Audio: your narration *or* on-screen TTS — judges can hear the loop  

**If live dies mid-demo:**  
1. Say: “Live network hiccup — here’s the same path recorded this morning.”  
2. Play from Profile or Search (whichever failed).  
3. Still close on the frozen outcome frame, not on APIs.

**Typed escape hatches (live):** mic broken → type Hindi/English into answer + search fields; STT flaky → paste prepared lines from §9; OpenAI proxy down → switch provider to Claude in Setup if key ready.

---

## 8. Mistakes to avoid

From the demo brief / grading posture:

- **Don’t pitch the stack.** Freeze on the working product. Name vendors only if asked.
- **Don’t sell “we added translation.”** Show ranked search + skill gap + job chat — the product, not a translate button.
- **Don’t overclaim Voice Experience.** Honest L3 working loop beats unverified L4/L5 (barge-in, noisy code-switch). If asked: state real limits.
- **Don’t burn the minute on Setup.** Keys ready before the clock. Setup is plumbing, not the story.
- **Don’t tour every feature.** One language, short profile, one CV pass, one job, one chat.
- **Don’t use mocked job cards.** Live results matter for JTBD credibility.
- **Don’t end on architecture or a blank screen.** End on gap + answer.
- **Don’t apologize into a spiral.** One line, fallback recording, continue.
- **Don’t hide the human.** You’re demoing for a person who searches by voice — keep Rahul’s or Arjun’s story, not the API diagram.

---

## 9. Demo data suggestions

Pick **one** persona per run. Backend (§9a) is the default; robotics (§9b) when you want a different JTBD story. Full robotics sheet: `docs/sample-profile-robotics-hindi.md`.

### 9a. Persona — Backend (default)
**Rahul Sharma** — Hindi-speaking backend engineer (~3 years, Node.js + PostgreSQL). Bangalore or remote; no night shifts. Fintech / deep-tech. Mid-level Backend or Full-stack. Sample file: `docs/sample-cv-backend.pdf`.

### Voice profile (1–2 answers — Hindi)

**Strengths:**  
> मुझे API बनाना और डेटाबेस डिजाइन करना अच्छा लगता है। Node.js और PostgreSQL में मैं मजबूत हूँ।

**Proud of / highlight:**  
> पेमेंट वाली API बनाई थी जो बिना डाउनटाइम के हाई वॉल्यूम हैंडल करती थी।

### Search terms
| Field | Use |
|-------|-----|
| Roles | `Backend Engineer` or speak: बैकएंड इंजीनियर |
| Keywords | `fintech` · optional: `remote` |
| Companies (optional) | skip unless time — e.g. leave blank |

### One job-chat question (Hindi)
> इस जॉब में AWS कितना ज़रूरी है? मेरे पास अभी basics हैं।

English backup if STT fails:  
> How important is AWS for this role if I only have basics?

### English profile (if you must paste)
> 3 years backend, Node.js and PostgreSQL. Bangalore or remote, no night shifts. Fintech or deep-tech. Mid-level Backend or Full-stack.

---

### 9b. Persona — Robotics (Hindi alternate)

**Arjun Mehra** — Hindi-speaking robotics engineer (~2.5 years, ROS2 / perception / embedded). Bangalore; daytime IST. Warehouse AMR / industrial / deep-tech. Strong junior → early mid. Upload: `docs/sample-cv-robotics.pdf` (regen via `python3 docs/generate-sample-cv.py`). Full Q&A: `docs/sample-profile-robotics-hindi.md`.

### Voice profile (1–2 answers — Hindi) — prefer Q1 + Q4 live

**Strengths (romanized):**  
> Mujhe robot perception aur ROS2 pipelines banana accha lagta hai. Python, C++, OpenCV, aur STM32 embedded pe main solid hoon.

**Proud of / highlight (romanized):**  
> Warehouse AMR pe camera + ultrasonic se obstacle avoidance pipeline banayi. ROS2 nodes se latency kam ki, Gazebo pe pehle validate kiya.

**Devanagari (strengths):**  
> मुझे रोबोट perception और ROS2 pipelines बनाना अच्छा लगता है। Python, C++, OpenCV, और STM32 embedded पे मैं solid हूँ।

### Search terms
| Field | Use |
|-------|-----|
| Roles | `Robotics Engineer` or speak: रोबोटिक्स इंजीनियर |
| Keywords | `ROS2` · optional: `OpenCV` · `Bangalore` |
| Companies (optional) | `GreyOrange` · `Addverb` · `Ati Motors` — skip if short on time |

### One job-chat question (Hindi)
> Is role me ROS2 production experience kitna zaroori hai? Mere paas warehouse AMR pe ROS2 perception pipeline hai, lekin multi-robot fleet nahi.

English backup if STT fails:  
> How important is production ROS2 for this role if I’ve shipped AMR perception but not multi-robot fleets?

### English profile (if you must paste)
> About 2.5 years in robotics. ROS2, Python, C++, OpenCV, STM32. AMR perception and obstacle avoidance in Bangalore. Want Robotics Engineer — perception, control, or ROS. Bangalore, Hyderabad, or remote IST daytime.

---

## Timing cheat card

| Clock | Beat |
|-------|------|
| 0:00 | Cold open + business |
| 0:30 | Manual pain |
| 1:00 | Hindi → voice profile (short) |
| 1:25 | CV review → update → dual pane |
| 1:50 | Search |
| 2:15 | Skill gap on one card |
| 2:35 | Chat with job |
| 2:55 | Outcome close — freeze |

Rehearse twice with a timer. Prefer cutting profile depth over cutting skill gap or chat.
