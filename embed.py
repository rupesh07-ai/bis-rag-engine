import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Running embed.py...")

# Load data safely
file_path = "data/standards.json"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read().strip()
    
    if not content:
        raise ValueError("❌ JSON file empty hai: " + file_path)
    
    data = json.loads(content)

# Validate data
if not isinstance(data, list):
    raise ValueError("❌ JSON list format me hona chahiye")

# Extract text
texts = []
for d in data:
    title = d.get("title", "")
    scope = d.get("scope", "")
    texts.append(title + " " + scope)

if len(texts) == 0:
    raise ValueError("❌ texts empty hai, JSON check karo")

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(texts)

# Convert to float32 (FAISS requirement)
embeddings = np.array(embeddings).astype("float32")

# Save embeddings
np.save("embeddings.npy", embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "faiss_index.bin")

# Save mapping
with open("data/mapping.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Index created successfully!")