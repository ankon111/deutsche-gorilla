# DeutschGorilla — German Vocabulary Trainer Platform (Angular + SQLite)

## 1. Project Overview

Build a general-purpose German Vocabulary Trainer platform with:

- Dictionary browsing
- Flashcards learning mode
- Quiz mode
- User authentication + user profile
- Progress tracking + preferences
- AI integration (OpenAI, Gemini, extensible) for:
  - Example sentence generation
  - Word-specific Q&A chat
  - General chat assistant (Home page)

System must support multi-language translations (Bangla + English initially) and be extensible for additional languages.

System must support vocabulary levels (A1/A2/B1/B2/C1/C2) and later support grammar lessons by level.

Database storage is required (SQLite initially, PostgreSQL migration later).

## 2. Key Functional Requirements

### FR-1 Vocabulary Storage (General, Not TELC-only)

Vocabulary is not limited to TELC B1.

System must allow insertion of new vocabulary later.

Importing TELC PDF words is a separate utility tool (not main app runtime).

### FR-2 Multi-language Translations

Each word must support translations in multiple languages.

Initial languages:

- Bangla (bn)
- English (en)

Design must allow adding new language codes later.

### FR-3 Word Metadata

Each word must store:

- German word
- CEFR level: A1, A2, B1, B2, C1, C2 (nullable)
- Part of Speech (POS): Verb/Noun/Adjective/Adverb/etc. (normalized table)

### FR-4 Noun Rules

If POS = Noun:

- Store article: der/die/das
- Store plural form if known

### FR-5 Verb Rules

If POS = Verb:

Store conjugation forms:

- Präsens (all persons)
- Präteritum (all persons)
- Perfekt (auxiliary + Partizip II)
- Imperativ (du/ihr/Sie)

### FR-6 Example Sentences (Updated)

Each word must have at least 2 pre-filled example sentences stored in DB.

UI must allow user to regenerate examples using AI provider.

Generated examples should be simple/suitable, no strict B1 constraint.

### FR-7 AI Chat System

AI chat must exist in:

- Word Details page (context-aware chat)
- Home page (general AI chat)

The AI system must support multiple providers:

- OpenAI
- Gemini
- Extensible provider interface for future models

User must provide their API keys.
API keys must be stored only in browser localStorage.

### FR-8 Learning Modes

Frontend must support:

- Flashcards mode
- Dictionary mode
- Quiz mode

User can switch modes via Settings.

### FR-9 User Authentication and Profiles

Users can register/login/logout.

Passwords must be securely hashed.

User profile stores:

- preferences
- learning progress
- quiz stats
- AI provider preference

### FR-10 Progress Tracking

Track per user:

- learned status
- last_seen
- correct_count / wrong_count
- optionally spaced repetition parameters (future extension)

### FR-11 Grammar Lessons (Future Support)

System must support grammar lessons by CEFR level in DB:

- A1 grammar
- A2 grammar
- B1 grammar

Future pages should allow showing grammar content.

### FR-12 Performance Requirements

Must support 2000+ words smoothly.

Search and filtering must be efficient.

UI must use pagination or lazy loading for large lists.

### FR-13 Observability and Logging

All services must implement structured logging with clear log levels.

Logs should include request identifiers, error details, and provider metadata where applicable.

The system should be designed to integrate with centralized observability tooling later (metrics, tracing).

## 3. Non-Functional Requirements

### NFR-1 Security

Passwords must be hashed using bcrypt/argon2.

API keys must never be stored in DB.

API keys must only exist in localStorage.

User data must be isolated by authentication token.

### NFR-2 Portability

Must run locally on Windows/Linux/macOS.

SQLite used for development.

Design must allow PostgreSQL migration later.

### NFR-3 Maintainability

Clean separation of concerns:

- DB layer
- service layer
- API layer
- frontend UI layer

AI provider logic must be pluggable.

### NFR-4 Reliability

If AI provider fails, app must show error but remain usable.

## 4. Tech Stack Requirements

### Frontend

