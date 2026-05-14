# Autonomous Insurance Claims Processing Agent

AI-powered insurance FNOL (First Notice of Loss) processing system that extracts structured claim information from PDF/TXT documents, validates required fields, and automatically routes claims to the appropriate workflow.

---

# Tech Stack

## Backend
- FastAPI

## Frontend
- Streamlit

## OCR
- Mistral OCR API

## LLM
- Groq (Llama 3.1)

---

# Features

- PDF and TXT claim document support
- OCR-powered scanned PDF parsing using Mistral OCR
- AI-based structured field extraction using Groq LLM
- Automatic missing field detection
- Intelligent workflow routing
- Explainable routing decisions
- Streamlit dashboard UI
- Pipeline visibility for debugging and transparency

---

# AI Pipeline

```text
PDF / TXT
    ↓
Mistral OCR
    ↓
Structured OCR Text
    ↓
Groq LLM Extraction
    ↓
Structured JSON
    ↓
Validation
    ↓
Claim Routing
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo-url>
cd insurance-agent
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

# Environment Variables

```text
backend/.env.example already exists.

Add your API keys:

MISTRAL_API_KEY=your_mistral_api_key
GROQ_API_KEY=your_groq_api_key
```

---

# Running The Application

## Start Backend

From `backend/` folder:

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Start Frontend

Open a second terminal from project root:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# API Endpoint

## Analyze Claim

```http
POST /analyze
```

### Input
- PDF file
- TXT file

### Output

```json
{
  "extractedFields": {},
  "missingFields": [],
  "recommendedRoute": "",
  "reasoning": ""
}
```

---

# Pipeline Visibility

The frontend includes expandable debug sections showing:

- OCR Parsed Text
- Raw LLM Response
- Final Structured JSON

This helps inspect extraction quality and OCR behavior.

---

# Current Capabilities

- Handles scanned insurance PDFs
- Supports OCR-based extraction
- Performs AI-powered structured field extraction
- Detects missing mandatory fields
- Generates routing recommendations

---

# Future Improvements

- Confidence scoring
- Fraud detection layer
- Section-aware extraction
- Human-in-the-loop review
- Claim history database
- Multi-agent workflows
- Async processing queue

---

# Demo Flow

1. Upload FNOL document
2. OCR extracts document text
3. LLM extracts structured claim fields
4. Validation checks missing fields
5. Routing engine determines workflow
6. UI displays extracted information and reasoning

---

# Author

Shresht Vg
