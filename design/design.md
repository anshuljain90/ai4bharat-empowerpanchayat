# eGramSabha - System Design

## 1. Introduction

### 1.1 Purpose
This document describes the architectural approach and technical design for building the eGramSabha platform.

### 1.2 Vision
The design will create a scalable, secure, and maintainable system that brings modern technology to rural governance while remaining accessible to users with varying levels of digital literacy.

## 2. Architectural Approach

### 2.1 Service-Oriented Architecture

The platform will be built using a microservices approach with four independent services:

**Frontend Service**
A single-page application that will serve three distinct portals (Admin, Official, Citizen) with shared components and unified user experience.

**Backend Service**
A RESTful API service that will handle business logic, data management, authentication, and orchestration of other services.

**AI Service**
A specialized service dedicated to machine learning operations including speech-to-text, content generation, and translation.

**Database Service**
A document-oriented database that will store all application data with support for binary file storage.

### 2.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Browser                              │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐              │
│  │Admin Portal  │  │Official Portal│  │Citizen Portal│              │
│  │              │  │               │  │              │              │
│  │- Panchayat   │  │- Issue Mgmt   │  │- Face Login  │              │
│  │  Onboarding  │  │- Meeting Mgmt │  │- Issue Report│              │
│  │- Bulk Import │  │- Attendance   │  │- RSVP        │              │
│  │- Statistics  │  │- Agenda/MOM   │  │- Tracking    │              │
│  └──────────────┘  └───────────────┘  └──────────────┘              │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTPS/REST + JWT
                         │ JSON Payloads
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Backend API Service                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Middleware Pipeline                        │  │
│  │  Security → Rate Limit → Auth → Authorization → Data Scope    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │Route     │  │Business  │  │GridFS    │  │Cron      │             │
│  │Files     │  │Logic     │  │Storage   │  │Jobs      │             │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │
└────────┬────────────────────────────────────┬───────────────────────┘
         │                                    │
         │ REST/Async Polling                 │ Mongoose ODM
         │                                    │
         ▼                                    ▼
┌──────────────────────────┐         ┌─────────────────────────────┐
│   AI/ML Service          │         │   MongoDB Database          │
│  ┌────────────────────┐  │         │  ┌───────────────────────┐  │
│  │Provider Abstraction│  │         │  │Collections            │  │
│  │                    │  │         │  │- users                │  │
│  │- STT Pipeline      │  │         │  │- officials            │  │
│  │- LLM Pipeline      │  │         │  │- panchayats           │  │
│  │- Translation       │  │         │  │- issues               │  │
│  │- Async Processing  │  │         │  │- gramsabhas           │  │
│  └────────────────────┘  │         │  │- rsvps                │  │
│                          │         │  │- issuesummaries       │  │
│  ┌────────────────────┐  │         │  │- roles                │  │
│  │Request Tracker     │  │         │  │- supporttickets       │  │
│  │- Status Management │  │         │  │- ... and more         │  │
│  │- Progress Updates  │  │         │  │                       │  │
│  └────────────────────┘  │         │  │GridFS (fs.files/      │  │
└────────┬─────────────────┘         │  │        fs.chunks)     │  │
         │                           │  └───────────────────────┘  │
         │ HTTP/HTTPS                └─────────────────────────────┘
         │ API Keys/Tokens
         ▼