- Angular 17+
- Angular Router
- Angular Forms
- Angular HttpClient
- LocalStorage usage for API keys + UI preferences
- Token-based authentication (JWT)

### Backend

- Python (FastAPI recommended) OR Node.js (Express acceptable)
- REST API
- SQLite database
- ORM optional (SQLAlchemy recommended if Python)

## 5. Database Schema (SQLite)

### 5.1 Table: parts_of_speech

```sql
CREATE TABLE parts_of_speech (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE   -- Verb, Noun, Adjective, Adverb, etc.
);
```

### 5.2 Table: words

```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE,
    level TEXT NULL,                 -- A1/A2/B1/B2/C1/C2
    pos_id INTEGER NOT NULL,

    article TEXT NULL,               -- der/die/das (only nouns)
    plural TEXT NULL,                -- plural form (only nouns)

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(pos_id) REFERENCES parts_of_speech(id)
);
```

### 5.3 Table: translations

```sql
CREATE TABLE translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,     -- 'bn', 'en', later more
    meaning TEXT NOT NULL,

    FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE,
    UNIQUE(word_id, language_code)
);
```

### 5.4 Table: examples

```sql
CREATE TABLE examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    sentence TEXT NOT NULL,

    FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE
);
```

### 5.5 Table: verb_conjugations

```sql
CREATE TABLE verb_conjugations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL UNIQUE,

    praesens TEXT NOT NULL,
    praeteritum TEXT NOT NULL,
    perfekt TEXT NOT NULL,
    imperativ TEXT NOT NULL,

    FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE
);
```

### 5.6 Table: users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5.7 Table: user_settings

```sql
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,

    default_mode TEXT DEFAULT 'flashcards',  -- flashcards/dictionary/quiz
    daily_limit INTEGER DEFAULT 20,
    enabled_languages TEXT DEFAULT '["bn","en"]',
    srs_enabled INTEGER DEFAULT 0,

    preferred_ai_provider TEXT DEFAULT 'openai', -- openai/gemini

    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 5.8 Table: user_progress

```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,

    learned INTEGER DEFAULT 0,
    last_seen DATETIME NULL,

    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,

    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(word_id) REFERENCES words(id) ON DELETE CASCADE,

    UNIQUE(user_id, word_id)
);
```

### 5.9 Table: grammar_lessons (Future)

```sql
CREATE TABLE grammar_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT NOT NULL,           -- A1/A2/B1...
    title TEXT NOT NULL,
    content TEXT NOT NULL,         -- markdown/html
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 6. External Import Script Requirements (Separate Task)

Tool: PDF Word Importer

Must be separate script, not part of backend runtime.

Reads TELC PDF or other lists.

Extracts words and inserts them into DB.

Only inserts into:

- words
- parts_of_speech if necessary

Translation/enrichment handled later.

## 7. REST API Requirements (Backend)

### Authentication

POST `/api/auth/register`

Input:

```json
{"username":"x","email":"x@mail.com","password":"pass"}
```

POST `/api/auth/login`

Returns JWT token.

POST `/api/auth/logout`

Optional.

### Vocabulary

GET `/api/words`

Query params:

- `search=...`
- `pos=Verb|Noun|...`
- `level=A1|A2|B1|...`
- `page=1`
- `limit=50`

Returns list with translations.

GET `/api/words/{id}`

Returns full word detail:

- translations
- examples
- conjugations if verb
- progress status

### Progress

POST `/api/progress/update`

Input:

```json
{
  "word_id": 123,
  "learned": true,
  "correct_delta": 1,
  "wrong_delta": 0
}
```

### Examples

POST `/api/words/{id}/examples/generate`

Request body:

```json
{
  "provider": "openai",
  "apiKey": "<frontend localStorage key>",
  "count": 2
}
```

Response:

```json
{"examples":["...", "..."]}
```

Generated examples should optionally be saved to DB.

### AI Chat (Word Context)

POST `/api/chat/word`

Body:

```json
{
  "provider": "openai",
  "apiKey": "....",
  "word_id": 123,
  "message": "Explain the difference between ...",
  "history": []
}
```

