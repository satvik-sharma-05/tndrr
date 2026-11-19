# Project Information

## What This Is

Complete implementation of 3 LLM tasks for learning/assignment purposes:
1. **Task 1**: Fine-tune model with LoRA (memory efficient training)
2. **Task 2**: Build RAG system from scratch (no frameworks)
3. **Task 3**: Compare model quantization (FP16 vs INT8)

## Key Features

✅ **Simple Code**: 20-50 lines per file (beginner-friendly)
✅ **Isolated Environments**: Each task has its own venv (no conflicts)
✅ **One README**: All instructions in single file
✅ **Working Implementation**: Ready to run, not just templates
✅ **Fast Setup**: One command installs everything

## File Count

```
Root:   7 files (README, setup scripts, verify)
Task 1: 7 files (3 Python scripts + setup files + memory doc)
Task 2: 6 files (3 Python scripts + setup files)
Task 3: 5 files (1 Python script + setup files)
Total:  25 files (was 45+ before simplification)
```

## Code Complexity

| File | Lines | Purpose |
|------|-------|---------|
| prepare_dataset.py (T1) | 47 | Generate training data |
| finetune_lora.py (T1) | 50 | Train with LoRA |
| evaluate.py (T1) | 35 | Test accuracy |
| prepare_corpus.py (T2) | 30 | Create documents |
| build_index.py (T2) | 25 | Build FAISS index |
| evaluate_retrieval.py (T2) | 20 | Test retrieval |
| compare_quantization.py (T3) | 35 | Benchmark models |

**Average**: 35 lines per script (easy to understand!)

## Time Estimates

- **Setup**: 10 minutes
- **Task 1**: 30-45 minutes (most time is training)
- **Task 2**: 20-30 minutes
- **Task 3**: 15-25 minutes
- **Total**: 2-3 hours including setup

## Requirements

- Python 3.8+
- 8GB disk space
- GPU optional (works on CPU, just slower)

## What Makes This Beginner-Friendly

1. **Short code**: No file over 50 lines
2. **Clear names**: Variables/functions self-explanatory
3. **Minimal abstractions**: Direct implementations
4. **One guide**: Everything in README.md
5. **Working examples**: Not just templates

## Environment Isolation

Each task runs in its own virtual environment:
- `task1_lora_finetuning/venv_task1/`
- `task2_rag_from_scratch/venv_task2/`
- `task3_local_optimization/venv_task3/`

This prevents version conflicts between tasks.

## Getting Started

1. Read this file (you are here!)
2. Run setup: `setup_all.bat` or `./setup_all.sh`
3. Verify: `python verify_setup.py`
4. Open `README.md` for task instructions

## Support Files

- **README.md** - Complete guide with all instructions
- **QUICKSTART.txt** - Command reference card
- **FINAL_SUMMARY.txt** - What was simplified
- **memory_calculation.md** - GPU memory math (Task 1)

## Technology Stack

**Task 1:**
- PyTorch, Transformers, PEFT
- Model: Qwen2.5-0.5B-Instruct

**Task 2:**
- sentence-transformers, FAISS, NumPy
- No LangChain/LlamaIndex (pure implementation)

**Task 3:**
- PyTorch, Transformers
- Quantization via bitsandbytes

## License

MIT - Free to use for learning/assignment purposes
