from sources.browser import create_driver

print("Testing Edge WebDriver...")
try:
    driver = create_driver(headless=True, stealth_mode=False)
    print("✅ Driver created successfully")
    
    driver.get("https://www.example.com")
    print(f"✅ Navigated to: {driver.title}")
    
    driver.quit()
    print("✅ Driver closed successfully")
except Exception as e:
    print(f"❌ Error: {e}")