┌──────────────────────────┐
│  External AI Services    │
│                          │
│  ┌────────────────────┐  │
│  │Speech-to-Text      │  │
│  │Services            │  │
│  │(Multiple Providers)│  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │Language Model      │  │
│  │Services            │  │
│  │(Multiple Providers)│  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │Translation         │  │
│  │Services            │  │
│  │(Multiple Providers)│  │
│  └────────────────────┘  │
└──────────────────────────┘
```

### 2.3 Communication Patterns

**Frontend to Backend**
The frontend will communicate with the backend through REST APIs over HTTPS, using JSON for data exchange and JWT tokens for authentication.

**Backend to AI Service**
The backend will send requests to the AI service and poll for results, allowing long-running AI operations to complete without blocking user interactions.

**Services to Database**
Both backend and AI services will connect to the database using appropriate drivers, with the backend using synchronous operations and the AI service using asynchronous patterns.

**External Integrations**
The AI service will integrate with external providers for speech-to-text, language models, and translation services through standard HTTP APIs.

## 3. Frontend Design

### 3.1 Portal Architecture

**Three Independent Portals**

The frontend will provide three specialized portals, each optimized for its user group:

**Admin Portal**
Will provide comprehensive administrative capabilities including panchayat onboarding, bulk citizen registration, official management, platform configuration, and system-wide analytics.

**Official Portal**
Will enable panchayat officials to manage issues, schedule and conduct meetings, track attendance, generate agendas and minutes, and configure panchayat-specific settings.

**Citizen Portal**
Will offer citizens a simplified interface for face-based login, issue reporting with voice support, meeting RSVP, issue tracking, and attendance marking.

### 3.2 Technology Foundation

**Core Framework**
The frontend will be built using React, leveraging functional components and hooks for clean, maintainable code.

**User Interface**
Material-UI will provide the component library, ensuring consistent design and responsive behavior across devices.

**Routing**
React Router will handle client-side navigation, enabling smooth transitions between views without page reloads.

**State Management**
Context API will manage global state for authentication and language preferences, keeping the architecture simple and maintainable.

**HTTP Communication**
Axios will handle all API communication, with interceptors managing authentication tokens and error handling.

**Face Recognition**
The face-api.js library will run entirely in the browser, processing facial recognition without sending images to servers, protecting user privacy.

**Liveness Detection**
MediaPipe FaceMesh will provide real-time liveness detection, verifying natural blink patterns and head movements during face enrollment and login.

**Document Generation**
jsPDF will generate PDF documents with support for Hindi fonts and custom letterhead, enabling professional document output.

**Video Conferencing**
Integration with video conferencing SDKs will enable virtual meeting capabilities.

### 3.3 Component Organization

**Layered Structure**

The frontend will organize code into clear layers:

**Views Layer**
Page-level components that correspond to routes and compose smaller components into complete screens.

**Components Layer**
Reusable UI components that encapsulate specific functionality and can be used across different views.

**Services Layer**
Business logic and API communication, keeping components focused on presentation.

**Utils Layer**
Helper functions, contexts, and shared utilities used throughout the application.

**Constants Layer**
Enumerations, configuration values, and static data.

### 3.4 Authentication Flow

**Citizen Face Login Flow**

```
┌─────────────┐
│   Citizen   │
└──────┬──────┘
       │
       │ 1. Enter last 4 digits of Voter ID
       │    + Select Panchayat
       ▼
┌─────────────────────┐
│  Frontend (React)   │
└──────┬──────────────┘
       │
       │ 2. POST /api/auth/citizen/face-login/init
       │    { voterIdLastFour, panchayatId }
       ▼
┌─────────────────────────┐
│  Backend API            │
│  - Find user by         │
│    voter ID + panchayat |
│  - Generate security    │
│    token (10 min)       │
└──────┬──────────────────┘
       │
       │ 3. Return { userId, securityToken }
       ▼
┌──────────────────────┐
│  Frontend            │
│  - Start camera      │
│  - Liveness check    │
│    (blink + movement)|
│  - Capture face      │
│  - Extract descriptor|
└──────┬───────────────┘
       │
       │ 4. POST /api/auth/citizen/face-login/verify
       │    { userId, securityToken, faceDescriptor }
       ▼
┌─────────────────────┐
│  Backend API        │
│  - Verify token     │
│  - Match face       │
│    (Euclidean       │
│     distance < 0.4) │
│  - Generate JWT     │
└──────┬──────────────┘
       │
       │ 5. Return { token, refreshToken, user }
       ▼
