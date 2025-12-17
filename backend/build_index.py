import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

DATA_FILE = "shl_assessments_real.json"
INDEX_FILE = "faiss.index"
META_FILE = "meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [
    f"{d['name']} {d['description']} {' '.join(d['test_type'])}"
    for d in data
]

print("🔢 Creating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, INDEX_FILE)

with open(META_FILE, "wb") as f:
    pickle.dump(data, f)

print("✅ FAISS index built successfully")
