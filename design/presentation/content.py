"""
All slide content for eGramSabha Hackathon Presentation.
Verified against IMPACT.md, ARCHITECTURE.md, and source code.
"""

# ============================================================
# SLIDE 1: Team & Project Info
# ============================================================
SLIDE1 = {
    "team_name": "Empower Panchayat",
    "team_leader": "",
    "problem_statement": "AI-Powered Digital Gram Sabha Platform",
    "project_name": "eGramSabha",
    "tagline": "Sashakt Panchayat, Samriddh Bharat",
    "website": "empowerpanchayat.org | Apache 2.0 Open Source",
}

# ============================================================
# SLIDE 2: Problem Statement
# (Source: IMPACT.md:8-51, ARCHITECTURE.md:25-49)
# ============================================================
SLIDE2 = {
    "title": "Problem Statement",
    "headline": (
        "In 1992, India passed the 73rd Constitutional Amendment — a radical act of faith in its own people. "
        "It created 250,000+ Gram Panchayats and mandated Gram Sabhas as the foundation of grassroots democracy "
        "where every adult citizen can participate. Three decades later, that promise remains largely unfulfilled."
    ),
    "stats": [
        ("5-10%", "Average Gram Sabha\nattendance"),
        ("<3%", "Women participation\nin many states"),
        ("60%+", "Rural Indians with\nlimited literacy"),
        ("30%", "Eligible citizens excluded\nfrom welfare schemes"),
        ("ZERO", "Digital trail of\nGram Sabha decisions"),
    ],
    "barriers": [
        ("Paper agendas on notice boards", "Low awareness — excludes remote hamlets, women at home, daily wage workers"),
        ("Paper sign-in sheets", "Easy to forge — routinely inflated to show higher attendance numbers"),
        ("Hand-written minutes by clerk", "Subjective, often incomplete, sometimes pre-written before the meeting happens"),
        ("Single language proceedings", "Excludes tribal & minority communities — Gondi, Santhali, Bhili speakers silenced"),
        ("No issue tracking system", "Promises forgotten between meetings — citizens stop attending because nothing changes"),
        ("Physical presence required", "Excludes women (social norms), elderly (mobility), differently-abled citizens"),
    ],
    "context": (
        "India has the highest teledensity in the world at 85.69% — even rural teledensity is 59.19%. "
        "The phones are there. The connectivity is there. "
        "What's missing is a platform that meets citizens where they are — on their phones, in their language, with their voice."
    ),
}

# ============================================================
# SLIDE 3a: Brief About the Idea — Solution Overview
# (Source: ARCHITECTURE.md:52-102)
# ============================================================
SLIDE3A = {
    "title": "Brief About the Idea: Solution Overview",
    "overview": (
        "eGramSabha is a voice-first, face-authenticated platform that digitizes the entire "
        "Gram Sabha lifecycle — from citizen registration to issue resolution tracking. "
        "It is a direct response to the structural barriers that prevent Gram Sabhas from "
        "functioning as the Constitution intended."
    ),
    "workflow": "REGISTER (Face) -> REPORT (Voice) -> MEET (Agenda) -> RECORD (AI MOM) -> TRACK (Status)",
    "workflow_details": [
        ("1. REGISTER (Face)", "Citizens register with voter ID and face capture. 128-dimension face descriptor stored — no passwords, no OTPs. If you have a face, you can participate."),
        ("2. REPORT (Voice)", "Citizens record voice complaints in their native language, anytime. AI transcribes, corrects grammar, translates to English/Hindi, detects sentiment and urgency."),
        ("3. MEET (Agenda)", "Officials schedule Gram Sabha with date, time, location. AI generates structured agenda from citizen issues. Agenda translated to multiple languages and read aloud via Amazon Polly TTS. SMS notification sent to registered citizens."),
        ("4. RECORD (AI MOM)", "Meeting audio uploaded. AI generates structured Minutes of Meeting: Meeting Overview, Discussion Points, Decisions Taken, Action Items, Next Steps. Auto-translated to 3 languages. Downloadable as PDF with panchayat letterhead."),
        ("5. TRACK (Status)", "Every issue tracked through lifecycle: REPORTED -> PICKED_IN_AGENDA -> DISCUSSED_IN_GRAM_SABHA -> RESOLVED. Officials add resolution remarks. Citizens see status updates. Zero promises lost."),
    ],
}

