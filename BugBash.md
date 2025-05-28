# Bug Bash: Foundry Local CUDA Version Parsing Error

## Problem Summary

When running the Foundry Local CLI (e.g., `foundry model ls`), the application crashes with the following error:

```
System.FormatException: The input string '5\n      7' was not in a correct format.
   at System.Number.ThrowFormatException[TChar](ReadOnlySpan`1)
   at System.Version.ParseVersion(ReadOnlySpan`1, Boolean)
   at System.Version.Parse(String)
   at System.Version..ctor(String version)
   at Microsoft.AI.Foundry.Local.Common.CudaInfo.CheckCudaAvailability()
   ...
```

This is caused by the Foundry Local application's CUDA version detection logic attempting to parse a malformed version string (containing a newline or extra whitespace) as a `System.Version`. The bug is in the core Foundry Local application, not the SDK or user code.

## Root Cause

- The application retrieves the CUDA version from the system (possibly from a command, file, or registry) and attempts to parse it directly with `System.Version.Parse()`.
- If the version string contains unexpected characters (e.g., newlines, extra spaces), parsing fails and the application crashes.
- This prevents all CLI and SDK usage, as the backend service cannot start.

## Required Fix

- **Sanitize the CUDA version string** before passing it to `System.Version.Parse()`.
- The fix should:
  - Remove all newlines and carriage returns.
  - Trim leading/trailing whitespace.
  - Optionally, validate the string matches a version pattern (e.g., `\d+(\.\d+)*`).
- This should be done in the method responsible for CUDA version detection (likely in `CudaInfo.cs` or similar in the Foundry-Local source).

### Example Fix (C#):
```csharp
// ...existing code...
string rawVersion = /* get CUDA version string from system */;
string sanitizedVersion = rawVersion.Replace("\n", "").Replace("\r", "").Trim();
var version = new Version(sanitizedVersion);
// ...existing code...
```

## Validation Steps

1. **Rebuild the Foundry Local application** after applying the fix.
   ```powershell
   dotnet build Foundry-Local/sdk/cs/src/FoundryLocal.csproj
   ```
2. **Reinstall or copy the rebuilt binaries** to the appropriate location if needed.
3. **Run the CLI to confirm the error is resolved:**
   ```powershell
   foundry model ls
   ```
   - The command should now list available models without crashing.
4. **(Optional) Test with malformed CUDA version strings** in the environment, registry, or files to confirm the fix is robust.
5. **Validate SDK integration:**
   - Run a sample Python or JavaScript SDK script to ensure the backend service starts and responds as expected.

## Success Criteria

- `foundry model ls` runs without crashing, even if the CUDA version string is malformed.
- The Foundry Local service starts and is accessible via the SDK.
- No `System.FormatException` is thrown during CUDA version detection.

## Notes

- This bug is in the Foundry Local application's source code, not in user scripts or the SDK.
- If the fix is not applied, no workaround (environment variable, dummy `nvcc`, etc.) will reliably resolve the issue.
- After the fix, malformed CUDA version strings should be handled gracefully, defaulting to CPU or reporting a user-friendly error if parsing still fails.
