# Create document corpus and test questions
import json
from pathlib import Path

# Sample documents (Python documentation excerpts)
DOCS = [
    ("Context_Managers", """Context managers allow you to allocate and release resources precisely when you want to. 
The with statement clarifies code that previously would use try...finally blocks to ensure that clean-up code is executed.
Example: with open('file.txt', 'r') as f: data = f.read()
The with statement ensures that the file is properly closed after the block executes."""),
    
    ("Virtual_Environments", """Python applications often use packages that don't come with the standard library.
To create a virtual environment, run: python -m venv tutorial-env
On Windows: tutorial-env\\Scripts\\activate.bat
On Unix/MacOS: source tutorial-env/bin/activate"""),
    
    ("Data_Structures", """Lists have methods like append(), extend(), insert(), remove(), pop().
Tuples are immutable sequences. The main difference is tuples cannot be changed after creation."""),
    
    ("String_Methods", """str.upper() converts to uppercase. str.lower() converts to lowercase.
str.strip() removes leading/trailing whitespace. str.split() splits by delimiter.
Strings in Python are immutable."""),
    
    ("Introduction", """Python is easy to learn and powerful. It has efficient high-level data structures.
Python's elegant syntax makes it ideal for rapid application development.""")
]

# Test questions with ground truth
QUESTIONS = [
    {"question": "What is a context manager?", "ground_truth_passage": "Context managers allow you to allocate and release"},
    {"question": "How do I create a virtual environment?", "ground_truth_passage": "python -m venv tutorial-env"},
    {"question": "What's the difference between list and tuple?", "ground_truth_passage": "tuples cannot be changed after creation"},
    {"question": "How do I remove whitespace from strings?", "ground_truth_passage": "str.strip() removes leading/trailing whitespace"},
    {"question": "Is Python good for rapid development?", "ground_truth_passage": "ideal for rapid application development"},
    {"question": "Are strings mutable?", "ground_truth_passage": "Strings in Python are immutable"},
    {"question": "What does append do?", "ground_truth_passage": "Lists have methods like append()"},
    {"question": "How to activate venv on Windows?", "ground_truth_passage": "tutorial-env\\\\Scripts\\\\activate.bat"},
    {"question": "What does with statement do?", "ground_truth_passage": "with statement clarifies code"},
    {"question": "Can I change a tuple?", "ground_truth_passage": "tuples cannot be changed"},
    {"question": "What is str.upper()?", "ground_truth_passage": "str.upper() converts to uppercase"},
    {"question": "What is Python good for?", "ground_truth_passage": "elegant syntax"},
    {"question": "How do I split strings?", "ground_truth_passage": "str.split() splits by delimiter"},
    {"question": "What is venv for?", "ground_truth_passage": "Python applications often use packages"},
    {"question": "What methods do lists have?", "ground_truth_passage": "append(), extend(), insert()"}
]

# Save documents
Path("data/documents").mkdir(parents=True, exist_ok=True)
for name, content in DOCS:
    Path(f"data/documents/{name}.txt").write_text(content)

# Save test questions
with open("data/test_questions.json", 'w') as f:
    json.dump(QUESTIONS, f, indent=2)

print(f"✓ Created {len(DOCS)} documents and {len(QUESTIONS)} test questions")
