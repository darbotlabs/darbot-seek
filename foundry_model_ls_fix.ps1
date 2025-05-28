# This script is a specific fix for the 'foundry model ls' command
# which is failing due to CUDA version parsing issues

# Force CPU mode to bypass the CUDA detection issue
$env:CUDA_VISIBLE_DEVICES = "-1"

Write-Host "Running 'foundry model ls' with CUDA disabled (CPU-only mode)..." -ForegroundColor Green

try {
    & foundry model ls
}
catch {
    Write-Host "`nError running 'foundry model ls' even in CPU-only mode." -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    
    Write-Host "`nAttempting workaround with manually configured environment..." -ForegroundColor Yellow
    
    # Try with a combination of environment variables
    $env:FOUNDRY_EXECUTION_PROVIDER = "CPUExecutionProvider"
    $env:FOUNDRY_SKIP_CUDA_CHECK = "1"
    $env:CUDA_VERSION = "0.0.0"
    
    & foundry model ls
}