# ============================================================
# SLIDE 3b: Why AI is Required
# (Source: IMPACT.md:61-157)
# ============================================================
SLIDE3B = {
    "title": "Why AI is Required",
    "points": [
        (
            "Voice-First Removes the Literacy Barrier",
            "60%+ of rural Indians have limited literacy. Paper complaint registers, written agendas, and printed minutes exclude them by design. "
            "Voice-first AI lets a tribal woman in Jharkhand or an elderly farmer in Tamil Nadu speak a complaint and have it formally recorded "
            "in 3 languages — without writing a single word."
        ),
        (
            "AI Transcription + Grammar Correction + Translation",
            "Raw voice recordings are transcribed by STT (Jio/Whisper/AWS Transcribe — provider-agnostic). "
            "Amazon Bedrock then corrects grammar and translates to the original language + English + Hindi. "
            "A single voice complaint becomes a trilingual formal issue."
        ),
        (
            "AI Sentiment Analysis + Auto-Priority",
            "Every issue is analysed for sentiment (positive/negative/neutral/mixed), key phrases extracted, and urgency auto-detected. "
            "A complaint about 'sewage flowing into drinking water supply' is automatically flagged URGENT — "
            "it doesn't wait for the next monthly meeting. Officials see a prioritised dashboard: urgent issues first."
        ),
        (
            "AI-Generated Minutes of Meeting (MOM)",
            "Gram Sabha minutes are hand-written by clerks — often days later, subjective, incomplete, sometimes pre-written. "
            "AI generates structured MOM instantly: Meeting Overview, Discussion Points, Decisions Taken, Action Items, Next Steps. "
            "Auto-translated to 3 languages. For the first time, proceedings exist as a permanent, searchable, verifiable record."
        ),
        (
            "AI-Generated Agendas — Democratic by Default",
            "Current agendas are ad-hoc, influenced by powerful voices. AI generates structured agendas from ALL citizen-reported issues — "
            "every voice has equal weight. Officials cannot selectively omit issues."
        ),
        (
            "Text-to-Speech — Information Reaches Everyone",
            "Amazon Polly reads agendas aloud in the citizen's language. The illiterate elderly man who could never read "
            "the notice board can now listen to what will be discussed on his phone."
        ),
        (
            "Without AI: An Impossible Scale Problem",
            "250,000 panchayats x multiple languages x regular meetings = Without AI, this would require an army of clerks, "
            "translators, and transcribers at every panchayat. AI makes inclusive governance scalable."
        ),
    ],
}

# ============================================================
# SLIDE 3c: How AWS Services Are Used
# (Source: ARCHITECTURE.md:214-620)
# ============================================================
SLIDE3C = {
    "title": "How AWS Services Are Used (15 Services — 11 Active, 4 Code-Ready)",
    "active": [
        (
            "Amazon Bedrock (Nova Lite via Converse API)",
            "LLM backbone powering 5 AI tasks: MOM generation, agenda creation, grammar correction, sentiment analysis, and translation fallback. "
            "Temperature 0.3 for consistent output. Large transcriptions chunked (1500 chars, 200 overlap) to handle hour-long meetings."
        ),
        (
            "Amazon S3 (2 buckets, Intelligent-Tiering)",
            "egramsabha-assets: face photos, letterheads, issue attachments, TTS audio cache. "
            "egramsabha-transcribe-temp: temporary audio for Transcribe jobs. "
            "All uploads use INTELLIGENT_TIERING — auto-moves cold data to cheaper tiers."
        ),
        (
            "AWS Translate",
            "Real-time translation of AI-generated content (agendas, MOMs, corrected transcriptions) across 10+ Indian languages. "
            "Auto-detects source language. Used only for AI content — UI uses static translation files."
        ),
        (
            "Amazon Polly + S3 Caching",
            "Text-to-Speech for agenda read-aloud. Aditi voice (Hindi), Raveena (English). "
            "SHA256 content hash -> check S3 cache -> synthesize if miss -> cache result. "
            "Same text never synthesized twice."
        ),
        (
            "API Gateway (REST, REGIONAL)",
            "Single entry point for ALL API traffic. eGramSabha-MOM-API with prod stage. "
            "100 req/s rate limit, 200 burst, 100K requests/day quota. "
            "API key (x-api-key header) from frontend. Protects expensive AI endpoints from abuse."
        ),
        (
            "CloudWatch (2 log groups)",
            "/egramsabha/backend (Winston + winston-cloudwatch) and /egramsabha/video-mom (watchtower). "
            "Centralized structured JSON logging from both Node.js and Python. 30-day retention."
        ),
        (
            "Secrets Manager",
            "Single secret 'egramsabha/prod' storing JWT_ADMIN_SECRET, JWT_OFFICIAL_SECRET, JWT_CITIZEN_SECRET, JWT_REFRESH_SECRET. "
            "Loaded at startup, cached in memory. Graceful fallback to env vars for local dev."
        ),
        (
            "EC2 (t3.medium) + EBS (gp3) + Elastic IP",
            "2 vCPU, 4 GB RAM hosting Docker Compose with 4 containers. Burstable CPU handles AI processing spikes. "
            "20 GB gp3 for persistent volumes. Static IP for DNS and API Gateway."
        ),
        (
            "IAM",
            "Least-privilege policies per service. Each service only accesses AWS APIs it needs. "
            "Graceful degradation if permissions are missing."
        ),
    ],
    "code_ready": [
        (
            "Amazon Rekognition",
            "Server-side face verification. Collections per panchayat. IndexFaces during registration, "
            "SearchFacesByImage during login (90% similarity threshold). Activated via FACE_VERIFICATION_PROVIDER=rekognition."
        ),
        (
            "Amazon DocumentDB",
            "Managed MongoDB replacement. All Mongoose schemas are DocumentDB-compatible. "
            "Activated via USE_DOCUMENTDB=true. Provides automated backups, multi-AZ failover."
        ),
        (
            "AWS Transcribe",
            "Managed STT supporting Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi + more. "
            "Code complete — async batch jobs via S3. Activated via STT_PROVIDER=aws_transcribe."
        ),
        (
            "Amazon SNS",
            "SMS notifications for meeting schedules and issue status updates. "
            "Direct SMS publish with Transactional type, +91 formatting, sender ID 'eGramSbha'. "
            "API calls succeed — delivery needs AWS sandbox exit + India DLT registration."
        ),
    ],
}