┌─────────────────────┐
│  Frontend           │
│  - Store tokens     │
│  - Redirect to      │
│    dashboard        │
└─────────────────────┘
```

**Official Authentication**
Officials and administrators will use traditional username and password authentication, receiving JWT tokens that automatically refresh to maintain sessions.

### 3.5 Internationalization

**Language Support**
The platform will implement a language context provider that manages translations and user preferences. Translation files will contain all user-facing text in English and Hindi, with the architecture ready to support additional languages.

**Language Switching**
Users will switch languages through a header control, with their preference persisted across sessions.

## 4. Backend Design

### 4.1 API Architecture

**RESTful Design**
The backend will expose a RESTful API with resource-based URLs, standard HTTP methods, and JSON payloads. Responses will follow consistent structures for success and error cases.

**Route Organization**
The API will be organized into logical route groups:
- Authentication routes for each user type
- Resource management routes for panchayats, users, issues, officials, and wards
- Meeting management routes for scheduling, RSVP, and attendance
- Configuration routes for platform settings and location data
- Support routes for ticket management
- Summary routes for AI-generated content

### 4.2 Authentication and Authorization

**Three-Tier Token System**
The backend will implement separate JWT token types for admins, officials, and citizens, each with appropriate expiration times. Refresh tokens will enable session extension without re-authentication.

**Middleware Pipeline**
Requests will flow through a security middleware pipeline:
- Security headers and protection mechanisms
- Rate limiting to prevent abuse
- Request parsing and validation
- Authentication verification
- Authorization checks based on roles and resources
- Data scoping to ensure users only access appropriate data

**Role-Based Access Control**
The system will implement six distinct roles (Admin, Secretary, President, Ward Member, Committee Secretary, Guest) with granular permissions for five resource types (panchayat, user, official, issue, ward). Each role will have specific create, read, update, and delete permissions.

### 4.3 Data Models

**Document Structure**

The database will use thirteen primary collections:

**User Collection**
Will store citizen information including personal details, voter ID, ward assignment, facial biometric descriptors, and registration status.

**Official Collection**
Will maintain official accounts with credentials, role assignments, panchayat associations, and optional links to citizen profiles.

**Panchayat Collection**
Will hold panchayat profiles with location hierarchy, LGD codes, language settings, letterhead configuration, and contact information.

**Ward Collection**
Will define ward subdivisions within panchayats with geolocation and population data.

**Issue Collection**
Will track citizen issues with descriptions, audio attachments, transcription data, category classification, status, and resolution information.

**GramSabha Collection**
Will record meeting details including scheduling, agenda items, attendance records, guest information, and meeting recordings.

**RSVP Collection**
Will track citizen responses to meeting invitations with timestamps and status.

**AgendaItem Schema**
Will provide a reusable structure for multilingual agenda items with issue linkages.

**IssueSummary Collection**
Will store AI-generated agenda summaries per panchayat with linked issues.

**SummaryRequest Collection**
Will track asynchronous AI processing requests with status and result URLs.

**Role Collection**
Will define role permissions with resource-action matrices.

**PlatformConfiguration Collection**
Will maintain global system settings in a flexible structure.

**SupportTicket Collection**
Will manage support requests with categorization, attachments, and resolution tracking.

**Design Decisions**

The data model will use embedded documents for tightly coupled data like agenda items and attachments, while using references for entities that are queried independently. Compound indexes will optimize common query patterns, and text indexes will enable full-text search.

### 4.4 File Storage

**Binary Storage Strategy**

The system will use GridFS for storing binary files within MongoDB, providing:
- Chunked storage for large files
- Metadata tracking for each file
- Streaming upload and download
- Thumbnail generation for images

**File Types**
The storage system will handle face images with thumbnails, letterhead images, issue attachments, meeting recordings, and support ticket screenshots.

### 4.5 Background Processing

**Scheduled Tasks**

The backend will run seven scheduled background jobs:

**Transcription Status Monitoring**
Will poll the AI service every minute to check completion status of transcription requests and update issues with results.

**Transcription Retry**
Will automatically retry failed transcriptions up to three times, handling transient failures gracefully.

**Orphaned Transcription Recovery**
Will identify audio attachments that never received transcription requests and initiate processing.

**Summary Generation**
Will run hourly to identify panchayats with new transcribed issues and initiate agenda generation.

**Summary Result Collection**
Will poll hourly for completed summary generation and persist results to the database.

**Summary Retry**
Will retry failed summary requests every fifteen minutes.

**Agenda Translation**
Will fill in missing language translations for agenda items every fifteen minutes.

## 5. AI Service Design

### 5.1 Service Architecture

**Provider Abstraction**

The AI service will implement a provider pattern with abstract interfaces for three capabilities:
- Speech-to-text conversion
- Language model operations
- Text translation

This abstraction will allow switching between different AI service providers through configuration, supporting both cloud-based services and on-premise deployments.

### 5.2 Speech-to-Text Pipeline

**Audio Processing**

The service will accept audio files in various formats and convert them to a standard format (16kHz mono WAV) for processing. Format detection will happen automatically by examining file headers.

**Chunking Strategy**

Long audio files will be split into manageable chunks with overlapping segments to ensure no content is lost at boundaries. The system will then intelligently merge the transcribed chunks, removing duplicate content from overlaps.

**Multi-Provider Support**

The architecture will support multiple STT providers, allowing selection based on language support, accuracy requirements, and cost considerations.

### 5.3 Language Model Pipeline

**Transcription Enhancement**

Raw transcriptions will be processed through language models using specialized prompts that understand rural development context. The system will generate enhanced versions in multiple languages while preserving meaning.

**Content Generation**

Language models will power:
- Meeting agenda generation from issue collections
- Minutes of Meeting creation from transcriptions
- Issue clustering and categorization
- Formal document structuring

**Chunking for Large Content**

Large transcriptions will be processed in chunks with overlapping context, then intelligently merged to maintain coherence.

### 5.4 Asynchronous Processing

**Request Lifecycle**

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ 1. POST /transcription (with audio file)
       ▼
┌─────────────────────────────────────┐
│  AI Service                         │
│  - Generate request_id              │
│  - Store metadata in MongoDB        │
│  - Create background task           │
└──────┬──────────────────────────────┘
       │
       │ 2. Return immediately
       │    { request_id, status_url, result_url }
       ▼
┌─────────────┐
│   Client    │
│  - Continue │
│    other    │
│    work     │
└──────┬──────┘
       │
       │ 3. Poll GET /request/{id}/status
       │    (every few seconds)
       ▼
┌──────────────────────────────────────┐
│  AI Service                          │
│  - Return current status             │
│    { status, progress, step }        │
└──────────────────────────────────────┘

       Meanwhile, in background:
       
┌─────────────────────────────────────┐
│  Background Task                    │
│  1. Extract audio (progress: 10%)   │
│  2. Send to STT (progress: 40%)     │
│  3. Enhance with LLM (progress: 70%)│
│  4. Store results (progress: 100%)  │
│  5. Mark completed                  │
└─────────────────────────────────────┘

       When completed:
       
┌─────────────┐
│   Client    │
│  - Detects  │
│    completed│
│    status   │
└──────┬──────┘
       │
       │ 4. GET /transcription/{id}/result
       ▼
┌──────────────────────────────────────┐
│  AI Service                          │
│  - Return final results              │
│    { transcription, enhanced_text }  │
└──────────────────────────────────────┘
```

