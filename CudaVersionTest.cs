using System;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.IO;

class Program
{
    static void Main()
    {
        try 
        {
            // Try to get CUDA version using nvidia-smi
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "cmd.exe",
                    Arguments = "/c nvidia-smi",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                }
            };
            
            process.Start();
            var output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
            
            Console.WriteLine("NVIDIA-SMI Output:");
            Console.WriteLine(output);
            
            // Extract CUDA version from the output
            var match = Regex.Match(output, @"CUDA Version: (\S+)");
            if (match.Success)
            {
                var cudaVersionString = match.Groups[1].Value;
                Console.WriteLine($"Extracted CUDA version string: '{cudaVersionString}'");
                
                // Try parsing it (this is likely what's failing in Foundry)
                try
                {
                    var version = new Version(cudaVersionString);
                    Console.WriteLine($"Successfully parsed as System.Version: {version}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Failed to parse as System.Version: {ex.Message}");
                    
                    // Try a fix
                    var cleanVersion = Regex.Replace(cudaVersionString, @"\s+", "");
                    Console.WriteLine($"Cleaned version string: '{cleanVersion}'");
                    
                    try
                    {
                        var version = new Version(cleanVersion);
                        Console.WriteLine($"Successfully parsed cleaned version: {version}");
                    }
                    catch (Exception ex2)
                    {
                        Console.WriteLine($"Still failed with cleaned version: {ex2.Message}");
                    }
                }
            }
            else
            {
                Console.WriteLine("Could not find CUDA version in nvidia-smi output");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}
