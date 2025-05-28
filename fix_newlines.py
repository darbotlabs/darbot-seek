#!/usr/bin/env python3
"""Fix missing newlines in browser.py file"""

with open('sources/browser.py', 'r', encoding='utf-8') as file:
    content = file.read()

# Fix edgedriver_path and service syntax error
content = content.replace('service = Service(edgedriver_path)    if stealth_mode:', 'service = Service(edgedriver_path)\n    if stealth_mode:')

# Make sure to save the file
with open('sources/browser.py', 'w', encoding='utf-8') as file:
    file.write(content)

print("Fixed syntax issues in browser.py")
