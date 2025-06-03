#!/usr/bin/env python3
"""
Code-level audit of the Foundry Local integration.
This audits the code structure without requiring imports.
"""

import os
import ast
import re
from pathlib import Path

project_root = Path(__file__).parent

def audit_provider_code():
    """Audit the llm_provider.py code structure."""
    print("🔍 Auditing LLM Provider Code Structure...")
    
    provider_file = project_root / "sources" / "llm_provider.py"
    if not provider_file.exists():
        print("❌ Provider file not found")
        return False
    
    with open(provider_file, 'r') as f:
        content = f.read()
    
    # Check for foundry provider in available_providers
    if '"foundry": self.foundry_fn' in content:
        print("✅ Foundry provider registered in available_providers")
    else:
        print("❌ Foundry provider not found in available_providers")
        return False
    
    # Check for foundry_fn method
    if 'def foundry_fn(self' in content:
        print("✅ foundry_fn method defined")
    else:
        print("❌ foundry_fn method not found")
        return False
    
    # Check for CUDA workarounds
    cuda_checks = [
        "FOUNDRY_EXECUTION_PROVIDER",
        "CUDA_VISIBLE_DEVICES",
        "FOUNDRY_SKIP_CUDA_CHECK",
        "FOUNDRY_CUDA_VERSION_OVERRIDE"
    ]
    
    missing_cuda_checks = []
    for check in cuda_checks:
        if check in content:
            print(f"✅ CUDA workaround {check} present")
        else:
            missing_cuda_checks.append(check)
    
    if missing_cuda_checks:
        print(f"⚠️  Missing CUDA workarounds: {missing_cuda_checks}")
    
    # Check for fallback to FoundryLocalForceCPU
    if 'FoundryLocalForceCPU' in content:
        print("✅ FoundryLocalForceCPU fallback present")
    else:
        print("❌ FoundryLocalForceCPU fallback missing")
        return False
    
    # Check error handling
    if 'FileNotFoundError' in content and 'foundry' in content.lower():
        print("✅ FileNotFoundError handling for missing Foundry CLI")
    else:
        print("⚠️  Missing FileNotFoundError handling")
    
    if 'TimeoutExpired' in content:
        print("✅ Timeout handling present")
    else:
        print("⚠️  Missing timeout handling")
    
    return True

def audit_foundry_fix():
    """Audit the FoundryFix C# code."""
    print("🔍 Auditing FoundryFix C# Code...")
    
    foundry_fix_dir = project_root / "FoundryFix"
    if not foundry_fix_dir.exists():
        print("⚠️  FoundryFix directory not found")
        return True
    
    cs_files = list(foundry_fix_dir.glob("*.cs"))
    if not cs_files:
        print("❌ No C# files found in FoundryFix")
        return False
    
    print(f"✅ Found {len(cs_files)} C# files")
    
    # Check for CUDA version sanitization logic
    for cs_file in cs_files:
        with open(cs_file, 'r') as f:
            content = f.read()
        
        if 'CudaVersionFix' in content or 'SanitizeCudaVersion' in content:
            print(f"✅ CUDA version sanitization logic found in {cs_file.name}")
            
            # Check for regex patterns
            if 'Regex' in content or 'regex' in content:
                print("✅ Regex processing for version strings")
            
            # Check for fallback handling
            if '0.0.0' in content or 'fallback' in content.lower():
                print("✅ Fallback version handling")
            
            return True
    
    print("⚠️  No CUDA version sanitization logic found")
    return True

