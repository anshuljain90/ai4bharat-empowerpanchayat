# eGramSabha — Process Flow Diagrams (AI Pipelines)

## Pipeline 1: Voice Issue Reporting

```mermaid
flowchart TD
    A["Citizen Records Voice Complaint\n(native language, any time)"] --> B["Audio Uploaded\nas Issue Attachment"]
    B --> C["Stored in S3 / GridFS"]
    C --> D["Transcription Triggered\nImmediately on Upload"]
    D --> E["STT Provider Transcribes\n(Jio / Whisper / AWS Transcribe)"]
    E --> F{"Transcription\nSucceeded?"}
    F -->|No| G["Cron Job Retries\nFailed Transcriptions\n(retryTranscriptionInitiation)"]
    G --> E
    F -->|Yes| H["Raw Transcript → Bedrock Nova Lite\nGrammar Correction"]
    H --> I["Output:\nenhanced_original\n+ enhanced_english\n+ enhanced_hindi"]
    I --> J["Bedrock Sentiment Analysis"]
    J --> K["Returns:\nsentiment label + scores\nkey phrases (top 10)\nsuggested priority"]
    K --> L{"suggestedPriority\n=== URGENT?"}
    L -->|Yes| M["Auto-Upgrade\nIssue Priority → URGENT"]
    L -->|No| N["Keep Priority\nas NORMAL"]
    M --> O["Results Stored in MongoDB:\nissue.sentiment\nissue.keyPhrases\nissue.priority"]
    N --> O

    style A fill:#1565C0,color:#fff
    style D fill:#00838F,color:#fff
    style E fill:#FF6F00,color:#fff
    style G fill:#D32F2F,color:#fff
    style H fill:#2E7D32,color:#fff
    style J fill:#2E7D32,color:#fff
    style M fill:#D32F2F,color:#fff
    style O fill:#7B1FA2,color:#fff
```

### Detailed Steps

1. **Citizen records voice complaint** in their native language — can be from home, field, or anywhere with phone access
2. **Audio uploaded as issue attachment** along with category selection (6 categories: Infrastructure, Basic Amenities, Social Welfare Schemes, Earning Opportunities, Culture & Nature, Other; 20+ subcategories)
3. **Audio stored** in S3 (production) or GridFS (local dev) based on `STORAGE_BACKEND` env var
4. **Transcription triggered immediately** on audio upload — no waiting for a scheduled job
5. **STT provider transcribes** audio to text — provider selected via `STT_PROVIDER` env var:
   - `jio`: Jio STT API (real-time, Hindi-optimized)
   - `whisper`: HuggingFace Whisper (multilingual, open-source)
   - `aws_transcribe`: AWS Transcribe (24+ languages, batch processing via S3)
6. **If transcription fails**, a cron job (`cronJobs.js` → `retryTranscriptionInitiation`) detects failed transcriptions and retries them
7. **Raw transcript sent to Bedrock** (Nova Lite, Converse API) for grammar correction with rural development context awareness
8. **Output produced in 3 languages**: enhanced text in original language (`enhanced_original`), English translation (`enhanced_english`), and Hindi translation (`enhanced_hindi`)
9. **Sentiment analysis** via Bedrock: analyses corrected transcription for emotional tone and urgency
10. **Returns structured JSON**: sentiment label (POSITIVE/NEGATIVE/NEUTRAL/MIXED) with confidence scores, extracted key phrases (top 10), and suggested priority
11. **Auto-priority**: If health/safety keywords detected (sewage, sick, fire, flood, collapsed, emergency) and strong negative sentiment → `suggestedPriority === 'URGENT'` → auto-upgrades issue priority to URGENT

**Source references**: `cronJobs.js`, `llm_service.py`, `comprehend_service.py`

---

## Pipeline 2: AI Issue Summarization & Agenda Preparation

