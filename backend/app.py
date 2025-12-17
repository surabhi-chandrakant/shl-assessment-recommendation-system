# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# FastAPI setup
# -----------------------------
app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "shl_assessments_real.json"

# -----------------------------
# Load data
# -----------------------------
if not os.path.exists(DATA_FILE):
    raise RuntimeError("❌ shl_assessments_real.json not found")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    ASSESSMENTS = json.load(f)

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

TEXTS = [
    f"{a['name']} {a.get('description','')} {' '.join(a.get('test_type',[]))}"
    for a in ASSESSMENTS
]

EMBEDDINGS = MODEL.encode(TEXTS, normalize_embeddings=True)

# -----------------------------
# Schemas
# -----------------------------
class QueryRequest(BaseModel):
    query: str
    max_results: int = 10


class AssessmentResponse(BaseModel):
    name: str
    url: str
    description: str
    duration: int
    remote_support: str
    adaptive_support: str
    test_type: List[str]
    score: float


class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[AssessmentResponse]


# -----------------------------
# Health API
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "total_assessments": len(ASSESSMENTS),
        "version": "1.0.0"
    }


# -----------------------------
# Recommendation API
# -----------------------------
@app.post("/recommend", response_model=RecommendationResponse)
def recommend(req: QueryRequest):
    query_embedding = MODEL.encode(
        [req.query], normalize_embeddings=True
    )[0]

    scores = np.dot(EMBEDDINGS, query_embedding)
    top_idx = np.argsort(scores)[::-1][: req.max_results]

    results = []
    for i in top_idx:
        a = ASSESSMENTS[i]

        results.append({
            "name": a["name"],
            "url": a["url"],
            "description": a.get("description", ""),
            "duration": a.get("duration", 45),
            "remote_support": a.get("remote_support", "No"),
            "adaptive_support": a.get("adaptive_support", "No"),
            "test_type": a.get("test_type", []),
            "score": float(scores[i])
        })

    return {
        "query": req.query,
        "recommendations": results
    }