# ============================================================
# SLIDE 3d: Value AI Adds to User Experience
# (Source: IMPACT.md:57-157, 161-197)
# ============================================================
SLIDE3D = {
    "title": "Value AI Adds to User Experience",
    "comparisons": [
        (
            "Illiterate citizen (60%+ of rural India)",
            "Cannot report issues — requires writing in a complaint register during office hours",
            "Speaks complaint into phone in any language. AI transcribes, corrects, translates, assigns priority. Issue formally registered."
        ),
        (
            "Panchayat secretary",
            "Hand-writes minutes for hours, often days later. Subjective, sometimes pre-written before meeting.",
            "AI generates structured MOM in seconds: Discussion Points, Decisions, Action Items. 3 languages. Permanent verifiable record."
        ),
        (
            "Women at home (~3% participation)",
            "Must attend male-dominated public meeting. Social norms discourage public speaking. Domestic responsibilities prevent attendance.",
            "Reports issues via voice from home, in her language. Complaint has same formal weight as anyone else's. Face auth — no password needed."
        ),
        (
            "Official creating agenda",
            "Ad-hoc list influenced by powerful voices. No systematic inclusion of citizen complaints.",
            "AI structures agenda from ALL citizen-reported issues. Every voice has equal weight. Democratic by default."
        ),
        (
            "Tribal/minority citizen",
            "Excluded by state language proceedings. Gondi, Santhali, Bhili speakers cannot understand or participate.",
            "Speaks native language. AI translates. Agenda and MOM available in their language. TTS reads aloud."
        ),
        (
            "Block/District administrator",
            "Physical inspection needed to audit Gram Sabhas. Paper records inaccessible.",
            "Digital MOM records, biometric attendance data, issue analytics. Audit remotely. Pattern recognition across panchayats."
        ),
    ],
}

# ============================================================
# SLIDE 4: Features
# (Source: ARCHITECTURE.md full document, frontend components)
# ============================================================
SLIDE4 = {
    "title": "List of Features",
    "features": [
        # --- AI-Powered Features ---
        ("AI: Voice-First Issue Reporting", "Record complaint in any language. AI transcribes, corrects grammar, translates to English + Hindi. No typing required."),
        ("AI: Sentiment Analysis + Auto-Priority", "Every issue analysed for sentiment (positive/negative/neutral/mixed), key phrases extracted. Health/safety issues auto-flagged URGENT."),
        ("AI: Minutes of Meeting Generation", "Upload meeting audio. AI generates structured MOM: Overview, Discussion Points, Decisions, Action Items, Next Steps. 3 languages."),
        ("AI: Agenda Generation", "AI creates structured agenda from citizen-reported issues. Translated to multiple languages. Every voice gets equal representation."),
        ("AI: Text-to-Speech Read-Aloud", "Amazon Polly reads agendas aloud (Aditi voice Hindi, Raveena English). S3-cached — same text never re-synthesized. Accessibility for illiterate citizens."),
        ("AI: Grammar Correction + Translation", "Bedrock corrects STT output and produces enhanced_original + enhanced_english + enhanced_hindi. Rural development context-aware."),
        # --- Authentication & Identity ---
        ("Face Recognition Authentication", "128-dimension face descriptor via face-api.js. Liveness detection: blink (2 required) + head movement (5 required) via MediaPipe FaceMesh. Euclidean distance matching (threshold 0.4). No passwords, no OTPs."),
        ("Biometric Attendance Tracking", "Face-verified or manual check-in at Gram Sabhas. Verification method recorded (face/manual). Unforgeable digital attendance record. Eliminates paper sign-in fraud."),
        # --- Meeting Management ---
        ("Meeting RSVP & Scheduling", "Officials schedule Gram Sabha with date, time, location, expected duration. Citizens RSVP before meeting. SMS notifications to all registered citizens (SNS, code-ready)."),
        ("Issue Lifecycle Tracking", "REPORTED -> PICKED_IN_AGENDA -> DISCUSSED_IN_GRAM_SABHA -> RESOLVED / TRANSFERRED / NO_ACTION_NEEDED. Citizens see real-time status. Officials add resolution remarks. Zero promises lost."),
        # --- Multi-Portal System ---
        ("Citizen Portal", "Face login (last 4 digits of voter ID + face scan), voice/text issue reporting, meeting RSVP, issue status tracking, support tickets. Location-based access via LGD code or cascading dropdowns."),
        ("Official Portal", "Meeting management, AI agenda generation, AI MOM generation, biometric attendance, issue management (filter by status/category/priority/ward), citizen management, PDF exports with letterhead."),
        ("Admin Portal", "Panchayat CRUD with LGD code, ward management, official registration (6 roles), letterhead upload/preview, bulk CSV import (citizens/officials/panchayats), platform configuration, support ticket management."),
        # --- Infrastructure Features ---
        ("Provider Abstraction", "8 env var switches: STT_PROVIDER, LLM_PROVIDER, TRANSLATION_PROVIDER, TTS_PROVIDER, STORAGE_BACKEND, FACE_VERIFICATION_PROVIDER, USE_DOCUMENTDB, COMPREHEND_ENABLED. Swap any service without code changes."),
        ("PDF Export with Letterhead", "Attendance reports, MOM documents, issue summaries. Custom panchayat letterhead upload. Hindi font support via jsPDF + html2pdf.js."),
        ("Multi-Language UI", "English and Hindi interface via React Context language switcher with static translation files. 10+ languages supported. AI content translated via AWS Translate."),
        ("Support Ticket System", "Citizens and officials can raise help desk tickets. Anonymous submission allowed — protects vulnerable reporters."),
        ("4-Layer Security", "API Gateway (key + 100K/day quota) -> Nginx (TLS 1.2/1.3 + 10 req/s per IP) -> JWT Auth (3 role-specific secrets, expiry 12h-72h) -> Secrets Manager (encrypted credentials)."),
    ],
}