```mermaid
flowchart TD
    A["Cron Job Runs Hourly\n(summaryCronJobs.js →\ninitiateSummaryGeneration)"] --> B["Detect Unsummarized Issues\n(issues not in any IssueSummary)"]
    B --> C{"New Issues\nFound?"}
    C -->|No| D["No Action\n(next run in 1 hour)"]
    C -->|Yes| E["Send Issues to\nvideo-mom-backend\nfor AI Processing"]
    E --> F["Bedrock Categorizes,\nSummarizes & Deduplicates\nRelated Issues"]
    F --> G["Clubs Related Issues\ninto Grouped Summaries"]
    G --> H["Creates IssueSummary\nRecords in MongoDB"]
    H --> I["IssueSummary Backlog\nAvailable to Officials"]

    I --> J["Official Opens\nAgenda Management"]
    J --> K["Views IssueSummary Backlog\n(categorized, deduplicated)"]
    K --> L["Official Manually Selects\nItems for Meeting Agenda"]
    L --> M["Agenda Finalized\nfor Gram Sabha"]

    M --> N["After Meeting:\nupdateIssueSummaryForSelectedAgenda()"]
    N --> O["Discussed Items\nMarked as Discussed"]
    N --> P["Undiscussed Items\nReturned to Backlog"]

    style A fill:#1565C0,color:#fff
    style E fill:#FF6F00,color:#fff
    style F fill:#2E7D32,color:#fff
    style H fill:#7B1FA2,color:#fff
    style L fill:#00838F,color:#fff
    style O fill:#2E7D32,color:#fff
    style P fill:#D32F2F,color:#fff
```

### Detailed Steps

1. **Cron job runs hourly** (`0 * * * *`) via `summaryCronJobs.js` → `initiateSummaryGeneration`
2. **Detects unsummarized issues** — identifies issues that do not yet appear in any IssueSummary record
3. **Sends issues to video-mom-backend** for AI processing via Bedrock
4. **AI categorizes and summarizes** each issue, deduplicates similar complaints, and clubs related issues together into grouped summaries
5. **Creates IssueSummary records** in MongoDB — each record represents a categorized, deduplicated group of related citizen issues
6. **Officials view IssueSummary backlog** when preparing for an upcoming Gram Sabha meeting
7. **Officials manually select items** from the backlog to include in the meeting agenda
8. **After the meeting**: `updateIssueSummaryForSelectedAgenda()` processes outcomes — items that were discussed are marked accordingly, and undiscussed items are returned to the IssueSummary backlog for future meetings

**Source references**: `summaryCronJobs.js`, `gramSabhaRoutes.js`

---

## Pipeline 3: Face Authentication

### Registration Flow (by Official / Admin)

```mermaid
flowchart TD
    A["Official/Admin Registers Citizen"] --> B["Select Panchayat\n(LGD code / cascading dropdown / URL route)"]
    B --> C["Enter Voter ID\n(full 10-digit or state-specific format)"]
    C --> D{"Already\nRegistered?"}
    D -->|Yes| E["Already Registered\n(update details if needed)"]
    D -->|No| F["Face Capture Screen"]
    F --> G["Liveness Detection:\n• Blink Detection (2 blinks required)\n• Head Movement (5 movements required)\nvia MediaPipe FaceMesh"]
    G --> H["face-api.js Extracts\n128-dimension Face Descriptor"]
    H --> I["Face Image → S3\nfaces/{panchayatId}/{uuid}"]
    I --> J["Thumbnail Generated\nvia Sharp library"]
    J --> K["Descriptor + S3 References\nStored in MongoDB User Record"]
    K --> L["isRegistered = true\nJWT Issued (72h expiry)"]
    L --> M["Redirect to\nCitizen Dashboard"]

    style A fill:#1565C0,color:#fff
    style G fill:#FF6F00,color:#fff
    style H fill:#2E7D32,color:#fff
    style I fill:#00838F,color:#fff
    style L fill:#7B1FA2,color:#fff
```

### Login Flow

```mermaid
flowchart TD
    A["Citizen Opens Login"] --> B["Enter Last 4 Digits\nof Voter ID"]
    B --> C["System Fetches Matching\nRegistered Users with Thumbnails"]
    C --> D["Select Identity\n(if multiple matches)"]
    D --> E["Camera Capture\n(no liveness required on login)"]
    E --> F["face-api.js Computes\nNew 128-dim Descriptor"]
    F --> G["Euclidean Distance\nComparison"]
    G --> H{"Distance\n< 0.4?"}
    H -->|Yes| I["Security Token:\nRandom → SHA256 Hash\n(prevents replay)"]
    H -->|No| J["Verification Failed\nTry Again"]
    I --> K["JWT Issued:\nCitizen Token (72h)\nRefresh Token (7d)"]
    K --> L["Redirect to\nCitizen Dashboard"]

    style A fill:#1565C0,color:#fff
    style F fill:#2E7D32,color:#fff
    style G fill:#FF6F00,color:#fff
    style J fill:#D32F2F,color:#fff
    style K fill:#7B1FA2,color:#fff
```

