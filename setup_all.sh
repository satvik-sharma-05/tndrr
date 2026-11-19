#!/bin/bash
# Setup all task environments
echo "========================================"
echo "Setting up ALL Task Environments"
echo "========================================"
echo ""

echo "[1/3] Setting up Task 1 - LoRA Fine-tuning..."
cd task1_lora_finetuning
chmod +x setup_env.sh
./setup_env.sh
cd ..
echo ""

echo "[2/3] Setting up Task 2 - RAG from Scratch..."
cd task2_rag_from_scratch
chmod +x setup_env.sh
./setup_env.sh
cd ..
echo ""

echo "[3/3] Setting up Task 3 - Local Optimization..."
cd task3_local_optimization
chmod +x setup_env.sh
./setup_env.sh
cd ..
echo ""

echo "========================================"
echo "All environments setup complete!"
echo "========================================"
echo ""
echo "Each task has its own isolated environment:"
echo "  - task1_lora_finetuning/venv_task1/"
echo "  - task2_rag_from_scratch/venv_task2/"
echo "  - task3_local_optimization/venv_task3/"
echo ""
echo "To activate an environment:"
echo "  cd [task_folder]"
echo "  source venv_task[N]/bin/activate"