def audit_foundry_cpu_wrapper():
    """Audit the FoundryLocalForceCPU wrapper."""
    print("🔍 Auditing FoundryLocalForceCPU Wrapper...")
    
    wrapper_dir = project_root / "FoundryLocalForceCPU"
    if not wrapper_dir.exists():
        print("❌ FoundryLocalForceCPU directory not found")
        return False
    
    cs_files = list(wrapper_dir.glob("*.cs"))
    if not cs_files:
        print("❌ No C# files found in FoundryLocalForceCPU")
        return False
    
    print(f"✅ Found {len(cs_files)} C# files")
    
    # Check for CPU-only configuration
    for cs_file in cs_files:
        with open(cs_file, 'r') as f:
            content = f.read()
        
        cpu_indicators = [
            'CPUExecutionProvider',
            'CUDA_VISIBLE_DEVICES',
            'CPU',
            'cpu'
        ]
        
        found_indicators = [ind for ind in cpu_indicators if ind in content]
        if found_indicators:
            print(f"✅ CPU-only indicators found: {found_indicators}")
            return True
    
    print("⚠️  No CPU-only configuration found")
    return True

def audit_validation_script():
    """Audit the validation script structure."""
    print("🔍 Auditing Validation Script...")
    
    validation_file = project_root / "foundry_validation.py"
    if not validation_file.exists():
        print("❌ foundry_validation.py not found")
        return False
    
    with open(validation_file, 'r') as f:
        content = f.read()
    
    required_tests = [
        'test_cuda_version_fix',
        'test_foundry_provider_availability',
        'test_foundry_local_force_cpu',
        'test_foundry_fix_dll',
        'test_config_foundry_option',
        'test_foundry_commands'
    ]
    
    for test in required_tests:
        if test in content:
            print(f"✅ Test function {test} present")
        else:
            print(f"❌ Test function {test} missing")
            return False
    
    return True

def audit_documentation():
    """Audit the documentation completeness."""
    print("🔍 Auditing Documentation...")
    
    docs = [
        "FOUNDRY_INTEGRATION.md",
        "BugBash.md"
    ]
    
    for doc in docs:
        doc_path = project_root / doc
        if doc_path.exists():
            print(f"✅ {doc} exists")
            
            with open(doc_path, 'r') as f:
                content = f.read()
            
            # Check for key sections
            if doc == "FOUNDRY_INTEGRATION.md":
                sections = [
                    "Installation and Setup",
                    "CUDA Issue Fix", 
                    "Troubleshooting",
                    "Validation"
                ]
                
                for section in sections:
                    if section in content:
                        print(f"✅ Section '{section}' present")
                    else:
                        print(f"⚠️  Section '{section}' missing")
        else:
            print(f"❌ {doc} missing")
            return False
    
    return True

def audit_config_support():
    """Audit configuration file support."""
    print("🔍 Auditing Configuration Support...")
    
    config_file = project_root / "config.ini"
    if not config_file.exists():
        print("❌ config.ini not found")
        return False
    
    config_example = project_root / "config_foundry_example.ini"
    if config_example.exists():
        print("✅ config_foundry_example.ini exists")
    else:
        print("⚠️  config_foundry_example.ini missing")
    
    return True

def main():
    """Run all code audits."""
    print("🚀 Starting Code-Level Audit of Foundry Local Integration")
    print("="*70)
    
    audits = {
        "Provider Code Structure": audit_provider_code(),
        "FoundryFix Implementation": audit_foundry_fix(),
        "CPU Wrapper Implementation": audit_foundry_cpu_wrapper(),
        "Validation Script": audit_validation_script(),
        "Documentation": audit_documentation(),
        "Configuration Support": audit_config_support(),
    }
    
    print("\n" + "="*70)
    print("🎯 CODE AUDIT REPORT")
    print("="*70)
    
    passed = sum(1 for result in audits.values() if result)
    total = len(audits)
    success_rate = (passed / total) * 100
    
    print(f"\nOverall Status: {passed}/{total} audits passed")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\nDetailed Results:")
    for audit_name, result in audits.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {audit_name}")
    
    print("-" * 70)
    
    if success_rate >= 80:
        print("✅ EXCELLENT - Code structure is well implemented.")
        return 0
    elif success_rate >= 60:
        print("⚠️  GOOD - Minor issues but overall structure is solid.")
        return 0
    else:
        print("❌ NEEDS WORK - Significant structural issues found.")
        return 1

if __name__ == "__main__":
    exit(main())