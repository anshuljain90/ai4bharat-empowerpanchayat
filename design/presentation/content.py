"""
All slide content for eGramSabha Hackathon Presentation (33 slides).
Sourced from corrected design/docs/ files.

Slide mapping:
  1:     Template landing (fields filled in, background intact)
  2:     Our eGramSabha title slide (extra — logo, tagline)
  3-14:  Template slides 2-13 (with background images)
  15-31: Extra content slides (white bg + green header)
  32:    Our Thank You / closing slide (extra)
  33:    Template slide 14 (ending background, untouched)
"""

# ============================================================
# SLIDE 1: Title Slide (template slide 1)
# ============================================================
SLIDE1 = {
    "project_name": "eGramSabha",
    "tagline": "Sashakt Panchayat, Samriddh Bharat",
    "subtitle": "AI-Powered Digital Gram Sabha Platform",
    "team_name": "eGramSabha",
    "team_leader": "Anshul Jain",
    "problem_statement": "PS03 - AI for Rural Innovation & Sustainable Systems",
}

# ============================================================
# SLIDE_TITLE: Our branded eGramSabha title slide (extra, inserted as slide 2)
# ============================================================
SLIDE_TITLE = {
    "project_name": "eGramSabha",
    "tagline": '"Sashakt Panchayat, Samriddh Bharat"',
    "subtitle": "AI-Powered Digital Gram Sabha Platform",
    "event": "AWS AI for Bharat Hackathon",
}

# ============================================================
# SLIDE 2: Problem Statement (template slide 2)
# ============================================================
SLIDE2 = {
    "title": "Problem Statement",
    "headline": (
        "In 1992, India passed the 73rd Constitutional Amendment \u2014 a radical act of faith in its own people. "
        "It created 250,000+ Gram Panchayats and mandated Gram Sabhas as the foundation of grassroots democracy. "
        "Three decades later, that promise remains largely unfulfilled."
    ),
    "stats": [
        ("5-10%", "Average Gram Sabha\nattendance"),
        ("<3%", "Women participation\nin many states"),
        ("60%+", "Rural Indians with\nlimited literacy"),
        ("30%", "Eligible citizens excluded\nfrom welfare schemes"),
        ("ZERO", "Digital trail of\nGram Sabha decisions"),
    ],
    "barriers": [
        ("Paper agendas on notice boards", "Low awareness \u2014 excludes remote hamlets, women at home, daily wage workers"),
        ("Paper sign-in sheets", "Easy to forge \u2014 routinely inflated to show higher attendance numbers"),
        ("Hand-written minutes by clerk", "Subjective, often incomplete, sometimes pre-written before the meeting"),
        ("Single language proceedings", "Excludes tribal & minority communities \u2014 Gondi, Santhali, Bhili speakers silenced"),
        ("No issue tracking system", "Promises forgotten between meetings \u2014 citizens stop attending"),
        ("Physical presence required", "Excludes women (social norms), elderly (mobility), differently-abled citizens"),
    ],
}

# ============================================================
# SLIDE 3: Solution Overview (template slide 3)
# ============================================================
SLIDE3 = {
    "title": "Solution Overview",
    "overview": (
        "eGramSabha is an AI-driven, voice-first, face-authenticated platform that digitizes the entire "
        "Gram Sabha lifecycle \u2014 from citizen registration to issue resolution tracking. "
        "Three role-based portals (Admin, Official, Citizen) serve every stakeholder."
    ),
    "portals": [
        ("Admin Portal", "Panchayat CRUD, CSV import, official management (6 roles), letterhead, platform config"),
        ("Official Portal", "Citizen registration, issue management, meeting scheduling, AI agenda, attendance, PDF exports"),
        ("Citizen Portal", "Face login, voice/text issue reporting, RSVP, issue tracking, support tickets"),
    ],
    "lifecycle": "REGISTER (Face) \u2192 REPORT (Voice) \u2192 MEET (Agenda) \u2192 RECORD (Attendance) \u2192 TRACK (Status)",
}

# ============================================================
# SLIDE 4: 5-Step Gram Sabha Lifecycle (template slide 4)
# ============================================================
SLIDE4 = {
    "title": "5-Step Gram Sabha Lifecycle",
    "steps": [
        ("1. REGISTER", "Face", "Admin adds citizens via CSV or manual entry. Officials onboard via face biometric. 128-dim face descriptor stored \u2014 no passwords, no OTPs."),
        ("2. REPORT", "Voice", "Citizens record voice complaints in their native language, anytime. AI transcribes, corrects grammar, translates, analyses sentiment, assigns priority."),
        ("3. MEET", "Agenda", "Officials schedule Gram Sabha. AI summarises issues into backlog. Officials select items for agenda. Translated to multiple languages. TTS read-aloud."),
        ("4. RECORD", "Attendance", "Officials take facial biometric attendance to meet quorum threshold. Meeting auto-transitions to IN_PROGRESS when quorum met."),
        ("5. TRACK", "Status", "Every issue tracked: REPORTED \u2192 PICKED_IN_AGENDA \u2192 DISCUSSED_IN_GRAM_SABHA \u2192 RESOLVED. Officials add resolution remarks. Zero promises lost."),
    ],
}

# ============================================================
# SLIDE 5: Citizen Portal (template slide 5)
# ============================================================
SLIDE5 = {
    "title": "Citizen Portal",
    "features": [
        ("Face Login", "Last 4 digits of voter ID + face scan. Euclidean distance < 0.4. No passwords needed."),
        ("Voice Issue Reporting", "Record complaint in native language. 6 categories, 20+ subcategories. AI transcribes and translates."),
        ("Issue Tracking", "Real-time status: REPORTED \u2192 PICKED_IN_AGENDA \u2192 DISCUSSED \u2192 RESOLVED."),
        ("Meeting RSVP", "View upcoming Gram Sabhas. RSVP to confirm attendance."),
        ("Multilingual UI", "English and Hindi interface. AI content in 10+ languages."),
        ("Support Tickets", "Raise help desk tickets. Anonymous submission for vulnerable reporters."),
    ],
    "screenshot_label": "Citizen Portal \u2014 Dashboard & Issue Reporting",
}

