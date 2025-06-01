#!/usr/bin/env python3
"""
Simple test to check if foundry provider exists in the llm_provider.py without importing httpx.
"""

import re
from pathlib import Path

def test_foundry_provider_in_source():
    """Check if foundry provider is properly added to the source code."""
    provider_file = Path("sources/llm_provider.py")
    
    if not provider_file.exists():
        return False, "llm_provider.py not found"
    
    with open(provider_file, 'r') as f:
        content = f.read()
    
    # Check if foundry is in available_providers
    if '"foundry": self.foundry_fn' not in content:
        return False, "foundry not found in available_providers dict"
    
    # Check if foundry_fn method exists
    if 'def foundry_fn(self, history, verbose=False):' not in content:
        return False, "foundry_fn method not found"
    
    # Check if foundry_fn has meaningful implementation
    if 'Use Microsoft Foundry Local to generate text' not in content:
        return False, "foundry_fn implementation seems incomplete"
    
    # Check for CUDA workaround environment variables
    if 'FOUNDRY_EXECUTION_PROVIDER' not in content:
        return False, "CUDA workaround environment variables not found"
    
    return True, "All foundry provider checks passed"

if __name__ == "__main__":
    success, message = test_foundry_provider_in_source()
    print(f"Foundry Provider Test: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"Details: {message}")