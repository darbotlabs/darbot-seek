# 🎮 AgenticSeek Edge Setup Quest

## Complete Installation & Configuration Adventure

---

### ✅ LEVEL 1: Repository Setup & Environment

- Repository cloned and in correct directory
- Virtual environment created and activated
- .env file exists and is valid
- **Note:** Python version used: 3.13.2 (works, but 3.10.0 is recommended for full compatibility)

---

### ✅ LEVEL 2: Edge WebDriver Installation

- Microsoft Edge installed (version 136.0.3240.92)
- EdgeDriver installed via webdriver-manager
- Edge path detection and driver validation successful

---

### ✅ LEVEL 3: Dependencies Installation

- All critical Python packages installed (see test_packages.py)
- PyAudio skipped due to Python 3.13 incompatibility (not required for browser tests)
- If using Python 3.10, you may install pyaudio with pipwin

---

### ✅ LEVEL 4: Configuration Setup

- config.ini exists and is valid
- SEARXNG_BASE_URL environment variable set

---

### ✅ LEVEL 5: Browser Functionality Test

- test_edge_browser.py runs successfully
- **Edge/stealth fix:**
  - The selenium_stealth library does NOT support Edge. The stealth() call in sources/browser.py must be removed or commented out for Edge support.
  - See sources/browser.py for the correct implementation: do not call stealth() for Edge, just create the driver and proceed.
- Edge WebDriver creates, navigates, and closes with no errors

---

### ⏳ LEVEL 6: Service Setup & Launch

- [ ] Install Ollama (for local LLM)
- [ ] Pull Deepseek model
- [ ] Start Ollama service
- [ ] Start Docker services
- [ ] Validate Ollama, SearxNG, and Redis are running

---

### ⏳ LEVEL 7: Final Integration Test

- [ ] Test CLI mode (python cli.py)
- [ ] Test API mode (python api.py, then curl health endpoint)
- [ ] Test Web Interface ([http://localhost:3000](http://localhost:3000))
- [ ] Run full system test (see quest for script)

---

## Notes for Repeatability

- If you encounter syntax errors in sources/browser.py, check for concatenated statements and remove any stealth() calls for Edge.
- Always run `python -m py_compile sources/browser.py` after editing for syntax validation.
- Use test_edge_browser.py to validate Edge WebDriver functionality after any changes.
- For Python 3.10 users, you may install all dependencies as listed in requirements.txt. For Python 3.13+, skip or manually install only compatible packages.

---

**Progress:**

- Levels 1–5: ✅ Complete and validated
- Levels 6–7: ⏳ To be completed next

---

## Continue with Level 6: Service Setup & Launch