**Status Tracking**

Each request will progress through states (initiated, processing, completed, failed) with progress percentages and descriptive status messages.

**Resume Capability**

The system will check for existing intermediate results and resume from the last successful step, avoiding redundant processing.

## 6. Database Design

### 6.1 Database Selection

**Document Database Approach**

The platform will use MongoDB for its flexible schema, native JSON support, built-in file storage capabilities, geospatial indexing, and horizontal scaling potential.

### 6.2 Indexing Strategy

**Performance Optimization**

The database will use strategic indexes:
- Compound indexes for common query patterns (voter ID + panchayat)
- Location hierarchy indexes for cascading searches
- Text indexes for full-text search capabilities
- Status indexes for filtering operations
- Date indexes for temporal queries

**Unique Constraints**

Unique indexes will enforce data integrity for voter IDs per panchayat, official credentials, panchayat LGD codes, meeting RSVPs, and support ticket numbers.

### 6.3 Data Relationships

**Entity Relationship Overview**

```
┌──────────────┐
│  Panchayat   │
└───┬──────────┘
    │
    │ has many
    ├─────────────────┬─────────────────┬──────────────┐
    ▼                 ▼                 ▼              ▼
┌────────┐      ┌──────────┐     ┌──────────┐    ┌──────────┐
│  Ward  │      │   User   │     │ Issue    │    │GramSabha │
└────┬───┘      └────┬─────┘     └─────┬────┘    └────┬─────┘
     │               │                 │              │
     │ assigned to   │ created by      │ discussed in │
     └───────────────┴─────────────────┴──────────────┘

┌──────────────┐
│  Official    │
└───┬──────────┘
    │
    │ optional link
    ▼
┌──────────────┐
│    User      │
│  (Citizen)   │
└──────────────┘

┌──────────────┐
│ GramSabha    │
└───┬──────────┘
    │
    │ has embedded
    ├─────────────────┬─────────────────┐
    ▼                 ▼                 ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│AgendaItems │  │Attendance  │  │  Guests    │
└────────────┘  └────────────┘  └────────────┘

┌──────────────┐
│    Issue     │
└───┬──────────┘
    │
    │ has embedded
    ▼
┌──────────────┐
│ Attachments  │
└──────────────┘
```

