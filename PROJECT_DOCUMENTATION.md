# ResumeAI — Project Documentation

> **Document purpose:** Product, technical, operational, and stakeholder overview of the ResumeAI resume and career-category analysis application.
>
> **Audience:** Product owners, recruiters, career services teams, engineering teams, data scientists, and project reviewers.
>
> **Implementation note:** This document describes the repository as it currently exists. The project contains a FastAPI service, a legacy static web interface, and a separate React/Vite frontend. Some frontend expectations and API response fields are not yet aligned; see [Known limitations and integration notes](#15-known-limitations-and-integration-notes).

---

## 1. Executive summary

ResumeAI is a web application that analyzes job-related text and text-based PDF resumes. It combines a trained Bidirectional Gated Recurrent Unit (BiGRU) classifier with deterministic resume parsing and skill-to-role comparison logic.

The application supports two analysis goals:

1. **Career-category prediction:** classify text into one of seven broad employment categories and return a probability distribution.
2. **Resume profile extraction:** extract a supported job title and recognized technical skills from a PDF resume.

The codebase also contains a role requirement catalog and comparison logic. That logic computes a percentage match and lists matched and missing requirements for supported roles. Its intended use is career exploration and skills-gap awareness—not automated hiring decisions.

ResumeAI is a decision-support prototype. It is not a validated hiring assessment, an applicant tracking system, or a substitute for human review.

## 2. Introduction

Resumes express experience and skills in varied formats. A reviewer may need to identify the likely professional domain, extract relevant skills, and compare those skills with possible roles. ResumeAI provides an initial, structured view of that information through a web interface and HTTP API.

The project combines:

- A supervised text-classification model for broad career categories.
- PDF text extraction and phrase-based recognition of supported job titles and skills.
- A curated role-to-requirement map for explainable, rule-based skill comparison.
- A FastAPI backend and two browser UI implementations.

The classifier and the role matcher serve different purposes. The classifier predicts a broad category from text. The role matcher compares recognized resume skills to a predefined list of role requirements. A high score from one should not be interpreted as a prediction from the other.

## 3. Problem statement

### 3.1 Operational problem

Manual resume triage can involve repetitive reading, categorization, and skill inventory work. This can make it harder for job seekers, educators, and talent teams to quickly understand the broad professional themes in a profile.

### 3.2 Product response

ResumeAI turns free-form job-related text or a supported text-based PDF into:

- A predicted career category.
- Model confidence and category probabilities.
- A detected job title when the title appears in the supported title vocabulary.
- A list of skills recognized from the resume text.
- A role-by-role matched and missing skill comparison when the comparison function is integrated into the request flow.

### 3.3 Product goals

- Provide a quick, understandable first-pass categorization.
- Make the classification output more transparent by showing probabilities.
- Surface recognized resume skills in a structured format.
- Help users explore skill alignment with a catalog of career roles.
- Keep the initial workflow simple enough for a web demo and API integration.

### 3.4 Non-goals

- Making hiring, rejection, promotion, or compensation decisions.
- Verifying that a candidate truly possesses a listed skill.
- Parsing every resume layout, language, or file type.
- Performing optical character recognition (OCR) on image-only PDFs.
- Replacing a recruiter, career advisor, or formal skills assessment.
- Providing a calibrated probability of job success or future performance.

## 4. Users and stakeholder roles

| User or stakeholder | Primary need | How ResumeAI can help |
|---|---|---|
| Job seeker | Understand how a profile is categorized and identify skills to develop | Submit job-related text or a resume and review category probabilities and skill matches |
| Career coach or educator | Support structured career conversations | Use the output as a starting point for discussing skills and possible pathways |
| Recruiter or talent operations analyst | Organize profiles for human review | Use broad category suggestions as triage assistance, subject to human oversight |
| Product or platform integrator | Add profile classification to a workflow | Call the prediction or resume-analysis API |
| ML or data engineering team | Maintain and evaluate model and parsing behavior | Review model artifacts, tokenizer, datasets, and deterministic matching rules |
| Administrator or operator | Run the application and monitor service readiness | Start the API and use the health endpoint to check whether model artifacts loaded |

These are stakeholder/use-case roles, not authenticated application roles. The current service does not implement login, permissions, or organization-specific access control.

## 5. Use cases

### UC-01 — Predict a career category from text

**Primary actor:** Job seeker, coach, recruiter, or integrating application  
**Input:** Job title, role description, skills summary, or other job-related text (up to 2,000 characters in the UI schema)  
**Outcome:** One predicted category, its model confidence, and the model's probability for each supported category.

### UC-02 — Analyze a PDF resume

**Primary actor:** Job seeker or career coach  
**Input:** A PDF resume  
**Outcome:** The service extracts readable PDF text, detects a supported title if present, recognizes skills from a fixed vocabulary, and predicts a broad category from the extracted profile.

### UC-03 — Explore role skill alignment

**Primary actor:** Job seeker, career coach, or educator  
**Input:** A set of recognized skills  
**Outcome:** A deterministic comparison against role requirements, with a match percentage and matched/missing requirements for each role.

**Interpretation:** The percentage is a ratio of matched catalog requirements to total requirements for a role. It is not a hiring probability or a measure of competency.

### UC-04 — Integrate classification into another service

**Primary actor:** Product or platform engineer  
**Input:** JSON text or multipart PDF request  
**Outcome:** A typed JSON response from the FastAPI endpoints.

### UC-05 — Check model service readiness

**Primary actor:** Operator or integration client  
**Input:** `GET /health`  
**Outcome:** A status message and a boolean indicating whether the model and tokenizer have been loaded into the running application.

## 6. Industry value

ResumeAI can provide a useful starting point for:

- **Reducing repetitive first-pass sorting:** automatically proposes a broad category so a human reviewer can focus on exceptions and context.
- **Improving profile visibility:** extracts recognized skills into a consistent, inspectable list.
- **Supporting career planning:** makes potential skill gaps visible relative to a predefined role catalog.
- **Enabling workflow integration:** exposes classification and resume analysis through HTTP endpoints.
- **Encouraging consistent initial review:** applies the same model and skill vocabulary to each request, while leaving decisions to people.

### 6.1 Value measurement framework

No measured ROI, model accuracy, throughput, or time-saving benchmark is established in the repository. Teams evaluating a production pilot should measure these locally before making business claims.

| Measurement area | Example metric | Suggested evaluation |
|---|---|---|
| Processing efficiency | Median and 95th-percentile analysis time | Compare automated processing with the existing manual workflow |
| Classification quality | Per-category precision, recall, F1, and confusion matrix | Evaluate on a representative, labeled holdout set |
| Resume extraction quality | Job-title and skill extraction precision/recall | Annotate representative resumes and compare extracted entities |
| Role comparison usefulness | Agreement with career advisor review | Evaluate the role catalog and match explanations with domain experts |
| User experience | Completion rate, error rate, and user-rated clarity | Run usability sessions with target users |
| Fairness and robustness | Quality differences across relevant groups and resume formats | Assess only with appropriate, lawful, consented data and governance |

Do not treat the values emitted by the model as independently verified facts or calibrated probabilities without a separate evaluation and calibration process.

## 7. Functional capabilities

### 7.1 Text classification

- Accepts a JSON object with a `text` field.
- Normalizes text by lowercasing, removing apostrophes, replacing non-alphanumeric punctuation, and collapsing whitespace.
- Converts the text to token IDs using the saved Keras tokenizer.
- Pads or truncates the sequence to 50 tokens.
- Runs the BiGRU classifier and returns the predicted label and category probabilities.

### 7.2 Resume text extraction

- Accepts a PDF upload.
- Extracts embedded page text with `pypdf`.
- Searches for supported job titles and skill phrases.
- Builds classification input from the detected title and extracted skills.
- Returns a clear HTTP error if the upload is not a PDF or no supported skills are found.

PDFs that contain only scanned images may produce no extractable text because the current flow does not run OCR.

### 7.3 Skill and role comparison

The comparison implementation normalizes skill aliases, compares a user's recognized skills against role requirements, and sorts roles by descending match score. Its score is:

```text
matched unique requirements / total unique requirements × 100
```

Each requirement is counted at most once. The result includes matched requirements and missing requirements. Since the vocabulary and role catalog are curated in code, results depend on that coverage and may not recognize equivalent skills outside the configured aliases.

### 7.4 User interface

The repository includes:

- A **React 19 / Vite** application under `frontend/` with text-prediction and resume-analysis routes, a model-health indicator, probability bars, and expandable role-match cards.
- A **static HTML/CSS/JavaScript** interface under `static/`, which is served by the FastAPI root route.

The two interfaces are separate implementations and should not be assumed to have identical functionality.

## 8. Career categories and role catalog

### 8.1 Classifier categories

The classifier returns one of these seven categories:

1. Business
2. Cloud & Infrastructure
3. Data & AI
4. Design
5. Marketing
6. Product & Management
7. Software Engineering

### 8.2 Supported title vocabulary

Resume title detection checks for titles explicitly listed in the code. The current vocabulary includes:

- AI/ML Engineer
- Machine Learning Engineer
- Deep Learning Engineer
- NLP Engineer
- Computer Vision Engineer
- Data Scientist
- Data Analyst
- Software Engineer
- Backend Developer
- Frontend Developer
- Full Stack Developer
- Full Stack Engineer
- MERN Stack Developer
- PERN Stack Developer
- Python Developer
- Research Engineer
- AI Engineer
- ML Engineer

Title detection is phrase-based; an unlisted or differently worded title may not be detected.

### 8.3 Role skill matching

The role requirement catalog is maintained in `dependencies/job_title_analyze.py`. It includes role-specific requirements for multiple software, data, AI, and engineering careers. Role comparison is a rules-based calculation, independent of the neural model. Keep the title vocabulary, skill vocabulary, and role requirement catalog versioned and reviewed as product data.

## 9. Technical architecture

### 9.1 Logical architecture

```text
┌──────────────────────────────────────┐
│ Browser                              │
│ React/Vite UI or legacy static UI    │
└───────────────────┬──────────────────┘
                    │ HTTP / JSON or multipart PDF
                    ▼
┌──────────────────────────────────────┐
│ FastAPI application                  │
│ /predict · /analyze-resume · /health │
└───────────────┬──────────────────────┘
                │
       ┌────────┴───────────────┐
       ▼                        ▼
┌─────────────────┐   ┌────────────────────────┐
│ Text classifier │   │ Resume parsing         │
│ tokenizer +     │   │ pypdf → title/skill    │
│ BiGRU model     │   │ phrase recognition     │
└────────┬────────┘   └───────────┬────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐   ┌────────────────────────┐
│ Category labels │   │ Role requirement map   │
│ and probabilities│  │ and skill comparisons  │
└────────┬────────┘   └───────────┬────────────┘
         └────────────┬───────────┘
                      ▼
              JSON API response
```

### 9.2 Request lifecycle — text prediction

1. The browser sends `POST /predict` with JSON.
2. Pydantic validates the `text` input.
3. The service normalizes text, tokenizes it, and pads/truncates it to 50 tokens.
4. The loaded Keras model predicts category probabilities.
5. The service returns the selected category, confidence, and all category probabilities.

### 9.3 Request lifecycle — resume analysis

1. The browser sends a PDF using `multipart/form-data` to `POST /analyze-resume`.
2. The service verifies the filename extension.
3. `pypdf` extracts text from the PDF pages.
4. The title and skills recognizers find phrases present in their supported vocabularies.
5. The detected title and skills are sent to the category classifier.
6. The endpoint returns the extracted profile and classification response.

The role comparison helper exists in the repository. Confirm that the deployed API route and frontend contract include its response before relying on role match cards in a release.

## 10. Technology stack

| Layer | Technology | Purpose |
|---|---|---|
| Primary backend language | Python | API, parsing, classification orchestration, and skill matching |
| Web API | FastAPI | HTTP endpoints, request validation, file upload handling, and OpenAPI docs |
| ASGI server | Uvicorn | Runs the FastAPI application locally or as a service |
| API data validation | Pydantic | Validates JSON inputs and structures API responses |
| Machine learning runtime | TensorFlow / Keras | Loads the trained model and performs inference |
| Text tokenization | Saved Keras tokenizer (`tokenizer.pkl`) | Converts normalized text into token sequences compatible with model training |
| Numerical operations | NumPy | Selects the highest-probability class and converts output values |
| PDF processing | `pypdf` | Extracts embedded text from PDF pages |
| Skill parsing | Python phrase matching and curated vocabularies | Detects known title and skill strings in resume text |
| Optional NLP utility | spaCy | Imported by the extraction module; an optional NER helper also references `en_core_web_sm` |
| Frontend framework | React 19 | Component-based user interface in `frontend/` |
| Frontend routing | React Router | Routes between text prediction and resume analysis views |
| Frontend build/dev server | Vite | Serves and bundles the React application |
| Frontend styling | Tailwind CSS 4 and custom CSS | Responsive layout, theme, components, and interaction styling |
| Legacy frontend | HTML, CSS, vanilla JavaScript | Alternative static interface served directly by FastAPI |
| Data format | CSV | Role and job-posting datasets stored under `dataset/` |
| Model artifact format | Keras `.keras` and Python pickle | Persists the trained network and tokenizer |

### 10.1 Key technical concepts

- **BiGRU:** A bidirectional recurrent neural network that processes a sequence in both directions. The trained model maps token sequences to category scores.
- **Tokenizer:** A fitted vocabulary mapping words to integer IDs. It must remain compatible with the model's training preprocessing.
- **Padding/truncation:** Makes input lengths consistent for model inference; the service uses a maximum sequence length of 50.
- **Softmax-style category probabilities:** Model outputs are presented as per-category values. Their interpretation as calibrated confidence requires independent validation.
- **Phrase-aware matching:** Resume title/skill recognition uses known phrases and boundary-aware matching, rather than a general-purpose understanding of all skills.
- **Deterministic role score:** A transparent ratio over a curated requirements list; it is not produced by the neural model.

## 11. Data and model assets

### 11.1 Runtime artifacts

| Asset | Location | Purpose |
|---|---|---|
| Trained classifier | `Artifacts/BiGRU_Model.keras` | Predicts one of the seven career categories |
| Tokenizer | `Artifacts/tokenizer.pkl` | Converts normalized text into model-compatible sequences |

Both artifacts are loaded during the FastAPI lifespan startup. If either is missing or incompatible, the service may fail to start or may not be ready to serve predictions.

### 11.2 Dataset files

The repository contains CSV files for job data and several role/category-specific datasets under `dataset/`, including AI/ML, business, cloud/infrastructure, design, developer, marketing, and product management data.

The existence of a dataset in the repository does not establish that it was used to train the checked-in model. The project should retain dataset provenance, license/permission, preprocessing steps, train/validation/test splits, and model evaluation evidence if the model is to be used beyond a demonstration.

### 11.3 Data handling

The current request handlers do not intentionally persist uploaded resumes. However, uploaded content is processed in memory by the application and may be exposed through infrastructure logs, debugging, hosting providers, or backups depending on deployment configuration. Production deployments should document retention and deletion behavior explicitly.

## 12. API reference

The API is served by the FastAPI application in `main.py`. When running locally, the documented default URL is `http://127.0.0.1:8000`.

### `POST /predict`

Classifies manually supplied text.

**Request**

```json
{
  "text": "Machine learning engineer skilled in Python, PyTorch, TensorFlow, and deep learning."
}
```

**Successful response shape**

```json
{
  "text": "Machine learning engineer skilled in Python, PyTorch, TensorFlow, and deep learning.",
  "prediction_emotion": "Data & AI",
  "confidence": 0.91,
  "all_probabilities": {
    "Business": 0.01,
    "Cloud & Infrastructure": 0.02,
    "Data & AI": 0.91,
    "Design": 0.01,
    "Marketing": 0.01,
    "Product & Management": 0.01,
    "Software Engineering": 0.03
  }
}
```

The values above illustrate the response shape only; they are not a benchmark or guaranteed prediction.

### `POST /analyze-resume`

Accepts one PDF as multipart form data. The form field name is `file`.

```powershell
curl.exe -X POST http://127.0.0.1:8000/analyze-resume -F "file=@resume.pdf"
```

The current FastAPI response includes `job_title`, `skills`, `prediction_category`, `confidence`, `all_probabilities`, and a ranked `job_analysis` list with each role's score and matched/missing skills.

### `GET /health`

Returns a service status message and `model_loaded`, which indicates whether the model and tokenizer are present in the in-memory model registry.

### Common error responses

| Status | Meaning |
|---|---|
| `415` | The uploaded filename is not a PDF |
| `422` | Input validation failed or no supported resume skills were recognized |
| `503` | The classifier or tokenizer is not loaded |

FastAPI's interactive API documentation is available at `/docs` when the service is running.

## 13. Repository guide

```text
project-root/
├── Artifacts/
│   ├── BiGRU_Model.keras
│   └── tokenizer.pkl
├── api/                       # Earlier/alternate API route organization
├── dataset/                   # CSV job and role datasets
├── dependencies/
│   ├── Funtions.py            # Resume extraction orchestration and role comparison helper
│   ├── job_title_analyze.py   # Role requirement matching and score calculation
│   ├── model_prediction.py   # Title/skill vocabularies and phrase recognition
│   └── pdf_funtionality.py    # PDF text extraction
├── frontend/
│   ├── src/                   # React application
│   ├── package.json           # Frontend dependencies and scripts
│   └── vite.config.js         # Vite development server and API proxy
├── schema/
│   └── InputSchema.py         # Shared API request/response models
├── static/
│   ├── index.html             # Legacy static interface
│   ├── script.js              # Legacy interface behavior
│   └── style.css              # Legacy interface styling
├── main.py                    # FastAPI app, model loading, and API routes
├── requirements.txt           # Python dependency declarations
└── PROJECT_DOCUMENTATION.md   # This document
```

## 14. Local setup and operation

### 14.1 Prerequisites

- Python compatible with the installed TensorFlow/Keras versions.
- Node.js and npm for the React/Vite interface.
- The model and tokenizer artifacts under `Artifacts/`.
- Python packages from `requirements.txt`.
- The backend requirements include spaCy for the optional NER helper. The primary title and skill extraction path uses the configured phrase vocabulary and does not require the `en_core_web_sm` model.

### 14.2 Start the API

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
Set-Location backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Check `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`.

### 14.3 Start the React frontend

In a second terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (configured for port `5173`). The Vite configuration proxies `/predict`, `/analyze-resume`, and `/health` to the backend on port `8000`.

### 14.4 Build and lint the frontend

From the `frontend/` directory:

```powershell
npm run build
npm run lint
```

### 14.5 Static interface

The FastAPI root route (`/`) serves the interface from `static/index.html`. This is separate from the React/Vite frontend and does not require the Vite dev server.

## 15. Known limitations and integration notes

1. **Two frontend implementations:** The FastAPI root serves `static/`, while the React application is served separately by Vite. Features and presentation can diverge unless the team chooses one UI as the supported product and maintains the other deliberately.
2. **Text-based PDF assumption:** `pypdf` extracts embedded text only; image-only or scanned resumes require OCR, which is not present.
3. **Fixed vocabularies:** Title and skill extraction only recognizes configured phrases and aliases. New terminology requires an update to the vocabulary and tests.
4. **Fixed sequence length:** Text beyond the 50-token model input length is truncated; very short or sparse input may not contain enough signal.
5. **Model quality evidence:** The repository documentation does not establish validated accuracy, calibration, robustness, or bias results. Evaluate using representative, labeled data before operational use.
6. **No authentication or authorization:** Endpoints are not protected by a user identity or role-based access-control layer.
7. **No persistence or audit workflow:** The application does not provide a resume record store, user history, review queue, or audit trail.
8. **Operational hardening:** File size limits, content-based file validation, rate limiting, structured production logging, monitoring, and deployment configuration should be reviewed before exposing the service publicly.
9. **No business performance claims:** Throughput, accuracy, cost reduction, and time savings must be measured; they should not be inferred from the model or the presence of datasets.

## 16. Responsible use, privacy, and security

- Keep a human reviewer responsible for consequential employment decisions.
- Do not use category scores or skill-match percentages as a sole screening or rejection criterion.
- Communicate that extracted skills are text matches, not verified qualifications.
- Minimize resume data collection and retention. Avoid logging resume contents or personally identifiable information.
- Define a lawful basis, purpose limitation, access policy, retention period, and deletion process before processing real candidate data.
- Restrict public access with authentication, authorization, network controls, and request throttling where appropriate.
- Validate uploaded file type and size at the service boundary; treat all document content as untrusted input.
- Track model, tokenizer, vocabulary, role-map, and dataset versions to make results reproducible.
- Evaluate classification and extraction performance across relevant resume formats and populations, subject to applicable law and privacy safeguards.

## 17. Future roadmap

Potential improvements, subject to product and governance review:

1. Add contract tests to keep the React resume page and resume-analysis API response aligned.
2. Select one supported frontend or define a parity policy for the static and React interfaces.
3. Add OCR as an explicit, opt-in capability for scanned documents.
4. Add configurable upload limits, stricter file validation, and operational error reporting.
5. Add API authentication, rate limiting, monitoring, and privacy-aware audit events.
6. Version the role catalog and skills vocabulary as data, and provide domain-expert review workflows.
7. Build a labeled evaluation set and publish per-category metrics, limitations, and calibration evidence.
8. Add automated tests for PDF parsing, title/skill extraction, category response contracts, and role matching.
9. Add deployment artifacts and a documented production configuration if the service is to be hosted.

## 18. Screenshots

Add screenshots manually in the blank areas below. Suggested captures: the text prediction page, the resume upload page, and the complete resume results with role matches.

### 18.1 Text prediction screen



### 18.2 Resume upload screen



### 18.3 Resume analysis results



### 18.4 Architecture or workflow diagram



---

## 19. Glossary

| Term | Definition |
|---|---|
| BiGRU | Bidirectional Gated Recurrent Unit, a recurrent neural network architecture |
| Category probability | The model's output value associated with a classifier category; not necessarily calibrated |
| Confidence | The API's value for the predicted class, taken from the model output |
| OCR | Optical character recognition, which converts text in images into machine-readable text |
| Role match score | Percentage of unique catalog requirements matched by extracted resume skills |
| Skill vocabulary | Curated set of phrases that the deterministic extractor can recognize |
| Tokenizer | Saved text-to-integer mapping used to prepare model input |
