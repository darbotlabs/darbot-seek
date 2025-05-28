# This script sets up the environment to use the FoundryFix.dll
# and then runs the Foundry Local command

# Path to the FoundryFix.dll
$fixDllPath = "G:\Github\new\darbot-seek\FoundryFix\bin\Debug\net7.0\FoundryFix.dll"

# Check if the fix DLL exists
if (-not (Test-Path $fixDllPath)) {
    Write-Error "FoundryFix.dll not found at $fixDllPath. Please build the project first."
    exit 1
}

# Set environment variables for workaround
$env:FOUNDRY_CUDA_VERSION_OVERRIDE = "12.7.0"

# Create a dummy CUDA version string that's properly formatted
# This is for the case where we can't inject our DLL
$env:CUDA_VERSION = "12.7.0"

# Add our fix path to the .NET Core Additional Deps
# This doesn't directly work with packaged apps but demonstrates the approach
$env:DOTNET_ADDITIONAL_DEPS = $fixDllPath

# Run the Foundry Local command, passing through any arguments
$foundryArgs = $args
Write-Host "Running Foundry Local with CUDA version fix..." -ForegroundColor Green
Write-Host "Command: foundry $foundryArgs" -ForegroundColor Gray

# Try to run with the fix
try {
    & foundry $foundryArgs
}
catch {
    Write-Host "`nError running Foundry Local. Trying alternative approach..." -ForegroundColor Yellow
    
    # If direct injection doesn't work, let's try with a CPU-only mode
    Write-Host "Setting CUDA_VISIBLE_DEVICES=-1 to force CPU mode" -ForegroundColor Yellow
    $env:CUDA_VISIBLE_DEVICES = "-1"
    & foundry $foundryArgs
}