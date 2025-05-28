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

            // Remove any whitespace, newlines, etc.
            var sanitized = Regex.Replace(versionString, @"\s+", "");
            
            Console.WriteLine($"Original CUDA version: '{versionString}', Sanitized: '{sanitized}'");
            
            return sanitized;
        }
    }
}