# ============================================================
# SLIDE 5: Visual Representations
# (Uses Mermaid-rendered diagram images)
# ============================================================
SLIDE5 = {
    "title": "Visual Representations",
    "workflow_steps": [
        ("1. REGISTER", "Face-authenticated\ncitizen onboarding"),
        ("2. REPORT", "Voice-first issue\nsubmission"),
        ("3. MEET", "AI-generated agenda\n& scheduled Sabha"),
        ("4. RECORD", "AI Minutes of Meeting\n& attendance"),
        ("5. TRACK", "Issue lifecycle\n& status updates"),
    ],
    "governance_loop": (
        "Report Issue (anytime) -> Issue Analysed (AI sentiment + priority) -> "
        "Agenda Generated (AI from issues) -> Meeting Held (biometric attendance) -> "
        "MOM Generated (AI structured) -> Decisions Tracked (lifecycle status) -> "
        "Status Updates (to citizens) -> (continuous cycle)"
    ),
}

# ============================================================
# SLIDE 6: Process Flow / Use-Case Diagrams
# (Source: ARCHITECTURE.md:781-888, verified against source)
# ============================================================
SLIDE6 = {
    "title": "Process Flow: AI Pipelines",
    "pipelines": [
        {
            "name": "Voice Issue Reporting Pipeline",
            "steps": [
                "Citizen records voice complaint in native language (6 categories: Infrastructure, Basic Amenities, Social Welfare, Earning Opportunities, Culture & Nature, Other; 20+ subcategories)",
                "Audio uploaded as issue attachment, stored in S3 or GridFS",
                "Cron job detects audio attachment, initiates transcription",
                "STT provider transcribes (Jio/Whisper/AWS Transcribe — provider-agnostic)",
                "Raw transcript sent to Bedrock Nova Lite for grammar correction",
                "Output: enhanced_original + enhanced_english + enhanced_hindi",
                "Completed transcription sent to Bedrock for sentiment analysis",
                "Returns: sentiment label/scores, key phrases, suggested priority",
                "If suggestedPriority === 'URGENT' (health/safety), auto-upgrades issue priority",
                "All results stored in MongoDB: issue.sentiment, issue.keyPhrases, issue.priority",
            ],
            "source": "cronJobs.js:51-53, llm_service.py, comprehend_service.py",
        },
        {
            "name": "MOM Generation Pipeline",
            "steps": [
                "Official uploads meeting audio recording",
                "STT provider converts audio to full text transcript",
                "If transcript > 2000 chars: split into 1500-char chunks with 200-char overlap",
                "Each chunk processed independently by Bedrock for key points",
                "Final synthesis prompt merges all chunk summaries into coherent MOM",
                "Bedrock generates structured output: Meeting Overview, Discussion Points, Decisions Taken, Action Items, Next Steps",
                "Output as JSON: {english_mom, hindi_mom, {primary_language}_mom}",
                "Temperature 0.3 for consistent, factual output. Formal government-record language.",
                "Stored in MongoDB as permanent digital record",
            ],
            "source": "llm_service.py:763-791",
        },
        {
            "name": "Agenda Generation Pipeline",
            "steps": [
                "Official selects citizen issues for upcoming Gram Sabha",
                "Issue list sent to Bedrock Nova Lite for structured agenda generation",
                "AI creates numbered agenda items with context from each issue",
                "AWS Translate creates Hindi and regional language versions",
                "Agenda text sent to Amazon Polly for TTS synthesis (Read Aloud)",
                "Audio cached in S3 (tts-cache/{lang}/{sha256hash}.mp3)",
                "SNS sends meeting notification SMS to all registered citizens",
            ],
            "source": "llm_service.py, tts_service.py, notificationService.js",
        },
        {
            "name": "Face Authentication Pipeline",
            "steps": [
                "Registration: Voter ID + panchayat selection (cascading dropdowns or LGD code) + face capture",
                "Liveness checks: blink detection (2 blinks required) + head movement (5 movements) via MediaPipe FaceMesh",
                "128-dimension face descriptor computed client-side (face-api.js)",
                "Face image stored in S3 (faces/{panchayatId}/{uuid}), thumbnail generated via Sharp",
                "Descriptor + S3 references stored in MongoDB user record, isRegistered = true",
                "Login: Last 4 digits of voter ID -> fetch matching registered users with thumbnails",
                "Camera capture (no liveness on login), new face descriptor computed",
                "Euclidean distance comparison: threshold < 0.4 (verified at citizenAuthRoutes.js:210,335)",
                "Security token: random token generated client-side, SHA256 hashed server-side, prevents replay",
                "On match: JWT issued (citizen token, 72h expiry, refresh 7d, secret from Secrets Manager)",
                "Production upgrade: Rekognition SearchFacesByImage (90% similarity, per-panchayat collections)",
            ],
            "source": "citizenAuthRoutes.js, FaceRegistration.js",
        },
    ],
}