# ============================================================
# SLIDE 6: Official Portal (template slide 6)
# ============================================================
SLIDE6 = {
    "title": "Official Portal",
    "features": [
        ("Citizen Registration", "Register citizens with voter ID + face capture. Liveness: 2 blinks + 5 head movements."),
        ("Issue Management", "Filter by status, category, priority, ward. View transcriptions, sentiment, summaries."),
        ("Meeting Scheduling", "Set date, time, location, expected duration. SMS notifications to citizens."),
        ("AI Agenda Generation", "View AI-summarised issue backlog. Select items for agenda. Translate and TTS read-aloud."),
        ("Biometric Attendance", "Mark citizen attendance via face verification or manual check-in. Quorum auto-check."),
        ("PDF Exports", "Attendance reports, agenda documents with custom panchayat letterhead."),
    ],
    "screenshot_label": "Official Portal \u2014 Meeting Management & Agenda",
}

# ============================================================
# SLIDE 7: Admin Portal (template slide 7)
# ============================================================
SLIDE7 = {
    "title": "Admin Portal",
    "features": [
        ("Panchayat Management", "Create/edit panchayats with LGD code. Ward management. Letterhead upload and preview."),
        ("Official Management", "Register officials with 6 roles: Secretary, President, Ward Member, Committee Secretary, Guest, Admin."),
        ("Bulk CSV Import", "Import citizens, officials, and panchayats via CSV upload. Batch operations."),
        ("Platform Configuration", "Sabha quorum criteria, feature toggles, system-wide settings."),
        ("Support Ticket Management", "View and respond to citizen/official help desk tickets."),
    ],
    "screenshot_label": "Admin Portal \u2014 Panchayat & Official Management",
}

# ============================================================
# SLIDE 8: Continuous Governance Loop (template slide 8)
# ============================================================
SLIDE8 = {
    "title": "Continuous Governance Loop",
    "caption": "Citizens can report issues at any time \u2014 the cycle is continuous, not tied to meeting dates",
    "descriptions": [
        ("Report", "Citizens report issues via voice in any language, any time \u2014 not tied to meeting dates."),
        ("Summarise", "AI categorises, deduplicates, and summarises issues hourly via cron jobs."),
        ("Agenda", "Officials review AI summaries and select items for the next Gram Sabha agenda."),
        ("Discuss", "Face-verified attendance, quorum check, structured discussion of agenda items."),
        ("Resolve", "Resolution remarks recorded. Undiscussed items return to backlog automatically."),
    ],
}

# ============================================================
# SLIDE 9: Why AI? (template slide 9)
# ============================================================
SLIDE9 = {
    "title": "Why AI? \u2014 Before vs After",
    "comparisons": [
        ("Illiterate citizen\n(60%+ of rural India)", "Cannot report issues \u2014 requires writing in complaint register during office hours", "Speaks complaint in any language. AI transcribes, corrects, translates, assigns priority."),
        ("Panchayat secretary", "Hand-writes minutes for hours, often days later. Subjective, sometimes pre-written.", "AI generates structured MOM (Planned): Discussion Points, Decisions, Action Items. 3 languages."),
        ("Women at home\n(~3% participation)", "Must attend male-dominated meeting. Social norms discourage speaking.", "Reports issues via voice from home. Same formal weight. Face auth \u2014 no password."),
        ("Official creating agenda", "Ad-hoc list influenced by powerful voices. No systematic inclusion.", "AI structures backlog from ALL citizen issues. Officials select. Equal weight."),
        ("Tribal/minority citizen", "Excluded by state-language proceedings. Cannot understand.", "Speaks native language. AI translates. Agenda in their language. TTS reads aloud."),
        ("Block/District admin", "Physical inspection needed. Paper records inaccessible.", "Digital records, attendance data, issue analytics. Audit remotely."),
    ],
}

# ============================================================
# SLIDE 10: Voice Issue Reporting Pipeline (template slide 10)
# ============================================================
SLIDE10 = {
    "title": "Voice Issue Reporting Pipeline",
    "steps": [
        ("Citizen records voice", "Native language, 6 categories, 20+ subcategories"),
        ("Audio uploaded", "Stored in S3 or GridFS as issue attachment"),
        ("STT transcription", "Provider-agnostic: Jio / Whisper / AWS Transcribe"),
        ("Grammar correction", "Bedrock Nova Lite corrects and enhances"),
        ("3-language output", "enhanced_original + enhanced_english + enhanced_hindi"),
        ("Sentiment analysis", "Bedrock: sentiment label, scores, key phrases (top 10)"),
        ("Auto-priority", "Health/safety + strong negative \u2192 URGENT auto-upgrade"),
        ("Results stored", "MongoDB: issue.sentiment, issue.keyPhrases, issue.priority"),
    ],
}

# ============================================================
# SLIDE 11: AI Issue Summarisation & Agenda (template slide 11)
# ============================================================
SLIDE11 = {
    "title": "AI Issue Summarisation & Agenda Generation",
    "summarization_steps": [
        "Cron job runs hourly (summaryCronJobs.js) \u2014 checks for unsummarised issues in MongoDB",
        "Calls video-mom-backend /summarize-issues endpoint with batch of new issues",
        "Bedrock Nova Lite categorises by type, deduplicates similar issues, generates concise summaries",
        "Sentiment + priority carried forward; URGENT issues flagged for immediate attention",
        "IssueSummary records created in MongoDB \u2014 linked to original issues for traceability",
    ],
    "agenda_steps": [
        "Officials view IssueSummary backlog \u2014 filterable by category, ward, priority, date",
        "Officials select items for agenda; AI structures numbered items with citizen context",
        "AWS Translate converts agenda to Hindi + regional languages (auto-detect source)",
        "Amazon Polly synthesises TTS audio; S3 cache: tts-cache/{lang}/{sha256}.mp3",
        "Citizens can Read Aloud agenda in their language before the meeting",
        "Post-meeting: undiscussed items return to backlog automatically for next Sabha",
    ],
    "key_flow": "Source: summaryCronJobs.js \u2192 /api/summarize-issues \u2192 Bedrock \u2192 IssueSummary \u2192 Agenda \u2192 Translate \u2192 Polly TTS",
    "key_point": "AI summarises \u2014 Officials decide. Every citizen voice gets equal representation.",
}

