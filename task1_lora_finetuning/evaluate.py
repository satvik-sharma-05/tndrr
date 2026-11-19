# Evaluate: Compare base model vs fine-tuned model
import json, torch, re
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

# Load test data
test_data = []
with open("data/test.jsonl") as f:
    for line in f:
        test_data.append(json.loads(line))

tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token

def evaluate(model, name):
    correct = 0
    for ex in test_data[:50]:  # Test on 50 examples
        prompt = f"Convert to JSON: {ex['input']}\nOutput:"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=50)
        result = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        
        # Check if output matches expected
        try:
            pred = re.search(r'\{[^}]+\}', result)
            if pred and json.loads(pred.group()).get("action") == json.loads(ex["output"]).get("action"):
                correct += 1
        except:
            pass
    
    accuracy = correct / 50 * 100
    print(f"{name}: {correct}/50 correct ({accuracy:.1f}%)")
    return accuracy

print("Evaluating BASE model...")
base_model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float16, device_map="auto")
base_acc = evaluate(base_model, "Base Model")

print("\nEvaluating FINE-TUNED model...")
ft_model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float16, device_map="auto")
ft_model = PeftModel.from_pretrained(ft_model, "./lora_model")
ft_acc = evaluate(ft_model, "Fine-tuned Model")

print(f"\n✓ Improvement: +{ft_acc - base_acc:.1f}%")
