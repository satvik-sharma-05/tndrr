# Compare quantization levels: FP16 vs INT8
import torch, time, psutil, os, json
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
PROMPTS = [
    "What is the capital of France?",
    "Write a haiku about programming",
    "Explain machine learning simply",
    "Calculate 15 * 37",
    "List 5 benefits of exercise",
    "def factorial(n):",
    "What came first: chicken or egg?",
    "Describe the water cycle",
    "What is Python?",
    "Write a short story about AI"
]

def benchmark(model, tokenizer, name):
    print(f"\n{'='*50}\n{name}\n{'='*50}")
    total_tokens, total_time = 0, 0
    mem_before = psutil.Process().memory_info().rss / 1024**3
    
    for prompt in PROMPTS:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        start = time.time()
        outputs = model.generate(**inputs, max_new_tokens=50)
        elapsed = time.time() - start
        
        tokens = outputs.shape[1] - inputs.input_ids.shape[1]
        total_tokens += tokens
        total_time += elapsed
    
    mem_after = psutil.Process().memory_info().rss / 1024**3
    speed = total_tokens / total_time
    
    print(f"Speed: {speed:.1f} tokens/sec")
    print(f"Memory: {mem_after:.2f} GB")
    return {"speed": speed, "memory": mem_after}

# Load models and test
tokenizer = AutoTokenizer.from_pretrained(MODEL)

print("Testing FP16...")
fp16 = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float16, device_map="auto")
fp16_results = benchmark(fp16, tokenizer, "FP16")

print("\nTesting INT8...")
int8 = AutoModelForCausalLM.from_pretrained(MODEL, load_in_8bit=True, device_map="auto")
int8_results = benchmark(int8, tokenizer, "INT8")

# Save results
os.makedirs("results", exist_ok=True)
with open("results/quantization.json", 'w') as f:
    json.dump({"fp16": fp16_results, "int8": int8_results}, f, indent=2)

print(f"\n✓ Results saved")
