# 🎯 SHL Assessment Recommendation System (RAG-based)

This repository contains a **web-based GenAI Assessment Recommendation System** built using a **Retrieval-Augmented Generation (RAG)** approach.  
The system maps natural language hiring requirements or job descriptions to the most relevant **SHL assessments** using semantic search.

This project fulfills all requirements of the **GenAI Assessment Recommendation assignment**, including:
- Data scraping and storage
- Modern RAG-based retrieval
- Evaluation and test-set predictions
- Public web application and API

---

## 🚀 Project Overview

Recruiters often struggle to choose the correct SHL assessments for specific job roles.  
This system solves that problem by allowing users to input free-form text (e.g., job descriptions) and receive ranked SHL assessment recommendations.

The system consists of:
- A **FastAPI backend** implementing semantic retrieval
- A **React frontend** for interactive usage
- A **Streamlit web app** deployed on Hugging Face Spaces
- An **evaluation pipeline** to measure retrieval quality

---

## 📁 Repository Structure

```
shl-assessment-recommendation-system/
│
├── backend/
│   ├── app.py
│   ├── scraper.py
│   ├── build_index.py
│   ├── evaluate.py
│   ├── requirements.txt
│   ├── shl_assessments_real.json
│   ├── faiss.index
│   ├── meta.pkl
│   ├── test_set.xlsx
│   └── surabhi_bhor.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── package-lock.json
│
├── streamlit_app/
│   └── app.py
│
├── .gitignore
└── README.md
```

---

## 🔗 Live Deployments

### 🌐 Web Application (Hugging Face Spaces)
https://huggingface.co/spaces/surabhic/shl-assessment-recommendation-system

### 🔌 Backend API (Render)
POST https://shl-assessment-recommendation-system-1-uosh.onrender.com/recommend

Health check:
GET https://shl-assessment-recommendation-system-1-uosh.onrender.com/health

---

## 🧠 RAG & Retrieval Approach

- Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings
- FAISS / cosine similarity for retrieval
- Top-K ranked SHL assessments returned as JSON

---

## 🔌 API Usage

### Example Request
```json
{
  "query": "Hiring data analyst with analytical reasoning",
  "max_results": 5
}
```

### Example Response
```json
{
  "query": "Hiring data analyst with analytical reasoning",
  "recommendations": [
    {
      "name": "Numerical Reasoning Test",
      "url": "https://www.shl.com/...",
      "score": 0.82,
      "test_type": ["Ability & Aptitude"],
      "duration": 30
    }
  ]
}
```

---

## 🧪 Evaluation

- Evaluation implemented in `evaluate.py`
- Test dataset: `test_set.xlsx`
- Predictions file: `surabhi_bhor.csv` (required format)

---

## 🛠️ How to Run Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Open: http://127.0.0.1:8000/docs

---

## 📊 Technologies Used

Python, FastAPI, Sentence Transformers, FAISS, React, Streamlit, Hugging Face Spaces, Render

---

## 👤 Author

**Surabhi Chandrakant Bhor**
