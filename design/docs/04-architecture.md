# eGramSabha — Architecture Diagram

## System Architecture Overview

```mermaid
flowchart TB
    subgraph BROWSER["Browser / Mobile"]
        FE["React 19 + MUI 7\nface-api.js · MediaPipe FaceMesh\nJioMeet SDK · jsPDF · html2pdf.js"]
    end

    subgraph EDGE["AWS Edge"]
        APIGW["API Gateway (REST, REGIONAL)\neGramSabha-MOM-API\n100 req/s · 200 burst · 100K/day\nAPI Key (x-api-key header)"]
    end

    subgraph EC2["EC2 t3.medium — Docker Compose (4 containers on egramsabha-net)"]
        NGINX["Nginx Reverse Proxy\nTLS 1.2/1.3 · GZIP\n10 req/s per IP · 500MB upload\nSecurity Headers"]

        NODE["Node.js / Express :5000\nAuth (JWT 4 secrets) · CRUD\nS3 Upload · SNS · Cron Jobs"]

        PYTHON["Python / FastAPI :8000\nAI Service Backend\nSTT (3 providers) · Bedrock LLM (5 tasks)\nPolly TTS · AWS Translate"]

        MONGO["MongoDB :27017\n14 Collections · GridFS\nDocumentDB-compatible"]

        NGINX -->|"/api/*"| NODE
        NGINX -->|"/mom-api/*"| PYTHON
        NODE -->|"Docker network"| PYTHON
        NODE --> MONGO
        PYTHON --> MONGO
    end

    subgraph AWS_ACTIVE["AWS Services — Active (11)"]
        direction TB
        BEDROCK["Amazon Bedrock\nNova Lite (Converse API)\nGrammar Correction · Summarization\nSentiment · Translation Fallback"]
        TRANSLATE["AWS Translate\n10+ Indian Languages\nAuto-detect Source"]
        POLLY["Amazon Polly\nAditi (Hindi) · Raveena (English)\nS3 Cache (SHA256)"]
        S3["Amazon S3 (×2)\nIntelligent-Tiering\negramsabha-assets\negramsabha-transcribe-temp"]
        CW["CloudWatch\n2 Log Groups\n30-day Retention"]
        SM["Secrets Manager\negramsabha/prod\n4 JWT Secrets"]
        IAM["IAM\nLeast-Privilege"]
    end

    subgraph AWS_READY["Code-Ready — Activate via ENV (4)"]
        direction TB
        REK["Rekognition\n90% Threshold\nPer-Panchayat Collections"]
        DOCDB["DocumentDB\nManaged MongoDB\nMulti-AZ Failover"]
        TRANS["AWS Transcribe\n24+ Languages\nBatch via S3"]
        SNS["Amazon SNS\nTransactional SMS\n+91 · eGramSbha\nNeeds sandbox exit +\nTRAI DLT registration"]
    end

    FE -->|"HTTPS"| APIGW
    APIGW --> NGINX
    PYTHON --> BEDROCK
    PYTHON --> TRANSLATE
    PYTHON --> POLLY
    POLLY --> S3
    NODE --> S3
    NODE --> CW
    PYTHON --> CW
    NODE --> SM

    style BROWSER fill:#1565C0,color:#fff,stroke:#0D47A1
    style EDGE fill:#FF6F00,color:#fff,stroke:#E65100
    style EC2 fill:#37474F,color:#fff,stroke:#263238
    style AWS_ACTIVE fill:#1B5E20,color:#fff,stroke:#1B5E20
    style AWS_READY fill:#E65100,color:#fff,stroke:#E65100
    style FE fill:#1976D2,color:#fff
    style APIGW fill:#FB8C00,color:#fff
    style NGINX fill:#607D8B,color:#fff
    style NODE fill:#43A047,color:#fff
    style PYTHON fill:#FB8C00,color:#fff
    style MONGO fill:#7B1FA2,color:#fff
    style BEDROCK fill:#2E7D32,color:#fff
    style TRANSLATE fill:#2E7D32,color:#fff
    style POLLY fill:#2E7D32,color:#fff
    style S3 fill:#00838F,color:#fff
    style CW fill:#00838F,color:#fff
    style SM fill:#00838F,color:#fff
    style IAM fill:#00838F,color:#fff
    style REK fill:#FFA000,color:#fff
    style DOCDB fill:#FFA000,color:#fff
    style TRANS fill:#FFA000,color:#fff
    style SNS fill:#FFA000,color:#fff
```

