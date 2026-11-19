# Train model with LoRA (efficient fine-tuning)
import json, torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

# LoRA Config: Train only 0.24% of parameters
lora_config = LoraConfig(
    r=16,  # Rank: controls adapter size
    lora_alpha=32,  # Scaling factor
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    task_type=TaskType.CAUSAL_LM
)

# Load model and tokenizer
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float16, device_map="auto")
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load data
data = []
with open("data/train.jsonl") as f:
    for line in f:
        data.append(json.loads(line))

# Format prompts
def format_prompt(ex):
    return f"Convert to JSON: {ex['input']}\nOutput: {ex['output']}"

prompts = [format_prompt(ex) for ex in data]
train_dataset = Dataset.from_dict({"text": prompts})

# Tokenize
def tokenize(examples):
    tokens = tokenizer(examples["text"], truncation=True, max_length=256)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

train_dataset = train_dataset.map(tokenize, batched=True, remove_columns=["text"])

# Train
trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
        logging_steps=50,
        save_strategy="epoch"
    ),
    train_dataset=train_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

print("Training...")
trainer.train()

# Save
model.save_pretrained("./lora_model")
tokenizer.save_pretrained("./lora_model")
print("✓ Training complete! Model saved to ./lora_model")