# ============================================================
# SLIDE 7: Wireframes / Prototype Screenshots
# ============================================================
SLIDE7 = {
    "title": "Wireframes / Prototype Screenshots",
    "screens": [
        "Citizen Login — Voter ID + Panchayat selection + Face scan with liveness detection overlay",
        "Citizen Dashboard — Welcome card, issue statistics, upcoming meetings, report issue button",
        "Voice Issue Reporting — Audio recorder, file attachments, category & subcategory selector",
        "Issue List — Sentiment badges, priority indicators (URGENT/NORMAL), transcription status (PENDING/COMPLETED)",
        "AI-Generated Agenda — Multi-language tabs (English/Hindi/Regional), Read Aloud button per item",
        "Official Dashboard — Meeting management, attendance tracking, issue management, MOM generation",
    ],
}

# ============================================================
# SLIDE 8: Architecture
# (Source: ARCHITECTURE.md:105-175)
# ============================================================
SLIDE8 = {
    "title": "Architecture Diagram",
    "layers": [
        ("Browser (React 19 + MUI 7)", "face-api.js, MediaPipe FaceMesh, JioMeet SDK, jsPDF"),
        ("AWS API Gateway (REST, REGIONAL)", "eGramSabha-MOM-API, 100 req/s, API key auth, 100K/day quota"),
        ("Nginx Reverse Proxy", "TLS 1.2/1.3 termination, GZIP compression, 10 req/s per IP rate limit, 500MB max upload, 300s proxy timeout, security headers (X-Frame-Options, HSTS, XSS-Protection)"),
        ("Node.js / Express :5000", "Auth (JWT 4 secrets), CRUD, S3 file upload, SNS notifications, cron jobs"),
        ("Python / FastAPI :8000", "STT (3 providers), Bedrock LLM (5 tasks), Polly TTS, AWS Translate, sentiment"),
        ("MongoDB :27017", "14 collections (users, officials, panchayats, wards, gramsabhas, issues, issuesummaries, summaryrequests, rsvps, roles, supporttickets, platformconfigs, modelrefs, requests), GridFS, DocumentDB-compatible schemas, 3 named Docker volumes"),
    ],
    "traffic_flows": [
        "Browser -> API Gateway -> Nginx :443 -> /api/* -> Node.js :5000 (CRUD, auth, uploads)",
        "Browser -> API Gateway -> Nginx :443 -> /mom-api/* -> FastAPI :8000 (TTS, MOM, agenda)",
        "Node.js -> Docker internal network -> FastAPI :8000 (STT, sentiment, cron-triggered AI)",
    ],
    "aws_services": {
        "active": ["Bedrock", "S3 (x2)", "Translate", "Polly", "API Gateway", "CloudWatch", "Secrets Manager", "EC2", "EBS", "Elastic IP", "IAM"],
        "code_ready": ["Rekognition", "DocumentDB", "Transcribe", "SNS"],
    },
    "docker": "4 containers on shared bridge network (egramsabha-net): frontend, backend, video-mom-backend, mongodb. 3 named volumes: mongodb_data, backend_uploads, video_mom_temp_storage.",
    "source": "docker-compose.prod.yml, infra/setup-api-gateway.js, frontend/nginx.prod.conf",
}

