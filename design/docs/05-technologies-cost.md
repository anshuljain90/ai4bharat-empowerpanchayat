# eGramSabha — Technologies Utilized & Estimated Implementation Cost

## Technologies Utilized

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19, MUI 7, face-api.js, MediaPipe FaceMesh | Single Page Application with client-side face recognition, audio recording, multi-language UI |
| **Backend API** | Node.js 20, Express 4, Mongoose 8 | RESTful API for CRUD, JWT authentication, file management, cron jobs, S3/SNS integration |
| **AI Backend** | Python 3.11, FastAPI, Motor (async MongoDB) | Asynchronous AI pipelines: STT, Bedrock LLM (grammar correction, issue summarization, sentiment analysis), TTS, translation. Separate scaling from CRUD. |
| **Database** | MongoDB 7 (DocumentDB-compatible) | 14 collections with flexible schemas. 128-dim face descriptor arrays. Nested attendance records. GridFS for files. |
| **AI/LLM** | Amazon Bedrock — Nova Lite (Converse API) | 4 active AI tasks: grammar correction, issue summarization, sentiment analysis, translation fallback. MOM generation available in separate module (planned integration). Temp 0.3. |
| **STT** | Provider-agnostic: Jio STT / Whisper / AWS Transcribe | 3 swappable providers via STT_PROVIDER env var. Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali + more. |
| **Translation** | AWS Translate (auto-detect source) | AI-generated content translated across 10+ Indian languages. 2M chars/mo free tier. |
| **TTS** | Amazon Polly + S3 content-hash cache | Aditi (Hindi), Raveena (English). SHA256 cache key → never re-synthesize same text. |
| **Object Storage** | Amazon S3 (Intelligent-Tiering, 2 buckets) | Face images, TTS audio cache, letterheads, attachments, transcription temp files. |
| **Security** | Secrets Manager + JWT (4 secrets) + Helmet + CORS + xss-clean + hpp | Zero hardcoded credentials. JWT expiry: Admin 12h, Official 24h, Citizen 72h, Refresh 7d. 6-role RBAC with per-resource permissions. |
| **Traffic** | API Gateway + Nginx reverse proxy | Defense in depth: API key + throttle (100 req/s) + TLS + rate limit (10/s per IP) + security headers. |
| **Logging** | CloudWatch: winston-cloudwatch + watchtower | 2 log groups (/egramsabha/backend, /egramsabha/video-mom). Structured JSON. 30-day retention. |
| **SNS** | Amazon SNS | SMS notifications for meeting schedules. Integrated in code (triggers on Gram Sabha scheduling with SNS_ENABLED=true). Delivery requires AWS sandbox exit + India TRAI DLT registration. |
| **Infrastructure** | Docker Compose, EC2 t3.medium, EBS gp3, Elastic IP | 4 containers on bridge network. Same Dockerfiles work in ECS Fargate for production scale. |
| **PDF** | jsPDF + html2pdf.js | Attendance reports, MOM documents with custom panchayat letterhead. Hindi font support. |
| **Video** | JioMeet SDK | Virtual Gram Sabha participation for citizens who cannot attend in person. |

### Frontend Dependencies (Key Libraries)

| Library | Version | Purpose |
|---------|---------|---------|
| react | 19.x | UI framework |
| @mui/material | 7.0.1 | Component library |
| face-api.js | 0.22.2 | Face detection & descriptor extraction |
| @mediapipe/face_mesh | latest | Liveness detection (blink, head movement) |
| @jiomeet/core-sdk-web | 1.1.0 | Video meeting integration |
| jspdf | 3.0.1 | PDF generation |
| html2pdf.js | 0.10.3 | HTML-to-PDF conversion |
| axios | 1.8.4 | HTTP client |
| react-router-dom | 7.5.0 | SPA routing |
| date-fns | 2.29.3 | Date formatting |

### Backend Dependencies (Key Libraries)

