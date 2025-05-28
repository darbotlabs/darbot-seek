#!/usr/bin/env python3
"""Test critical packages"""

import sys
required = ['selenium', 'beautifulsoup4', 'markdownify', 'fake_useragent', 'selenium_stealth', 'undetected_chromedriver']
missing = []

for pkg in required:
    try:
        __import__(pkg.replace('-', '_'))
        print(f"✅ {pkg}")
    except ImportError:
        missing.append(pkg)
        print(f"❌ {pkg}")

if missing:
    print(f'❌ Missing packages: {missing}')
    sys.exit(1)
else:
    print('✅ All critical packages installed')
