# eGramSabha — Visual Representations

## 5-Step Gram Sabha Lifecycle

```mermaid
flowchart LR
    R["1. REGISTER\n(Face)"] --> RE["2. REPORT\n(Voice)"]
    RE --> M["3. MEET\n(Agenda)"]
    M --> REC["4. RECORD\n(Decisions)"]
    REC --> T["5. TRACK\n(Status)"]

    style R fill:#2E7D32,color:#fff,stroke:#1B5E20
    style RE fill:#1565C0,color:#fff,stroke:#0D47A1
    style M fill:#FF6F00,color:#fff,stroke:#E65100
    style REC fill:#7B1FA2,color:#fff,stroke:#6A1B9A
    style T fill:#00838F,color:#fff,stroke:#006064
```

| Step | Actor | Action | AI Involvement | AWS Services |
|------|-------|--------|---------------|-------------|
| REGISTER | Official / Admin | Admin adds citizen data from CSV. Official/Admin captures face biometric with liveness (blink + head movement) | Face descriptor extraction (face-api.js, 128-dim) | S3 (face storage), Rekognition (production) |
| REPORT | Citizen | Record voice complaint in native language, anytime | STT → Grammar Correction → Translation → Sentiment | Bedrock, Translate, S3, Transcribe |
| MEET | Official | Schedule Gram Sabha, select issues for agenda | AI summarizes issues into backlog, officials select for agenda | Bedrock, Translate, Polly, SNS |
| RECORD | Official | Officials take facial biometric attendance of citizens to meet quorum. Decisions and outcomes recorded. | Officials capture resolutions and next steps per agenda item | — |
| TRACK | Both | Monitor issue lifecycle, verify resolutions | Auto-priority detection (URGENT flag) | CloudWatch (logging) |

---

## Continuous Governance Loop

```mermaid
flowchart TD
    A["Report Issue\n(anytime, voice/text)"] --> B["Issue Analysed\n(AI sentiment + priority)"]
    B --> C["AI Summarizes Issues\ninto Backlog"]
    C --> D["Officials Select Items\nfor Agenda"]
    D --> E["Meeting Held\n(biometric attendance)"]
    E --> F["Decisions Recorded\n(officials capture outcomes)"]
    F --> G["Status Updates\n(to citizens)"]
    G --> A

    style A fill:#1565C0,color:#fff
    style B fill:#FF6F00,color:#fff
    style C fill:#2E7D32,color:#fff
    style D fill:#4CAF50,color:#fff
    style E fill:#7B1FA2,color:#fff
    style F fill:#D32F2F,color:#fff
    style G fill:#FFA000,color:#fff
```

Citizens can report issues at any time — the cycle is continuous, not tied to meeting dates. AI summarizes and deduplicates issues into a backlog; officials curate the final agenda. This creates a persistent feedback loop between citizens and local government that did not exist before.

---

## Citizen Journey — 3 Portal Views

### Admin Portal Flow

```mermaid
flowchart TD
    ALOGIN["Admin Login"] --> ADASH["Admin Dashboard\n(overall metrics & stats)"]

    ADASH --> PANCHAYAT["Create / Manage Panchayats\n(LGD code, state/district/block,\npopulation, language, wards, sabhaCriteria)"]
    ADASH --> BULK["Add Citizens from CSV\n(Election Commission data)"]
    ADASH --> OFFICIALS["Create / Manage Officials\n(Pradhan, Sachiv, Ward Members, etc)"]
    ADASH --> ONBOARD["Optionally Onboard Citizens\nvia Face Biometric"]
    ADASH --> UPDATE["Update Citizen Profiles"]
    ADASH --> TICKETS["Manage Support Tickets"]
    ADASH --> CONFIG["Platform Configuration\n(liveness thresholds:\nblink_count, movement_count)"]

    OFFICIALS --> ROLES["6 Roles:\nSECRETARY, PRESIDENT,\nWARD_MEMBER, COMMITTEE_SECRETARY,\nGUEST, ADMIN"]

    style ALOGIN fill:#D32F2F,color:#fff
    style ADASH fill:#37474F,color:#fff
    style PANCHAYAT fill:#2E7D32,color:#fff
    style OFFICIALS fill:#1565C0,color:#fff
    style BULK fill:#FF6F00,color:#fff
    style ONBOARD fill:#7B1FA2,color:#fff
    style ROLES fill:#00838F,color:#fff
```

### Official Portal Flow

