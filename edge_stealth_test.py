#!/usr/bin/env python3
"""Test Edge WebDriver with updated stealth logic"""

from sources.browser import create_driver

print("Testing Edge WebDriver...")

try:
    # Test without stealth mode
    print("1. Testing without stealth mode...")
    driver = create_driver(headless=True, stealth_mode=False)
    print("✅ Driver created successfully (no stealth)")
    driver.get("https://www.example.com")
    print(f"✅ Navigated to: {driver.title}")
    driver.quit()
    print("✅ Driver closed successfully")
    
    # Test with stealth mode
    print("\n2. Testing with stealth mode...")
    driver = create_driver(headless=True, stealth_mode=True)
    print("✅ Driver created successfully (with stealth)")
    driver.get("https://www.example.com")
    print(f"✅ Navigated to: {driver.title}")
    driver.quit()
    print("✅ Driver closed successfully")
    
    print("\n🎉 All Edge WebDriver tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
