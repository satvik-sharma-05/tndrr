# Build FAISS index from documents (no frameworks!)
import json, numpy as np, faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

chunk_size = 512  # Characters per chunk

# Load documents
docs = []
for f in Path("data/documents").glob("*.txt"):
    docs.append(f.read_text())

# Chunk documents
chunks = []
for doc in docs:
    for i in range(0, len(doc), chunk_size - 100):  # 100 char overlap
        chunks.append(doc[i:i+chunk_size].strip())

print(f"Created {len(chunks)} chunks from {len(docs)} documents")

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Generating embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True, normalize_embeddings=True)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.astype('float32'))

# Save
Path("indices").mkdir(exist_ok=True)
faiss.write_index(index, "indices/faiss.index")
with open("indices/metadata.json", 'w') as f:
    json.dump([{"text": c} for c in chunks], f)

print(f"✓ Index saved with {len(chunks)} chunks")