**Reference Patterns**

The design will use references for one-to-many relationships (panchayat to users, issues, meetings) and many-to-one relationships (issue to panchayat, user). Many-to-many relationships (meetings to issues) will be handled through embedded arrays with references.

**Embedded Documents**

Tightly coupled data like agenda items, attachments, attendance records, and guest information will be embedded within parent documents for efficient retrieval.

## 7. Security Design

### 7.1 Authentication Security

**Password Protection**
Passwords will be hashed using bcrypt with appropriate salt rounds. Password reset will use time-limited tokens hashed with SHA-256.

**Token Security**
JWT tokens will use separate secrets for each user type, with short-lived access tokens and longer-lived refresh tokens. Token rotation will occur on refresh operations.

**Biometric Security**
Facial recognition will store only mathematical descriptors, not actual images. Liveness detection will prevent spoofing attacks. The two-step verification process will use time-limited security tokens.

### 7.2 API Security

**Request Protection**
The API will implement security headers, input sanitization, parameter pollution protection, CORS with origin whitelisting, and rate limiting.

**Data Validation**
All inputs will be validated against schemas, with file uploads restricted by type and size. Binary data will be base64 encoded for safe transmission.

### 7.3 Authorization Security

**Access Control**
The system will enforce role-based permissions at the resource level, implement panchayat data isolation, restrict ward members to their ward data, and verify ownership for sensitive operations.

**Audit Trail**
Comprehensive logging will track authentication attempts, administrative actions, data modifications, and security events.

## 8. Integration Design

### 8.1 External Service Integration

**AI Service Providers**

The platform will integrate with cloud-based AI services for:
- Speech-to-text conversion supporting multiple Indian languages
- Language model operations for content generation and enhancement
- Translation services for multilingual support

Authentication will use API keys or bearer tokens, with retry logic handling transient failures.

**Video Conferencing**

Integration with video conferencing services will enable virtual meeting capabilities through JavaScript SDKs with JWT-based authentication.

### 8.2 Internal Service Integration

**Backend to AI Service**

The backend will use a request-response-polling pattern, sending requests with 30-second timeouts for initiation, then polling for completion. Automatic retry will handle failures up to three attempts.

**Frontend to Backend**

The frontend will use REST APIs with JWT authentication, implementing interceptor-based token refresh and providing loading states during operations.

## 9. Scalability Design

### 9.1 Horizontal Scaling

**Stateless Services**

All services will be designed as stateless, allowing multiple instances to run behind load balancers. The frontend will be served as static files through CDN, while backend and AI services will scale independently.

**Database Scaling**

