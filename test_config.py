#!/usr/bin/env python3
"""Test config.ini validation"""

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

required_sections = ['MAIN', 'BROWSER']
required_main = ['is_local', 'provider_name', 'provider_model']
missing = []

for section in required_sections:
    if section not in config:
        missing.append(f'Section [{section}]')

for key in required_main:
    if key not in config['MAIN']:
        missing.append(f'Key {key} in [MAIN]')

if missing:
    print(f'❌ Missing config: {missing}')
else:
    print('✅ Config valid')
