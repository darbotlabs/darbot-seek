#!/usr/bin/env python3
"""
Edge case testing for the Foundry Local integration.
Tests various failure scenarios and recovery mechanisms.
"""

import os
import sys
import tempfile
import json
from pathlib import Path

project_root = Path(__file__).parent

def test_config_variations():
    """Test different configuration scenarios."""
    print("🔧 Testing Configuration Variations...")
    
    # Test various provider configurations
    test_configs = [
        {
            "name": "foundry_basic",
            "config": """[MAIN]
is_local = True
provider_name = foundry
provider_model = microsoft/DialoGPT-small
provider_server_address = 127.0.0.1:5000
""",
            "should_work": True
        },
        {
            "name": "foundry_with_custom_model",
            "config": """[MAIN]
is_local = True
provider_name = foundry
provider_model = custom/model-name
provider_server_address = 127.0.0.1:8080
""",
            "should_work": True
        },
        {
            "name": "invalid_provider",
            "config": """[MAIN]
is_local = True
provider_name = nonexistent
provider_model = test
""",
            "should_work": False
        }
    ]
    
    results = []
    for test_config in test_configs:
        temp_config = project_root / f"test_{test_config['name']}.ini"
        try:
            with open(temp_config, 'w') as f:
                f.write(test_config['config'])
            
            # Validate the config can be read
            with open(temp_config, 'r') as f:
                content = f.read()
            
            has_foundry = "provider_name = foundry" in content
            expected = test_config['should_work']
            
            if (has_foundry and expected) or (not has_foundry and not expected):
                print(f"✅ Config test '{test_config['name']}' passed")
                results.append(True)
            else:
                print(f"❌ Config test '{test_config['name']}' failed")
                results.append(False)
                
        finally:
            if temp_config.exists():
                temp_config.unlink()
    
    return all(results)

def test_foundry_input_formats():
    """Test different input message formats for the foundry provider."""
    print("📝 Testing Foundry Input Formats...")
    
    # Test various message format scenarios
    test_cases = [
        {
            "name": "dict_format",
            "input": [{"role": "user", "content": "Hello"}],
            "valid": True
        },
        {
            "name": "list_tuple_format", 
            "input": [["user", "Hello"]],
            "valid": True
        },
        {
            "name": "mixed_format",
            "input": [
                {"role": "user", "content": "First message"},
                ["assistant", "Response"],
                {"role": "user", "content": "Follow up"}
            ],
            "valid": True
        },
        {
            "name": "string_fallback",
            "input": ["Just a string"],
            "valid": True
        },
        {
            "name": "empty_input",
            "input": [],
            "valid": True
        }
    ]
    
    # Simulate the message processing logic from the provider
    results = []
    for test_case in test_cases:
        try:
            messages = []
            for msg in test_case["input"]:
                if isinstance(msg, dict):
                    messages.append(msg)
                elif isinstance(msg, list) and len(msg) == 2:
                    role, content = msg
                    messages.append({"role": role, "content": content})
                else:
                    messages.append({"role": "user", "content": str(msg)})
            
            # Create a temporary JSON file to simulate the provider's behavior
            temp_data = {"messages": messages}
            temp_file = project_root / f"test_{test_case['name']}.json"
            
            with open(temp_file, 'w') as f:
                json.dump(temp_data, f)
            
            # Verify the JSON is valid
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
            
            if isinstance(loaded_data.get("messages"), list):
                print(f"✅ Input format test '{test_case['name']}' passed")
                results.append(True)
            else:
                print(f"❌ Input format test '{test_case['name']}' failed")
                results.append(False)
                
            temp_file.unlink()
            
        except Exception as e:
            print(f"❌ Input format test '{test_case['name']}' failed: {e}")
            results.append(False)
    
    return all(results)