| Library | Version | Purpose |
|---------|---------|---------|
| express | 4.21.2 | Web framework |
| mongoose | 8.15.1 | MongoDB ODM |
| jsonwebtoken | 9.0.2 | JWT authentication |
| bcryptjs | 3.0.2 | Password hashing |
| multer | 1.4.4 | File upload handling |
| sharp | 0.34.2 | Image processing (thumbnails) |
| winston | 3.11.0 | Logging framework |
| node-cron | 4.1.0 | Scheduled jobs |
| helmet | 8.1.0 | Security headers |
| @aws-sdk/* | 3.600.0 | AWS service clients (S3, Secrets Manager, Rekognition, SNS, API Gateway) |

### AI Backend Dependencies (Key Libraries)

| Library | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Async web framework |
| motor | 3.3.2 | Async MongoDB driver |
| boto3 | 1.34.0+ | AWS SDK (Bedrock, Transcribe, Polly, Translate) |
| watchtower | 3.0.0 | CloudWatch log integration |
| pydantic | 2.5.0 | Data validation |
| ffmpeg-python | 0.2.0 | Audio/video processing |

---

## Estimated Implementation Cost

### Current Hackathon Cost: $15-20/month

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| EC2 (t3.medium, 2 vCPU, 4 GB) | $12-30 | On-demand vs reserved. Burstable CPU for AI spikes. |
| EBS (20 GB gp3) | $1.60 | 3 Docker volumes: mongodb_data, backend_uploads, temp_storage |
| Elastic IP | $0 | Free while attached to running instance |
| S3 (2 buckets) | $0.50 | Intelligent-Tiering. Minimal storage at demo scale. |
| Bedrock (Nova Lite) | $2-5 | Pay per token. $0.06/1K input + $0.24/1K output tokens. |
| Translate | $0-1 | 2M chars/mo free tier. AI content only (not UI). |
| Polly | $0-0.50 | 5M chars/mo free tier. S3 caching reduces repeat calls. |
| CloudWatch | $0-0.50 | 5 GB/mo free tier. 2 log groups. |
| Secrets Manager | $0.40 | 1 secret (egramsabha/prod with 4 JWT keys) |
| API Gateway | $0 | 1M calls/mo free tier. REST API with usage plan. |
| **TOTAL** | **$15-20** | |

### Scale Projections

| Phase | Scale | What Changes | Monthly Cost | Per Citizen/Year |
|-------|-------|-------------|-------------|-----------------|
| **Hackathon** | 1-5 panchayats | Current setup | $15-20 | — |
| **Pilot** | 100 panchayats | Config changes only: STORAGE_BACKEND=s3, USE_DOCUMENTDB=true | $320 | ~$3 |
| **State** | 5K panchayats | ECS Fargate auto-scaling, CloudFront CDN, multi-AZ DocumentDB | $3,250 | ~$0.80 |
| **National** | 250K panchayats, 250M+ citizens | Multi-region, full service mesh, Bedrock provisioned throughput | $30-37K | $0.60-0.72 |

### Physical vs Digital: ~100x Cost Reduction

> **Physical Gram Sabha**: Rs 500+ per meeting (stationery, printing, logistics, travel, venue setup)
>
> **Digital eGramSabha**: Rs 5 per citizen per year
>
> **At national scale**: Rs 0.60 per citizen per year — less than printing one notice board poster

### Cost Optimizations Built-In

| Optimization | Mechanism |
|-------------|-----------|
| S3 Intelligent-Tiering | Auto-moves cold face images and old attachments to cheaper storage tiers |
| Polly S3 Caching | SHA256 hash of text as cache key — same agenda text never re-synthesized |
| API Gateway Throttling | 100 req/s protects expensive Bedrock/Polly endpoints from abuse or DDoS |
| Bedrock Low Temperature (0.3) | Shorter, focused responses = fewer output tokens = lower cost |
| Chunked Processing | 1500-char chunks with 200 overlap avoid token limits on long transcripts |
| Transcribe Cleanup | Auto-delete temp S3 objects and transcription jobs after completion |

### Scale Without Code Rewrite — Config Changes Only

| Migration | Environment Variable |
|-----------|---------------------|
| MongoDB → DocumentDB | `USE_DOCUMENTDB=true` |
| GridFS → S3 | `STORAGE_BACKEND=s3` |
| face-api.js → Rekognition | `FACE_VERIFICATION_PROVIDER=rekognition` |
| Whisper → AWS Transcribe | `STT_PROVIDER=aws_transcribe` |
| Docker → ECS Fargate | Same Dockerfiles, orchestration change only |

---

*Continue to: [Performance & Impact →](./06-performance-impact.md)*