# ============================================================
# SLIDE 9: Technologies Utilized
# (Source: package.json files, requirements.txt, ARCHITECTURE.md)
# ============================================================
SLIDE9 = {
    "title": "Technologies Utilized",
    "tech": [
        ("Frontend", "React 19, MUI 7, face-api.js, MediaPipe FaceMesh", "Single Page Application with client-side face recognition, audio recording, multi-language UI"),
        ("Backend API", "Node.js 20, Express 4, Mongoose 8", "RESTful API for CRUD, JWT authentication, file management, cron jobs, S3/SNS integration"),
        ("AI Backend", "Python 3.11, FastAPI, Motor (async MongoDB)", "Asynchronous AI pipelines: STT, LLM, TTS, translation, sentiment. Separate scaling from CRUD."),
        ("Database", "MongoDB 7 (DocumentDB-compatible)", "14 collections with flexible schemas. 128-dim face descriptor arrays. Nested attendance records. GridFS for files."),
        ("AI/LLM", "Amazon Bedrock — Nova Lite (Converse API)", "5 AI tasks: MOM generation, agenda creation, grammar correction, sentiment analysis, translation fallback. Temp 0.3."),
        ("STT (Speech-to-Text)", "Provider-agnostic: Jio STT / Whisper (HuggingFace) / AWS Transcribe", "3 swappable providers via STT_PROVIDER env var. Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali + more."),
        ("Translation", "AWS Translate (auto-detect source)", "AI-generated content translated across 10+ Indian languages. 2M chars/mo free tier."),
        ("TTS (Text-to-Speech)", "Amazon Polly + S3 content-hash cache", "Aditi (Hindi), Raveena (English). SHA256 cache key -> never re-synthesize same text."),
        ("Object Storage", "Amazon S3 (Intelligent-Tiering, 2 buckets)", "Face images, TTS audio cache, letterheads, attachments, transcription temp files."),
        ("Security", "Secrets Manager + JWT (4 secrets) + Helmet + CORS + xss-clean + hpp", "Zero hardcoded credentials. JWT expiry: Admin 12h, Official 24h, Citizen 72h, Refresh 7d. 6-role RBAC with per-resource permissions."),
        ("Traffic Management", "API Gateway + Nginx reverse proxy", "Defense in depth: API key + throttle (100 req/s) + TLS + rate limit (10/s per IP) + security headers."),
        ("Logging", "CloudWatch: winston-cloudwatch + watchtower", "2 log groups (/egramsabha/backend, /egramsabha/video-mom). Structured JSON. 30-day retention."),
        ("Infrastructure", "Docker Compose, EC2 t3.medium, EBS gp3, Elastic IP", "4 containers on bridge network. Same Dockerfiles work in ECS Fargate for production scale."),
        ("PDF Generation", "jsPDF + html2pdf.js", "Attendance reports, MOM documents with custom panchayat letterhead. Hindi font support."),
        ("Video Meetings", "JioMeet SDK", "Virtual Gram Sabha participation for citizens who cannot attend in person."),
    ],
}