### Production Enhancement: AWS Rekognition

```mermaid
flowchart LR
    A["Set ENV:\nFACE_VERIFICATION_PROVIDER=rekognition"] --> B["Registration:\nIndexFaces to\negramsabha-{panchayatId}\ncollection"]
    B --> C["Login:\nSearchFacesByImage\n90% similarity threshold"]
    C --> D["Non-blocking:\nIf Rekognition unavailable,\nlocal check still works"]

    style A fill:#FFA000,color:#fff
    style B fill:#2E7D32,color:#fff
    style C fill:#2E7D32,color:#fff
```

### Detailed Steps

**Registration (by Official / Admin):**
Citizens cannot self-register. Admin adds citizen data from CSV (Election Commission data). Official or Admin then onboards the citizen by capturing face biometric:
1. Official/Admin selects panchayat via cascading dropdowns (State -> District -> Block -> Panchayat), LGD code lookup, or direct URL route (e.g., `/Haryana/Palwal/Prithla/Tatarpur`)
2. Enters voter ID — system checks for existing registration (unique constraint: voter ID + panchayat)
3. Face capture screen with real-time liveness verification via MediaPipe FaceMesh:
   - Blink detection: eyes must close & open (2 blinks required, configurable)
   - Head movement: head must move left-right and up-down (5 movements required, configurable)
   - Real-time UI indicators show checkmarks for each verified action
4. face-api.js extracts 128-dimensional face embedding (descriptor)
5. Face image stored in S3 at `faces/{panchayatId}/{uuid}`, thumbnail generated via Sharp
6. Descriptor + S3 references stored in MongoDB user record
7. `user.isRegistered = true`, JWT issued (72-hour expiry)

**Login:**
1. Enter last 4 digits of voter ID (privacy-preserving lookup)
2. System fetches matching registered users with stored thumbnails for visual confirmation
3. Camera capture — single face detection (no liveness check on login for speed)
4. New descriptor computed, Euclidean distance calculated against stored descriptor
5. Threshold: < 0.4 distance units (0 = identical, higher = more different)
6. Security token: random token generated client-side, SHA256 hashed server-side (prevents replay attacks)
7. On match: JWT issued with payload `{id, name, voterIdNumber, panchayatId, wardId, userType: 'CITIZEN'}`

**Source references**: `citizenAuthRoutes.js`, `FaceRegistration.js`

---

## Pipeline 4: Meeting Day Flow

```mermaid
flowchart TD
    A["Meeting Day\nGram Sabha Scheduled"] --> B["Attendance Marking"]
    B --> D["Official Takes\nFacial Biometric Attendance\nof Citizens"]
    D --> F["Attendance Recorded"]

    F --> G["Quorum Check:\nattendanceCount >=\nceil(totalVoters * sabhaCriteria / 100)"]
    G --> H{"Quorum\nMet?"}
    H -->|No| I["Continue Marking\nAttendance"]
    I --> B
    H -->|Yes| J["Sabha Starts\nMeeting → IN_PROGRESS"]

    J --> K["Discussion on\nAgenda Items"]
    K --> L["Update Issue Statuses:\nPICKED_IN_AGENDA →\nDISCUSSED_IN_GRAM_SABHA"]
    L --> M["Further Resolution:\nRESOLVED / TRANSFERRED /\nNO_ACTION_NEEDED"]
    M --> N["Officials Add\nResolution Remarks"]

    J --> O["When Meeting Ends:\nOfficial selects which items\nwere discussed"]
    O --> P["Discussed Items\nMarked Complete"]
    O --> Q["Undiscussed Items\nReturned to\nIssueSummary Backlog"]

    style A fill:#1565C0,color:#fff
    style D fill:#FF6F00,color:#fff
    style G fill:#00838F,color:#fff
    style J fill:#2E7D32,color:#fff
    style L fill:#7B1FA2,color:#fff
    style Q fill:#D32F2F,color:#fff
```