Response:

```json
{"reply":"..."}
```

### AI Chat (Home / General)

POST `/api/chat/general`

Body:

```json
{
  "provider": "gemini",
  "apiKey": "....",
  "message": "Explain accusative vs dative",
  "history": []
}
```

Response:

```json
{"reply":"..."}
```

### Grammar Lessons (Future)

GET `/api/grammar?level=B1`

Returns grammar lessons list.

## 8. AI Provider Architecture Requirements

### AI Provider Interface

Backend must implement provider abstraction:

- OpenAIProvider
- GeminiProvider
- BaseAIProvider

Each provider supports:

- `generateExamples(word, count)`
- `chat(prompt, history, context)`

The provider selection is controlled by frontend settings.

API keys are passed in request (from localStorage).

## 9. Angular Frontend Requirements

### Pages / Routes

| Route | Page |
| --- | --- |
| `/` | Home Dashboard + General AI Chat |
| `/login` | Login |
| `/register` | Register |
| `/dictionary` | Dictionary Mode |
| `/flashcards` | Flashcards Mode |
| `/quiz` | Quiz Mode |
| `/word/:id` | Word Details + Word Chat + Example Regeneration |
| `/settings` | User Settings |
| `/grammar` | Grammar by level (future-ready) |

### Components

- NavbarComponent
- WordCardComponent
- WordDetailComponent
- FlashcardComponent
- QuizComponent
- DictionaryComponent
- SettingsComponent
- AiChatBoxComponent (reusable for Home + Word page)
- ProgressBadgeComponent

### LocalStorage Keys

Frontend must store:

- `ai_provider = "openai" | "gemini"`
- `openai_api_key`
- `gemini_api_key`
- `ui_theme` (optional)
- `language_display = bn/en/both`

## 10. UI / Design Guidelines

### Color Palette (Mandatory)

Use the following palette consistently:

| Role | Name | Hex | Usage |
| --- | --- | --- | --- |
| Deep Base | Obsidian | #080808 | Main page background |
| Surface | Carbon | #1A1A1A | Cards, input fields, modals |
| Elevated | Slate | #2D2D2D | Hover states, dividers |
| Primary | Electric Mint | #00FFAD | CTA buttons, progress bars, active icons |
| Secondary | Soft Mint | #98FB98 | Secondary labels, success messages |
| Text Main | Snow White | #FFFFFF | Headings |
| Text Sub | Ash Grey | #B2BEB5 | Body text |

### Typography

- Modern sans-serif
- High contrast text
- Clear spacing for readability

### UI Layout Style

- Dark mode default
- Card-based UI
- Rounded corners
- Clean minimal style
- Smooth hover transitions
- Progress bars in Electric Mint

### Page UI Requirements

#### Home Page

- Welcome header
- Stats summary:
  - learned words
  - daily goal progress
- Buttons:
  - Flashcards
  - Dictionary
  - Quiz
- General AI Chat Box at bottom or right panel

#### Dictionary Page

- Search bar
- POS filter dropdown
- Level filter dropdown
- Paginated list of word cards
- Each card links to details page

#### Word Details Page

- Word + POS + Level badge
- Translations (Bangla + English)
- Examples list
- Button: "Generate more examples"
- Verb conjugation panel (if verb)
- Chat box (context-aware)

#### Flashcards Page

- Large centered card
- Buttons: again/hard/learned
- Next/previous navigation

#### Quiz Page

- Question area
- Multiple choice options
- Score + progress indicator

#### Settings Page

- Default mode
- Daily limit
- Language view
- AI provider selection
- API key input fields (stored in localStorage)

## 11. Deliverables

- Backend REST API project
- Angular frontend project
- SQLite DB schema + migration-ready structure
- AI provider integration layer (OpenAI + Gemini)
- Authentication system + user profiles
- Progress tracking
- AI chat on home page and word detail page
- Example regeneration feature
- Grammar DB support for future

The app name is: **DeutschGorilla**.