# ============================================================
# SLIDE 10: Estimated Implementation Cost
# (Source: ARCHITECTURE.md:1038-1088)
# ============================================================
SLIDE10 = {
    "title": "Estimated Implementation Cost",
    "hackathon_costs": [
        ("EC2 (t3.medium, 2 vCPU, 4 GB)", "$12-30", "On-demand vs reserved. Burstable CPU for AI spikes."),
        ("EBS (20 GB gp3)", "$1.60", "3 Docker volumes: mongodb_data, backend_uploads, temp_storage"),
        ("Elastic IP", "$0", "Free while attached to running instance"),
        ("S3 (2 buckets)", "$0.50", "Intelligent-Tiering. Minimal storage at demo scale."),
        ("Bedrock (Nova Lite)", "$2-5", "Pay per token. $0.06/1K input + $0.24/1K output tokens."),
        ("Translate", "$0-1", "2M chars/mo free tier. AI content only (not UI)."),
        ("Polly", "$0-0.50", "5M chars/mo free tier. S3 caching reduces repeat calls."),
        ("CloudWatch", "$0-0.50", "5 GB/mo free tier. 2 log groups."),
        ("Secrets Manager", "$0.40", "1 secret (egramsabha/prod with 4 JWT keys)"),
        ("API Gateway", "$0", "1M calls/mo free tier. REST API with usage plan."),
    ],
    "total": "$15-20/month",
    "scale": [
        ("Hackathon", "1-5 panchayats", "$15-20", "--"),
        ("Pilot (100 panchayats)", "Config changes only: STORAGE_BACKEND=s3, USE_DOCUMENTDB=true", "$320", "~$3/citizen/yr"),
        ("State (5K panchayats)", "ECS Fargate auto-scaling, CloudFront CDN, multi-AZ DocumentDB", "$3,250", "~$0.80/citizen/yr"),
        ("National (250K panchayats)", "Multi-region, full service mesh, Bedrock provisioned throughput", "$30-37K", "$0.60-0.72/citizen/yr"),
    ],
    "comparison": (
        "Physical Gram Sabha: Rs 500+ per meeting (stationery, printing, logistics). "
        "Digital eGramSabha: Rs 5 per citizen per year. ~100x cost reduction. "
        "At national scale: Rs 0.60 per citizen per year — less than printing one notice board poster."
    ),
    "optimizations": [
        "S3 Intelligent-Tiering — auto-moves cold face images to cheaper tiers",
        "Polly S3 caching — SHA256 hash key, same text never re-synthesized",
        "API Gateway throttling — 100 req/s protects expensive AI endpoints",
        "Bedrock low temperature (0.3) — shorter, focused responses = fewer output tokens",
        "Chunked processing — 1500-char chunks avoid token limits on long transcripts",
        "Transcribe cleanup — auto-delete temp S3 objects and jobs after completion",
    ],
    "scale_without_rewrite": [
        ("MongoDB -> DocumentDB", "USE_DOCUMENTDB=true"),
        ("GridFS -> S3", "STORAGE_BACKEND=s3"),
        ("face-api.js -> Rekognition", "FACE_VERIFICATION_PROVIDER=rekognition"),
        ("Whisper -> AWS Transcribe", "STT_PROVIDER=aws_transcribe"),
        ("Docker -> ECS Fargate", "Same Dockerfiles, orchestration change only"),
    ],
}

# ============================================================
# SLIDE 11: Snapshots of the Prototype
# ============================================================
SLIDE11 = {
    "title": "Snapshots of the Prototype",
    "snapshots": [
        "Citizen Login — Voter ID entry, panchayat selection (State/District/Block/Panchayat), face scan with liveness overlay",
        "Voice Issue Reporting — Audio recorder with waveform, category selector (6 categories, 20+ subcategories), file attachments",
        "Transcription Result — Original transcription + Enhanced English + Enhanced Hindi, powered by Bedrock grammar correction",
        "Sentiment Analysis — Badge showing POSITIVE/NEGATIVE/NEUTRAL/MIXED with confidence scores, extracted key phrases, auto-priority",
        "AI-Generated Agenda — Numbered items from citizen issues, multi-language tabs, Read Aloud button (Polly TTS)",
        "MOM Output — Structured sections: Meeting Overview, Discussion Points, Decisions Taken, Action Items, Next Steps. 3 languages.",
        "Official Dashboard — Meeting list with status (SCHEDULED/IN_PROGRESS/CONCLUDED), attendance count, MOM generation button",
        "Admin Portal — Panchayat management, official management, role-based access control configuration, system settings",
    ],
}

# ============================================================
# SLIDE 12: Performance / Benchmarking
# (Source: IMPACT.md:328-363, 404-417)
# ============================================================
SLIDE12 = {
    "title": "Prototype Performance Report / Benchmarking",
    "tatarpur_title": "Tatarpur Digital Gram Sabha (April 2025) — India's First",
    "tatarpur_description": (
        "In April 2025, India's first Digital Gram Sabha was held in Tatarpur village, Haryana. "
        "The results demonstrated what happens when technology removes barriers to participation."
    ),
    "tatarpur_metrics": [
        ("Voter registration", "~10% active participation nationally", "81% registered (650 of 801 eligible voters)", "8x improvement"),
        ("Issues submitted", "Handful (verbal, unrecorded)", "100+ issues submitted in 3 days", "Order of magnitude increase"),
        ("Women participation", "Below 3% in many states", "Approximately 50%", "16x improvement"),
        ("Decisions taken", "Few, unrecorded or pre-written", "Multiple, digitally signed decisions", "Permanent record"),
        ("Time to minutes", "Days later (if at all)", "Minutes — AI-generated instantly", "Instant"),
    ],
    "tatarpur_outcomes": (
        "Concrete outcomes from a single meeting: garbage management system with tenant fees, "
        "prioritised road repairs, transgender welfare allocation (Rs 2,100 minimum), and a solar power plant "
        "on 24 acres of unused land. Citizens independently decided to levy local taxes and contribute resources — "
        "a private company donated a tractor. Door-to-door registration campaign with tablets brought 250 additional "
        "participants beyond typical attendance. Women specifically encouraged by female enumerators. "
        "This is self-governance working as Gandhi envisioned."
    ),
    "impact": [
        ("Citizen Participation", "Voice-first reporting, face authentication, phone-based access", "5% -> 30%+ Gram Sabha attendance"),
        ("Women's Empowerment", "Remote voice reporting from home, no public speaking required", "3% -> 50% women participation (Tatarpur benchmark)"),
        ("Welfare Delivery", "Citizen-verified beneficiary lists in Gram Sabha, digital tracking", "Reduce 30% exclusion error in welfare schemes"),
        ("Transparency", "AI-generated MOMs, permanent digital records, searchable & auditable", "Every decision verifiable — no more pre-written minutes"),
        ("Accountability", "Issue lifecycle tracking: REPORTED -> DISCUSSED -> RESOLVED", "Zero promises lost between meetings"),
        ("Local Economy", "Citizens advocate for infrastructure, livelihood schemes via formal channel", "Reduce distress migration push factors"),
        ("Youth Engagement", "Mobile-first interface, real-time tracking, transparent process", "Younger demographic participating in governance"),
        ("Administrative Efficiency", "Digital records, pattern analytics, automated MOM & agenda", "Block/District oversight without physical inspection"),
        ("Cost Reduction", "Digital vs paper-based processes at scale", "~100x cost reduction (Rs 500+/meeting vs Rs 5/citizen/year)"),
        ("Constitutional Compliance", "Regular, documented, inclusive, multilingual Gram Sabhas", "73rd Amendment actually implemented as designed"),
    ],
    "national_scale": (
        "If eGramSabha increases participation from 5% to 25-30%: "
        "125-175 million additional citizens actively participating in local governance. "
        "Millions of issues formally recorded and tracked. "
        "Digital MOM records for every meeting in every panchayat — "
        "the largest governance transparency dataset in the world."
    ),
}