The database will support read replicas for query distribution, sharding by panchayat or state for data partitioning, connection pooling for efficient resource use, and index optimization for query performance.

### 9.2 Caching Strategy

**Application Caching**

The system will cache location hierarchies, platform configuration, role permissions, and panchayat metadata to reduce database load.

**Database Caching**

MongoDB's built-in caching will handle query results, indexes, and GridFS chunks.

### 9.3 Performance Optimization

**Frontend Optimization**

The frontend will use code splitting by route, lazy loading of components, and image optimization.

**Backend Optimization**

The backend will optimize database queries, implement pagination for large datasets, stream file downloads, and process heavy tasks asynchronously.

**AI Service Optimization**

The AI service will process chunks in parallel, batch requests where possible, and cache model data.

## 10. Observability Design

### 10.1 Logging

**Structured Logging**

The system will implement structured logs with timestamps, request IDs, user identification, service names, log levels, messages, and contextual information.

### 10.2 Health Monitoring

**Health Endpoints**

Each service will expose health check endpoints indicating database connectivity, external API availability, resource utilization, and overall service health.

### 10.3 Metrics

**Application Metrics**

The platform will track request rates and latencies, error rates by endpoint, authentication success rates, face recognition accuracy, and transcription completion times.

**Business Metrics**

The system will monitor active users by type, issues created and resolved, meetings conducted, and attendance rates.

## 11. Deployment Design

### 11.1 Containerization

**Docker Containers**

Each service will run in its own Docker container with defined resource limits, health checks, and restart policies.

**Orchestration**

Docker Compose will orchestrate local development and small deployments, with the architecture ready for container orchestration platforms in production.

### 11.2 Configuration Management

**Environment Variables**

All configuration will be externalized through environment variables including database connections, API credentials, feature flags, service URLs, and logging levels.

**Secret Management**

Sensitive credentials will be managed through secure secret storage appropriate to the deployment environment.

## 12. Data Protection

### 12.1 Backup Strategy

**Regular Backups**

The system will perform regular full backups with incremental backups between full backups, storing encrypted backups securely, and regularly testing restoration procedures.

### 12.2 Recovery Planning

**Disaster Recovery**

The platform will maintain documented recovery procedures, define recovery time and point objectives, and regularly test recovery processes.

## 13. Technology Choices

### 13.1 Frontend Technologies

React will provide the UI framework for its component model and ecosystem. Material-UI will ensure consistent, professional design. face-api.js will enable client-side face recognition for privacy.

### 13.2 Backend Technologies

Node.js with Express will power the backend for its asynchronous capabilities and JavaScript ecosystem. Mongoose will provide elegant MongoDB object modeling.

### 13.3 AI Service Technologies

Python with FastAPI will enable the AI service for its rich ML libraries and async support. Motor will provide async MongoDB access.

### 13.4 Database Technology

MongoDB will serve as the database for its flexible schema, GridFS support, and scaling capabilities.

## 14. Design Trade-offs

### 14.1 Client-Side Face Recognition

Processing face recognition in the browser protects privacy by never sending face images to servers and reduces server load, though it requires capable client devices.

### 14.2 Asynchronous AI Processing

Using async processing with polling enables better scalability and avoids timeout issues, though it adds complexity to client logic.

### 14.3 Document vs Relational Database

Choosing a document database provides schema flexibility and easier scaling, though it requires careful design of data relationships.

### 14.4 Monorepo Structure

Using a single repository for all services simplifies coordination and enables shared code, though it creates a larger codebase.

## 15. Conclusion

This design provides a comprehensive blueprint for building eGramSabha with emphasis on:

**Scalability** - Supporting growth in panchayats and users
**Accessibility** - Enabling participation through voice and face recognition
**Multilingual** - Supporting diverse Indian languages
**Security** - Protecting sensitive data and preventing unauthorized access
**Modularity** - Enabling independent service evolution
**Extensibility** - Supporting future enhancements and integrations

The architecture balances immediate needs with long-term flexibility, creating a foundation for transforming rural governance in India.
