#!/usr/bin/env python3
"""Fix syntax issues in browser.py file"""

try:
    with open('sources/browser.py', 'r') as file:
        content = file.read()

    # Fix the syntax issue with the missing newline
    content = content.replace(
        'edgedriver_path = install_edgedriver()    service = Service(edgedriver_path)', 
        'edgedriver_path = install_edgedriver()\n    service = Service(edgedriver_path)'
    )

    # Fix stealth mode section with missing newline
    content = content.replace(
        'edge_options.add_argument("--disable-blink-features=AutomationControlled")        driver = create_undetected_edgedriver', 
        'edge_options.add_argument("--disable-blink-features=AutomationControlled")\n        driver = create_undetected_edgedriver'
    )

    # Remove stealth() call that doesn't support Edge
    content = content.replace(
        'edge_version = driver.capabilities[\'browserVersion\']\n        stealth(driver,', 
        'edge_version = driver.capabilities[\'browserVersion\']\n        # Note: selenium_stealth doesn\'t support Edge, so we use manual stealth configurations\n        # stealth(driver,'
    )

    # Comment out the stealth parameters
    content = content.replace(
        'languages=["en-US", "en"],\n            vendor=user_agent["vendor"],\n            platform="Win64" if "windows" in user_agent["ua"].lower() else "MacIntel" if "mac" in user_agent["ua"].lower() else "Linux x86_64",\n            webgl_vendor="Intel Inc.",\n            renderer="Intel Iris OpenGL Engine",\n            fix_hairline=True,\n        )',
        '# languages=["en-US", "en"],\n            # vendor=user_agent["vendor"],\n            # platform="Win64" if "windows" in user_agent["ua"].lower() else "MacIntel" if "mac" in user_agent["ua"].lower() else "Linux x86_64",\n            # webgl_vendor="Intel Inc.",\n            # renderer="Intel Iris OpenGL Engine",\n            # fix_hairline=True,\n        # )'
    )

    with open('sources/browser.py', 'w') as file:
        file.write(content)
    print('Fixed browser.py syntax issues')
    
except Exception as e:
    print(f'Error: {str(e)}')