# ============================================================
# SLIDE 12: Face Authentication (template slide 12)
# ============================================================
SLIDE12 = {
    "title": "Face Authentication Pipeline",
    "registration": [
        "Official/Admin registers citizen with voter ID",
        "Liveness: 2 blinks + 5 head movements (MediaPipe FaceMesh)",
        "face-api.js extracts 128-dim face descriptor client-side",
        "Face image \u2192 S3, thumbnail generated via Sharp",
        "Descriptor stored in MongoDB user record",
    ],
    "login": [
        "Enter last 4 digits of voter ID",
        "Camera capture (no liveness on login)",
        "New face descriptor computed via face-api.js",
        "Euclidean distance: threshold < 0.4",
        "Security token: random \u2192 SHA256 hash (anti-replay)",
        "On match: JWT issued (citizen 72h, refresh 7d)",
    ],
    "production": "Rekognition: IndexFaces per panchayat, SearchFacesByImage at 90% similarity. Non-blocking fallback to local.",
}

# ============================================================
# SLIDE 13: Prototype Assets (template slide 13 — links)
# ============================================================
SLIDE13_LINKS = {
    "title": "Prototype Assets:",
    "github_repo": "https://github.com/anshuljain90/ai4bharat-empowerpanchayat",
    "demo_video": "https://drive.google.com/drive/folders/1aLeLtSPIDUaoypi3TAu2tg4I-TpxVUNH",
    "live_prototype": "https://44.194.253.143/",
}

# ============================================================
# SLIDE 13 (moved to extra): Meeting Day Flow
# ============================================================
SLIDE13 = {
    "title": "Meeting Day Flow",
    "steps": [
        ("Officials Take Attendance", "Face-verified or manual check-in. Verification method recorded."),
        ("Quorum Check", "attendanceCount >= ceil(totalVoters \u00d7 sabhaCriteria / 100)"),
        ("Meeting Auto-Starts", "Status: SCHEDULED \u2192 IN_PROGRESS when quorum met."),
        ("Issues Discussed", "Agenda items discussed. Status: PICKED_IN_AGENDA \u2192 DISCUSSED."),
        ("Decisions Recorded", "Resolution remarks added. RESOLVED / TRANSFERRED / NO_ACTION_NEEDED."),
        ("Post-Meeting", "Undiscussed items return to backlog for next meeting."),
    ],
    "planned": "MOM Generation (Planned): meeting audio \u2192 STT \u2192 Bedrock structured MOM \u2192 3 languages",
}

# ============================================================
# SLIDE 14: TTS & Multilingual Support (extra slide)
# ============================================================
SLIDE14 = {
    "title": "TTS & Multilingual Support",
    "tts_flow": [
        "Agenda text ready (English / Hindi / Regional)",
        "Generate SHA256 hash of text content",
        "Check S3 cache: tts-cache/{language}/{hash}.mp3",
        "Cache hit \u2192 return cached audio instantly",
        "Cache miss \u2192 Polly synthesises (Aditi Hindi, Raveena English)",
        "Store in S3, return audio. Same text never re-synthesised.",
    ],
    "languages": [
        "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam",
        "Bengali", "Gujarati", "Marathi", "Punjabi", "English",
    ],
    "ui_i18n": "English and Hindi UI via React Context with static translation files",
    "ai_translation": "AI content (agendas, summaries, transcriptions) translated via AWS Translate across 10+ languages",
}

# ============================================================
# SLIDE 15: System Architecture - Diagram (extra slide)
# ============================================================
SLIDE15 = {
    "title": "System Architecture",
    "docker": "4 containers on bridge network: frontend, backend, video-mom-backend, mongodb",
    "services_active": "11 Active AWS Services",
    "services_ready": "4 Code-Ready AWS Services",
}

# ============================================================
# SLIDE 16: System Architecture - Details (extra slide)
# ============================================================
SLIDE16 = {
    "title": "Architecture Layers",
    "layers": [
        ("Browser (Client)", "React 19, MUI 7, face-api.js, MediaPipe FaceMesh, JioMeet SDK, jsPDF"),
        ("API Gateway", "eGramSabha-MOM-API, REST REGIONAL, 100 req/s, API key, 100K/day quota"),
        ("Nginx Reverse Proxy", "TLS 1.2/1.3, GZIP, 10 req/s per IP, security headers, 500MB upload"),
        ("Node.js / Express :5000", "JWT auth (4 secrets), CRUD, S3 upload, SNS, cron jobs, Winston logging"),
        ("Python / FastAPI :8000", "STT (3 providers), Bedrock LLM, Polly TTS, Translate, sentiment analysis"),
        ("MongoDB :27017", "14 collections, GridFS, DocumentDB-compatible, 3 Docker volumes"),
    ],
}

# ============================================================
# SLIDE 17: Security Architecture (extra slide)
# ============================================================
SLIDE17 = {
    "title": "Security Architecture \u2014 6 Layers",
    "layers": [
        ("1. API Gateway", "API key (x-api-key) + 100 req/s rate limit + 200 burst + 100K/day quota"),
        ("2. Nginx", "TLS 1.2/1.3 + 10 req/s per IP + X-Frame-Options + HSTS + XSS-Protection"),
        ("3. Express Middleware", "Helmet + CORS + xss-clean + hpp + content security"),
        ("4. JWT Authentication", "3 role-specific secrets: Admin 12h, Official 24h, Citizen 72h, Refresh 7d"),
        ("5. RBAC Authorization", "6 roles with per-resource permissions, ward-scoped data access"),
        ("6. Secrets Manager", "Zero hardcoded credentials. egramsabha/prod secret with 4 JWT keys."),
    ],
    "roles": ["ADMIN", "SECRETARY", "PRESIDENT", "WARD_MEMBER", "COMMITTEE_SECRETARY", "GUEST", "CITIZEN"],
}

