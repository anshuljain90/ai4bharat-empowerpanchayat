# eGramSabha

**eGramSabha** is an AI-driven, voice-first, face-authenticated platform that digitizes the entire Gram Sabha lifecycle — from citizen registration to issue resolution tracking. It serves 250,000+ Gram Panchayats through three role-based portals: Admin, Official, and Citizen.

**Problem Statement:** PS03 - AI for Rural Innovation & Sustainable Systems
**Team:** eGramSabha | **Team Leader:** Anshul Jain
**Hackathon:** AWS AI for Bharat Hackathon

---

## Live Prototype

| Portal | URL | Login Details |
|--------|-----|---------------|
| **Admin Portal** | [https://44.194.253.143/admin/login](https://44.194.253.143/admin/login) | Username: `admin`, Password: `AdminPassword123` |
| **Official Portal** | [https://44.194.253.143/official/login](https://44.194.253.143/official/login) | Username: configured official username, Password: same as username |
| **Citizen Portal** | [https://44.194.253.143/citizen/login](https://44.194.253.143/citizen/login) | Last 4 digits of Voter ID + Face scan (passwordless) |

**Demo Video:** [Google Drive](https://drive.google.com/drive/folders/1aLeLtSPIDUaoypi3TAu2tg4I-TpxVUNH)

### Portal Access Details

**Admin Portal** — Full system administration
- Login with username `admin` and password `AdminPassword123`
- Manage panchayats (create/edit with LGD codes), officials (6 roles), and citizen records
- Import members via CSV — sample files available in [`demo/`](demo/) folder (`sample-10citizens.csv`, `sample-30citizens.csv`, `sample-citizens.csv`)
- Configure sabha quorum criteria, feature toggles, letterhead upload

**Official Portal** — Gram Sabha management
- Login with the official's configured username (password is the same as the username)
- Register citizens with voter ID + face capture (liveness: 2 blinks + 5 head movements)
- Create/manage issues, schedule Gram Sabha meetings, take biometric attendance
- Generate AI-powered agendas and issue summaries, export PDF reports

**Citizen Portal** — Voice-first citizen participation
- Login using last 4 digits of Voter ID + face recognition (passwordless, no OTP)
- Citizens must be registered by an official first (face photo captured during registration)
- Report issues via voice or text in native language, view meeting history, RSVP for meetings

---

## The Problem

India's 73rd Constitutional Amendment (1992) created 250,000+ Gram Panchayats and mandated Gram Sabhas as the foundation of grassroots democracy. Three decades later, that promise remains largely unfulfilled:

| Statistic | Impact |
|-----------|--------|
| **5-10%** | Average Gram Sabha attendance |
| **<3%** | Women participation in many states |
| **60%+** | Rural Indians with limited literacy |
| **30%** | Eligible citizens excluded from welfare schemes |
| **ZERO** | Digital trail of Gram Sabha decisions |

Key barriers include paper-based agendas (low awareness), forgeable sign-in sheets, handwritten minutes (subjective/incomplete), single-language proceedings (excludes tribal communities), no issue tracking (promises forgotten), and physical presence required (excludes women, elderly, differently-abled).

---

## 5-Step Gram Sabha Lifecycle

```
REGISTER (Face) → REPORT (Voice) → MEET (Agenda) → RECORD (Attendance) → TRACK (Status)
```

1. **REGISTER** — Admin adds citizens via CSV or manual entry. Officials onboard via face biometric. 128-dim face descriptor stored — no passwords, no OTPs.
2. **REPORT** — Citizens record voice complaints in native language, anytime. AI transcribes, corrects grammar, translates, analyzes sentiment, assigns priority.
3. **MEET** — Officials schedule Gram Sabha. AI summarizes issues into backlog. Officials select items for agenda. Translated to multiple languages with TTS read-aloud.
4. **RECORD** — Officials take facial biometric attendance to meet quorum threshold. Meeting auto-transitions to IN_PROGRESS when quorum met.
5. **TRACK** — Every issue tracked: `REPORTED → PICKED_IN_AGENDA → DISCUSSED_IN_GRAM_SABHA → RESOLVED`. Officials add resolution remarks. Zero promises lost.

---

## AI Features

### Voice Issue Reporting Pipeline
1. Citizen records voice in native language (6 categories, 20+ subcategories)
2. Audio uploaded to S3/GridFS as issue attachment
3. STT transcription — provider-agnostic: Jio / Whisper / AWS Transcribe
4. Grammar correction via Bedrock Nova Lite
5. 3-language output: enhanced_original + enhanced_english + enhanced_hindi
6. Sentiment analysis: label, scores, key phrases (top 10)
7. Auto-priority: Health/safety + strong negative → URGENT auto-upgrade
8. Results stored in MongoDB: issue.sentiment, issue.keyPhrases, issue.priority

### AI Issue Summarization & Agenda Generation
- **Summarization:** Hourly cron job checks for unsummarized issues → Bedrock Nova Lite categorizes, deduplicates, generates concise summaries with sentiment + priority carried forward
- **Agenda:** Officials select from AI-summarized backlog → structured numbered items → AWS Translate converts to Hindi + regional languages → Amazon Polly TTS read-aloud with S3 caching
- Post-meeting: undiscussed items return to backlog automatically

### Face Authentication
- **Registration:** Liveness check (2 blinks + 5 head movements via MediaPipe FaceMesh) → face-api.js extracts 128-dim descriptor → stored in MongoDB
- **Login:** Last 4 digits of voter ID + camera capture → Euclidean distance threshold < 0.4 → JWT issued
- **Production:** Rekognition IndexFaces per panchayat, SearchFacesByImage at 90% similarity

### TTS & Multilingual Support
- SHA256 content hash caching — same text never re-synthesized
- **10+ languages:** Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi, English
- UI: English and Hindi via React Context with static translation files
- AI content translated via AWS Translate across all supported languages

---

## Architecture

### System Overview

```
Browser → API Gateway → Nginx (TLS) → Backend Services → MongoDB
                                     ├── Node.js/Express :5000 (CRUD, Auth, Cron)
                                     └── Python/FastAPI :8000 (AI Pipelines)
```

4 Docker containers on bridge network: frontend, backend, video-mom-backend, mongodb

### Architecture Layers

| Layer | Components |
|-------|-----------|
| **Browser (Client)** | React 19, MUI 7, face-api.js, MediaPipe FaceMesh, JioMeet SDK, jsPDF |
| **API Gateway** | REST REGIONAL, 100 req/s, API key auth, 100K/day quota |
| **Nginx Reverse Proxy** | TLS 1.2/1.3, GZIP, 10 req/s per IP, security headers, 500MB upload |
| **Node.js / Express** | JWT auth (4 secrets), CRUD, S3 upload, SNS, cron jobs, Winston logging |
| **Python / FastAPI** | STT (3 providers), Bedrock LLM, Polly TTS, Translate, sentiment analysis |
| **MongoDB** | 14 collections, GridFS, DocumentDB-compatible, 3 Docker volumes |

### Security — 6 Layers

1. **API Gateway** — API key + 100 req/s rate limit + 200 burst + 100K/day quota
2. **Nginx** — TLS 1.2/1.3 + 10 req/s per IP + HSTS + XSS-Protection
3. **Express Middleware** — Helmet + CORS + xss-clean + hpp + content security policy
4. **JWT Authentication** — 3 role-specific secrets: Admin 12h, Official 24h, Citizen 72h, Refresh 7d
5. **RBAC Authorization** — 7 roles with per-resource permissions, ward-scoped data access
6. **Secrets Manager** — Zero hardcoded credentials (egramsabha/prod secret with 4 JWT keys)

**Roles:** ADMIN, SECRETARY, PRESIDENT, WARD_MEMBER, COMMITTEE_SECRETARY, GUEST, CITIZEN

### Provider Abstraction — Zero Lock-In

Swap any service without code changes by flipping environment variables:

| Variable | Options | Purpose |
|----------|---------|---------|
| `STT_PROVIDER` | jio / whisper / aws_transcribe | Speech-to-Text engine |
| `LLM_PROVIDER` | bedrock / huggingface | Large Language Model backend |
| `TRANSLATION_PROVIDER` | aws_translate / llm | Translation engine |
| `TTS_PROVIDER` | polly / disabled | Text-to-Speech service |
| `STORAGE_BACKEND` | s3 / gridfs | File storage backend |
| `FACE_VERIFICATION_PROVIDER` | local / rekognition | Face matching engine |
| `USE_DOCUMENTDB` | true / false | MongoDB → DocumentDB switch |

---

## AWS Services — 15 Total

### Active (11)
| Service | Usage |
|---------|-------|
| **Amazon Bedrock** | Nova Lite — grammar correction, summarization, sentiment, translation fallback |
| **Amazon S3** | 2 buckets, Intelligent-Tiering — face photos, TTS cache, letterheads, attachments |
| **AWS Translate** | Auto-detect source — AI content across 10+ Indian languages |
| **Amazon Polly** | Aditi (Hindi) + Raveena (English) — TTS read-aloud with SHA256 S3 caching |
| **API Gateway** | REST REGIONAL — single entry point, 100 req/s, API key auth |
| **CloudWatch** | 2 log groups — Winston + watchtower, JSON logs, 30-day retention |
| **Secrets Manager** | egramsabha/prod — 4 JWT secrets, graceful fallback to env vars |
| **EC2** | t3.medium — Docker Compose host, burstable CPU for AI spikes |
| **EBS** | 20 GB gp3 — 3 persistent Docker volumes |
| **Elastic IP** | Static address — DNS and API Gateway endpoint |
| **IAM** | Least-privilege — per-service access policies |

### Code-Ready (4)
| Service | Usage |
|---------|-------|
| **Rekognition** | Server-side face verification, 90% threshold, per-panchayat collections |
| **DocumentDB** | Managed MongoDB, multi-AZ, automated backups |
| **AWS Transcribe** | 24+ languages, async batch via S3 |
| **SNS** | SMS notifications, requires TRAI DLT registration |

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 19, MUI 7, face-api.js 0.22.2, MediaPipe FaceMesh, JioMeet SDK, jsPDF + html2pdf.js |
| **Backend API** | Node.js 20, Express 4, Mongoose 8, Sharp, Winston |
| **AI Backend** | Python 3.11, FastAPI, Motor, boto3, ffmpeg-python |
| **Database** | MongoDB 7 (14 collections, GridFS), DocumentDB-compatible |
| **Infrastructure** | Docker Compose, Nginx, AWS (11 active + 4 code-ready services) |

---

## Cost — $15–20/month

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| EC2 (t3.medium) | $12–30 | Burstable CPU for AI spikes |
| EBS (20 GB gp3) | $1.60 | 3 Docker volumes |
| Bedrock (Nova Lite) | $2–5 | $0.06/1K input, $0.24/1K output |
| S3 (2 buckets) | $0.50 | Intelligent-Tiering |
| Secrets Manager | $0.40 | 1 secret |
| Translate, Polly, CloudWatch, API Gateway | $0–2 | Free tier covers most usage |
| **Total** | **$15–20** | Hackathon scale (1–5 panchayats) |

### Scale Projections

| Stage | Scale | Monthly Cost | Per Citizen/Year |
|-------|-------|-------------|-----------------|
| Hackathon | 1–5 panchayats | $15–20 | — |
| Pilot | 100 panchayats | $320 | ~$3 |
| State | 5K panchayats | $3,250 | ~$0.80 |
| National | 250K panchayats | $30–37K | $0.60–0.72 |

> Physical Gram Sabha: Rs 500+/meeting vs Digital eGramSabha: Rs 5/citizen/year — **~100x cost reduction**

---

## Roadmap

| Phase | Items |
|-------|-------|
| **Immediate** | Activate AWS Transcribe, TRAI DLT for SNS SMS, Enable Rekognition |
| **Short-term** | DocumentDB migration, MOM full integration, eSign, Mobile app (React Native), e-Gram Swaraj integration |
| **Medium-term** | Multi-panchayat escalation, Analytics dashboards, Video Gram Sabha, Citizen self-attendance |
| **National** | 250K panchayats rollout, Aadhaar integration, Open API for CSOs, Scheme delivery tracking |

---

## How to Get Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/anshuljain90/ai4bharat-empowerpanchayat.git
   cd ai4bharat-empowerpanchayat
   ```

2. **Set up MongoDB:**
   - Ensure MongoDB is installed and running on your system
   - Start MongoDB on the default port (27017)

3. **Set up Backend:**
   ```bash
   cd backend
   npm install
   npm start
   ```
   The backend server will start running on `http://localhost:5000`

4. **Set up Frontend:**
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

5. **Access the Application:**
   - Open your browser and go to `http://localhost:3000`
   - The backend API will be available at `http://localhost:5000`

---

## Contribution Guidelines

We welcome contributions from everyone! Here's how you can help:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Make your changes and test thoroughly.
4. Submit a pull request explaining your changes.

---

## Licensing

eGramSabha is open source. Please review the [LICENSE](LICENSE) file for detailed terms.

---

## Contact

For queries or collaboration opportunities, please reach out at:
**Anshul Jain**
📧 [anshul_jain2008@yahoo.co.in](mailto:anshul_jain2008@yahoo.co.in)