### Detailed Steps

1. **Meeting day begins** — the Gram Sabha is scheduled, officials and citizens arrive
2. **Officials take facial biometric attendance** of citizens based on their availability, ensuring accountability of their presence
3. **Quorum check**: system continuously evaluates `attendanceCount >= ceil(totalVoters * sabhaCriteria / 100)` where `sabhaCriteria` is the configured percentage threshold for the panchayat
4. **When quorum is met**, the meeting auto-transitions to `IN_PROGRESS` status
5. **During and after the meeting**, officials update issue statuses through the lifecycle:
   - `PICKED_IN_AGENDA` -> `DISCUSSED_IN_GRAM_SABHA` -> `RESOLVED` / `TRANSFERRED` / `NO_ACTION_NEEDED`
6. **Officials add resolution remarks** documenting decisions and outcomes for each discussed issue
7. **MOM generation** from meeting recording is planned via the video-mom-backend module (see [Planned / Future](#planned--future))
8. **When the meeting ends**, official selects which items were actually discussed in the Gram Sabha. `updateIssueSummaryForSelectedAgenda()` processes all agenda items:
   - Items that were discussed are marked as complete
   - Items left undiscussed are moved back to the IssueSummary backlog to be picked in agenda again for future meetings

**Source references**: `gramSabhaRoutes.js`

---

## Pipeline 5: Text-to-Speech (Agenda Read Aloud)

```mermaid
flowchart TD
    A["Agenda Text Ready\n(English / Hindi / Regional)"] --> B["Amazon Polly TTS Request"]
    B --> C["Generate SHA256 Hash\nof Text Content"]
    C --> D{"S3 Cache Check:\ntts-cache/{language}/{hash}.mp3"}
    D -->|Cache Hit| E["Return Existing\nCached Audio"]
    D -->|Cache Miss| F["Amazon Polly Synthesizes Speech\n• Aditi (Hindi)\n• Raveena (English)"]
    F --> G["Store Audio in S3:\ntts-cache/{language}/{hash}.mp3"]
    G --> E
    E --> H["Audio Returned\nto Client"]
    H --> I["Read Aloud Button\nin Citizen / Official UI"]

    style A fill:#1565C0,color:#fff
    style B fill:#FF6F00,color:#fff
    style D fill:#00838F,color:#fff
    style F fill:#2E7D32,color:#fff
    style G fill:#7B1FA2,color:#fff
    style I fill:#1565C0,color:#fff
```

### Detailed Steps

1. **Agenda text is available** in English, Hindi, or regional language after agenda preparation
2. **TTS request initiated** — system sends the text content to the TTS service
3. **SHA256 content hash computed** from the text content to serve as a cache key
4. **S3 cache lookup** at path `tts-cache/{language}/{hash}.mp3`:
   - **Cache hit**: existing audio file is returned immediately, no Polly API call needed
   - **Cache miss**: Amazon Polly synthesizes speech, audio is stored in S3, then returned
5. **Voice selection**:
   - Aditi voice for Hindi content
   - Raveena voice for English content
6. **Audio delivered to client** and played via the Read Aloud button in the citizen or official UI

**Source reference**: `tts_service.py`

---

## Planned / Future

### MOM Generation

A separate `video-mom-backend` module exists for generating Minutes of Meeting from meeting recordings. The pipeline: meeting audio/video is uploaded → transcribed via STT → sent to Bedrock which generates a structured MOM containing Meeting Overview, Discussion Points, Decisions Taken, Action Items, and Next Steps → output translated into 3 languages (English, Hindi, and regional). This module is built but not yet integrated into the main eGramSabha application. Full integration is planned for a future release.

### eSign

Planned — digital signatures on Gram Sabha agenda and Minutes of Meeting by the Pradhan and other ward members. Will provide official authentication of meeting records and decisions. Not yet implemented.

### Citizen Self-Attendance

Planned — allow citizens to mark their own attendance via face biometric at the meeting venue, in addition to official-marked attendance.

---

*Continue to: [Architecture Diagram ->](./04-architecture.md)*