```mermaid
flowchart TD
    OLOGIN["Official Login\n(username / default password,\ncan change password)"] --> ODASH["Official Dashboard"]

    ODASH --> ISSUES["Report Issues\n(for self or on behalf\nof citizens via createdForId)"]
    ODASH --> REGCIT["Register Citizens\n(face biometric + voter ID\n+ update details)"]
    ODASH --> PANEDIT["Edit Panchayat\nContact Details & Letterhead"]
    ODASH --> MEETING["Schedule & Manage Gram Sabha\n(date, time, location, duration)"]
    ODASH --> AGENDA["Manage Agenda\n(create/update/delete items,\nselect from AI-generated summary)"]
    ODASH --> ATTEND["Take Biometric Attendance\n(face verification of citizens)"]
    ODASH --> ISSMGMT["View All Issues & Suggestions\n(filter by status/category/\npriority/ward, update status,\nadd resolution remarks)"]
    ODASH --> REPORTS["View / Export Reports\n(PDF with letterhead)"]

    style OLOGIN fill:#2E7D32,color:#fff
    style ODASH fill:#1565C0,color:#fff
    style ISSUES fill:#FF6F00,color:#fff
    style MEETING fill:#7B1FA2,color:#fff
    style AGENDA fill:#D32F2F,color:#fff
    style ATTEND fill:#00838F,color:#fff
    style REGCIT fill:#4CAF50,color:#fff
```

### Citizen Portal Flow

```mermaid
flowchart TD
    PREREQ["Pre-requisite:\nAdmin adds citizen from CSV\nOfficial/Admin onboards via face biometric"] --> LOGIN

    LOGIN["Citizen Login:\nLast 4 digits of Voter ID\n+ Live Face Capture\n(Euclidean distance < 0.4)"] --> DASH["Citizen Dashboard"]

    DASH --> REPORT["Report Issues\n(voice recording with category\nselection, or text,\noptional file attachments)"]
    DASH --> VIEW["View Issues\n(own issues +\nall panchayat issues, detailed view)"]
    DASH --> RSVP["RSVP for\nUpcoming Gram Sabhas"]
    DASH --> PASTMEET["View Past Meetings\n(with details & decisions)"]
    DASH --> UPMEET["View Upcoming Meetings\n(with agenda details)"]
    DASH --> SUPPORT["Support Tickets"]

    REPORT --> CAT["Select Category\n(6 categories, 20+ subcategories)"]
    CAT --> VOICE["Record Regional Audio\nor Type Text"]
    VOICE --> ATTACH["Upload Optional Attachments\n(photos, documents)"]
    ATTACH --> SUBMIT["Submit Issue\n(status: REPORTED)"]

    style PREREQ fill:#37474F,color:#fff
    style DASH fill:#2E7D32,color:#fff
    style REPORT fill:#FF6F00,color:#fff
    style SUBMIT fill:#7B1FA2,color:#fff
    style LOGIN fill:#00838F,color:#fff
    style VIEW fill:#4CAF50,color:#fff
```

---

## Issue Categories & Subcategories

```mermaid
mindmap
  root((Citizen Issues))
    Infrastructure
      Roads
      Bridges
      Buildings
      Street Lights
      Drainage
    Basic Amenities
      Drinking Water
      Sanitation
      Electricity
      Healthcare
      Education
    Social Welfare Schemes
      Pension
      Housing
      BPL Cards
      Ration
      MGNREGA
    Earning Opportunities
      Employment
      Skill Training
      Market Access
      Agriculture
    Culture & Nature
      Temples
      Community Halls
      Environment
      Heritage
    Other
      General
      Administrative
      Emergency
```

---

## Issue Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> REPORTED: Citizen submits issue
    REPORTED --> PICKED_IN_AGENDA: Official selects for Gram Sabha
    PICKED_IN_AGENDA --> DISCUSSED_IN_GRAM_SABHA: Discussed in meeting
    DISCUSSED_IN_GRAM_SABHA --> RESOLVED: Action taken, problem solved
    DISCUSSED_IN_GRAM_SABHA --> TRANSFERRED: Escalated to Block/District
    DISCUSSED_IN_GRAM_SABHA --> NO_ACTION_NEEDED: Invalid or irrelevant

    note right of REPORTED
        AI processes in background:
        STT → Grammar → Translation
        → Sentiment → Auto-Priority
    end note

    note right of PICKED_IN_AGENDA
        Official selects from
        AI-generated IssueSummary backlog
    end note

    note right of RESOLVED
        Official adds resolution
        remarks. Citizen notified.
    end note
