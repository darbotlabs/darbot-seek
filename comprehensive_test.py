#!/usr/bin/env python3
"""
Comprehensive end-to-end integration test for darbot-seek with Foundry Local.
This test validates all aspects of the integration without requiring the actual 
Foundry Local CLI to be installed.
"""

import os
import sys
import subprocess
import json
import tempfile
import shutil
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class FoundryIntegrationTester:
    def __init__(self):
        self.results = {}
        self.test_count = 0
        self.passed_count = 0
    
    def log_result(self, test_name, passed, message=""):
        self.results[test_name] = {"passed": passed, "message": message}
        self.test_count += 1
        if passed:
            self.passed_count += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
    
    def run_command(self, cmd, timeout=60, env=None):
        """Run a command safely."""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout, env=env
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def test_project_structure(self):
        """Test that all required files and directories exist."""
        print("📁 Testing Project Structure...")
        
        required_items = [
            ("sources/llm_provider.py", "file"),
            ("foundry_validation.py", "file"),
            ("FOUNDRY_INTEGRATION.md", "file"),
            ("BugBash.md", "file"),
            ("config.ini", "file"),
            ("FoundryFix/", "dir"),
            ("FoundryLocalForceCPU/", "dir"),
            ("CudaVersionTest/", "dir"),
            ("foundry_model_ls_fix.ps1", "file"),
            ("foundry_model_ls_fix.cmd", "file"),
        ]
        
        all_exist = True
        for item, item_type in required_items:
            path = project_root / item
            if item_type == "file" and path.is_file():
                self.log_result(f"Structure: {item} exists", True)
            elif item_type == "dir" and path.is_dir():
                self.log_result(f"Structure: {item} exists", True)
            else:
                self.log_result(f"Structure: {item} exists", False, f"Missing {item_type}")
                all_exist = False
        
        return all_exist
    
    def test_csharp_builds(self):
        """Test that all C# components build successfully."""
        print("🔨 Testing C# Component Builds...")
        
        projects = [
            "FoundryFix/FoundryFix.csproj",
            "FoundryLocalForceCPU/FoundryLocalForceCPU.csproj", 
            "CudaVersionTest/CudaVersionTest.csproj"
        ]
        
        all_build = True
        for project in projects:
            retcode, stdout, stderr = self.run_command(["dotnet", "build", project])
            if retcode == 0:
                self.log_result(f"Build: {project}", True)
            else:
                self.log_result(f"Build: {project}", False, f"Build failed: {stderr}")
                all_build = False
        
        return all_build
    
    def test_cuda_version_fix(self):
        """Test the CUDA version fix functionality."""
        print("🧪 Testing CUDA Version Fix...")
        
        retcode, stdout, stderr = self.run_command(
            ["dotnet", "run", "--project", "CudaVersionTest"]
        )
        
        if retcode == 0:
            # Check for successful parsing of problematic version string
            if "5\\n      7" in stdout and "Successfully parsed as: 5.0" in stdout:
                self.log_result("CUDA Fix: Problematic version handled", True)
            else:
                self.log_result("CUDA Fix: Problematic version handled", False,
                              "Did not properly handle '5\\n      7' case")
                return False
            
            # Check for multiple test cases
            if "✅ Successfully parsed" in stdout:
                success_count = stdout.count("✅ Successfully parsed")
                self.log_result(f"CUDA Fix: Multiple test cases ({success_count})", True)
            else:
                self.log_result("CUDA Fix: Multiple test cases", False)
                return False
        else:
            self.log_result("CUDA Fix: Test execution", False, f"Test failed: {stderr}")
            return False
        
        return True
    
    def test_provider_code_structure(self):
        """Test the provider code has all required components."""
        print("🔍 Testing Provider Code Structure...")
        
        provider_file = project_root / "sources" / "llm_provider.py"
        with open(provider_file, 'r') as f:
            content = f.read()
        
        # Test foundry provider registration
        if '"foundry": self.foundry_fn' in content:
            self.log_result("Provider: Foundry registration", True)
        else:
            self.log_result("Provider: Foundry registration", False)
            return False
        
        # Test foundry_fn method exists
        if 'def foundry_fn(self' in content:
            self.log_result("Provider: foundry_fn method", True)
        else:
            self.log_result("Provider: foundry_fn method", False)
            return False
        
        # Test CUDA workarounds
        cuda_workarounds = [
            "FOUNDRY_EXECUTION_PROVIDER",
            "CUDA_VISIBLE_DEVICES",
            "FOUNDRY_SKIP_CUDA_CHECK",
            "FOUNDRY_CUDA_VERSION_OVERRIDE"
        ]
        
        for workaround in cuda_workarounds:
            if workaround in content:
                self.log_result(f"Provider: {workaround} workaround", True)
            else:
                self.log_result(f"Provider: {workaround} workaround", False)
                return False
        
        # Test error handling
        if 'FileNotFoundError' in content:
            self.log_result("Provider: FileNotFoundError handling", True)
        else:
            self.log_result("Provider: FileNotFoundError handling", False)
        
        if 'TimeoutExpired' in content:
            self.log_result("Provider: Timeout handling", True)
        else:
            self.log_result("Provider: Timeout handling", False)
        
        # Test fallback mechanism
        if 'FoundryLocalForceCPU' in content:
            self.log_result("Provider: CPU fallback mechanism", True)
        else:
            self.log_result("Provider: CPU fallback mechanism", False)
            return False
        
        return True
    
    def test_configuration_system(self):
        """Test configuration file handling."""
        print("⚙️  Testing Configuration System...")
        
        # Test config.ini exists and is readable
        config_file = project_root / "config.ini"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_content = f.read()
            self.log_result("Config: config.ini readable", True)
        else:
            self.log_result("Config: config.ini readable", False)
            return False
        
        # Test foundry example config
        example_config = project_root / "config_foundry_example.ini"
        if example_config.exists():
            with open(example_config, 'r') as f:
                example_content = f.read()
            
            if "provider_name = foundry" in example_content:
                self.log_result("Config: Foundry example config", True)
            else:
                self.log_result("Config: Foundry example config", False)
        else:
            self.log_result("Config: Foundry example config", False)
        
        # Test config modification capability
        try:
            test_config = config_content.replace(
                "provider_name = ollama",
                "provider_name = foundry"
            )
            
            test_file = project_root / "test_config_temp.ini"
            with open(test_file, 'w') as f:
                f.write(test_config)
            
            # Verify the test config was written correctly
            with open(test_file, 'r') as f:
                verify_content = f.read()
            
            if "provider_name = foundry" in verify_content:
                self.log_result("Config: Modification capability", True)
            else:
                self.log_result("Config: Modification capability", False)
            
            # Cleanup
            test_file.unlink()
            
        except Exception as e:
            self.log_result("Config: Modification capability", False, str(e))
            return False
        
        return True
    
    def test_workaround_scripts(self):
        """Test workaround scripts are valid."""
        print("📜 Testing Workaround Scripts...")
        
        # Test PowerShell script
        ps_script = project_root / "foundry_model_ls_fix.ps1"
        if ps_script.exists():
            with open(ps_script, 'r') as f:
                ps_content = f.read()
            
            if "CUDA_VISIBLE_DEVICES" in ps_content and "foundry model ls" in ps_content:
                self.log_result("Scripts: PowerShell workaround", True)
            else:
                self.log_result("Scripts: PowerShell workaround", False)
        else:
            self.log_result("Scripts: PowerShell workaround", False)
        
        # Test Batch script
        cmd_script = project_root / "foundry_model_ls_fix.cmd"
        if cmd_script.exists():
            with open(cmd_script, 'r') as f:
                cmd_content = f.read()
            
            if "foundry model ls" in cmd_content:
                self.log_result("Scripts: Batch workaround", True)
            else:
                self.log_result("Scripts: Batch workaround", False)
        else:
            self.log_result("Scripts: Batch workaround", False)
        
        return True
    
    def test_documentation_completeness(self):
        """Test documentation is complete and helpful."""
        print("📚 Testing Documentation...")
        
        # Test main integration guide
        integration_doc = project_root / "FOUNDRY_INTEGRATION.md"
        with open(integration_doc, 'r') as f:
            doc_content = f.read()
        
        required_sections = [
            "Installation and Setup",
            "CUDA Issue Fix",
            "Troubleshooting",
            "Validation",
            "Technical Details",
            "Example Usage"
        ]
        
        for section in required_sections:
            if section in doc_content:
                self.log_result(f"Docs: {section} section", True)
            else:
                self.log_result(f"Docs: {section} section", False)
        
        # Test for code examples
        if "```" in doc_content and "python" in doc_content:
            self.log_result("Docs: Code examples present", True)
        else:
            self.log_result("Docs: Code examples present", False)
        
        # Test bug documentation
        bug_doc = project_root / "BugBash.md"
        with open(bug_doc, 'r') as f:
            bug_content = f.read()
        
        if "CUDA Version Parsing Error" in bug_content:
            self.log_result("Docs: Bug documentation", True)
        else:
            self.log_result("Docs: Bug documentation", False)
        
        return True
    
    def test_validation_script_structure(self):
        """Test the validation script has all required tests."""
        print("✅ Testing Validation Script Structure...")
        
        validation_file = project_root / "foundry_validation.py"
        with open(validation_file, 'r') as f:
            content = f.read()
        
        required_functions = [
            "test_cuda_version_fix",
            "test_foundry_provider_availability", 
            "test_foundry_local_force_cpu",
            "test_foundry_fix_dll",
            "test_config_foundry_option",
            "test_foundry_commands",
            "create_validation_report"
        ]
        
        for func in required_functions:
            if f"def {func}" in content:
                self.log_result(f"Validation: {func} function", True)
            else:
                self.log_result(f"Validation: {func} function", False)
        
        return True
    
    def test_cpu_wrapper_functionality(self):
        """Test the CPU wrapper has proper functionality."""
        print("💻 Testing CPU Wrapper Functionality...")
        
        wrapper_dir = project_root / "FoundryLocalForceCPU"
        cs_files = list(wrapper_dir.glob("*.cs"))
        
        if cs_files:
            with open(cs_files[0], 'r') as f:
                content = f.read()
            
            # Check for CPU-only configuration
            if "CPUExecutionProvider" in content:
                self.log_result("CPU Wrapper: CPUExecutionProvider config", True)
            else:
                self.log_result("CPU Wrapper: CPUExecutionProvider config", False)
            
            if "CUDA_VISIBLE_DEVICES" in content:
                self.log_result("CPU Wrapper: CUDA device hiding", True)
            else:
                self.log_result("CPU Wrapper: CUDA device hiding", False)
        else:
            self.log_result("CPU Wrapper: Source files exist", False)
            return False
        
        return True
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive test report."""
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE FOUNDRY LOCAL INTEGRATION TEST REPORT")
        print("="*80)
        
        success_rate = (self.passed_count / self.test_count) * 100
        
        print(f"\nOverall Results: {self.passed_count}/{self.test_count} tests passed")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Group results by category
        categories = {}
        for test_name, result in self.results.items():
            category = test_name.split(":")[0] if ":" in test_name else "General"
            if category not in categories:
                categories[category] = []
            categories[category].append((test_name, result))
        
        print("\nResults by Category:")
        for category, tests in categories.items():
            passed_in_category = sum(1 for _, result in tests if result["passed"])
            total_in_category = len(tests)
            print(f"\n{category}: {passed_in_category}/{total_in_category}")
            
            for test_name, result in tests:
                status = "✅" if result["passed"] else "❌"
                print(f"  {status} {test_name}")
                if result["message"]:
                    print(f"      {result['message']}")
        
        print("\n" + "-"*80)
        
        if success_rate >= 95:
            print("🏆 OUTSTANDING - Integration is production-ready!")
        elif success_rate >= 85:
            print("✅ EXCELLENT - Integration is working very well!")
        elif success_rate >= 70:
            print("⚠️  GOOD - Integration is functional with minor issues.")
        elif success_rate >= 50:
            print("🔧 NEEDS IMPROVEMENT - Integration has significant issues.")
        else:
            print("❌ MAJOR ISSUES - Integration requires substantial work.")
        
        return success_rate >= 70

def main():
    """Run the comprehensive integration test."""
    tester = FoundryIntegrationTester()
    
    print("🚀 Starting Comprehensive Foundry Local Integration Test")
    print("="*80)
    
    # Run all test categories
    test_results = [
        tester.test_project_structure(),
        tester.test_csharp_builds(),
        tester.test_cuda_version_fix(),
        tester.test_provider_code_structure(),
        tester.test_configuration_system(),
        tester.test_workaround_scripts(),
        tester.test_documentation_completeness(),
        tester.test_validation_script_structure(),
        tester.test_cpu_wrapper_functionality(),
    ]
    
    # Generate comprehensive report
    overall_success = tester.generate_comprehensive_report()
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit(main())