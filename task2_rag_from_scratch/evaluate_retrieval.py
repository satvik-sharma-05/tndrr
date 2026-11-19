# Evaluate retrieval accuracy
import json, faiss
from sentence_transformers import SentenceTransformer

# Load test questions
with open("data/test_questions.json") as f:
    questions = json.load(f)

# Load index
index = faiss.read_index("indices/faiss.index")
with open("indices/metadata.json") as f:
    chunks = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# Evaluate
correct = 0
for q in questions:
    query_emb = model.encode([q["question"]], normalize_embeddings=True)
    _, indices = index.search(query_emb, k=5)
    
    # Check if ground truth in top 5
    for idx in indices[0]:
        if q["ground_truth_passage"].lower() in chunks[idx]["text"].lower():
            correct += 1
            break

recall = correct / len(questions) * 100
print(f"Recall@5: {correct}/{len(questions)} ({recall:.1f}%)")