# ============================================================
# SLIDE 18: Traffic Flow (extra slide)
# ============================================================
SLIDE18 = {
    "title": "Traffic Flow",
    "flows": [
        ("CRUD Flow", "Browser \u2192 API Gateway \u2192 Nginx :443 \u2192 /api/* \u2192 Node.js :5000", "Auth, issue CRUD, file uploads, citizen management"),
        ("AI Flow", "Browser \u2192 API Gateway \u2192 Nginx :443 \u2192 /mom-api/* \u2192 FastAPI :8000", "TTS synthesis, agenda generation, sentiment analysis"),
        ("Cron Flow", "Node.js :5000 \u2192 Docker internal \u2192 FastAPI :8000", "Hourly summarisation, transcription retry, STT + grammar correction"),
    ],
    "volumes": [
        ("mongodb_data", "Persistent database storage"),
        ("backend_uploads", "Face photos, attachments, letterheads"),
        ("video_mom_temp_storage", "Temporary audio for AI processing"),
    ],
}

# ============================================================
# SLIDE 19: AWS Services (extra slide)
# ============================================================
SLIDE19 = {
    "title": "How AWS \u2014 15 Services",
    "active": [
        ("Amazon Bedrock", "Nova Lite, Converse API", "Grammar correction, summarisation, sentiment, translation fallback"),
        ("Amazon S3", "2 buckets, Intelligent-Tiering", "Face photos, TTS cache, letterheads, attachments"),
        ("AWS Translate", "Auto-detect source", "AI content across 10+ Indian languages"),
        ("Amazon Polly", "Aditi + Raveena", "TTS read-aloud with SHA256 S3 caching"),
        ("API Gateway", "REST, REGIONAL", "Single entry point, 100 req/s, API key auth"),
        ("CloudWatch", "2 log groups", "Winston + watchtower, JSON logs, 30-day retention"),
        ("Secrets Manager", "egramsabha/prod", "4 JWT secrets, graceful fallback to env vars"),
        ("EC2", "t3.medium", "Docker Compose host, burstable CPU for AI spikes"),
        ("EBS", "20 GB gp3", "3 persistent Docker volumes"),
        ("Elastic IP", "Static address", "DNS and API Gateway endpoint"),
        ("IAM", "Least-privilege", "Per-service access policies"),
    ],
    "code_ready": [
        ("Rekognition", "Server-side face verification, 90% threshold, per-panchayat collections"),
        ("DocumentDB", "Managed MongoDB, multi-AZ, automated backups"),
        ("AWS Transcribe", "24+ languages, async batch via S3"),
        ("SNS", "SMS notifications, requires TRAI DLT registration"),
    ],
}

# ============================================================
# SLIDE 20: Provider Abstraction (extra slide)
# ============================================================
SLIDE20 = {
    "title": "Provider Abstraction \u2014 Zero Lock-In",
    "switches": [
        ("STT_PROVIDER", "jio / whisper / aws_transcribe", "Speech-to-Text engine"),
        ("LLM_PROVIDER", "bedrock / huggingface", "Large Language Model backend"),
        ("TRANSLATION_PROVIDER", "aws_translate / llm", "Translation engine"),
        ("TTS_PROVIDER", "polly / disabled", "Text-to-Speech service"),
        ("STORAGE_BACKEND", "s3 / gridfs", "File storage backend"),
        ("FACE_VERIFICATION_PROVIDER", "local / rekognition", "Face matching engine"),
        ("USE_DOCUMENTDB", "true / false", "MongoDB \u2192 DocumentDB switch"),
        ("COMPREHEND_ENABLED", "true / false", "AWS Comprehend for NLP"),
    ],
    "benefit": "Swap any service without code changes. Move from hackathon to production by flipping environment variables.",
}

# ============================================================
# SLIDE 21: Technologies Utilized (extra slide)
# ============================================================
SLIDE21 = {
    "title": "Technologies Utilized",
    "sections": [
        ("Frontend", "#2E7D32", [
            ("React 19 + MUI 7", "SPA with Material UI components"),
            ("face-api.js 0.22.2", "Client-side face recognition (128-dim)"),
            ("MediaPipe FaceMesh", "Liveness detection (blink + head)"),
            ("JioMeet SDK", "Video meeting integration"),
            ("jsPDF + html2pdf.js", "PDF generation with Hindi fonts"),
        ]),
        ("Backend API", "#1565C0", [
            ("Node.js 20 + Express 4", "RESTful API, JWT auth, cron jobs"),
            ("Mongoose 8", "MongoDB ODM, 14 collection schemas"),
            ("Sharp", "Image processing, thumbnails"),
            ("Winston", "Structured logging \u2192 CloudWatch"),
        ]),
        ("AI Backend", "#FB8C00", [
            ("Python 3.11 + FastAPI", "Async AI pipelines"),
            ("Motor", "Async MongoDB driver"),
            ("boto3", "AWS SDK: Bedrock, S3, Polly, Translate"),
            ("ffmpeg-python", "Audio format conversion"),
        ]),
        ("Database", "#7B1FA2", [
            ("MongoDB 7", "14 collections, GridFS"),
            ("DocumentDB-compatible", "Schemas ready for migration"),
            ("3 Docker volumes", "Persistent data, uploads, temp"),
        ]),
    ],
}

# ============================================================
# SLIDE 22: Cost Breakdown (extra slide)
# ============================================================
SLIDE22 = {
    "title": "Cost \u2014 $15\u201320/month",
    "costs": [
        ("EC2 (t3.medium)", "$12\u201330", "Burstable CPU for AI spikes"),
        ("EBS (20 GB gp3)", "$1.60", "3 Docker volumes"),
        ("Elastic IP", "$0", "Free while attached"),
        ("S3 (2 buckets)", "$0.50", "Intelligent-Tiering"),
        ("Bedrock (Nova Lite)", "$2\u20135", "$0.06/1K input, $0.24/1K output"),
        ("Translate", "$0\u20131", "2M chars/mo free tier"),
        ("Polly", "$0\u20130.50", "5M chars/mo free, S3 cache"),
        ("CloudWatch", "$0\u20130.50", "5 GB/mo free tier"),
        ("Secrets Manager", "$0.40", "1 secret"),
        ("API Gateway", "$0", "1M calls/mo free tier"),
    ],
    "total": "$15\u201320/month",
}