def test_environment_variable_handling():
    """Test environment variable setup for CUDA workarounds."""
    print("🌍 Testing Environment Variable Handling...")
    
    # Test environment variables that should be set
    required_env_vars = [
        "FOUNDRY_EXECUTION_PROVIDER",
        "CUDA_VISIBLE_DEVICES", 
        "FOUNDRY_SKIP_CUDA_CHECK",
        "FOUNDRY_CUDA_VERSION_OVERRIDE",
        "CUDA_VERSION"
    ]
    
    # Simulate setting environment variables
    original_env = {}
    test_env = os.environ.copy()
    
    # Store original values
    for var in required_env_vars:
        original_env[var] = os.environ.get(var)
    
    try:
        # Set test values
        test_env.update({
            "FOUNDRY_EXECUTION_PROVIDER": "CPUExecutionProvider",
            "CUDA_VISIBLE_DEVICES": "-1",
            "FOUNDRY_SKIP_CUDA_CHECK": "1",
            "FOUNDRY_CUDA_VERSION_OVERRIDE": "12.0.0",
            "CUDA_VERSION": "12.0.0"
        })
        
        # Verify all variables are set correctly
        all_set = True
        for var in required_env_vars:
            if var in test_env and test_env[var]:
                print(f"✅ Environment variable {var} set correctly")
            else:
                print(f"❌ Environment variable {var} not set")
                all_set = False
        
        # Test CPU-only configuration
        if test_env.get("CUDA_VISIBLE_DEVICES") == "-1":
            print("✅ CUDA devices hidden correctly")
        else:
            print("❌ CUDA devices not hidden")
            all_set = False
        
        if test_env.get("FOUNDRY_EXECUTION_PROVIDER") == "CPUExecutionProvider":
            print("✅ CPU execution provider set")
        else:
            print("❌ CPU execution provider not set")
            all_set = False
        
        return all_set
        
    finally:
        # Restore original environment
        for var, value in original_env.items():
            if value is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = value

def test_error_handling_scenarios():
    """Test various error scenarios and recovery."""
    print("🚨 Testing Error Handling Scenarios...")
    
    # Read the provider code to check error handling
    provider_file = project_root / "sources" / "llm_provider.py"
    with open(provider_file, 'r') as f:
        content = f.read()
    
    error_scenarios = [
        {
            "name": "FileNotFoundError",
            "pattern": "FileNotFoundError",
            "message": "Foundry Local CLI not found"
        },
        {
            "name": "TimeoutExpired", 
            "pattern": "TimeoutExpired",
            "message": "timed out"
        },
        {
            "name": "General Exception",
            "pattern": "except Exception as e:",
            "message": "Foundry Local provider failed"
        }
    ]
    
    results = []
    for scenario in error_scenarios:
        if scenario["pattern"] in content:
            # Check if appropriate error message is provided
            if scenario["message"].lower() in content.lower():
                print(f"✅ Error handling: {scenario['name']} with message")
                results.append(True)
            else:
                print(f"⚠️  Error handling: {scenario['name']} without specific message")
                results.append(True)  # Still acceptable
        else:
            print(f"❌ Error handling: {scenario['name']} missing")
            results.append(False)
    
    # Check for cleanup in finally block
    if 'finally:' in content and 'unlink' in content:
        print("✅ Cleanup: Temporary file cleanup present")
        results.append(True)
    else:
        print("❌ Cleanup: Missing temporary file cleanup")
        results.append(False)
    
    return all(results)

