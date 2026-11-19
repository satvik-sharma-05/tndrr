# LLM Tasks: LoRA Fine-tuning, RAG, and Optimization

Complete implementation of 3 LLM tasks with isolated environments.

## Quick Setup

**Windows:**
```bash
setup_all.bat
python verify_setup.py
```

**Linux/macOS:**
```bash
chmod +x setup_all.sh
./setup_all.sh
python verify_setup.py
```

---

## Task 1: LoRA Fine-tuning

Train a model to convert text → JSON (e.g., "Create high priority task" → `{"action": "create", "priority": "high"}`).

### Run

```bash
cd task1_lora_finetuning
# Windows: call venv_task1\Scripts\activate.bat
# Linux/macOS: source venv_task1/bin/activate

python prepare_dataset.py  # Generate 500 train + 100 test examples
python finetune_lora.py     # Train with LoRA (15-20 min on GPU)
python evaluate.py          # Compare base vs fine-tuned
```

### LoRA Settings

- **Rank (r)**: 16 - Controls adapter size
- **Alpha**: 32 - Scaling factor (2× rank)
- **Target modules**: q_proj, k_proj, v_proj, o_proj (attention layers)
- **Learning rate**: 2e-4 (higher than full fine-tuning)
- **Epochs**: 3

**Why LoRA?** Trains only 0.24% of parameters, uses 72% less memory than full fine-tuning.

### GPU Memory for 7B Model

| Method | Memory | Calculation |
|--------|--------|-------------|
| Full FT | ~65-70 GB | Model(14GB) + Gradients(14GB) + Optimizer(28GB) + Activations(8-12GB) |
| LoRA | ~18-20 GB | Frozen model(14GB) + LoRA params(34MB) + Gradients(34MB) + Optimizer(68MB) + Activations(4-6GB) |
| QLoRA | ~9-12 GB | 4-bit model(3.5GB) + LoRA adapters(~150MB) + Activations(3-5GB) + Compute buffer(1-2GB) |

**Key insight**: LoRA freezes base model (no gradients/optimizer states), trains tiny adapters instead.

---

## Task 2: RAG from Scratch

Build retrieval system using only embeddings + FAISS (no LangChain/LlamaIndex).

### Run

```bash
cd task2_rag_from_scratch
# Windows: call venv_task2\Scripts\activate.bat
# Linux/macOS: source venv_task2/bin/activate

python prepare_corpus.py    # Create 5 documents + 15 test questions
python build_index.py        # Build FAISS index (512-char chunks)
python evaluate_retrieval.py # Test Recall@5
```

### How It Works

1. **Documents** → Split into 512-char chunks (100-char overlap)
2. **Embeddings** → all-MiniLM-L6-v2 encodes each chunk
3. **FAISS Index** → L2 distance search (normalized for cosine similarity)
4. **Query** → Encode → Search top-5 chunks

**No frameworks!** Pure Python + sentence-transformers + FAISS + NumPy.

### BM25 vs Embeddings

- **BM25**: Keyword matching, great for rare terms, fast
- **Embeddings**: Semantic matching, handles synonyms, slower
- **Hybrid**: Use both (BM25 for keywords + embeddings for meaning) = best results

### Re-ranker

- **First stage (Bi-encoder)**: Fast retrieval of top 100 candidates
- **Second stage (Cross-encoder)**: Accurate re-ranking of top 20
- **Trade-off**: Slower but more precise

---

## Task 3: Model Optimization

Compare quantization levels (FP16 vs INT8).

### Run

```bash
cd task3_local_optimization
# Windows: call venv_task3\Scripts\activate.bat
# Linux/macOS: source venv_task3/bin/activate

python compare_quantization.py  # Benchmark both settings
```

### Results

| Setting | Memory | Speed | Quality Loss |
|---------|--------|-------|--------------|
| FP16 | ~1.0 GB | ~50 tok/s | 0% (baseline) |
| INT8 | ~0.5 GB | ~80 tok/s | ~1-2% |

### KV Cache

**Problem**: Without cache, must recompute attention for all previous tokens at each step.

**Solution**: Store key/value matrices from previous tokens.

- **Speedup**: O(n²) → O(n) complexity
- **Cost**: For 7B model with 4K context: ~2 GB per sequence (FP16)

### Why Quantization Works

- **FP16 → INT8**: 2 bytes → 1 byte (50% memory reduction)
- **How**: Map float range to 256 discrete values with per-channel scaling
- **Quality**: Minimal loss because neural networks are over-parameterized

### Serving 20 Users on 24GB GPU

**Model**: 7B-INT4 (~4 GB)

```
Memory budget:
- Model weights: 4 GB
- KV cache (20 users × 0.5 GB): 10 GB
- Safety buffer: 2 GB
Total: 16 GB ✓ Fits!
```

**Strategy**:
- Continuous batching (vLLM-style)
- Batch size: 8-16 sequences
- PagedAttention for cache efficiency
- Throughput: ~2500 tok/s / 20 users = 125 tok/s per user

---

## Deliverables Checklist

### Task 1
- [x] Base vs fine-tuned comparison (≥50 test examples)
- [x] LoRA settings with justification
- [x] 3 failure cases (see evaluate.py output)
- [x] GPU memory calculations (above)

### Task 2
- [x] 15 test questions with ground truth
- [x] Retrieval accuracy (Recall@5)
- [x] 2 failure cases (see evaluate output)
- [x] BM25 and re-ranker explanations (above)

### Task 3
- [x] Tokens/sec and memory for 2 settings
- [x] Output quality on 10 prompts
- [x] KV cache explanation (above)
- [x] Quantization memory savings (above)
- [x] Multi-user serving plan (above)

---

## Project Structure

```
├── task1_lora_finetuning/
│   ├── venv_task1/          # Isolated environment
│   ├── prepare_dataset.py
│   ├── finetune_lora.py
│   ├── evaluate.py
│   └── memory_calculation.md
│
├── task2_rag_from_scratch/
│   ├── venv_task2/          # Isolated environment
│   ├── prepare_corpus.py
│   ├── build_index.py
│   └── evaluate_retrieval.py
│
└── task3_local_optimization/
    ├── venv_task3/          # Isolated environment
    └── compare_quantization.py
```

Each task has its own virtual environment - no dependency conflicts!

---

## Requirements

- Python 3.8+
- GPU optional (all tasks work on CPU, just slower)
- ~8GB disk space

---

## Troubleshooting

**Import errors**: Check you're in correct environment
```bash
# Windows: where python
# Linux/macOS: which python
# Should show: .../venv_task[N]/...
```

**CUDA out of memory**: Reduce batch size or use CPU

**Slow training**: Normal on CPU, use free Colab GPU for Task 1

---

## License

MIT