# ============================================================
# SLIDE 13: Additional Details / Future Development
# (Source: IMPACT.md:369-400, ARCHITECTURE.md:963-1035)
# ============================================================
SLIDE13 = {
    "title": "Additional Details / Future Development",
    "phases": [
        ("Immediate (Config changes)", [
            "Activate AWS Transcribe — code complete, needs subscription activation. Switch STT_PROVIDER=aws_transcribe",
            "DLT registration for SNS SMS — API calls succeed, delivery needs India TRAI DLT entity + template registration",
            "Enable Rekognition — server-side face verification. Set FACE_VERIFICATION_PROVIDER=rekognition. 90% threshold.",
        ]),
        ("Short-term", [
            "DocumentDB migration — set USE_DOCUMENTDB=true. Automated backups, multi-AZ failover, read replicas",
            "Native mobile app (React Native) — extend reach to feature phones and offline-first scenarios",
            "e-Gram Swaraj + Panchayat Nirnay integration — feed citizen issues to government planning portal",
        ]),
        ("Medium-term", [
            "Multi-panchayat escalation — issues affecting multiple villages escalated to Block/District level",
            "Block/District analytics dashboards — aggregate issue data reveals systemic problems across panchayats",
            "Video Gram Sabha with AI transcription — virtual meeting participation via JioMeet with real-time MOM",
        ]),
        ("Long-term (National)", [
            "National rollout to 250,000 panchayats, 250M+ citizens — ECS Fargate multi-region, global DocumentDB",
            "Aadhaar integration — biometric identity layer alongside face-api.js for maximum coverage",
            "Open API for third-party integrations — CSOs, researchers, government dashboards access Gram Sabha data",
            "Scheme delivery tracking — verify whether announced welfare schemes reach intended beneficiaries",
        ]),
    ],
    "vision": '"Sashakt Panchayat, Samriddh Bharat" — Strong Panchayat, Prosperous India',
    "alignment": (
        "Digital India alignment: UPI (350M+ users proves simple inclusive interfaces drive mass adoption), "
        "Aadhaar (identity infrastructure), DBT (funds reach beneficiaries — eGramSabha ensures RIGHT beneficiaries selected), "
        "CoWIN (scaled to hundreds of millions in months). "
        "Well-designed Digital Public Goods, once adopted, scale to hundreds of millions in years, not decades."
    ),
    "dpg": (
        "eGramSabha is designed as a Digital Public Good (DPG) — Apache 2.0 licensed, open source. "
        "Any state government, CSO, or development organisation can deploy, customise, and extend it. "
        "The 29 subjects under Panchayat jurisdiction represent Rs 25+ lakh crore in welfare spending. "
        "When citizens actively participate, leakage reduces and impact increases."
    ),
}

# ============================================================
# SLIDE 14: Prototype Assets
# ============================================================
SLIDE14 = {
    "title": "Prototype Assets",
    "assets": [
        ("GitHub Public Repository", "https://github.com/anshuljain90/ai4bharat-empowerpanchayat"),
        ("Live Deployment", "https://empowerpanchayat.org/"),
        ("Demo Video", "(Max 3 minutes — link to be provided)"),
        ("License", "Apache 2.0 — Digital Public Good (DPG)"),
    ],
}
