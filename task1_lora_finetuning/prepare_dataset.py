# Generate dataset for training: Natural language → JSON conversion
import json
import random
from pathlib import Path

random.seed(42)

TEMPLATES = [
    "Create a {priority} priority task to {description} by {deadline}",
    "Update task {task_id} to {priority} priority",
    "Delete task {task_id}",
    "List {priority} priority tasks",
]

PRIORITIES = ["low", "medium", "high"]
DESCRIPTIONS = ["fix bug", "update docs", "write tests"]
DEADLINES = ["Monday", "Friday", "today"]

def generate_example():
    template = random.choice(TEMPLATES)
    if "Create" in template:
        text = template.format(
            priority=random.choice(PRIORITIES),
            description=random.choice(DESCRIPTIONS),
            deadline=random.choice(DEADLINES)
        )
        output = {"action": "create", "priority": random.choice(PRIORITIES)}
    elif "Update" in template:
        text = template.format(task_id=random.randint(1, 100), priority=random.choice(PRIORITIES))
        output = {"action": "update", "task_id": random.randint(1, 100)}
    elif "Delete" in template:
        text = template.format(task_id=random.randint(1, 100))
        output = {"action": "delete", "task_id": random.randint(1, 100)}
    else:
        text = template.format(priority=random.choice(PRIORITIES))
        output = {"action": "list", "filter": "priority"}
    
    return {"input": text, "output": json.dumps(output)}

# Generate data
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

train = [generate_example() for _ in range(500)]
test = [generate_example() for _ in range(100)]

with open(data_dir / "train.jsonl", 'w') as f:
    for ex in train:
        f.write(json.dumps(ex) + '\n')

with open(data_dir / "test.jsonl", 'w') as f:
    for ex in test:
        f.write(json.dumps(ex) + '\n')

print(f"✓ Created {len(train)} train + {len(test)} test examples")
print("Sample:", train[0])