---

## Architecture Layers

### Layer 1: Frontend (Browser/Mobile)

| Component | Purpose |
|-----------|---------|
| React 19 | Single Page Application framework |
| MUI 7 (Material-UI) | UI component library with responsive design |
| face-api.js | 128-dimension face descriptor extraction for authentication |
| MediaPipe FaceMesh | Real-time liveness detection (blink + head movement) |
| JioMeet SDK | Virtual meeting integration for remote Gram Sabha participation |
| jsPDF + html2pdf.js | Client-side PDF generation with Hindi font support |
| Axios | HTTP client for API communication |
| React Context | State management for auth and language switching |

### Layer 2: AWS Edge — API Gateway

| Property | Value |
|----------|-------|
| API Name | eGramSabha-MOM-API |
| Type | REST API (REGIONAL endpoint) |
| Stage | prod |
| Rate Limit | 100 requests/second |
| Burst | 200 requests |
| Daily Quota | 100,000 requests/day |
| Auth | API Key required (x-api-key header) |
| Integration | HTTP_PROXY to Nginx on EC2 |
| Timeout | 29 seconds |
| Monitoring | CloudWatch tracing enabled (X-Ray), INFO level logging |

### Layer 3: Nginx Reverse Proxy

| Property | Value |
|----------|-------|
| HTTPS | HTTP → HTTPS redirect on port 80 |
| TLS | 1.2 and 1.3 only, high cipher suites |
| Compression | GZIP enabled (text, JSON, JavaScript, SVG) |
| Max Upload | 500 MB |
| Proxy Timeout | 300 seconds (read/send) |
| Rate Limit | 10 req/sec per IP with 20 burst (for /api/) |
| Security Headers | X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy, HSTS |
| Static Cache | 30-day expires for .js, .css, images, fonts |
| Routing | `/` → React frontend, `/api/*` → Node.js :5000, `/mom-api/*` → FastAPI :8000 |

### Layer 4: Node.js / Express Backend (:5000)

| Responsibility | Details |
|---------------|---------|
| Authentication | JWT with 4 secrets (Admin 12h, Official 24h, Citizen 72h, Refresh 7d). Secrets from Secrets Manager. |
| CRUD Operations | RESTful API for panchayats, officials, citizens, issues, meetings, wards, RSVPs |
| File Management | S3 upload/download for face images, letterheads, attachments |
| Cron Jobs | `cronJobs.js`: retries failed transcriptions, runs sentiment after transcription. `summaryCronJobs.js`: hourly issue summarization for agenda backlog. |
| Notifications | SNS SMS on meeting scheduling (integrated but requires AWS sandbox exit + TRAI DLT registration for actual delivery) |
| Security | Helmet, CORS, xss-clean, hpp, express-rate-limit, bcryptjs |
| Logging | Winston + winston-cloudwatch → CloudWatch `/egramsabha/backend` |

### Layer 5: Python / FastAPI AI Backend (:8000)

The `video-mom-backend` service is the AI service backend. It handles speech-to-text, LLM-powered text processing, text-to-speech, and translation. MOM generation capability exists in the codebase as a separate module but is not yet integrated into the main application workflow.