```

---

## Meeting Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> SCHEDULED: Official creates meeting (isPanchayatPresident)
    SCHEDULED --> IN_PROGRESS: Quorum met, meeting auto-starts
    IN_PROGRESS --> CONCLUDED: Meeting ends

    note right of SCHEDULED
        Citizens RSVP
        Officials manage agenda
        from IssueSummary backlog
    end note

    note right of IN_PROGRESS
        Quorum check:
        attendanceCount >=
        ceil(totalVoters * sabhaCriteria / 100)

        Officials take facial biometric
        attendance of citizens
    end note

    note right of CONCLUDED
        Decisions recorded by officials
        Issue statuses updated
        PDF report with letterhead
    end note
```

---

## IssueSummary / Agenda Flow

```mermaid
flowchart TD
    CRON["Cron Job\nDetects unsummarized issues"] --> SEND["Send issues to\nvideo-mom-backend"]
    SEND --> AI["AI Summarization\n(deduplication / clubbing\nof related issues)"]
    AI --> RECORDS["Create IssueSummary Records\n(stored in DB)"]
    RECORDS --> BACKLOG["IssueSummary Backlog\n(available to officials)"]
    BACKLOG --> SELECT["Officials Select Items\nfor Meeting Agenda"]
    SELECT --> MEETING["Meeting Conducted\nwith Selected Agenda"]
    MEETING --> DISCUSSED["Discussed Items:\nStatus updated\n(DISCUSSED_IN_GRAM_SABHA)"]
    MEETING --> UNDISCUSSED["Undiscussed Items:\nReturned to Backlog\nfor future meetings"]

    style CRON fill:#37474F,color:#fff
    style AI fill:#FF6F00,color:#fff
    style RECORDS fill:#2E7D32,color:#fff
    style BACKLOG fill:#1565C0,color:#fff
    style SELECT fill:#7B1FA2,color:#fff
    style MEETING fill:#D32F2F,color:#fff
    style DISCUSSED fill:#00838F,color:#fff
    style UNDISCUSSED fill:#FFA000,color:#fff
```

---

## Provider Abstraction — Vendor Independence

```mermaid
flowchart LR
    subgraph ENV["Environment Variables (8 Switches)"]
        direction TB
        E1["STT_PROVIDER"]
        E2["LLM_PROVIDER"]
        E3["TRANSLATION_PROVIDER"]
        E4["TTS_PROVIDER"]
        E5["STORAGE_BACKEND"]
        E6["FACE_VERIFICATION_PROVIDER"]
        E7["USE_DOCUMENTDB"]
        E8["COMPREHEND_ENABLED"]
    end

    E1 --> |jio| JIO["Jio STT API"]
    E1 --> |whisper| WHISPER["HuggingFace Whisper"]
    E1 --> |aws_transcribe| TRANSCRIBE["AWS Transcribe"]

    E2 --> |bedrock| BEDROCK["Amazon Bedrock\n(Nova Lite)"]
    E2 --> |huggingface| HF["HuggingFace\nInference API"]

    E3 --> |aws_translate| TRANSLATE["AWS Translate"]
    E3 --> |llm| LLM_T["LLM-based\nTranslation"]

    E4 --> |polly| POLLY["Amazon Polly"]
    E4 --> |disabled| NONE1["Disabled"]

    E5 --> |s3| S3["Amazon S3"]
    E5 --> |gridfs| GRIDFS["MongoDB GridFS"]

    E6 --> |local| LOCAL["Client-side\nface-api.js"]
    E6 --> |rekognition| REK["AWS Rekognition"]

    E7 --> |true| DOCDB["Amazon DocumentDB"]
    E7 --> |false| MONGO["MongoDB"]

    style ENV fill:#37474F,color:#fff
    style BEDROCK fill:#2E7D32,color:#fff
    style S3 fill:#00838F,color:#fff
    style TRANSCRIBE fill:#2E7D32,color:#fff
    style POLLY fill:#2E7D32,color:#fff
    style TRANSLATE fill:#2E7D32,color:#fff
    style REK fill:#FFA000,color:#fff
    style DOCDB fill:#FFA000,color:#fff
```

**Benefit**: No code changes needed to switch providers. Enable A/B testing and cost optimization. Scale from hackathon to national deployment by changing config, not code.

---

*Continue to: [Process Flow Diagrams →](./03-process-flows.md)*
