import faiss
import json
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

# 🔥 Load everything only once
@st.cache_resource
def load_all():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("faiss_index.bin")

    with open("data/mapping.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return model, index, data


model, index, data = load_all()


def search(query, top_k=3):
    query_vec = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    distances, indices = index.search(query_vec, top_k)

    seen = set()
    results = []

    for i in indices[0]:
        item = data[i]

        if item["standard_id"] not in seen:
            item["reason"] = f"Relevant because it relates to {item['title']} used in {query}"
            results.append(item)
            seen.add(item["standard_id"])

    return results