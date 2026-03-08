# eGramSabha — AWS AI for Bharat Hackathon Submission

## Team Name

**Empower Panchayat**

## Team Leader Name

*(See submission form)*

## Problem Statement

**AI-Powered Digital Gram Sabha Platform**

---

In 1992, India passed the 73rd Constitutional Amendment — a radical act of faith in its own people. It created 250,000+ Gram Panchayats and mandated Gram Sabhas as the foundation of grassroots democracy where every adult citizen can participate. Three decades later, that promise remains largely unfulfilled.

### The Scale of the Problem

65% of India's population (~900 million people) lives in rural areas governed by these 250,000+ Gram Panchayats. The 73rd Amendment grants Panchayats jurisdiction over 29 subjects (Schedule XI of the Constitution) — from drinking water to rural roads, primary education to public health — representing Rs 25+ lakh crore in annual welfare spending.

| Statistic | Detail |
|-----------|--------|
| **5-10%** | Average Gram Sabha attendance across India |
| **< 3%** | Women participation in many states |
| **60%+** | Rural Indians with limited literacy |
| **30%** | Eligible citizens excluded from welfare schemes |
| **ZERO** | Digital trail of Gram Sabha decisions |

### Structural Barriers

| Barrier | Impact |
|---------|--------|
| Paper agendas on notice boards | Low awareness — excludes remote hamlets, women at home, daily wage workers |
| Paper sign-in sheets | Easy to forge — routinely inflated to show higher attendance numbers |
| Hand-written minutes by clerk | Subjective, often incomplete, sometimes pre-written before the meeting happens |
| Single language proceedings | Excludes tribal & minority communities — Gondi, Santhali, Bhili speakers silenced |
| No issue tracking system | Promises forgotten between meetings — citizens stop attending because nothing changes |
| Physical presence required | Excludes women (social norms), elderly (mobility), differently-abled citizens |

### The Opportunity

India has the highest teledensity in the world at 85.69% — even rural teledensity is 59.19%. The phones are there. The connectivity is there. What's missing is a platform that meets citizens where they are — on their phones, in their language, with their voice.

---

## Brief About the Idea

### Solution Overview

eGramSabha is a voice-first, face-authenticated platform that digitizes the entire Gram Sabha lifecycle — from citizen registration to issue resolution tracking. It is a direct response to the structural barriers that prevent Gram Sabhas from functioning as the Constitution intended.

The platform is built as a **3-portal system**:

- **Admin Portal** — Platform-level management: create and manage panchayats, add citizen data from CSV (Election Commission data), create and manage officials, optionally onboard citizens via face biometric, update citizen profiles, manage support tickets, view overall metrics via dashboard.
- **Official Portal** — Day-to-day governance: register citizens via face biometric, report issues for self or on behalf of citizens, edit panchayat contact details and letterhead, schedule and manage Gram Sabhas, create/update/delete agenda items, select agenda from AI-generated summary, take facial biometric attendance, issue management, PDF exports.
- **Citizen Portal** — Citizen participation: face-authenticated login, voice/text reporting of issues, grievances, and suggestions with optional attachments, RSVP for upcoming Gram Sabhas, view own and all panchayat issues, view past and upcoming meetings with details, support tickets.

### 5-Step Gram Sabha Lifecycle

```
REGISTER (Face) → REPORT (Voice) → MEET (Agenda) → RECORD (Track) → TRACK (Status)
```

| Step | What Happens |
|------|-------------|
| **1. REGISTER (Face)** | Admin adds citizen data from CSV (Election Commission). Officials or Admin onboard citizens by capturing face biometric and voter ID. 128-dimension face descriptor stored — no passwords, no OTPs. Citizens cannot self-register. |
| **2. REPORT (Voice)** | Citizens record voice issues, grievances, or suggestions in their native language, anytime. AI transcribes, corrects grammar, translates to English/Hindi, detects sentiment and urgency. |
| **3. MEET (Agenda)** | Officials schedule Gram Sabha with date, time, location. AI summarizes and categorizes citizen issues into an agenda backlog. Officials select relevant items for each meeting. Agenda translated to multiple languages and read aloud via Amazon Polly TTS. SMS notifications triggered on schedule (requires DLT registration for delivery). |
| **4. RECORD (Attendance)** | Officials take facial biometric attendance of citizens to meet quorum so the Gram Sabha can start. Verification method recorded per citizen. Digital attendance creates an unforgeable record. |
| **5. TRACK (Status)** | Every issue tracked through lifecycle: REPORTED → PICKED_IN_AGENDA → DISCUSSED_IN_GRAM_SABHA → RESOLVED. Officials add resolution remarks. Citizens see status updates. Zero promises lost. |