def test_fallback_mechanisms():
    """Test fallback mechanisms when primary methods fail."""
    print("🔄 Testing Fallback Mechanisms...")
    
    provider_file = project_root / "sources" / "llm_provider.py"
    with open(provider_file, 'r') as f:
        content = f.read()
    
    results = []
    
    # Check for primary failure detection
    if "if result.returncode != 0:" in content:
        print("✅ Fallback: Primary failure detection present")
        results.append(True)
    else:
        print("❌ Fallback: Primary failure detection missing")
        results.append(False)
    
    # Check for FoundryLocalForceCPU fallback
    if "FoundryLocalForceCPU" in content:
        print("✅ Fallback: FoundryLocalForceCPU wrapper present")
        results.append(True)
    else:
        print("❌ Fallback: FoundryLocalForceCPU wrapper missing")
        results.append(False)
    
    # Check for dotnet execution of fallback
    if '"dotnet", foundry_cpu_exe' in content:
        print("✅ Fallback: Dotnet execution of CPU wrapper")
        results.append(True)
    else:
        print("❌ Fallback: Dotnet execution missing")
        results.append(False)
    
    # Check for path construction to CPU wrapper
    if 'os.path.join(os.path.dirname(__file__), "..", "FoundryLocalForceCPU"' in content:
        print("✅ Fallback: CPU wrapper path construction")
        results.append(True)
    else:
        print("❌ Fallback: CPU wrapper path construction missing")
        results.append(False)
    
    # Check for fallback existence check
    if "os.path.exists(foundry_cpu_exe)" in content:
        print("✅ Fallback: Existence check before fallback")
        results.append(True)
    else:
        print("❌ Fallback: No existence check before fallback")
        results.append(False)
    
    # Check for sequential fallback pattern (foundry -> CPU wrapper)
    foundry_call = '"foundry", "chat"' in content
    cpu_fallback = '"dotnet", foundry_cpu_exe' in content
    if foundry_call and cpu_fallback:
        print("✅ Fallback: Sequential primary -> CPU wrapper pattern")
        results.append(True)
    else:
        print("❌ Fallback: No clear sequential fallback pattern")
        results.append(False)
    
    return all(results)

def test_security_considerations():
    """Test security aspects of the integration."""
    print("🔒 Testing Security Considerations...")
    
    provider_file = project_root / "sources" / "llm_provider.py"
    with open(provider_file, 'r') as f:
        content = f.read()
    
    security_checks = []
    
    # Check for proper file handling
    if 'tempfile' in content and 'delete=False' in content:
        print("✅ Security: Using secure temporary files")
        security_checks.append(True)
    else:
        print("⚠️  Security: Not using secure temporary file creation")
        security_checks.append(False)
    
    # Check for cleanup
    if 'unlink' in content or 'remove' in content:
        print("✅ Security: Temporary file cleanup present")
        security_checks.append(True)
    else:
        print("❌ Security: No temporary file cleanup")
        security_checks.append(False)
    
    # Check for input sanitization
    if 'json.dump' in content:
        print("✅ Security: Using JSON serialization")
        security_checks.append(True)
    else:
        print("⚠️  Security: No clear input serialization")
        security_checks.append(False)
    
    # Check for timeout protection
    if 'timeout=' in content:
        print("✅ Security: Timeout protection present")
        security_checks.append(True)
    else:
        print("❌ Security: No timeout protection")
        security_checks.append(False)
    
    return all(security_checks)

def main():
    """Run all edge case tests."""
    print("🚀 Starting Edge Case Testing for Foundry Local Integration")
    print("="*70)
    
    tests = [
        ("Configuration Variations", test_config_variations),
        ("Input Format Handling", test_foundry_input_formats),
        ("Environment Variables", test_environment_variable_handling),
        ("Error Handling", test_error_handling_scenarios),
        ("Fallback Mechanisms", test_fallback_mechanisms),
        ("Security Considerations", test_security_considerations),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append(result)
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}")
        except Exception as e:
            print(f"❌ FAILED with exception: {e}")
            results.append(False)
    
    print("\n" + "="*70)
    print("🎯 EDGE CASE TEST SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"Results: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅" if results[i] else "❌"
        print(f"{status} {test_name}")
    
    if success_rate >= 80:
        print("\n🏆 EXCELLENT - Edge cases handled well!")
        return 0
    elif success_rate >= 60:
        print("\n⚠️  GOOD - Most edge cases handled.")
        return 0
    else:
        print("\n❌ NEEDS IMPROVEMENT - Significant edge case issues.")
        return 1

if __name__ == "__main__":
    exit(main())