| Responsibility | Details |
|---------------|---------|
| Speech-to-Text | 3 providers (Jio/Whisper/AWS Transcribe) via STT_PROVIDER env var |
| LLM Tasks (4 active) | Bedrock Nova Lite: grammar correction, issue summarization (for agenda backlog), sentiment analysis, translation fallback. MOM generation available in module (planned integration). |
| Text-to-Speech | Amazon Polly with S3 SHA256 caching |
| Translation | AWS Translate for AI-generated content across 10+ Indian languages |
| Sentiment | Bedrock-based: sentiment label/scores, key phrases, suggested priority |
| Async Processing | Motor (async MongoDB driver) for non-blocking database operations |
| Logging | watchtower → CloudWatch `/egramsabha/video-mom` |

### Layer 6: MongoDB (:27017)

14 collections with DocumentDB-compatible schemas:

| Collection | Purpose | Key Fields |
|-----------|---------|-----------|
| users | Citizen profiles | voterIdNumber, faceDescriptor (128-dim array), faceImageId, panchayatId, isRegistered |
| officials | Panchayat officials | name, role (6 roles), panchayatId, password (bcrypt), isActive |
| panchayats | Gram Panchayat registry | name, lgdCode, state, district, block, population, language, wards[], letterheadImageId |
| wards | Sub-divisions | name, wardNumber, population, panchayatId |
| gramsabhas | Meeting records | title, dateTime, location, agenda[], issues[], attendances[], minutes, transcript, status |
| issues | Citizen complaints | text, category, subcategory, priority, status, statusHistory, sentiment, keyPhrases, transcription |
| issueSummaries | AI-generated summaries | panchayatId, summary, insights |
| summaryRequests | Async job tracking | status (PENDING/PROCESSING/COMPLETED/FAILED), requestId, retryCount |
| rsvps | Meeting RSVPs | gramSabhaId, userId, status |
| roles | Role definitions | name (ADMIN/SECRETARY/PRESIDENT/WARD_MEMBER/COMMITTEE_SECRETARY/GUEST), permissions[] |
| supporttickets | Help desk tickets | subject, description, status, priority, createdBy |
| platformconfigs | System config | liveness settings (blink_count, movement_count), feature flags |
| modelrefs | Reference constants | metadata |
| requests | AI processing queue | status, requestType, result (Python backend, Motor) |

Docker volumes: `mongodb_data`, `backend_uploads`, `video_mom_temp_storage`

---

## Traffic Flow

```mermaid
sequenceDiagram
    participant Browser
    participant APIGW as API Gateway
    participant Nginx
    participant Node as Node.js :5000
    participant Python as FastAPI :8000
    participant MongoDB
    participant AWS as AWS Services

    Note over Browser,AWS: Standard CRUD Request
    Browser->>APIGW: HTTPS + API Key (x-api-key)
    APIGW->>Nginx: HTTP_PROXY (rate-checked)
    Nginx->>Node: /api/* (TLS terminated, rate-limited)
    Node->>MongoDB: Mongoose query
    MongoDB-->>Node: Result
    Node-->>Nginx: JSON response
    Nginx-->>APIGW: Response
    APIGW-->>Browser: HTTPS response

    Note over Browser,AWS: AI Request (Transcription/Summarization/TTS)
    Browser->>APIGW: HTTPS + API Key
    APIGW->>Nginx: HTTP_PROXY
    Nginx->>Python: /mom-api/*
    Python->>AWS: Bedrock / Translate / Polly
    AWS-->>Python: AI result
    Python->>MongoDB: Store result (Motor async)
    Python-->>Nginx: JSON response
    Nginx-->>APIGW: Response
    APIGW-->>Browser: HTTPS response

    Note over Node,Python: Internal AI Trigger — cronJobs.js
    Node->>Python: Retry failed transcriptions (Docker :8000)
    Python->>AWS: STT / Grammar Correction
    AWS-->>Python: Transcription result
    Node->>Python: Run sentiment after transcription
    Python->>AWS: Bedrock sentiment analysis
    AWS-->>Python: Sentiment result
    Python->>MongoDB: Update issue

    Note over Node,Python: Internal AI Trigger — summaryCronJobs.js
    Node->>Python: Hourly issue summarization (Docker :8000)
    Python->>AWS: Bedrock summarization
    AWS-->>Python: Summary result
    Python->>MongoDB: Store in issueSummaries
```

