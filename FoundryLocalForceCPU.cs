using System;
using System.Diagnostics;
using System.IO;

class FoundryLocalForceCPU
{
    static void Main(string[] args)
    {
        Console.WriteLine("FoundryLocalForceCPU - Running Foundry Local in CPU-only mode");
        
        // Set environment variables to force CPU execution
        Environment.SetEnvironmentVariable("FOUNDRY_EXECUTION_PROVIDER", "CPUExecutionProvider");
        Environment.SetEnvironmentVariable("CUDA_VISIBLE_DEVICES", "-1");
        Environment.SetEnvironmentVariable("FOUNDRY_SKIP_CUDA_CHECK", "1");
        Environment.SetEnvironmentVariable("FOUNDRY_CUDA_VERSION_OVERRIDE", "0.0.0");
        Environment.SetEnvironmentVariable("CUDA_VERSION", "0.0.0");
        
        // Build the command arguments - default to "model ls" if none provided
        string arguments = args.Length > 0 ? string.Join(" ", args) : "model ls";
        
        Console.WriteLine($"Running: foundry {arguments}");
        Console.WriteLine();
        
        // Create and configure the process
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "foundry",
                Arguments = arguments,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = false
            }
        };
        
        // Hook up output handlers
        process.OutputDataReceived += (sender, e) => 
        {
            if (!string.IsNullOrEmpty(e.Data))
                Console.WriteLine(e.Data);
        };
        
        process.ErrorDataReceived += (sender, e) => 
        {
            if (!string.IsNullOrEmpty(e.Data))
                Console.Error.WriteLine(e.Data);
        };
        
        try
        {
            // Start the process and begin reading output
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            
            // Wait for the process to exit
            process.WaitForExit();
            
            // Return the exit code
            Environment.Exit(process.ExitCode);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error running foundry: {ex.Message}");
            Environment.Exit(1);
        }
    }
}