# ============================================================
# SLIDE 23: Cost Optimizations (extra slide)
# ============================================================
SLIDE23 = {
    "title": "Cost Optimizations",
    "optimizations": [
        ("S3 Intelligent-Tiering", "Auto-moves cold face images and audio to cheaper storage tiers", "#2E7D32"),
        ("Polly S3 Caching", "SHA256 content hash as key \u2014 same text never re-synthesised", "#1565C0"),
        ("API Gateway Throttling", "100 req/s protects expensive Bedrock AI endpoints from abuse", "#FB8C00"),
        ("Bedrock Low Temp (0.3)", "Shorter, focused responses = fewer output tokens = lower cost", "#7B1FA2"),
        ("Chunked Processing", "1500-char chunks with 200 overlap \u2014 handles hour-long transcripts", "#D32F2F"),
        ("Transcribe Cleanup", "Auto-delete temp S3 objects and jobs after completion", "#00695C"),
    ],
}

# ============================================================
# SLIDE 24: Scale Projections (extra slide)
# ============================================================
SLIDE24 = {
    "title": "Scale Projections",
    "scale": [
        ("Hackathon", "1\u20135 panchayats", "Current config", "$15\u201320", "\u2014"),
        ("Pilot", "100 panchayats", "STORAGE_BACKEND=s3, USE_DOCUMENTDB=true", "$320", "~$3/citizen/yr"),
        ("State", "5K panchayats", "ECS Fargate, CloudFront, multi-AZ DocumentDB", "$3,250", "~$0.80/citizen/yr"),
        ("National", "250K panchayats", "Multi-region, service mesh, Bedrock provisioned", "$30\u201337K", "$0.60\u20130.72/citizen/yr"),
    ],
    "comparison": "Physical Gram Sabha: Rs 500+/meeting  vs  Digital eGramSabha: Rs 5/citizen/year",
    "reduction": "~100x Cost Reduction",
    "national_note": "At national scale: Rs 0.60 per citizen per year \u2014 less than printing one notice board poster.",
}

# ============================================================
# SLIDE 25: Impact Potential (extra slide)
# ============================================================
SLIDE25 = {
    "title": "Impact Potential \u2014 What Digital Gram Sabha Can Achieve",
    "metrics": [
        ("Voter registration", "~10% nationally", "81% (650 of 801 eligible)", "8x"),
        ("Issues submitted", "Handful (verbal, unrecorded)", "100+ issues in 3 days", "10x+"),
        ("Women participation", "Below 3% in many states", "Approximately 50%", "16x"),
        ("Decisions recorded", "Few, unrecorded or pre-written", "Multiple, digitally recorded", "Permanent"),
        ("Time to minutes", "Days later (if at all)", "AI-generated instantly", "Instant"),
    ],
    "approach": "Door-to-door registration with tablets, female enumerators for women\u2019s participation, elder-friendly assisted registration.",
}

# ============================================================
# SLIDE 26: Impact Outcomes (extra slide)
# ============================================================
SLIDE26 = {
    "title": "Measurable Outcomes \u2014 From a Single Digital Gram Sabha",
    "outcomes": [
        ("Garbage Management", "Structured tenant fee collection system approved by citizens"),
        ("Road Repairs", "Multiple road repairs prioritised and scheduled by citizen consensus"),
        ("Welfare Allocation", "Transgender welfare: Rs 2,100 minimum approved by the sabha"),
        ("Clean Energy", "24-acre solar power plant approved on unused community land"),
        ("Self-Governance", "Citizens independently levied local taxes and contributed resources"),
        ("Community Mobilisation", "Private company donated a tractor based on community initiative"),
        ("Fraud Prevention", "Digital attendance eliminated paper sign-in fraud"),
        ("Democratic Inclusion", "AI-generated agenda ensured every citizen\u2019s issue was formally considered"),
    ],
    "takeaway": "One digitally-enabled Gram Sabha produced more accountable decisions than years of paper-based proceedings.",
}

# ============================================================
# SLIDE 27: National Impact Projection (extra slide)
# ============================================================
SLIDE27 = {
    "title": "National Impact Projection",
    "impact": [
        ("Citizen Participation", "Voice-first, face auth, phone-based access", "5% \u2192 30%+ attendance"),
        ("Women\u2019s Empowerment", "Remote voice reporting, no public speaking needed", "3% \u2192 50% participation"),
        ("Welfare Delivery", "Citizen-verified beneficiary lists, digital tracking", "Reduce 30% exclusion error"),
        ("Transparency", "AI-generated records, searchable & auditable", "Every decision verifiable"),
        ("Accountability", "Issue lifecycle: REPORTED \u2192 DISCUSSED \u2192 RESOLVED", "Zero promises lost"),
        ("Cost Reduction", "Digital vs paper-based at scale", "~100x cost reduction"),
    ],
    "national_scale": (
        "If participation increases from 5% to 25\u201330%: 125\u2013175 million additional citizens "
        "actively participating in local governance. Digital records for every meeting in every panchayat \u2014 "
        "the largest governance transparency dataset in the world."
    ),
    "multipliers": [
        "Reduced rural-urban migration \u2014 local issues resolved locally",
        "Better welfare delivery \u2014 citizen-verified beneficiary lists",
        "Rs 25+ lakh crore welfare spending \u2014 active participation reduces leakage",
        "Youth engagement \u2014 transparent, mobile-first governance",
    ],
}