---

## Security Architecture

```mermaid
flowchart TD
    REQ["Incoming Request"] --> L1["Layer 1: API Gateway\nAPI Key validation\n100 req/s rate limit\n100K/day quota"]
    L1 --> L2["Layer 2: Nginx\nTLS 1.2/1.3 termination\n10 req/s per IP rate limit\nSecurity headers (HSTS, CSP)"]
    L2 --> L3["Layer 3: Express Middleware\nHelmet · CORS · xss-clean · hpp\nRequest ID (UUID)\nMorgan logging"]
    L3 --> L4["Layer 4: JWT Authentication\n3 role-specific secrets\nAdmin: 12h · Official: 24h · Citizen: 72h\nRefresh: 7d"]
    L4 --> L5["Layer 5: RBAC Authorization\n6 roles · Per-resource permissions\nWard-scoped access\nPanchayat isolation"]
    L5 --> L6["Layer 6: Secrets Manager\nZero hardcoded credentials\nCached in memory\nEnv var fallback for dev"]
    L6 --> APP["Application Logic"]

    style L1 fill:#FF6F00,color:#fff
    style L2 fill:#607D8B,color:#fff
    style L3 fill:#1565C0,color:#fff
    style L4 fill:#2E7D32,color:#fff
    style L5 fill:#7B1FA2,color:#fff
    style L6 fill:#00838F,color:#fff
```

### RBAC Role Hierarchy

| Role | Scope | Key Permissions |
|------|-------|----------------|
| ADMIN | System-wide | All operations. Bypasses permission checks. |
| SECRETARY | Panchayat | Full panchayat management, meeting CRUD, citizen management, all wards |
| PRESIDENT | Panchayat | Meeting conduct, agenda approval, all wards |
| WARD_MEMBER | Ward | Issues in assigned ward only, attendance marking |
| COMMITTEE_SECRETARY | Panchayat | Meeting notes, limited management |
| GUEST | Read-only | View meetings and public issues only |
| CITIZEN | Own data | Submit issues, RSVP, view own status, support tickets |

---

## Docker Compose Topology

```mermaid
flowchart LR
    subgraph DOCKER["Docker Compose — egramsabha-net (bridge)"]
        FE["frontend\n(React + Nginx)\nPort 80/443"]
        BE["backend\n(Node.js)\nPort 5000"]
        AI["video-mom-backend\n(FastAPI)\nPort 8000"]
        DB["mongodb\n(Mongo 7)\nPort 27017"]

        FE --> BE
        FE --> AI
        BE --> AI
        BE --> DB
        AI --> DB
    end

    VOL1["mongodb_data\n(persistent)"]
    VOL2["backend_uploads\n(persistent)"]
    VOL3["video_mom_temp_storage\n(persistent)"]

    DB --- VOL1
    BE --- VOL2
    AI --- VOL3

    style DOCKER fill:#37474F,color:#fff
    style FE fill:#1976D2,color:#fff
    style BE fill:#43A047,color:#fff
    style AI fill:#FB8C00,color:#fff
    style DB fill:#7B1FA2,color:#fff
```

| Container | Image Base | Port | Health Check | Depends On |
|-----------|-----------|------|-------------|-----------|
| frontend | Node → Nginx (multi-stage) | 80, 443 | — | backend, video-mom-backend |
| backend | Node.js | 5000 (internal) | — | mongodb |
| video-mom-backend | Python | 8000 (exposed) | Every 30s | mongodb |
| mongodb | mongo:7 | 27017 (internal) | — | — |

**Source references**: `docker-compose.prod.yml`, `infra/setup-api-gateway.js`, `frontend/nginx.prod.conf`

---

*Continue to: [Technologies & Cost →](./05-technologies-cost.md)*