> See [Workflow Diagram](./02-diagrams.md#5-step-gram-sabha-lifecycle) and [Governance Loop](./02-diagrams.md#continuous-governance-loop)

---

### Why AI is Required in Your Solution

#### 1. Voice-First Removes the Literacy Barrier

60%+ of rural Indians have limited literacy. Paper complaint registers, written agendas, and printed minutes exclude them by design. Voice-first AI lets a tribal woman in Jharkhand or an elderly farmer in Tamil Nadu speak a complaint and have it formally recorded in 3 languages — without writing a single word.

#### 2. AI Transcription + Grammar Correction + Translation

Raw voice recordings are transcribed by STT (Jio/Whisper/AWS Transcribe — provider-agnostic). Audio upload triggers immediate transcription; a cron job retries any failed transcriptions automatically. Amazon Bedrock then corrects grammar and produces three outputs: enhanced_original (corrected in the source language), enhanced_english, and enhanced_hindi. A single voice complaint becomes a trilingual formal issue.

> See [Voice Issue Reporting Pipeline](./03-process-flows.md#pipeline-1-voice-issue-reporting)

#### 3. AI Sentiment Analysis + Auto-Priority

After transcription completes, every issue is automatically analysed for sentiment (positive/negative/neutral/mixed) and key phrases are extracted. A suggested priority is computed — if the issue is flagged URGENT (e.g., "sewage flowing into drinking water supply"), the system auto-upgrades the issue priority without waiting for human review. Officials see a prioritised dashboard: urgent issues first.

#### 4. AI Agenda Summarization

Current agendas are ad-hoc, influenced by powerful voices. A dedicated cron job runs hourly, processing unsummarized citizen issues, grievances, and suggestions through Amazon Bedrock to produce IssueSummary records — categorized, deduplicated, and clubbed by topic. Officials then select relevant IssueSummary items from this AI-generated backlog when building the agenda for each meeting. AI ensures every citizen voice is surfaced; officials curate the final agenda for relevance.

> See [Agenda Generation Pipeline](./03-process-flows.md#pipeline-3-agenda-generation)

#### 5. Text-to-Speech — Information Reaches Everyone

Amazon Polly reads agenda items aloud in the citizen's language. The illiterate elderly man who could never read the notice board can now listen to what will be discussed on his phone.

#### 6. Without AI: An Impossible Scale Problem

250,000 panchayats x multiple languages x regular meetings = Without AI, this would require an army of clerks, translators, and transcribers at every panchayat. AI makes inclusive governance scalable.

#### 7. Minutes of Meeting Generation (Planned)

A separate video-mom-backend module exists for AI-generated Minutes of Meeting from uploaded meeting audio. It produces structured MOM output: Meeting Overview, Discussion Points, Decisions Taken, Action Items, Next Steps — auto-translated to 3 languages. This module is built but not yet integrated into the main application workflow; full integration is planned for a future release.

> See [Planned Features](./03-process-flows.md#planned--future)

---

### How AWS Services Are Used Within Your Architecture

eGramSabha uses **15 AWS services** — 11 actively deployed in the live demo, 4 code-ready (activate via environment variable with zero code changes).

#### Active Services (11)

| Service | How It's Used |
|---------|--------------|
| **Amazon Bedrock** (Nova Lite via Converse API) | LLM backbone powering 4 active AI tasks: grammar correction, sentiment analysis, translation fallback, and agenda summarization (IssueSummary generation via hourly cron). Temperature 0.3 for consistent output. MOM generation available in separate module (planned integration). |
| **Amazon S3** (2 buckets, Intelligent-Tiering) | `egramsabha-assets`: face photos, letterheads, issue attachments, TTS audio cache. `egramsabha-transcribe-temp`: temporary audio for Transcribe jobs. All uploads use INTELLIGENT_TIERING — auto-moves cold data to cheaper tiers. |
| **AWS Translate** | Real-time translation of AI-generated content (agendas, corrected transcriptions) across 10+ Indian languages. Auto-detects source language. Used only for AI content — UI uses static translation files. |
| **Amazon Polly** + S3 Caching | Text-to-Speech for agenda read-aloud. Aditi voice (Hindi), Raveena (English). SHA256 content hash → check S3 cache → synthesize if miss → cache result. Same text never synthesized twice. |
| **API Gateway** (REST, REGIONAL) | Single entry point for ALL API traffic. eGramSabha-MOM-API with prod stage. 100 req/s rate limit, 200 burst, 100K requests/day quota. API key (x-api-key header) from frontend. Protects expensive AI endpoints from abuse. |
| **CloudWatch** (2 log groups) | `/egramsabha/backend` (Winston + winston-cloudwatch) and `/egramsabha/video-mom` (watchtower). Centralized structured JSON logging from both Node.js and Python. 30-day retention. |
| **Secrets Manager** | Single secret `egramsabha/prod` storing JWT_ADMIN_SECRET, JWT_OFFICIAL_SECRET, JWT_CITIZEN_SECRET, JWT_REFRESH_SECRET. Loaded at startup, cached in memory. Graceful fallback to env vars for local dev. |
| **EC2** (t3.medium) + **EBS** (gp3) + **Elastic IP** | 2 vCPU, 4 GB RAM hosting Docker Compose with 4 containers. Burstable CPU handles AI processing spikes. 20 GB gp3 for persistent volumes. Static IP for DNS and API Gateway. |
| **IAM** | Least-privilege policies per service. Each service only accesses AWS APIs it needs. Graceful degradation if permissions are missing. |

#### Code-Ready Services (4) — Activate via Environment Variable

| Service | Activation | What It Does |
|---------|-----------|-------------|
| **Amazon Rekognition** | `FACE_VERIFICATION_PROVIDER=rekognition` | Server-side face verification. Collections per panchayat. IndexFaces during registration, SearchFacesByImage during login (90% similarity threshold). |
| **Amazon DocumentDB** | `USE_DOCUMENTDB=true` | Managed MongoDB replacement. All Mongoose schemas are DocumentDB-compatible. Provides automated backups, multi-AZ failover. |
| **AWS Transcribe** | `STT_PROVIDER=aws_transcribe` | Managed STT supporting Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi + more. Code complete — async batch jobs via S3. |
| **Amazon SNS** | `SNS_ENABLED=true` | SMS notifications triggered on meeting schedule. Code is fully integrated: Direct SMS publish with Transactional type, +91 formatting, sender ID 'eGramSbha'. API calls succeed — actual SMS delivery requires AWS sandbox exit + India TRAI DLT registration. |

> See [Architecture Diagram](./04-architecture.md) for full system topology

---

### What Value the AI Layer Adds to the User Experience

| User | Without AI | With eGramSabha AI |
|------|-----------|-------------------|
| **Illiterate citizen** (60%+ of rural India) | Cannot report issues — requires writing in a complaint register during office hours | Speaks complaint into phone in any language. AI transcribes, corrects, translates, assigns priority. Issue formally registered. |
| **Women at home** (~3% participation) | Must attend male-dominated public meeting. Social norms discourage public speaking. Domestic responsibilities prevent attendance. | Reports issues, grievances, or suggestions via voice from home, in her language. Complaint has same formal weight as anyone else's. Face auth — no password needed. |
| **Official creating agenda** | Ad-hoc list influenced by powerful voices. No systematic inclusion of citizen complaints. | AI summarizes and categorizes all citizen issues into a backlog. Official selects relevant items for each meeting — every voice is surfaced, none buried in paperwork. |
| **Tribal/minority citizen** | Excluded by state language proceedings. Gondi, Santhali, Bhili speakers cannot understand or participate. | Speaks native language. AI translates. Agenda available in their language. TTS reads aloud. |
| **Block/District administrator** | Physical inspection needed to audit Gram Sabhas. Paper records inaccessible. | Digital attendance data, issue analytics. Audit remotely. Pattern recognition across panchayats. |

---

## List of Features

### AI-Powered Features

| Feature | Description |
|---------|------------|
| **Voice-First Issue Reporting** | Record issues, grievances, or suggestions in any language. AI transcribes, corrects grammar, translates to English + Hindi. No typing required. Cron retries failed transcriptions. |
| **Sentiment Analysis + Auto-Priority** | Every issue analysed for sentiment (positive/negative/neutral/mixed), key phrases extracted. Health/safety issues auto-flagged URGENT with automatic priority upgrade. |
| **AI Agenda Summarization** | Hourly cron processes unsummarized issues through Bedrock — categorizes, deduplicates, and clubs related items into IssueSummary records. Officials select from this backlog to build each meeting's agenda. |
| **Text-to-Speech Read-Aloud** | Amazon Polly reads agenda items aloud (Aditi voice Hindi, Raveena English). S3-cached — same text never re-synthesized. Accessibility for illiterate citizens. |
| **Grammar Correction + Translation** | Bedrock corrects STT output and produces enhanced_original + enhanced_english + enhanced_hindi. Rural development context-aware. |
| **MOM Generation (Planned)** | Separate video-mom-backend module generates structured Minutes of Meeting from uploaded audio. Built but not yet integrated into the main application. Planned for future release. |

### Authentication & Identity

| Feature | Description |
|---------|------------|
| **Face Recognition Authentication** | 128-dimension face descriptor via face-api.js. Liveness detection: blink (2 required) + head movement (5 required) via MediaPipe FaceMesh. Euclidean distance matching (threshold 0.4). No passwords, no OTPs. |
| **Biometric Attendance** | Officials take facial biometric attendance of citizens to meet quorum. Verification method recorded per citizen (face/manual). Unforgeable digital attendance record. Eliminates paper sign-in fraud. |

### Meeting Management

| Feature | Description |
|---------|------------|
| **Meeting Scheduling & RSVP** | Officials schedule Gram Sabha with date, time, location, expected duration. Citizens RSVP before meeting. SNS notifications triggered on schedule (delivery requires DLT registration). |
| **Quorum Enforcement** | Minimum quorum required for Gram Sabha — meeting can only start once quorum is met. Sabha criteria configurable per panchayat (supports decimal values). |
| **Issue Lifecycle Tracking** | REPORTED → PICKED_IN_AGENDA → DISCUSSED_IN_GRAM_SABHA → RESOLVED / TRANSFERRED / NO_ACTION_NEEDED. Citizens see real-time status. Officials add resolution remarks. Zero promises lost. |

### Multi-Portal System

| Portal | Description |
|--------|------------|
| **Citizen Portal** | Face login (last 4 digits of voter ID + face scan), voice/text reporting of issues with optional attachments, view own and all panchayat issues, RSVP for upcoming Gram Sabhas, view past and upcoming meetings with details, mark attendance via face biometric, support tickets. |
| **Official Portal** | Login with username/password (changeable), report issues for self or on behalf of citizens, register citizens via face biometric, edit panchayat contact details and letterhead, schedule and manage Gram Sabhas, create/update/delete agenda items, select from AI-generated agenda summary, take facial biometric attendance, issue management (filter by status/category/priority/ward), PDF exports with letterhead. |
| **Admin Portal** | Create and manage panchayats (with LGD code, wards, sabhaCriteria), add citizen data from CSV, create and manage officials (6 roles), optionally onboard citizens via face biometric, update citizen profiles, manage support tickets, view overall metrics via dashboard. |

### Infrastructure Features

| Feature | Description |
|---------|------------|
| **Provider Abstraction** | 8 env var switches: STT_PROVIDER, LLM_PROVIDER, TRANSLATION_PROVIDER, TTS_PROVIDER, STORAGE_BACKEND, FACE_VERIFICATION_PROVIDER, USE_DOCUMENTDB, COMPREHEND_ENABLED. Swap any service without code changes. |
| **PDF Export with Letterhead** | Attendance reports, issue summaries. Custom panchayat letterhead upload. Hindi font support via jsPDF + html2pdf.js. |
| **Multi-Language UI** | English and Hindi interface via React Context language switcher with static translation files. 10+ languages supported. AI content translated via AWS Translate. |
| **Support Ticket System** | Citizens and officials can raise help desk tickets. Anonymous submission allowed — protects vulnerable reporters. |
| **4-Layer Security** | API Gateway (key + 100K/day quota) → Nginx (TLS 1.2/1.3 + 10 req/s per IP) → JWT Auth (3 role-specific secrets, expiry 12h-72h) → Secrets Manager (encrypted credentials). |

### Planned / Future Features

| Feature | Status |
|---------|--------|
| **Integrated MOM Generation** | video-mom-backend module built separately. Full integration into main app workflow planned. |
| **eSign for Documents** | Planned — digital signing of Gram Sabha agenda and MOM by Pradhan and ward members. |
| **Citizen Self-Attendance** | Planned — allow citizens to mark their own attendance via face biometric at the meeting venue. |
| **Live SMS Delivery** | SNS code integrated and triggers on meeting schedule. Requires AWS sandbox exit + TRAI DLT registration for actual SMS delivery. |

---

*Continue to: [Visual Representations & Diagrams →](./02-diagrams.md)*
