#!/usr/bin/env python3
"""Test EdgeDriver installation and functionality"""

try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.edge.options import Options
    
    print("Testing EdgeDriver installation...")
    
    # Install EdgeDriver
    driver_path = EdgeChromiumDriverManager().install()
    print(f"✅ EdgeDriver installed at: {driver_path}")
    
    # Test basic EdgeDriver functionality
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(driver_path)
    
    driver = webdriver.Edge(service=service, options=options)
    print("✅ EdgeDriver created successfully")
    
    driver.get("https://www.example.com")
    print(f"✅ Navigated to: {driver.title}")
    
    driver.quit()
    print("✅ EdgeDriver test completed successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
