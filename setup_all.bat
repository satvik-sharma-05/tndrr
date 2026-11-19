@echo off
REM Setup all task environments
echo ========================================
echo Setting up ALL Task Environments
echo ========================================
echo.

echo [1/3] Setting up Task 1 - LoRA Fine-tuning...
cd task1_lora_finetuning
call setup_env.bat
cd ..
echo.

echo [2/3] Setting up Task 2 - RAG from Scratch...
cd task2_rag_from_scratch
call setup_env.bat
cd ..
echo.

echo [3/3] Setting up Task 3 - Local Optimization...
cd task3_local_optimization
call setup_env.bat
cd ..
echo.

echo ========================================
echo All environments setup complete!
echo ========================================
echo.
echo Each task has its own isolated environment:
echo   - task1_lora_finetuning/venv_task1/
echo   - task2_rag_from_scratch/venv_task2/
echo   - task3_local_optimization/venv_task3/
echo.
echo To activate an environment:
echo   cd [task_folder]
echo   call venv_task[N]\Scripts\activate.bat
