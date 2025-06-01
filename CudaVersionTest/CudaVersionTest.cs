using System;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.IO;

class Program
{
    static void Main()
    {
        Console.WriteLine("CUDA Version Parsing Test");
        Console.WriteLine("========================");
        
        // Simulate various malformed CUDA version strings that could cause issues
        string[] testVersions = {
            "12.0",                    // Valid version
            "12.0\n",                  // Version with newline  
            "12.0\r\n",                // Version with carriage return + newline
            "  12.0  ",                // Version with whitespace
            "12.0\n      ",            // Version with newline and trailing spaces
            "5\n      7",              // The specific error case from BugBash.md
            "\t12.0\t",                // Version with tabs
            "12.0.1",                  // Version with patch number
            "12.0.1\n\r\t  ",         // Complex malformed version
        };

        foreach (var versionString in testVersions)
        {
            TestVersionParsing(versionString);
            Console.WriteLine();
        }
        
        Console.WriteLine("Testing FoundryFix sanitization...");
        Console.WriteLine("=================================");
        
        foreach (var versionString in testVersions)
        {
            TestWithFoundryFix(versionString);
            Console.WriteLine();
        }
    }
    
    static void TestVersionParsing(string versionString)
    {
        Console.WriteLine($"Testing version string: '{EscapeString(versionString)}'");
        
        try
        {
            var version = new Version(versionString);
            Console.WriteLine($"✅ Successfully parsed as: {version}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Failed to parse: {ex.GetType().Name}: {ex.Message}");
            
            // Try manual cleanup
            var cleanVersion = versionString?.Replace("\n", "").Replace("\r", "").Trim();
            Console.WriteLine($"   Attempting manual fix: '{cleanVersion}'");
            
            try
            {
                if (!string.IsNullOrEmpty(cleanVersion))
                {
                    var version = new Version(cleanVersion);
                    Console.WriteLine($"   ✅ Manual fix succeeded: {version}");
                }
            }
            catch (Exception ex2)
            {
                Console.WriteLine($"   ❌ Manual fix failed: {ex2.Message}");
            }
        }
    }
    
    static void TestWithFoundryFix(string versionString)
    {
        Console.WriteLine($"Testing with FoundryFix: '{EscapeString(versionString)}'");
        
        try
        {
            // Simulate the FoundryFix sanitization
            var sanitized = SanitizeCudaVersionString(versionString);
            Console.WriteLine($"   Sanitized to: '{sanitized}'");
            
            if (!string.IsNullOrEmpty(sanitized))
            {
                var version = new Version(sanitized);
                Console.WriteLine($"   ✅ Successfully parsed as: {version}");
            }
            else
            {
                Console.WriteLine($"   ⚠️  Empty version string after sanitization");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ❌ Failed even with FoundryFix: {ex.Message}");
        }
    }
    
    // Replicate the improved FoundryFix sanitization logic
    static string SanitizeCudaVersionString(string versionString)
    {
        if (string.IsNullOrEmpty(versionString))
        {
            return string.Empty;
        }

        // First try to extract the first valid version-like pattern from the original string
        var match = System.Text.RegularExpressions.Regex.Match(versionString, @"(\d+(?:\.\d+)*)");
        if (match.Success)
        {
            var extracted = match.Groups[1].Value;
            
            // Ensure we have at least major.minor format for System.Version
            if (!extracted.Contains('.'))
            {
                extracted += ".0";
                Console.WriteLine($"   Normalized single digit to: '{extracted}'");
            }
            
            Console.WriteLine($"   Extracted version pattern: '{extracted}' from input: '{EscapeString(versionString)}'");
            return extracted;
        }
        
        // If no valid pattern found, remove whitespace and try again
        var sanitized = System.Text.RegularExpressions.Regex.Replace(versionString, @"\s+", "");
        
        // Check if sanitized version looks valid
        if (System.Text.RegularExpressions.Regex.IsMatch(sanitized, @"^\d+(\.\d+)*$"))
        {
            if (!sanitized.Contains('.'))
            {
                sanitized += ".0";
            }
            return sanitized;
        }
        
        // Fallback: return a default version to prevent crashes
        Console.WriteLine($"   Warning: Could not parse CUDA version '{EscapeString(versionString)}', defaulting to 0.0.0");
        return "0.0.0";
    }
    
    static string EscapeString(string input)
    {
        return input?.Replace("\n", "\\n").Replace("\r", "\\r").Replace("\t", "\\t") ?? "(null)";
    }
}
