# Foundry Local Integration Guide

This guide explains how to use Microsoft Foundry Local as a provider in AgenticSeek.

## Overview

Foundry Local is Microsoft's local AI inference runtime that allows you to run AI models locally. This integration provides:

- CUDA version parsing fix to prevent crashes
- CPU-only fallback mode for systems without CUDA
- Integration with the AgenticSeek provider system
- Automatic environment setup for CUDA workarounds

## Installation and Setup

### 1. Install Foundry Local

First, install Microsoft Foundry Local CLI from the official Microsoft documentation.

### 2. Configure AgenticSeek

Update your `config.ini` file to use the foundry provider:

```ini
[MAIN]
is_local = True
provider_name = foundry
provider_model = microsoft/DialoGPT-medium
provider_server_address = 127.0.0.1:5000
# ... other settings
```

### 3. Test the Integration

You can test if everything is working with:

```bash
# Run the validation script
python foundry_validation.py

# Or test manually
python -c "from sources.llm_provider import Provider; p = Provider('foundry', 'test-model'); print('✅ Foundry provider available')"
```

## CUDA Issue Fix

The integration includes automatic fixes for the common CUDA version parsing issue:

### Problem
Foundry Local can crash with errors like:
```
System.FormatException: The input string '5\n      7' was not in a correct format.
   at System.Version.Parse(String)
   at Microsoft.AI.Foundry.Local.Common.CudaInfo.CheckCudaAvailability()
```

### Solution
The integration automatically sets environment variables to work around CUDA issues:

- `FOUNDRY_EXECUTION_PROVIDER=CPUExecutionProvider` - Forces CPU execution
- `CUDA_VISIBLE_DEVICES=-1` - Hides CUDA devices
- `FOUNDRY_SKIP_CUDA_CHECK=1` - Skips CUDA detection
- `FOUNDRY_CUDA_VERSION_OVERRIDE=12.0.0` - Provides a valid CUDA version

## Manual Workarounds

If you need to run foundry commands manually with the workarounds:

### Using PowerShell (Windows)
```powershell
.\foundry_model_ls_fix.ps1
```

### Using Command Prompt (Windows)
```cmd
foundry_model_ls_fix.cmd
```

### Using the C# Wrapper
```bash
# Build the wrapper
dotnet build FoundryLocalForceCPU/FoundryLocalForceCPU.csproj

# Run foundry commands through the wrapper
dotnet run --project FoundryLocalForceCPU model ls
```

### Manual Environment Setup (Linux/macOS)
```bash
export FOUNDRY_EXECUTION_PROVIDER=CPUExecutionProvider
export CUDA_VISIBLE_DEVICES=-1
export FOUNDRY_SKIP_CUDA_CHECK=1
export FOUNDRY_CUDA_VERSION_OVERRIDE=12.0.0

foundry model ls
```

## Troubleshooting

### Common Issues

1. **"foundry command not found"**
   - Install Foundry Local CLI
   - Ensure it's in your PATH

2. **CUDA version parsing errors**
   - The integration should handle this automatically
   - If it persists, use the manual workarounds above

3. **Provider not available**
   - Check that you've updated `sources/llm_provider.py`
   - Verify dependencies are installed

### Validation

Run the comprehensive validation:
```bash
python foundry_validation.py
```

This will test:
- ✅ CUDA Version Fix
- ✅ Foundry Provider Available  
- ✅ FoundryLocalForceCPU Tool
- ✅ FoundryFix DLL
- ✅ Configuration Support
- ⚠️ Foundry CLI Commands (requires Foundry Local installation)

## Technical Details

### CUDA Version Sanitization

The `FoundryFix/CudaVersionFix.cs` provides robust CUDA version string sanitization:

```csharp
// Handles malformed inputs like "5\n      7"
// Extracts valid version patterns
// Normalizes single digits to "x.0" format  
// Falls back to "0.0.0" if parsing fails
```

### Provider Implementation

The foundry provider in `sources/llm_provider.py`:

- Converts chat history to Foundry Local format
- Sets CUDA workaround environment variables
- Falls back to FoundryLocalForceCPU wrapper if needed
- Handles timeouts and error conditions

## Example Usage

```python
from sources.llm_provider import Provider

# Create foundry provider
provider = Provider("foundry", "microsoft/DialoGPT-medium", is_local=True)

# Generate response
history = [{"role": "user", "content": "Hello, how are you?"}]
response = provider.foundry_fn(history, verbose=True)
print(response)
```

## Files Created/Modified

- `sources/llm_provider.py` - Added foundry provider
- `FoundryFix/CudaVersionFix.cs` - CUDA version sanitization  
- `FoundryLocalForceCPU/` - CPU-only wrapper tool
- `CudaVersionTest/` - Test suite for CUDA parsing
- `foundry_validation.py` - End-to-end validation script
- `foundry_model_ls_fix.ps1` - PowerShell workaround
- `foundry_model_ls_fix.cmd` - Batch file workaround

This integration ensures that Foundry Local works reliably with AgenticSeek, even on systems with CUDA configuration issues.