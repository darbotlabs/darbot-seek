@echo off
echo Running 'foundry model ls' with CUDA disabled (CPU-only mode)...
set CUDA_VISIBLE_DEVICES=-1
set FOUNDRY_EXECUTION_PROVIDER=CPUExecutionProvider
set FOUNDRY_SKIP_CUDA_CHECK=1
set CUDA_VERSION=0.0.0

foundry model ls

if %ERRORLEVEL% neq 0 (
    echo Failed to run 'foundry model ls' with workarounds.
)