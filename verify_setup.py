# Verify all environments are set up correctly
import subprocess, sys
from pathlib import Path

def check_env(name, path):
    if not path.exists():
        print(f"❌ {name}: Not found")
        return False
    
    exe = path / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if not exe.exists():
        print(f"❌ {name}: Python not found")
        return False
    
    try:
        result = subprocess.run([str(exe), "-m", "pip", "list"], capture_output=True, timeout=10)
        pkgs = len(result.stdout.decode().split('\n')) - 2
        print(f"✅ {name}: {pkgs} packages installed")
        return True
    except:
        print(f"⚠️  {name}: Cannot verify packages")
        return False

print("Checking environments...\n")

tasks = [
    ("Task 1", Path("task1_lora_finetuning/venv_task1")),
    ("Task 2", Path("task2_rag_from_scratch/venv_task2")),
    ("Task 3", Path("task3_local_optimization/venv_task3")),
]

results = [check_env(name, path) for name, path in tasks]

print(f"\n{'='*50}")
if all(results):
    print("✅ All environments ready!")
    print("\nNext: Open README.md and follow task instructions")
else:
    print("⚠️  Some environments not set up")
    print("\nRun: setup_all.bat (Windows) or ./setup_all.sh (Linux/macOS)")

sys.exit(0 if all(results) else 1)