# ============================================================
# GALLERY SLIDES: One screenshot per slide with context
# ============================================================
GALLERY_SLIDES = [
    # ── Citizen Portal (4 screenshots) ──
    {
        "title": "Citizen Portal — Face Login",
        "screenshot": "citizen_login",
        "portal": "Citizen Portal",
        "portal_color": "#2E7D32",
        "page_name": "Citizen Login",
        "description": (
            "Citizens log in using just the last 4 digits of their voter ID and a face scan. "
            "No passwords, no OTPs. The camera captures a live face descriptor and matches it "
            "against the registered 128-dim biometric using Euclidean distance < 0.4."
        ),
        "highlights": [
            "Passwordless login \u2014 voter ID + face scan only",
            "Panchayat selection dropdown for multi-panchayat support",
            "face-api.js client-side matching, no server round-trip for speed",
        ],
    },
    {
        "title": "Citizen Portal — Dashboard",
        "screenshot": "citizen_dashboard",
        "portal": "Citizen Portal",
        "portal_color": "#2E7D32",
        "page_name": "Citizen Dashboard",
        "description": (
            "The citizen's home screen after face login. Shows a personalised welcome card, "
            "quick action buttons for raising issues and checking meeting schedules, "
            "and a summary of past meetings and reported issues."
        ),
        "highlights": [
            "Personalised welcome with citizen name and panchayat",
            "Quick actions: Report Issue, View Meetings, Track Issues",
            "Past meeting history and issue status at a glance",
        ],
    },
    {
        "title": "Citizen Portal — Report Issue",
        "screenshot": "citizen_create_issue",
        "portal": "Citizen Portal",
        "portal_color": "#2E7D32",
        "page_name": "Create Issue / Suggestion",
        "description": (
            "Citizens can report issues by recording a voice message in their native language "
            "or typing text. Choose from 6 categories and 20+ subcategories. "
            "AI transcribes, corrects grammar, translates, and assigns priority automatically."
        ),
        "highlights": [
            "Voice recording in any native language",
            "6 categories: Infrastructure, Health, Education, Water, Sanitation, Other",
            "AI auto-transcription, grammar correction, and translation",
        ],
    },
    {
        "title": "Citizen Portal — My Issues",
        "screenshot": "citizen_all_issues",
        "portal": "Citizen Portal",
        "portal_color": "#2E7D32",
        "page_name": "All Issues & Suggestions",
        "description": (
            "Citizens can track every issue they have reported with real-time status updates. "
            "Each issue shows its current lifecycle stage from REPORTED through to RESOLVED, "
            "along with priority level and category."
        ),
        "highlights": [
            "Real-time status: REPORTED \u2192 PICKED_IN_AGENDA \u2192 DISCUSSED \u2192 RESOLVED",
            "Priority indicators and sentiment badges",
            "Full transparency \u2014 no promises lost between meetings",
        ],
    },
    # ── Official Portal (16 screenshots) ──
    {
        "title": "Official Portal — Login",
        "screenshot": "official_login",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Official Login",
        "description": (
            "The Official Portal login page in English. Officials authenticate using their "
            "credentials with role-based JWT tokens. Supports 6 roles: Secretary, President, "
            "Ward Member, Committee Secretary, Guest, and Admin."
        ),
        "highlights": [
            "Role-based JWT authentication with per-role token expiry",
            "Secretary 24h, President 24h, Ward Member 24h token lifetime",
            "Automatic redirect to role-appropriate dashboard",
        ],
    },
    {
        "title": "Official Portal — Login (Hindi)",
        "screenshot": "official_login_hindi",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Official Login \u2014 Hindi",
        "description": (
            "The same Official Portal login page rendered in Hindi, demonstrating "
            "full i18n support. Language toggle is available on every page. "
            "All UI labels, placeholders, and validation messages are translated."
        ),
        "highlights": [
            "Complete Hindi translation via React Context + static files",
            "One-click language toggle persisted in local storage",
            "All form validation messages also translated",
        ],
    },
    {
        "title": "Official Portal — Dashboard",
        "screenshot": "official_dashboard",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Official Dashboard",
        "description": (
            "The official's command centre showing quick action cards for all key workflows: "
            "citizen registration, issue management, Gram Sabha scheduling, and attendance tracking. "
            "Provides at-a-glance statistics and pending action items."
        ),
        "highlights": [
            "Quick actions: Register Citizens, Manage Issues, Schedule Meetings",
            "At-a-glance statistics for pending and resolved items",
            "Role-based access: Secretary, President, Ward Member, etc.",
        ],
    },
    {
        "title": "Official Portal — Dashboard (Hindi)",
        "screenshot": "official_dashboard_hindi",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Dashboard \u2014 Hindi",
        "description": (
            "The entire Official Portal dashboard rendered in Hindi, demonstrating "
            "full i18n support. Every label, button, card title, and status indicator "
            "is translated using static translation files via React Context."
        ),
        "highlights": [
            "Complete UI translation: English \u2194 Hindi toggle",
            "AI content translated to 10+ Indian languages via AWS Translate",
            "TTS read-aloud for agenda items via Amazon Polly",
        ],
    },
    {
        "title": "Official Portal — Create Issue",
        "screenshot": "official_create_issue",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Create Issue / Suggestion",
        "description": (
            "Officials can also create issues on behalf of citizens who visit the panchayat office. "
            "The form captures category, subcategory, description, and optional voice recording. "
            "Issues are linked to the citizen's profile for tracking."
        ),
        "highlights": [
            "6 categories with 20+ subcategories for structured reporting",
            "Voice recording or text input with file attachments",
            "Auto-assigned priority based on category and sentiment",
        ],
    },
    {
        "title": "Official Portal — Create Issue (Hindi)",
        "screenshot": "official_create_issue_hindi",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Create Issue \u2014 Hindi",
        "description": (
            "The Create Issue form in Hindi, showing complete translation of all form fields, "
            "dropdown options, category labels, and action buttons. Officials comfortable "
            "in Hindi can operate the entire workflow in their preferred language."
        ),
        "highlights": [
            "All form labels and dropdowns translated to Hindi",
            "Category and subcategory options in Hindi",
            "Consistent UI layout across both languages",
        ],
    },
    {
        "title": "Official Portal — Issue Management",
        "screenshot": "official_issues_list",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Issues & Suggestions",
        "description": (
            "A filterable table of all citizen-reported issues with status, category, priority, "
            "and ward filters. Officials can view AI transcriptions, sentiment analysis results, "
            "and manage issue lifecycle from this screen."
        ),
        "highlights": [
            "Filter by status, category, priority, ward, and date range",
            "AI-generated transcription and sentiment visible per issue",
            "Bulk operations for agenda selection",
        ],
    },
    {
        "title": "Official Portal — AI Issue Summary",
        "screenshot": "official_issues_summary",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Issues / Suggestions Summary",
        "description": (
            "AI-generated summaries of citizen issues, grouped by category and deduplicated. "
            "Bedrock Nova Lite runs hourly via cron to summarise new issues into agenda-ready items. "
            "Officials select items from this backlog for the next Gram Sabha agenda."
        ),
        "highlights": [
            "Hourly AI summarisation via Bedrock Nova Lite cron job",
            "Category-wise grouping with deduplication of similar issues",
            "One-click selection of items for Gram Sabha agenda",
        ],
    },
    {
        "title": "Official Portal — Issue Details",
        "screenshot": "official_issue_details",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Issue Details Modal",
        "description": (
            "Detailed view of a single issue showing the original voice transcription, "
            "AI-enhanced versions in 3 languages, sentiment analysis results, audio playback, "
            "and the full issue lifecycle history."
        ),
        "highlights": [
            "Original + enhanced transcription in English and Hindi",
            "Embedded audio player for original voice recording",
            "Sentiment scores, key phrases, and priority justification",
        ],
    },
    {
        "title": "Official Portal — Gram Sabha Management",
        "screenshot": "official_gram_sabha_list",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Gram Sabha Meetings",
        "description": (
            "Lists all scheduled, in-progress, and completed Gram Sabhas. "
            "Officials can create new meetings, set quorum criteria, manage agendas, "
            "and view attendance reports from this central meeting management screen."
        ),
        "highlights": [
            "Meeting lifecycle: SCHEDULED \u2192 IN_PROGRESS \u2192 COMPLETED",
            "Quorum tracking with automatic status transitions",
            "PDF export for attendance reports and agenda documents",
        ],
    },
    {
        "title": "Official Portal — Gram Sabha Details",
        "screenshot": "official_gram_sabha_details",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Gram Sabha Details",
        "description": (
            "Detailed view of a specific Gram Sabha showing date, time, location, "
            "expected attendance, quorum status, assigned agenda items, and attendance records. "
            "Officials can manage the meeting lifecycle from this modal."
        ),
        "highlights": [
            "Meeting metadata: date, time, venue, expected duration",
            "Agenda items linked to citizen issues with AI summaries",
            "Attendance count vs quorum threshold indicator",
        ],
    },
    {
        "title": "Official Portal — Schedule Meeting",
        "screenshot": "official_create_meeting",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Create New Gram Sabha",
        "description": (
            "Modal for scheduling a new Gram Sabha meeting. Officials set the date, time, "
            "location, and expected duration. SMS notifications are sent to registered citizens "
            "once the meeting is created."
        ),
        "highlights": [
            "Date, time, and venue selection for new meetings",
            "SMS notification to citizens via Amazon SNS (TRAI DLT ready)",
            "Auto-populates panchayat details from admin configuration",
        ],
    },
    {
        "title": "Official Portal — Biometric Attendance",
        "screenshot": "official_mark_attendance",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Mark Attendance",
        "description": (
            "Face-verified attendance marking during Gram Sabha meetings. "
            "The camera captures the citizen's face and matches it against their registered "
            "128-dim face descriptor. Verification method (face/manual) is recorded for audit."
        ),
        "highlights": [
            "Face verification with Euclidean distance < 0.4 threshold",
            "Quorum auto-check: meeting starts when threshold met",
            "Eliminates paper sign-in fraud completely",
        ],
    },
    {
        "title": "Official Portal — Attendance Confirmed",
        "screenshot": "official_attendance_success",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Attendance Marked Successfully",
        "description": (
            "Success confirmation after marking attendance via face verification. "
            "Shows the matched citizen's name, verification method used, and updated "
            "attendance count vs quorum threshold."
        ),
        "highlights": [
            "Visual confirmation with citizen name and photo match",
            "Verification method recorded: face-verified or manual",
            "Live attendance count updates toward quorum threshold",
        ],
    },
    {
        "title": "Official Portal — Meeting Details",
        "screenshot": "official_meeting_details",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Meeting Details",
        "description": (
            "Comprehensive meeting details modal showing the full meeting record: "
            "attendance list, agenda items discussed, decisions recorded, and resolution remarks. "
            "Officials can mark agenda items as discussed and add resolution notes."
        ),
        "highlights": [
            "Full attendance list with verification method per citizen",
            "Agenda items with discussion status and resolution remarks",
            "Post-meeting: undiscussed items return to backlog automatically",
        ],
    },
    {
        "title": "Official Portal — Agenda Selection",
        "screenshot": "official_agenda_selection",
        "portal": "Official Portal",
        "portal_color": "#1565C0",
        "page_name": "Agenda Item Selection",
        "description": (
            "Officials select which AI-summarised issues to include in the Gram Sabha agenda. "
            "Selected items are structured into numbered agenda points with citizen context. "
            "The agenda can be translated and read aloud via TTS in multiple languages."
        ),
        "highlights": [
            "Select from AI-summarised issue backlog for agenda",
            "Mark agenda items as discussed during the meeting",
            "Translate agenda to Hindi + regional languages with TTS",
        ],
    },
    # ── Admin Portal (13 screenshots) ──
    {
        "title": "Admin Portal — Login",
        "screenshot": "admin_login",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Admin Login",
        "description": (
            "The Admin Portal login page. Admins have the highest privilege level "
            "with access to platform configuration, panchayat CRUD, official management, "
            "and system-wide settings. JWT token with 12-hour expiry."
        ),
        "highlights": [
            "Highest privilege role with full platform access",
            "12-hour JWT token with 7-day refresh token",
            "Access to all panchayats and system configuration",
        ],
    },
    {
        "title": "Admin Portal — Dashboard",
        "screenshot": "admin_dashboard",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Admin Dashboard",
        "description": (
            "The admin's central hub for platform management. Shows system-wide statistics, "
            "quick actions for panchayat creation, official management, and bulk CSV import. "
            "Admins manage the entire multi-panchayat hierarchy from here."
        ),
        "highlights": [
            "System-wide stats: total panchayats, officials, citizens",
            "Quick actions: Add Panchayat, Register Officials, Import CSV",
            "Support ticket management for citizen/official help requests",
        ],
    },
    {
        "title": "Admin Portal — Member Search",
        "screenshot": "admin_member_search",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Member Search",
        "description": (
            "Search for registered members across all panchayats by name, voter ID, or phone number. "
            "Results show member details, registration status, and face registration status. "
            "Admins can click through to view or edit any member's profile."
        ),
        "highlights": [
            "Cross-panchayat search by name, voter ID, or phone",
            "Registration and face biometric status indicators",
            "Quick navigation to member profile for edits",
        ],
    },
    {
        "title": "Admin Portal — Member Profile",
        "screenshot": "admin_member_profile",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Member Profile",
        "description": (
            "Detailed member profile showing personal information, panchayat assignment, "
            "ward, and face registration status. Admins can capture or update the member's "
            "face biometric with liveness detection (2 blinks + 5 head movements)."
        ),
        "highlights": [
            "Face registration with liveness detection via MediaPipe",
            "128-dim face descriptor stored for future authentication",
            "Edit member details: name, voter ID, phone, ward assignment",
        ],
    },
    {
        "title": "Admin Portal — All Members",
        "screenshot": "admin_member_list",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "All Members",
        "description": (
            "Complete list of all registered members across all panchayats. "
            "Sortable and filterable by panchayat, ward, and registration status. "
            "Shows face registration status and quick action buttons."
        ),
        "highlights": [
            "View all members with face registration status",
            "Filter by panchayat, ward, and registration status",
            "Pagination for large datasets with sort options",
        ],
    },
    {
        "title": "Admin Portal — CSV Import",
        "screenshot": "admin_import_csv",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "CSV Import",
        "description": (
            "Bulk import of citizens, officials, or panchayats via CSV upload. "
            "Shows required field specifications and validation rules. "
            "Batch processing with error reporting for failed rows."
        ),
        "highlights": [
            "Bulk import for citizens, officials, and panchayats",
            "Required field specifications and format validation",
            "Error reporting with row-level details for failed imports",
        ],
    },
    {
        "title": "Admin Portal — Panchayat Management",
        "screenshot": "admin_panchayat_list",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Panchayat Management",
        "description": (
            "Create, edit, and manage panchayats with LGD codes and ward structures. "
            "Each panchayat has its own letterhead, quorum criteria, and official assignments. "
            "Supports the full hierarchy from district to ward level."
        ),
        "highlights": [
            "CRUD operations with LGD code validation",
            "Ward management and letterhead upload",
            "Sabha quorum criteria configuration per panchayat",
        ],
    },
    {
        "title": "Admin Portal — Add Panchayat",
        "screenshot": "admin_add_panchayat",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Add New Panchayat",
        "description": (
            "Modal for creating a new panchayat in the system. Captures essential details "
            "including panchayat name, LGD code, district, block, state, and contact information. "
            "Ward structure is configured after initial creation."
        ),
        "highlights": [
            "LGD code integration for official government mapping",
            "District, block, and state hierarchy selection",
            "Contact details and location information capture",
        ],
    },
    {
        "title": "Admin Portal — Panchayat Form (Continued)",
        "screenshot": "admin_add_panchayat_form",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Add Panchayat \u2014 Extended Fields",
        "description": (
            "Continuation of the Add Panchayat form showing additional configuration fields "
            "including letterhead upload, quorum criteria percentage, ward count, "
            "and Sabha-specific settings."
        ),
        "highlights": [
            "Letterhead upload for branded PDF exports",
            "Quorum criteria percentage for Sabha validation",
            "Ward count and structure configuration",
        ],
    },
    {
        "title": "Admin Portal — Panchayat Form (Complete)",
        "screenshot": "admin_add_panchayat_complete",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Add Panchayat \u2014 Complete Form",
        "description": (
            "The complete Add Panchayat form ready for submission, showing all fields populated. "
            "Includes validation indicators for required fields and a preview of the "
            "panchayat configuration before creation."
        ),
        "highlights": [
            "Form validation with required field indicators",
            "Preview of full panchayat configuration",
            "Submit to create panchayat and initialize ward structure",
        ],
    },
    {
        "title": "Admin Portal — Edit Panchayat",
        "screenshot": "admin_edit_panchayat",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Edit Panchayat",
        "description": (
            "Edit dialog for updating an existing panchayat's details. "
            "All fields from creation are editable, including letterhead, quorum criteria, "
            "and contact information. Changes are applied immediately."
        ),
        "highlights": [
            "Edit all panchayat fields including LGD code and hierarchy",
            "Update letterhead and quorum criteria",
            "Immediate save with validation",
        ],
    },
    {
        "title": "Admin Portal — Official Management",
        "screenshot": "admin_officials_list",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Official Management",
        "description": (
            "List of all registered officials across panchayats with their roles, "
            "assigned panchayat, and status. Admins can register new officials, "
            "edit roles, and manage access from this screen."
        ),
        "highlights": [
            "6 official roles: Secretary, President, Ward Member, Committee Secretary, Guest, Admin",
            "Role assignment and panchayat linkage",
            "Edit or deactivate official accounts",
        ],
    },
    {
        "title": "Admin Portal — Edit Official",
        "screenshot": "admin_edit_official",
        "portal": "Admin Portal",
        "portal_color": "#FB8C00",
        "page_name": "Edit Official Form",
        "description": (
            "Form for editing an official's details including name, role, assigned panchayat, "
            "contact information, and access level. Role changes take effect immediately "
            "and update the official's JWT permissions."
        ),
        "highlights": [
            "Role reassignment with immediate JWT permission update",
            "Panchayat and ward assignment management",
            "Contact details and credential management",
        ],
    },
]

