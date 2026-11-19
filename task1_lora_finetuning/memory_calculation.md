# GPU Memory Calculation for 7B Model Fine-tuning

## Model Parameters

A 7B parameter model in different precision formats:
- **FP32 (32-bit)**: 4 bytes per parameter
- **FP16 (16-bit)**: 2 bytes per parameter  
- **INT8 (8-bit)**: 1 byte per parameter
- **INT4 (4-bit)**: 0.5 bytes per parameter

---

## (a) Full Fine-tuning

Full fine-tuning requires storing:
1. **Model weights** (forward pass)
2. **Gradients** (backward pass) 
3. **Optimizer states** (Adam: 2x model size for momentum and variance)
4. **Activations** (intermediate computations)

### Calculation (FP16/Mixed Precision):

```
Model weights:           7B × 2 bytes = 14 GB
Gradients:              7B × 2 bytes = 14 GB  
Optimizer states:       7B × 2 × 2 bytes = 28 GB (Adam)
Activations (approx):   ~8-12 GB (batch size dependent)
─────────────────────────────────────────────
Total:                  ~64-70 GB
```

**Answer: ~65-70 GB for full fine-tuning with mixed precision (FP16)**

With FP32, this would double to **~130 GB**.

### Techniques to reduce:
- Gradient checkpointing: Saves ~30-40% memory (recomputes activations)
- Smaller batch size: Reduces activation memory
- DeepSpeed ZeRO: Distributes optimizer states across GPUs

---

## (b) LoRA Fine-tuning

LoRA only trains small adapter matrices, not the full model.

### What needs to be stored:
1. **Base model weights** (frozen, FP16): 14 GB
2. **LoRA parameters** (trainable)
3. **LoRA gradients**
4. **LoRA optimizer states**
5. **Activations** (reduced due to smaller trainable params)

### Calculation:

**LoRA parameters (rank r=16, target 8 attention layers per block):**

Typical 7B model has ~32 transformer blocks, each with attention projections (Q, K, V, O).

```
Per attention projection: d_model × r + r × d_model
For 7B model: d_model ≈ 4096

LoRA params per projection: 4096 × 16 × 2 = ~131K params
Total projections: 32 blocks × 4 projections = 128 projections  
Total LoRA params: 128 × 131K ≈ 16.8M params (~0.24% of 7B)
```

**Memory breakdown:**
```
Base model (frozen):     14 GB (FP16)
LoRA weights:           16.8M × 2 bytes = 33.6 MB
LoRA gradients:         33.6 MB
LoRA optimizer states:  33.6 MB × 2 = 67.2 MB
Activations:            ~4-6 GB (much less than full FT)
─────────────────────────────────────────────
Total:                  ~18-20 GB
```

**Answer: ~18-20 GB for LoRA fine-tuning (rank 16)**

### Why so much less?
- Base model is frozen → no gradients or optimizer states for 7B params
- Only training ~17M params instead of 7B
- Reduced activation memory

---

## (c) QLoRA Fine-tuning

QLoRA quantizes the base model to 4-bit while keeping LoRA adapters in higher precision.

### What needs to be stored:
1. **Base model weights** (4-bit quantized)
2. **LoRA parameters** (FP16)
3. **Dequantization constants** (small overhead)
4. **Computation in BF16** (temporary during forward/backward)
5. **LoRA gradients and optimizer states**

### Calculation:

```
Base model (4-bit):      7B × 0.5 bytes = 3.5 GB
Quantization metadata:   ~200-500 MB
LoRA weights (FP16):     33.6 MB  
LoRA gradients:          33.6 MB
LoRA optimizer states:   67.2 MB
Activations:             ~3-5 GB
Temp memory for compute: ~1-2 GB
─────────────────────────────────────────────
Total:                   ~8-12 GB
```

**Answer: ~9-12 GB for QLoRA (4-bit base + rank 16 LoRA)**

### Why even less?
- Base model compressed 4x (4-bit vs 16-bit)
- Only adapters need gradients and optimizer states
- Can fit on consumer GPUs (RTX 3090/4090: 24 GB)

---

## Comparison Table

| Method | Memory Required | Trainable Params | Training Speed |
|--------|----------------|------------------|----------------|
| Full Fine-tuning | ~65-70 GB | 7B (100%) | Fast |
| LoRA (r=16) | ~18-20 GB | ~17M (0.24%) | Medium |
| QLoRA (4-bit, r=16) | ~9-12 GB | ~17M (0.24%) | Slower* |

*QLoRA is slower due to quantization/dequantization overhead during forward/backward passes.

---

## Key Insights

1. **Full fine-tuning** requires storing gradients + optimizer states for ALL parameters
   - Memory = ~10x model size (FP16 + Adam optimizer)

2. **LoRA** dramatically reduces memory by:
   - Freezing base model (no gradients/optimizer states)
   - Training only tiny adapter matrices (<1% of params)

3. **QLoRA** goes further by:
   - Quantizing frozen base model to 4-bit (4x compression)
   - Maintaining adapter precision for training quality

4. **Rule of thumb:**
   - Full FT: ~10x model size
   - LoRA: ~3-4x model size  
   - QLoRA: ~2x model size (quantized)

---

## Practical Implications

For a 7B model:
- **Full fine-tuning**: Needs A100 80GB or multi-GPU setup
- **LoRA**: Fits on A100 40GB or RTX A6000
- **QLoRA**: Fits on RTX 3090/4090 (24GB) or even RTX 3060 (12GB) with small batch size

This makes QLoRA revolutionary for democratizing LLM fine-tuning on consumer hardware.
