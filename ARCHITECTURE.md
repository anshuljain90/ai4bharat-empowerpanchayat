# eGramSabha — Architecture Document

> **AI for Bharat Hackathon | Powered by AWS**
> Digital Platform for Gram Sabha Management — From Paper to Panchayat-as-a-Service

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [The Solution](#2-the-solution)
3. [System Architecture](#3-system-architecture)
4. [AWS Services Deep Dive](#4-aws-services-deep-dive)
5. [Data Architecture](#5-data-architecture)
6. [Provider Abstraction Pattern](#6-provider-abstraction-pattern)
7. [AI Pipeline Deep Dive](#7-ai-pipeline-deep-dive)
8. [Security Architecture](#8-security-architecture)
9. [Scale Story](#9-scale-story-hackathon--national)
10. [Cost Analysis](#10-cost-analysis)
11. [Technical Decisions & Justifications](#11-technical-decisions--justifications)
12. [Demo Script & Verification](#12-demo-script--verification)

---

## 1. The Problem

### India's Democratic Last Mile

India has **250,000+ Gram Panchayats** — the constitutional foundation of local self-governance. The 73rd Amendment mandates regular **Gram Sabha** meetings where every adult citizen can participate in decisions affecting their village.

### Current Reality

| Aspect | Current Process | Pain Point |
|--------|----------------|------------|
| **Agenda** | Hand-written, posted on notice boards | Low awareness, especially for remote hamlets |
| **Attendance** | Paper sign-in sheets | Easy to forge, no biometric verification |
| **Participation** | Physical presence only | Excludes women, elderly, differently-abled |
| **Minutes** | Hand-written by clerk | Subjective, often incomplete, no accountability trail |
| **Issue Tracking** | Paper registers or verbal complaints | No follow-up, no status visibility for citizens |
| **Language** | Single language (usually official state language) | Excludes communities speaking different dialects |
| **Notifications** | Word-of-mouth, wall posters | Many citizens unaware of meetings |

### The Numbers

- **Average Gram Sabha attendance: 5-10%** of eligible voters
- Women's participation often below **3%** in many states
- Over **60% of rural Indians** have limited literacy — making paper-based systems exclusionary
- No digital trail means **zero accountability** for promises made in meetings

---

## 2. The Solution

### eGramSabha: End-to-End Digital Gram Sabha Platform

A voice-first, face-authenticated platform that digitizes the entire Gram Sabha lifecycle — from citizen registration to issue resolution tracking.

### 5 Core Workflows

```
1. REGISTER  ──>  2. REPORT  ──>  3. MEET  ──>  4. RECORD  ──>  5. TRACK
   (Face)          (Voice)        (Agenda)      (AI MOM)       (Status)
```

**1. Citizen Registration (Face-Based)**
- Citizens register with voter ID and face capture
- 128-dimension face descriptor stored for future authentication
- No passwords — face is the credential (inclusive for low-literacy users)

**2. Issue Reporting (Voice-First)**
- Citizens record voice complaints in their native language
- AI transcribes, corrects grammar, translates to English/Hindi
- Sentiment analysis auto-detects urgency (health/safety → URGENT)

**3. Meeting Management**
- Officials schedule Gram Sabha, select issues for agenda
- AI generates structured agenda from reported issues
- Agenda translated to multiple languages, read aloud via TTS
- SMS notifications sent to all registered citizens (requires DLT registration for India)

**4. AI-Powered Minutes (MOM)**
- Meeting audio uploaded and transcribed
- AI generates structured Minutes of Meeting
- Auto-translated to English + Hindi + regional language
- Stored as permanent digital record

**5. Multi-Language Accessibility**
- UI available in 10+ Indian languages via static translation files (`frontend/src/utils/translations.js`)
- AI-generated content (agendas, MOMs, transcriptions) translated via AWS Translate
- Text-to-Speech for agenda read-aloud via Amazon Polly (accessibility for low-literacy)
- Voice-to-text for issue reporting (no typing needed)

### Key Differentiators

| Feature | Why It Matters |
|---------|---------------|
| **Voice-First** | 60%+ of rural India has limited literacy |
| **Face Auth** | No passwords to forget, no OTPs needed in low-connectivity |
| **AI MOM** | Eliminates subjective hand-written minutes |
| **10+ Languages** | Constitutional requirement for local language governance |
| **Issue Tracking** | First-ever accountability trail for Gram Sabha decisions |

---

## 3. System Architecture

### High-Level Architecture

```
                          ┌──────────────────────────────────────────┐
                          │            AWS Cloud Services             │
                          │                                          │
                          │  ┌──────────┐ ┌───────────┐ ┌────────┐ │
                          │  │ Bedrock   │ │Transcribe*│ │  S3    │ │
                          │  │(Nova Lite)│ │  (STT)    │ │(Store) │ │
                          │  └──────────┘ └───────────┘ └────────┘ │
                          │                                          │
                          │  ┌──────────┐ ┌───────────┐ ┌────────┐ │
                          │  │Translate  │ │  Polly    │ │ SNS**  │ │
                          │  │(AI text)  │ │  (TTS)    │ │ (SMS)  │ │
                          │  └──────────┘ └───────────┘ └────────┘ │
                          │                                          │
                          │  ┌──────────┐ ┌───────────┐ ┌────────┐ │
                          │  │CloudWatch│ │ Secrets   │ │  IAM   │ │
                          │  │ (Logs)   │ │ Manager   │ │(Access)│ │
                          │  └──────────┘ └───────────┘ └────────┘ │
                          │                                          │
                          │  ┌────────────────────────────────────┐ │
                          │  │         API Gateway (REST)          │ │
                          │  │  eGramSabha-MOM-API │ prod stage   │ │
                          │  │  100 req/s │ 200 burst │ API key   │ │
                          │  └──────────────────┬─────────────────┘ │
                          └─────────────────────┼───────────────────┘
                                                │ HTTP_PROXY
                                                │ /{proxy+} → :8000
                                                │
┌──────────┐     ┌──────────────────────────────┼───────────────────────┐
│          │     │           EC2 (t3.medium)     │                       │
│          │     │                               │                       │
│ Browser  │────>│  ┌────────────────────────────┼──────────────────┐   │
│ (React)  │ 443 │  │       Nginx (Reverse Proxy)│                  │   │
│          │     │  │  :80 → :443 redirect  │  TLS termination      │   │
│          │     │  └────────┬───────────────────┬──────────────────┘   │
│          │     │           │ /api/*            │ /mom-api/*           │
│          │     │  ┌────────▼────────┐ ┌───────▼──────────────────┐   │
│          │     │  │  Node.js :5000  │ │    FastAPI :8000         │   │
│          │     │  │  (Backend API)  │ │    (AI/MOM Backend)      │◄──┘
│          │     │  │                 │ │                          │
│          │     │  │ • Auth/JWT      │ │ • STT (Whisper/Transcribe)│
│          │     │  │ • CRUD APIs     │ │ • LLM (Bedrock Nova Lite)│
│          │     │  │ • File Upload   │ │ • TTS (Polly + S3 cache) │
│          │     │  │ • S3 Storage    │ │ • Translation (Translate)│
│          │     │  │ • SNS Notify    │ │ • Sentiment (Bedrock)    │
│          │     │  │ • Cron Jobs     │ │                          │
│          │     │  └────────┬────────┘ └───────┬──────────────────┘
│          │     │           │                   │
│          │     │  ┌────────▼───────────────────▼──────────────────┐
│          │     │  │              MongoDB :27017                    │
│          │     │  │       (DocumentDB-compatible schema)          │
│          │     │  └──────────────────────────────────────────────┘
│          │     │                                                    │
│          │     │  Docker Compose (4 containers on bridge network)   │
└──────────┘     └───────────────────────────────────────────────────┘

Traffic Flows:
  Browser → :443 → Nginx → /api/*     → Node.js :5000  (CRUD, auth, uploads)
  Browser → :443 → Nginx → /mom-api/* → FastAPI :8000  (TTS read-aloud only)
  Node.js → Docker net → FastAPI :8000                  (STT, MOM, agenda, sentiment)
  API GW  → :8000 → FastAPI directly                   (rate-limited external access)

  * Transcribe: code-ready, needs subscription activation
  ** SNS SMS: code-ready, needs DLT registration
```

### Three-Tier Architecture

| Tier | Technology | Container | Port |
|------|-----------|-----------|------|
| **Presentation** | React 18 + Nginx | `frontend` | 80, 443 |
| **Application** | Node.js (Express) | `backend` | 5000 (internal) |
| **AI Services** | Python (FastAPI) | `video-mom-backend` | 8000 |
| **Data** | MongoDB 7 | `mongodb` | 27017 (internal) |

### Docker Compose Orchestration

Four services on a shared bridge network (`egramsabha-net`):

```yaml
# docker-compose.prod.yml
services:
  frontend:     # React build served via Nginx, ports 80/443 exposed
  backend:      # Node.js API, port 5000 internal only
  video-mom-backend:  # FastAPI AI services, port 8000
  mongodb:      # MongoDB 7, port 27017 internal only
```

**Key design decisions:**
- Backend port 5000 is **not exposed** to the host — all traffic routes through Nginx
- MongoDB port 27017 is **internal only** — no direct database access from outside
- Video-MOM backend port 8000 is exposed for API Gateway integration
- Three named volumes persist data: `mongodb_data`, `backend_uploads`, `video_mom_temp_storage`

**Key Files:**
- `docker-compose.prod.yml` — Production orchestration
- `frontend/nginx.prod.conf` — Reverse proxy configuration
- `frontend/Dockerfile.prod` — Multi-stage React build
- `backend/Dockerfile` — Node.js backend container
- `video-mom-backend/Dockerfile` — Python AI backend container

---

## 4. AWS Services Deep Dive

### Overview: 11 Active + 4 Code-Ready Services

```
ACTIVE (11):                          CODE-READY (4):
├── EC2 (Compute)                     ├── Rekognition (Face Verification)
├── EBS (Storage)                     ├── DocumentDB (Managed MongoDB)
├── Elastic IP (Networking)           ├── Transcribe (Speech-to-Text)*
├── S3 (Object Storage)               └── SNS (SMS Notifications)**
├── Bedrock — Nova Lite (AI/LLM)
├── Translate (AI Content Translation)
├── Polly (Text-to-Speech)
├── CloudWatch (Logging)
├── Secrets Manager (Security)
├── API Gateway (Rate Limiting)
└── IAM (Access Control)

* Transcribe: Code complete, requires AWS account subscription activation
** SNS: Code complete, API calls succeed but SMS delivery blocked by
   AWS sandbox mode + India TRAI DLT registration requirement
```

---

### 4.1 Amazon EC2

| | |
|---|---|
| **WHY** | Single compute instance to host all 4 Docker containers during hackathon |
| **WHAT** | t3.medium (2 vCPU, 4 GB RAM) running Amazon Linux 2 with Docker Compose |
| **HOW** | Docker Compose orchestrates frontend, backend, video-mom-backend, and MongoDB containers |
| **COST** | Hackathon: ~$30/mo (on-demand) or ~$12/mo (reserved). National: ECS Fargate auto-scaling |

**Why t3.medium:** Burstable CPU handles periodic AI processing spikes (MOM generation, batch transcription) while keeping baseline cost low. 4 GB RAM is sufficient for Node.js + FastAPI + MongoDB for demo scale.

---

### 4.2 Amazon EBS

| | |
|---|---|
| **WHY** | Persistent block storage for Docker containers, MongoDB data, and uploaded files |
| **WHAT** | gp3 volume attached to EC2 instance |
| **HOW** | Docker named volumes (`mongodb_data`, `backend_uploads`, `video_mom_temp_storage`) map to EBS |
| **COST** | Hackathon: ~$1.60/mo (20 GB gp3). National: Scales with DocumentDB (no local storage needed) |

---

### 4.3 Elastic IP

| | |
|---|---|
| **WHY** | Static IP for consistent access — EC2 IP changes on restart |
| **WHAT** | One Elastic IP associated with the EC2 instance |
| **HOW** | DNS and API Gateway point to this static address |
| **COST** | Free while associated with a running instance |

---

### 4.4 Amazon S3

| | |
|---|---|
| **WHY** | Durable object storage for face images, TTS audio cache, letterheads, and transcription temp files |
| **WHAT** | Two buckets: `egramsabha-assets` (persistent) and `egramsabha-transcribe-temp` (ephemeral) |
| **HOW** | Provider-abstracted storage with `STORAGE_BACKEND=s3` env var |
| **COST** | Hackathon: ~$0.50/mo. National: ~$0.023/GB with Intelligent-Tiering |

**S3 Key Structure:**
```
egramsabha-assets/
├── faces/{panchayatId}/{uuid}_{filename}        # Citizen face photos
├── thumbnails/{panchayatId}/{uuid}_{filename}   # Compressed thumbnails
├── letterheads/{panchayatId}/{uuid}_{filename}  # Panchayat letterheads
├── attachments/{panchayatId}/{uuid}_{filename}  # Issue attachments
└── tts-cache/{language}/{sha256hash}.mp3        # Polly audio cache

egramsabha-transcribe-temp/
└── transcribe-input/{job-name}/{audio-file}     # Temp audio for Transcribe
```

**Implementation Files:**
- `backend/storage/s3Service.js` — S3 upload/download/delete with Intelligent-Tiering storage class
- `backend/storage/storageService.js` — Provider abstraction (`s3` vs `gridfs`)
- `video-mom-backend/app/services/tts_service.py` — S3 caching for Polly output
- `video-mom-backend/app/services/aws_stt_transcriber.py` — Temp upload for Transcribe jobs

**Key Detail:** All uploads use `StorageClass: 'INTELLIGENT_TIERING'` — automatically moves infrequently accessed face images to lower-cost tiers without lifecycle policy management.

---

### 4.5 Amazon Bedrock (Nova Lite)

| | |
|---|---|
| **WHY** | LLM backbone for MOM generation, agenda creation, grammar correction, and sentiment analysis |
| **WHAT** | Amazon Nova Lite (`amazon.nova-lite-v1:0`) via Bedrock Converse API |
| **HOW** | 5 distinct AI tasks, each with specialized prompts |
| **COST** | Hackathon: ~$2-5/mo (pay-per-token). National: ~$0.06/1K input + $0.24/1K output tokens |

**5 AI Tasks Powered by Bedrock:**

| Task | Function | Prompt Strategy |
|------|----------|----------------|
| **MOM Generation** | `generate_multilingual_mom()` | System prompt as MOM formatting expert; outputs JSON with `{lang}_mom`, `english_mom`, `hindi_mom` |
| **Agenda Generation** | `generate_multilingual_agenda_from_issues()` | Takes issue list, generates structured agenda with numbering |
| **Grammar Correction** | `correct_transcription()` | Rural development expert prompt; corrects STT output, translates to English + Hindi |
| **Sentiment Analysis** | `analyze_issue()` | Returns structured JSON: sentiment label/scores, key phrases, priority (URGENT/NORMAL) |
| **Translation** | `translate_text()` | Fallback translation when AWS Translate is unavailable |

**Implementation Files:**
- `video-mom-backend/app/services/llm_service.py` — Main LLM service (1400+ lines), all Bedrock interactions
- `video-mom-backend/app/services/comprehend_service.py` — Issue sentiment analysis via Bedrock

**Bedrock Converse API Usage:**
```python
# From llm_service.py:85-120
response = self.bedrock_client.converse(
    modelId=settings.BEDROCK_MODEL_ID,      # amazon.nova-lite-v1:0
    messages=converse_messages,
    system=system_parts,
    inferenceConfig={
        "maxTokens": bedrock_max,            # Up to 4096
        "temperature": 0.3,                   # Low for consistent output
        "topP": 0.9,
    },
)
```

---

### 4.6 Amazon Transcribe (Code-Ready)

| | |
|---|---|
| **WHY** | Speech-to-text for meeting recordings and voice issue reports in 10+ Indian languages |
| **WHAT** | Async batch transcription jobs via S3 |
| **HOW** | Upload audio to S3 temp bucket → Start transcription job → Poll for completion → Fetch result |
| **STATUS** | **Code complete but requires AWS account subscription activation** (`SubscriptionRequiredException`). Currently using Whisper (HuggingFace) as STT provider on production (`STT_PROVIDER=whisper`). Switch to `STT_PROVIDER=aws_transcribe` once subscription is activated. |
| **COST** | Hackathon: ~$1-3/mo (free tier: 60 min/mo). National: $0.024/min |

**Supported Indian Languages:**
Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi + more

**Flow:**
```
Audio File → Upload to S3 temp bucket
          → start_transcription_job(LanguageCode, MediaFormat)
          → Poll every 3s (max 5 min timeout)
          → Fetch transcript JSON from result URI
          → Delete temp S3 object + transcription job (cleanup)
```

**Implementation:** `video-mom-backend/app/services/aws_stt_transcriber.py`
**Fallback (Current):** `video-mom-backend/app/services/stt_service.py` (Whisper via HuggingFace Inference API)

---

### 4.7 Amazon Translate

| | |
|---|---|
| **WHY** | Real-time translation of AI-generated content (agendas, MOMs, transcriptions) across Indian languages |
| **WHAT** | `translate_text()` API calls with auto-detect source language |
| **HOW** | Integrated as translation provider in LLM service (`TRANSLATION_PROVIDER=aws_translate`) |
| **COST** | Hackathon: ~$1-2/mo (free tier: 2M chars/mo). National: $15/M chars |

**Important:** AWS Translate is used only for AI-generated content (agendas, MOMs, corrected transcriptions). The UI/frontend internationalization uses static translation files (`frontend/src/utils/translations.js`) with a React Context-based language switcher — no AWS service involved.

**Implementation:** `video-mom-backend/app/services/llm_service.py:156-177`

```python
# AWS Translate integration
response = self.translate_client.translate_text(
    Text=text[:10000],           # API limit per request
    SourceLanguageCode="auto",   # Auto-detect source
    TargetLanguageCode=target,   # e.g., "hi", "ta", "te"
)
```

---

### 4.8 Amazon Polly

| | |
|---|---|
| **WHY** | Text-to-speech for agenda read-aloud — accessibility for low-literacy citizens |
| **WHAT** | `synthesize_speech()` with S3 caching to avoid re-synthesizing identical text |
| **HOW** | SHA256 content hash → check S3 cache → synthesize if miss → cache result |
| **COST** | Hackathon: ~$0.50/mo (free tier: 5M chars/mo). National: $4/M chars (standard) |

**Voice Configuration:**
| Language | Voice | Engine |
|----------|-------|--------|
| Hindi (`hi`) | Aditi | Standard |
| English (`en`) | Raveena | Standard |
| Tamil, Telugu, Bengali, etc. | Aditi (fallback) | Standard |

**S3 Caching Strategy:**
```python
# tts_service.py — Cache key generation
cache_key = f"tts-cache/{language}/{sha256(text:language)}.mp3"

# Flow: Check S3 cache → Cache hit? Return cached audio
#                       → Cache miss? Polly synthesize → Store in S3 → Return
```

**Implementation:** `video-mom-backend/app/services/tts_service.py`

**UI Integration:** `ReadAloudButton` component in `frontend/src/components/ReadAloudButton.js` — placed next to each agenda item in `GramSabhaDetails.js`. Calls `POST /mom-api/tts/speak` and plays returned MP3 audio.

**Why Polly over Browser TTS (`window.speechSynthesis`):**
| | Browser TTS | Amazon Polly |
|---|---|---|
| Hindi quality | Inconsistent — many Android/desktop browsers have no Hindi voice or low-quality fallback | Consistent Aditi voice — natural Hindi prosody |
| Cross-device | Voice availability varies by OS/browser/device — unreliable on rural feature phones | Same quality everywhere — audio delivered as MP3 |
| Caching | No caching — re-synthesizes every time | S3 cache — identical text served from cache, zero latency |
| Offline | Works offline (if voice installed) | Requires network (but cached audio works offline) |

---

### 4.9 Amazon CloudWatch

| | |
|---|---|
| **WHY** | Centralized logging from both Node.js and Python backends for debugging and monitoring |
| **WHAT** | Two log groups: `/egramsabha/backend` and `/egramsabha/video-mom` |
| **HOW** | Winston + winston-cloudwatch (Node.js), watchtower (Python) |
| **COST** | Hackathon: ~$0.50/mo (free tier: 5 GB ingest). National: $0.50/GB |

**Node.js Implementation (`backend/utils/logger.js`):**
```javascript
const cwTransport = new WinstonCloudWatch({
    logGroupName: '/egramsabha/backend',
    logStreamName: `${hostname}-${date}`,
    jsonMessage: true,
    retentionInDays: 30,
});
```

**Resilience:** CloudWatch errors are caught and logged once — the transport auto-disables itself if IAM permissions are missing, preventing retry spam.

---

### 4.10 AWS Secrets Manager

| | |
|---|---|
| **WHY** | Secure storage for JWT secrets and API keys — no hardcoded credentials |
| **WHAT** | Single secret `egramsabha/prod` storing all sensitive configuration as JSON |
| **HOW** | Loaded at app startup, cached in memory, with env var fallback for local dev |
| **COST** | Hackathon: ~$0.40/mo (1 secret). National: $0.40/secret/mo + $0.05/10K API calls |

**Implementation (`backend/config/secrets.js`):**
```javascript
// Load at startup — graceful fallback to env vars
const response = await client.send(new GetSecretValueCommand({
    SecretId: 'egramsabha/prod',
}));
secretsCache = JSON.parse(response.SecretString);

// Runtime access — Secrets Manager first, env var fallback
function getSecret(key) {
    return secretsCache?.[key] || process.env[key];
}
```

**Secrets stored:** `JWT_ADMIN_SECRET`, `JWT_OFFICIAL_SECRET`, `JWT_CITIZEN_SECRET`, `JWT_REFRESH_SECRET`

---

### 4.11 Amazon SNS (Code-Ready)

| | |
|---|---|
| **WHY** | SMS notifications for meeting schedules and issue status updates |
| **WHAT** | Direct SMS publish (no topics) with Transactional SMS type |
| **HOW** | `PublishCommand` with Indian phone number formatting (+91) |
| **STATUS** | **Code complete, API calls succeed (returns MessageId), but SMS delivery blocked.** Two barriers: (1) AWS SNS SMS sandbox — requires phone number verification for each recipient, (2) India TRAI DLT registration — all bulk/transactional SMS to Indian numbers requires a registered sender entity and pre-approved templates. Both are administrative steps, not code issues. |
| **COST** | Hackathon: ~$0.50/mo. National: ~$0.02/SMS (India rate) |

**Two Notification Types:**

| Event | Message Example |
|-------|----------------|
| **Gram Sabha Scheduled** | "Gram Sabha meeting scheduled for {panchayat} on {date}. Please join..." |
| **Issue Status Change** | "Your issue '{text}...' has been picked for the next Gram Sabha agenda" |

**Implementation (`backend/services/notificationService.js`):**
- Sends to registered citizens only (`isRegistered: true` filter)
- Indian number formatting: automatically prepends `+91`
- Sender ID: `eGramSbha` (8 char limit for Indian SMS)
- SMS Type: `Transactional` (guaranteed delivery, higher cost)
- Gated by `SNS_ENABLED=true` env var

**To activate for production:**
1. Request SNS SMS sandbox exit via AWS Support
2. Register entity and message templates on India's DLT portal (Jio/Airtel/Vodafone)
3. Configure DLT Entity ID and Template ID in SNS SMS attributes

---

### 4.12 Amazon API Gateway

| | |
|---|---|
| **WHY** | Rate limiting, API key management, and quota enforcement for expensive AI endpoints (MOM generation, TTS, STT) |
| **WHAT** | REST API (REGIONAL) with HTTP_PROXY integration to EC2 FastAPI backend |
| **HOW** | `{proxy+}` catches all paths, forwards to `http://{EC2_IP}:8000/` (FastAPI directly) |
| **COST** | Hackathon: ~$0.01/mo (free tier: 1M calls/mo). National: $3.50/M calls + response caching |

**Deployed Configuration (verified active):**
```
API Name:    eGramSabha-MOM-API (REGIONAL endpoint)
Stage:       prod
Integration: HTTP_PROXY → EC2:8000 (FastAPI container)

Rate Limit:  100 requests/second
Burst Limit: 200 requests
Daily Quota:  100,000 requests/day (eGramSabha-Standard plan)
API Key:     eGramSabha-Demo-Key (enabled, required for all endpoints)
Security:    TLS 1.0+ (AWS managed)
```

**Why API Gateway for AI Endpoints:**
- MOM generation costs ~$0.02-0.05 per call (Bedrock tokens) — throttling prevents cost runaway
- TTS synthesis costs per character — quota prevents abuse
- API key authentication gates external integrations (mobile apps, third-party systems)
- Usage plan enables per-consumer tracking and billing at scale

**Implementation:** `infra/setup-api-gateway.js` — Automated setup script that creates:
1. REST API (`eGramSabha-MOM-API`) with REGIONAL endpoint
2. `{proxy+}` resource with ANY method
3. HTTP_PROXY integration to EC2 FastAPI on port 8000
4. Usage plan (`eGramSabha-Standard`) with throttling + daily quota
5. API key (`eGramSabha-Demo-Key`)
6. `prod` stage deployment

---

### 4.13 IAM

| | |
|---|---|
| **WHY** | Fine-grained access control — each service gets minimum required permissions |
| **WHAT** | IAM policies for S3, Bedrock, Transcribe, Translate, Polly, SNS, CloudWatch, Secrets Manager |
| **HOW** | Credentials passed via environment variables (hackathon) or IAM roles (production) |
| **COST** | Free |

**Principle of Least Privilege:** Each service only accesses the AWS APIs it needs. The application code checks for credential availability before initializing any AWS client — graceful degradation if permissions are missing.

---

### 4.14 Amazon Rekognition (Code-Ready)

| | |
|---|---|
| **WHY** | Server-side face verification — more secure than client-side face-api.js |
| **WHAT** | Face collections per panchayat, IndexFaces + SearchFacesByImage |
| **HOW** | Full implementation in `backend/services/rekognitionService.js`, activated via `FACE_VERIFICATION_PROVIDER=rekognition` |
| **COST** | $1/1K face operations. National: ~$0.001/verification |

**Implementation (`backend/services/rekognitionService.js`):**
```javascript
// Collection per panchayat: egramsabha-{panchayatId}
// IndexFaces: Store face during registration
// SearchFacesByImage: Match face during login (90% similarity threshold)
// DeleteFaces: Remove face on deregistration
```

**Why Code-Ready, Not Active:** face-api.js running client-side is sufficient for hackathon demo. Rekognition provides server-side verification needed for production (tamper-proof, works across devices).

---

### 4.15 Amazon DocumentDB (Code-Ready)

| | |
|---|---|
| **WHY** | Managed, scalable MongoDB replacement — eliminates database ops overhead |
| **WHAT** | MongoDB wire-compatible managed database |
| **HOW** | All Mongoose schemas are DocumentDB-compatible. Flag: `USE_DOCUMENTDB=true` |
| **COST** | ~$200/mo (db.t3.medium) for pilot. Multi-AZ for production |

**Why Code-Ready, Not Active:** Self-managed MongoDB in Docker is sufficient for hackathon. DocumentDB provides automated backups, multi-AZ failover, and read replicas needed for production scale.

---

## 5. Data Architecture

### MongoDB Collections (14 Models)

```
voter_registration (database)
├── users              # Citizen profiles with face descriptors
├── officials          # Panchayat officials (Sarpanch, Secretary, etc.)
├── panchayats         # Panchayat registry with ward structure
├── wards              # Ward-level divisions within panchayats
├── gramsabhas         # Meeting records with attendance + minutes
├── issues             # Citizen complaints with transcription + sentiment
├── issuesummaries     # AI-generated batch summaries
├── summaryrequests    # Async summary generation tracking
├── rsvps              # Meeting attendance RSVPs
├── roles              # Role definitions (ADMIN, OFFICIAL, CITIZEN)
├── supporttickets     # Help desk tickets
├── platformconfigs    # System-wide configuration
├── modelrefs          # Cross-model reference constants
└── requests (motor)   # AI processing request queue (Python backend)
```

### Key Schema Highlights

**User (Citizen) Schema — `backend/models/User.js`:**
```javascript
{
    name: String,
    voterIdNumber: String,          // Unique citizen identifier
    faceDescriptor: [Number],       // 128-dimension face embedding
    faceImageId: Mixed,             // ObjectId (GridFS) or String (S3 key)
    thumbnailImageId: Mixed,        // Compressed version for lists
    rekognitionFaceId: String,      // AWS Rekognition face ID (production)
    panchayatId: ObjectId,          // Which panchayat they belong to
    mobileNumber: String,           // For SNS notifications
    caste: { name, category },      // SC/ST/OBC/General tracking
    isRegistered: Boolean,          // Face registration complete?
}
```

**Issue Schema — `backend/models/Issue.js`:**
```javascript
{
    text: String,                    // Issue description
    category: Enum,                  // INFRASTRUCTURE, HEALTH, etc. (6 categories)
    subcategory: Enum,               // 20+ subcategories
    priority: 'URGENT' | 'NORMAL',   // Auto-set by AI sentiment analysis
    status: Enum,                    // REPORTED → PICKED_IN_AGENDA → DISCUSSED → RESOLVED
    attachments: [{                  // Voice recordings, photos
        attachment: String,
        mimeType: String,
    }],
    transcription: {                 // Voice-to-text pipeline state
        requestId: String,           // Async processing tracker
        status: Enum,                // PENDING → PROCESSING → COMPLETED
        originalTranscription: String,
        enhancedEnglishTranscription: String,
        enhancedHindiTranscription: String,
        transcriptionProvider: String,
    },
    sentiment: {                     // AI-generated sentiment
        label: String,               // POSITIVE | NEGATIVE | NEUTRAL | MIXED
        score: Number,               // Confidence (0-1)
        scores: { positive, negative, neutral, mixed },
    },
    keyPhrases: [String],            // AI-extracted key phrases
}
```

**GramSabha Schema — `backend/models/gramSabha.js`:**
```javascript
{
    title: String,
    dateTime: Date,
    location: String,
    status: Enum,                    // SCHEDULED → IN_PROGRESS → CONCLUDED
    agenda: [AgendaItem],            // AI-generated from issues
    issues: [ObjectId],              // Linked issues discussed
    attendances: [{                  // Biometric attendance records
        userId: ObjectId,
        checkInTime: Date,
        verificationMethod: String,  // 'face' | 'manual'
    }],
    minutes: String,                 // AI-generated MOM
    transcript: String,              // Raw meeting transcript
    recordingLink: String,           // Meeting audio/video URL
}
```

### Data Access Patterns

| Backend | Driver | Usage |
|---------|--------|-------|
| **Node.js** | Mongoose 8 | CRUD operations, auth, file management |
| **Python** | Motor (async) | AI processing queue, request tracking |

Both backends share the same `voter_registration` database, with the Python backend using Motor's async driver for non-blocking I/O during long-running AI tasks.

---

## 6. Provider Abstraction Pattern

### Strategy Pattern for Vendor Independence

Every external service is abstracted behind a provider interface, selectable via environment variables:

```
┌─────────────────────────────────────────────────────────────┐
│                    Provider Abstraction                      │
│                                                             │
│  ENV VAR                  OPTIONS              DEFAULT      │
│  ─────────────────────────────────────────────────────────  │
│  STT_PROVIDER          =  jio | whisper | aws_transcribe    │
│  LLM_PROVIDER          =  huggingface | bedrock             │
│  TRANSLATION_PROVIDER  =  llm | aws_translate               │
│  TTS_PROVIDER          =  polly | disabled                   │
│  STORAGE_BACKEND       =  gridfs | s3                        │
│  FACE_VERIFICATION_PROVIDER = local | rekognition            │
│  USE_DOCUMENTDB        =  true | false                       │
│  COMPREHEND_ENABLED    =  true | false                       │
└─────────────────────────────────────────────────────────────┘
```

### How It Works

**Storage Example (`backend/storage/storageService.js`):**
```javascript
const backend = process.env.STORAGE_BACKEND || 'gridfs';
if (backend === 's3') {
    module.exports = require('./s3Service');
} else {
    module.exports = require('./gridfsService');
}
```

**STT Example (`video-mom-backend/app/api/endpoints.py:254-272`):**
```python
provider = settings.STT_PROVIDER.lower()
if provider == "aws_transcribe":
    transcriber = get_aws_stt_transcriber()
    transcribe_func = lambda path: transcriber.transcribe_audio(path, language)
elif provider == "whisper":
    transcribe_func = stt_transcriber.transcribe_audio
else:  # "jio"
    transcribe_func = lambda path: jio_stt.transcribe_audio(path, language)
```

### Why This Matters

| Benefit | Example |
|---------|---------|
| **No vendor lock-in** | Switch from Jio STT to AWS Transcribe with one env var change |
| **Local dev without AWS** | Use `gridfs` + `huggingface` + `local` face — no AWS account needed |
| **A/B testing** | Compare AWS Transcribe vs Whisper accuracy by swapping provider |
| **Incremental AWS adoption** | Start with free-tier alternatives, switch to AWS services one by one |
| **Scale without rewrite** | Move from GridFS to S3, MongoDB to DocumentDB — same code, different config |

---

## 7. AI Pipeline Deep Dive

### Pipeline 1: Voice Issue Reporting

```
Citizen records voice complaint
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Audio Upload   │───>│  STT Provider   │───>│  Bedrock (Nova)  │
│  (attachment)   │    │  Whisper* or    │    │  Grammar Correct │
│                 │    │  AWS Transcribe  │    │  + Translate     │
└─────────────────┘    └─────────────────┘    └────────┬─────────┘
                                                       │
                       * Current: Whisper              │
                         (Transcribe needs             │
                          subscription)       ┌────────▼─────────┐
                                              │  Bedrock (Nova)  │
                                              │  Sentiment +     │
                                              │  Key Phrases +   │
                                              │  Priority        │
                                              └────────┬─────────┘
                                                       │
                                              ┌────────▼─────────┐
                                              │  MongoDB Store   │
                                              │  issue.sentiment │
                                              │  issue.keyPhrases│
                                              │  issue.priority  │
                                              └──────────────────┘
```

**Detailed Flow:**
1. Citizen records audio → uploaded as attachment to issue
2. Cron job detects audio attachment → initiates transcription (`cronJobs.js`)
3. STT provider transcribes audio (currently Whisper via HuggingFace; AWS Transcribe when subscription activated)
4. Raw transcription → Bedrock grammar correction prompt
5. Output: `enhanced_original`, `enhanced_english`, `enhanced_hindi`
6. Completed transcription → Bedrock sentiment analysis (`comprehend_service.py`)
7. Returns: sentiment label/scores, key phrases, suggested priority
8. **If `suggestedPriority === 'URGENT'`, auto-upgrades issue priority** (`cronJobs.js:51-52`)
9. All results stored in MongoDB (issue.sentiment, issue.keyPhrases, issue.priority)

### Pipeline 2: Meeting MOM Generation

```
Official uploads meeting recording
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Audio Upload   │───>│  STT Provider   │───>│  Bedrock (Nova)  │
│  (multipart)    │    │  Whisper* or    │    │  MOM Generation  │
│                 │    │  AWS Transcribe  │    │  3-lang output   │
└─────────────────┘    └─────────────────┘    └────────┬─────────┘
                                                       │
                                              ┌────────▼─────────┐
                                              │  JSON Output:    │
                                              │  {               │
                                              │   english_mom,   │
                                              │   hindi_mom,     │
                                              │   {lang}_mom     │
                                              │  }               │
                                              └──────────────────┘
```

**MOM Prompt Strategy (from `llm_service.py:763-791`):**
- System prompt positions AI as "MOM formatting expert familiar with Panchayat-level issues"
- Enforces structure: Meeting Overview → Discussion Points → Decisions → Action Items → Next Steps
- Requires formal government-record language but simple enough for villagers
- Outputs JSON with `english_mom`, `hindi_mom`, and `{primary_language}_mom`
- Temperature: 0.3 (low) for consistent, factual output

**Large Meeting Handling:**
- Transcriptions >2000 chars are split into overlapping chunks (1500 char chunks, 200 char overlap)
- Each chunk processed independently for key points
- Final synthesis prompt merges all chunk summaries into coherent MOM

### Pipeline 3: Agenda Generation

```
Official selects issues for Gram Sabha
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Issue List     │───>│  Bedrock (Nova)  │───>│  AWS Translate   │
│  (with IDs)     │    │  Structured      │    │  Multi-language  │
│                 │    │  Agenda Gen      │    │                  │
└─────────────────┘    └─────────────────┘    └────────┬─────────┘
                                                       │
                                              ┌────────▼─────────┐
                                              │  Amazon Polly    │
                                              │  TTS Read-Aloud  │
                                              │  (S3 cached)     │
                                              └────────┬─────────┘
                                                       │
                                              ┌────────▼─────────┐
                                              │  SNS Notify      │
                                              │  Citizens via SMS│
                                              └──────────────────┘
```

**Flow:**
1. Official selects issues → `POST /agenda/generate/{language}`
2. Bedrock generates structured agenda with numbered items
3. Agenda auto-translated to English + Hindi + regional language
4. Agenda text sent to Polly for TTS synthesis (Read Aloud button in UI)
5. Audio cached in S3 (`tts-cache/{lang}/{hash}.mp3`)
6. SNS sends meeting notification SMS to registered citizens

---

## 8. Security Architecture

### Authentication: Face-Based Biometric

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Registration │     │    Login      │     │   API Access  │
│              │     │              │     │              │
│ Voter ID +   │     │ Face capture  │     │ JWT token    │
│ Face capture │────>│ → match 128D  │────>│ per request  │
│ → Store 128D │     │   descriptor  │     │ in header    │
│   descriptor │     │ → Issue JWT   │     │              │
└──────────────┘     └───────────────┘     └──────────────┘
```

**Why Face Auth (No Passwords):**
- 60%+ of rural users have limited literacy → passwords are exclusionary
- No OTPs needed → works in areas with intermittent connectivity
- Face descriptor (128 numbers) is the credential — stored in MongoDB
- Client-side matching via face-api.js (hackathon) or Rekognition (production)

### JWT Architecture (4 Separate Secrets)

| Token Type | Secret | Expiry | Purpose |
|-----------|--------|--------|---------|
| Admin | `JWT_ADMIN_SECRET` | 12h | Platform administration |
| Official | `JWT_OFFICIAL_SECRET` | 24h | Panchayat management |
| Citizen | `JWT_CITIZEN_SECRET` | 72h | Issue reporting, meeting attendance |
| Refresh | `JWT_REFRESH_SECRET` | 7d | Token renewal without re-auth |

**Implementation:** `backend/config/jwt.js` — Secrets resolved lazily via Secrets Manager with env var fallback.

### Role-Based Access Control

```
backend/middleware/auth.js
├── isAdmin         → Admin-only routes (panchayat management, user management)
├── isOfficial      → Official routes (meeting management, agenda, MOM)
├── isCitizen       → Citizen routes (issue reporting, RSVP)
├── isAuthenticated → Any authenticated user (profile, settings)
└── anyAuthenticated → Cross-role routes (viewing meetings, issues)
```

### API Security Layers

```
Browser → Nginx (TLS + Rate Limiting) → Node.js (JWT Auth + Role Check)
                                       → FastAPI (TTS only via /mom-api/)

Node.js → Docker internal network → FastAPI (STT, MOM, agenda, sentiment)

External → API Gateway (API Key + Throttling + Quota) → FastAPI :8000
```

| Layer | Protection |
|-------|-----------|
| **Nginx** | TLS 1.2/1.3, rate limiting (10 req/s per IP, 20 burst), security headers (X-Frame-Options, X-XSS-Protection, CORS) |
| **API Gateway** | API key required, 100 req/s rate limit, 200 burst, 100K/day quota |
| **JWT Auth** | Per-request token verification, role-based route access |
| **Secrets Manager** | KMS-encrypted secrets at rest, no hardcoded credentials |
| **CORS** | Origin restriction via `CORS_ORIGIN` env var |

**Key Files:**
- `backend/middleware/auth.js` — JWT verification middleware
- `backend/middleware/roleCheck.js` — Role-based access control
- `backend/middleware/securityMiddleware.js` — Security headers
- `backend/config/jwt.js` — Token generation/verification
- `backend/config/secrets.js` — Secrets Manager integration
- `frontend/nginx.prod.conf` — TLS, rate limiting, security headers

---

## 9. Scale Story (Hackathon → National)

### Phase 1: Hackathon (Current)

```
1 EC2 instance → 4 Docker containers → 1-5 panchayats
```

| Component | Current | Cost |
|-----------|---------|------|
| Compute | t3.medium (single EC2) | ~$30/mo |
| Database | MongoDB in Docker | $0 (included) |
| Storage | GridFS/S3 (minimal) | ~$1/mo |
| AI Services | Bedrock + Translate + Polly (+ Transcribe when activated) | ~$5/mo |
| **Total** | | **~$15-20/mo** |

### Phase 2: Pilot (100 Panchayats)

```
Config changes only: STORAGE_BACKEND=s3, USE_DOCUMENTDB=true
```

| Component | Change | Cost |
|-----------|--------|------|
| Compute | t3.large (2→4 vCPU, 8 GB) | ~$60/mo |
| Database | DocumentDB (db.t3.medium) | ~$200/mo |
| Storage | S3 (all files) | ~$10/mo |
| AI Services | Higher volume, same services | ~$50/mo |
| **Total** | | **~$320/mo** |

### Phase 3: State Level (5,000 Panchayats)

```
Architecture changes: ECS Fargate, CloudFront CDN, multi-AZ
```

| Component | Change | Cost |
|-----------|--------|------|
| Compute | ECS Fargate (auto-scaling) | ~$500/mo |
| Database | DocumentDB multi-AZ (3 nodes) | ~$600/mo |
| Storage | S3 + CloudFront CDN | ~$100/mo |
| AI Services | Reserved throughput | ~$2,000/mo |
| API Gateway | Response caching enabled | ~$50/mo |
| **Total** | | **~$3,250/mo** |

### Phase 4: National (250,000 Panchayats, 250M+ Citizens)

```
Full service mesh: Multi-region, auto-scaling everything
```

| Component | Change | Cost |
|-----------|--------|------|
| Compute | ECS Fargate multi-region | ~$10,000/mo |
| Database | DocumentDB global cluster | ~$5,000/mo |
| Storage | S3 + CloudFront (global) | ~$3,000/mo |
| AI Services | Bedrock Provisioned Throughput | ~$12,000/mo |
| Monitoring | CloudWatch + X-Ray + dashboards | ~$500/mo |
| **Total** | | **~$30,000-37,000/mo** |

### Why It Scales Without Rewriting

Every phase transition is a **configuration change**, not a code rewrite:

| Transition | Config Change |
|-----------|---------------|
| MongoDB → DocumentDB | `USE_DOCUMENTDB=true` |
| GridFS → S3 | `STORAGE_BACKEND=s3` |
| face-api.js → Rekognition | `FACE_VERIFICATION_PROVIDER=rekognition` |
| Whisper → AWS Transcribe | `STT_PROVIDER=aws_transcribe` |
| HuggingFace → Bedrock | `LLM_PROVIDER=bedrock` |
| Docker → ECS | Same Dockerfiles, orchestration change |

---

## 10. Cost Analysis

### Hackathon Cost Breakdown (~$15-20/month)

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| EC2 (t3.medium) | $12-30 | On-demand vs reserved |
| EBS (20 GB gp3) | $1.60 | |
| Elastic IP | $0 | Free while attached |
| S3 | $0.50 | Minimal storage |
| Bedrock (Nova Lite) | $2-5 | Pay per token (MOM + agenda + sentiment) |
| Transcribe | $0 | Not active yet (using Whisper) |
| Translate | $0-1 | 2M chars/mo free tier |
| Polly | $0-0.50 | 5M chars/mo free tier |
| CloudWatch | $0-0.50 | 5 GB/mo free tier |
| Secrets Manager | $0.40 | 1 secret |
| SNS (SMS) | $0 | API works, SMS delivery pending DLT |
| API Gateway | $0 | 1M calls/mo free tier |
| IAM | $0 | Free |
| **Total** | **~$15-20** | |

### National Scale Cost Per Unit

| Metric | Cost |
|--------|------|
| **Per panchayat per month** | ~$120-148 |
| **Per citizen per month** | ~$0.05-0.06 |
| **Per citizen per year** | ~$0.60-0.72 |

### Cost Comparison: Physical vs Digital Gram Sabha

| | Physical | Digital (eGramSabha) |
|---|---------|---------------------|
| **Per meeting** | Rs 500+ (stationery, printing, logistics) | Rs 5/citizen/year |
| **Minutes** | Manual clerk (errors, delays) | AI-generated (instant, accurate) |
| **Notifications** | Wall posters, word-of-mouth | SMS (pennies each) |
| **Record keeping** | Paper files (fire/flood risk) | S3 (11 nines durability) |
| **Language access** | Single language | 10+ languages (auto-translated) |
| **Improvement** | | **~100x cost reduction** |

### Cost Optimization Strategies

| Strategy | Implementation | Savings |
|----------|---------------|---------|
| **S3 Intelligent-Tiering** | All uploads use `INTELLIGENT_TIERING` storage class | Auto-moves cold data to cheaper tiers |
| **Polly S3 Caching** | SHA256 hash-based cache keys in S3 | Avoid re-synthesizing same text |
| **Transcribe Cleanup** | Auto-delete temp S3 objects + jobs after completion | No orphaned storage |
| **API Gateway Throttling** | 100 req/s rate limit prevents abuse | Protects expensive AI endpoints |
| **Bedrock Low Temperature** | 0.3 temperature = shorter, more focused responses | Fewer output tokens = lower cost |
| **Chunked Processing** | Large transcriptions processed in 1500-char chunks | Avoids token limits and failures |

---

## 11. Technical Decisions & Justifications

| We Chose | Over | Because |
|----------|------|---------|
| **Bedrock Nova Lite** | GPT-4 / Claude API | Cost (10x cheaper), data residency (India region), native AWS integration, no external API keys |
| **DocumentDB** (code-ready) | DynamoDB | 128-dim face descriptor arrays need vector queries; aggregation pipelines for issue analytics; MongoDB wire compatibility = zero code changes |
| **REST API Gateway** | HTTP API | Response caching on status endpoints, usage plans with quotas, API key management, CloudWatch integration |
| **S3** | GridFS | 11-nines durability vs single MongoDB instance; lifecycle policies; prerequisite for DocumentDB migration (GridFS not supported) |
| **face-api.js** (hackathon) | Cognito | Face descriptor matching works offline; no email/phone verification needed; inclusive for low-literacy users |
| **Rekognition** (production) | face-api.js | Server-side verification is tamper-proof; scales across devices; liveness detection |
| **Bedrock for Sentiment** | Amazon Comprehend | Comprehend requires separate subscription activation (`SubscriptionRequiredException`); single Bedrock model handles sentiment + key phrases + priority in one call; more flexible prompt-based approach; also detects urgency (health/safety → URGENT) which Comprehend cannot |
| **MongoDB/DocumentDB** | RDS (PostgreSQL) | Flexible schemas for evolving issue categories; 128-dim face descriptor arrays as native fields; nested attendance records; JSON-native storage |
| **FastAPI** (AI backend) | Express.js for everything | Python ecosystem for ML (boto3, motor); async I/O for long-running AI tasks; separate scaling from CRUD backend |
| **Docker Compose** | Kubernetes | Right-sized for hackathon; same Dockerfiles work in ECS/Fargate for production |
| **Nginx reverse proxy** | Direct port exposure | Single TLS termination point; rate limiting; security headers; static asset caching |
| **Winston + CloudWatch** | Console.log / file logs | Centralized logging across containers; 30-day retention; structured JSON for querying |
| **Cron-based polling** | WebSockets for AI status | Simpler architecture; AI jobs take seconds-minutes; polling every minute is sufficient |

---

## 12. Demo Script & Verification

### End-to-End Flow (Touches All Active + Code-Ready AWS Services)

This walkthrough demonstrates every integrated AWS service in a single user journey:

#### Step 1: Register a Citizen
**Services: S3, (Rekognition ready)**
1. Navigate to Citizen Registration
2. Enter voter ID and personal details
3. Capture face photo → stored in **S3** (`faces/{panchayatId}/`)
4. 128-dim face descriptor computed client-side
5. *(Production: face indexed in **Rekognition** collection)*

#### Step 2: Citizen Login
**Services: Secrets Manager, IAM**
1. Citizen captures face → matched against stored descriptor
2. JWT token generated using secret from **Secrets Manager**
3. Token signed with `JWT_CITIZEN_SECRET` (72h expiry)

#### Step 3: Report an Issue via Voice
**Services: S3, Bedrock, CloudWatch** *(+ Transcribe when subscription activated)*
1. Citizen taps "Report Issue" → records voice complaint in Hindi
2. Audio uploaded as attachment → stored in **S3**
3. Cron job detects audio → STT provider transcribes (currently **Whisper**, swappable to **AWS Transcribe**)
4. Raw transcript → **Bedrock Nova Lite** grammar correction
5. Enhanced text returned in original + English + Hindi
6. **Bedrock** sentiment analysis: extracts sentiment, key phrases, priority
7. If URGENT detected (health/safety issues) → auto-upgrades issue priority
8. All operations logged to **CloudWatch**

#### Step 4: Schedule a Gram Sabha Meeting
**Services: SNS** *(SMS delivery pending DLT registration)*
1. Official logs in → schedules Gram Sabha with date/location
2. Selects issues for the agenda
3. **SNS** API called to send SMS to all registered citizens:
   *"Gram Sabha meeting scheduled for {panchayat} on {date}..."*
4. *(Note: SMS delivery requires AWS sandbox exit + India DLT registration — API call succeeds, delivery pending)*

#### Step 5: Generate Meeting Agenda
**Services: Bedrock, Translate**
1. Official clicks "Generate Agenda"
2. Selected issues sent to **Bedrock Nova Lite**
3. AI generates structured agenda with numbered items
4. **AWS Translate** creates Hindi and regional language versions

#### Step 6: Read Agenda Aloud
**Services: Polly, S3**
1. Official/Citizen clicks "Read Aloud" button on agenda
2. Text sent to **Amazon Polly** (Aditi voice for Hindi)
3. Audio cached in **S3** (`tts-cache/{lang}/{hash}.mp3`)
4. Subsequent requests served from cache (no re-synthesis)

#### Step 7: Conduct Meeting & Record
**Services: EC2, EBS**
1. Meeting conducted (in-person or via video link)
2. Audio recording uploaded
3. File stored temporarily in Docker volume on **EBS**

#### Step 8: Generate Minutes of Meeting (MOM)
**Services: Bedrock, Translate** *(+ Transcribe when subscription activated)*
1. Official uploads meeting recording
2. STT provider converts audio to text (currently **Whisper**, swappable to **AWS Transcribe**)
3. **Bedrock Nova Lite** generates structured MOM:
   - Meeting Overview, Discussion Points, Decisions, Action Items, Next Steps
4. MOM auto-translated to English + Hindi + regional language
5. Stored in MongoDB as permanent record

#### Step 9: Notify Citizens of Outcomes
**Services: SNS**
1. Issue statuses updated (DISCUSSED, RESOLVED, TRANSFERRED)
2. **SNS** sends SMS to issue reporter:
   *"Your issue 'broken road near...' was discussed in the Gram Sabha"*

#### Step 10: Verify via API Gateway
**Services: API Gateway, IAM**
1. External system calls AI endpoints via **API Gateway**
2. API key validated, rate limit checked (100 req/s)
3. Request proxied to EC2 → AI backend
4. Response returned with usage tracked in **CloudWatch**

### AWS Services Verification Checklist

| # | Service | Status | Where to Verify |
|---|---------|--------|----------------|
| 1 | **EC2** | Active | Server running at Elastic IP |
| 2 | **EBS** | Active | Docker volumes persist across restarts |
| 3 | **Elastic IP** | Active | Static IP doesn't change on reboot |
| 4 | **S3** | Active | Face images, TTS cache visible in S3 console |
| 5 | **Bedrock** | Active | MOM/agenda/sentiment responses in API output |
| 6 | **Translate** | Active | Multi-language agenda/MOM output |
| 7 | **Polly** | Active | Audio playback on "Read Aloud" button in agenda |
| 8 | **CloudWatch** | Active | Log groups with structured JSON entries |
| 9 | **Secrets Manager** | Active | Secret `egramsabha/prod` in console |
| 10 | **API Gateway** | Active | Invoke URL returns AI endpoint responses |
| 11 | **IAM** | Active | Policies attached to service user |
| 12 | **Transcribe** | Code-Ready | Code in `aws_stt_transcriber.py`, needs subscription activation |
| 13 | **SNS** | Code-Ready | API calls succeed (MessageId returned), SMS delivery needs DLT |
| 14 | **Rekognition** | Code-Ready | Code in `rekognitionService.js`, flag-activated |
| 15 | **DocumentDB** | Code-Ready | Code is wire-compatible, flag-activated |

---

## Appendix: Key File Reference

| Area | File Path | Purpose |
|------|-----------|---------|
| **Docker** | `docker-compose.prod.yml` | Production orchestration (4 services) |
| **Nginx** | `frontend/nginx.prod.conf` | Reverse proxy, TLS, rate limiting |
| **S3 Storage** | `backend/storage/s3Service.js` | S3 upload/download with Intelligent-Tiering |
| **Storage Abstraction** | `backend/storage/storageService.js` | GridFS ↔ S3 provider switch |
| **JWT Auth** | `backend/config/jwt.js` | 4-secret JWT with Secrets Manager |
| **Secrets** | `backend/config/secrets.js` | AWS Secrets Manager integration |
| **CloudWatch Logger** | `backend/utils/logger.js` | Winston + CloudWatch transport |
| **SNS Notifications** | `backend/services/notificationService.js` | SMS for meetings + issues |
| **Rekognition** | `backend/services/rekognitionService.js` | Face indexing + search (code-ready) |
| **Auth Middleware** | `backend/middleware/auth.js` | JWT verification (Admin/Official/Citizen) |
| **Cron Jobs** | `backend/utils/cronJobs.js` | Transcription polling + retry logic |
| **LLM Service** | `video-mom-backend/app/services/llm_service.py` | Bedrock: MOM, agenda, grammar, translation |
| **STT Service** | `video-mom-backend/app/services/aws_stt_transcriber.py` | AWS Transcribe integration |
| **TTS Service** | `video-mom-backend/app/services/tts_service.py` | Polly + S3 caching |
| **Sentiment** | `video-mom-backend/app/services/comprehend_service.py` | Issue analysis via Bedrock |
| **AI Endpoints** | `video-mom-backend/app/api/endpoints.py` | FastAPI routes for all AI services |
| **AI Config** | `video-mom-backend/app/core/config.py` | Provider flags + AWS config |
| **API Gateway** | `infra/setup-api-gateway.js` | Automated gateway setup script |
| **User Model** | `backend/models/User.js` | Citizen schema with face descriptors |
| **Issue Model** | `backend/models/Issue.js` | Issues with transcription + sentiment |
| **GramSabha Model** | `backend/models/gramSabha.js` | Meeting records with attendance |

---

*Document generated for AI for Bharat Hackathon submission — eGramSabha Platform*
*Architecture reflects deployed codebase as of March 2026*
*11 AWS services active, 4 code-ready (Transcribe, SNS SMS delivery, Rekognition, DocumentDB)*