# ============================================================
# SLIDE 30: Future Roadmap (extra slide)
# ============================================================
SLIDE30 = {
    "title": "Future Roadmap",
    "phases": [
        ("Phase 1\nImmediate", "#2E7D32", [
            "Activate AWS Transcribe",
            "TRAI DLT for SNS SMS",
            "Enable Rekognition",
        ]),
        ("Phase 2\nShort-term", "#1565C0", [
            "DocumentDB migration",
            "MOM full integration",
            "eSign (Planned)",
            "Mobile app (React Native)",
            "e-Gram Swaraj integration",
        ]),
        ("Phase 3\nMedium-term", "#FB8C00", [
            "Multi-panchayat escalation",
            "Analytics dashboards",
            "Video Gram Sabha",
            "Citizen self-attendance",
        ]),
        ("Phase 4\nNational", "#7B1FA2", [
            "250K panchayats rollout",
            "Aadhaar integration",
            "Open API for CSOs",
            "Scheme delivery tracking",
        ]),
    ],
}

# ============================================================
# SLIDE 31: Thank You (template slide 14 - closing background)
# ============================================================
SLIDE31 = {
    "vision": '"Sashakt Panchayat, Samriddh Bharat"',
    "subtitle": "Strong Panchayat, Prosperous India",
    "license": "Open Source",
    "closing": "eGramSabha \u2014 AI-Powered Digital Gram Sabha Platform",
}
