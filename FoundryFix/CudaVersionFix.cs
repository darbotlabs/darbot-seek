using System;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

namespace FoundryFix
{
    public static class CudaVersionFix
    {
        // This is the method that will be injected into Foundry Local
        public static string SanitizeCudaVersionString(string versionString)
        {
            if (string.IsNullOrEmpty(versionString))
            {
                return string.Empty;
            }

            // First try to extract the first valid version-like pattern from the original string
            var match = Regex.Match(versionString, @"(\d+(?:\.\d+)*)");
            if (match.Success)
            {
                var extracted = match.Groups[1].Value;
                
                // Ensure we have at least major.minor format for System.Version
                if (!extracted.Contains('.'))
                {
                    extracted += ".0";
                    Console.WriteLine($"Normalized single digit to: '{extracted}'");
                }
                
                Console.WriteLine($"Original CUDA version: '{versionString}', Sanitized: '{extracted}'");
                return extracted;
            }
            
            // If no valid pattern found, remove whitespace and try again
            var sanitized = Regex.Replace(versionString, @"\s+", "");
            
            // Check if sanitized version looks valid
            if (Regex.IsMatch(sanitized, @"^\d+(\.\d+)*$"))
            {
                if (!sanitized.Contains('.'))
                {
                    sanitized += ".0";
                }
                Console.WriteLine($"Original CUDA version: '{versionString}', Sanitized: '{sanitized}'");
                return sanitized;
            }
            
            // Fallback: return a default version to prevent crashes
            Console.WriteLine($"Warning: Could not parse CUDA version '{versionString}', defaulting to 0.0.0");
            return "0.0.0";
        }
    }
}
