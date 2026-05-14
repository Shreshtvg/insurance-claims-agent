**Autonomous Insurance Claims Processing Agent**

AI-powered insurance FNOL (First Notice of Loss) processing system that extracts structured claim information from PDF/TXT documents, validates required fields, and automatically routes claims to the appropriate workflow.

--------------------------------------------------------------------------------------------------------------------------------------

**Tech Stack**
Backend
FastAPI
Frontend
Streamlit
OCR
Mistral OCR API
LLM
Groq (Llama 3.1)

--------------------------------------------------------------------------------------------------------------------------------------

**Features**
PDF and TXT claim document support
OCR-powered scanned PDF parsing using Mistral OCR
AI-based structured field extraction using Groq LLM
Automatic missing field detection
Intelligent workflow routing
Explainable routing decisions
Streamlit dashboard UI
Pipeline visibility for debugging and transparency

--------------------------------------------------------------------------------------------------------------------------------------

**AI Pipeline**
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

--------------------------------------------------------------------------------------------------------------------------------------

**Setup Instructions**

1. Clone Repository
git clone <your-repo-url>
cd insurance-agent

3. Create Virtual Environment
Windows - 
python -m venv venv
venv\Scripts\activate

Mac/Linux -
python3 -m venv venv
source venv/bin/activate

5. Install Dependencies
cd backend
pip install -r requirements.txt

--------------------------------------------------------------------------------------------------------------------------------------

**Environment Variables**
Create:
backend/.env.example already exists
Please add the API keys for mistral OCR and Groq llm

--------------------------------------------------------------------------------------------------------------------------------------

**Running The Application**
**Start Backend**

From backend/ folder:
uvicorn app.main:app --reload
Backend runs on: http://127.0.0.1:8000

**Start Frontend**

Open a second terminal from project root:
streamlit run frontend/streamlit_app.py
Frontend runs on: http://localhost:8501

**Pipeline Visibility**

The frontend includes expandable debug sections showing:

OCR Parsed Text
Raw LLM Response
Final Structured JSON

This helps inspect extraction quality and OCR behavior.
