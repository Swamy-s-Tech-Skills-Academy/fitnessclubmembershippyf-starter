# 🚀 Pre-Sprint Setup & Verification Guide

## 📋 Quick Setup Commands (First Time Setup)

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create basic project structure (if needed)
mkdir -p src/templates src/static src/instance tests

# 5. Test basic setup
pytest tests\test_home.py -v
```

## 🧪 **PRE-SPRINT VERIFICATION CHECKLIST**

**Run these commands to verify your setup before starting Sprint 1:**

### **Step 1: Activate Virtual Environment**

```bash
# Navigate to project root
cd "d:\STSA\fitnessclubmembershippyf-starter"

# Activate virtual environment
.venv\Scripts\activate

# Verify you see (.venv) in your prompt
```

### **Step 2: Verify Python Environment**

```bash
# Check Python version (should be 3.12.5)
python --version

# List installed packages (should show 25+ packages)
pip list

# Verify Flask is installed
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

### **Step 3: Run Automated Tests**

```bash
# Run pytest validation (should pass 2/2 tests)
pytest tests\test_home.py -v

# Expected output:
# tests/test_home.py::test_home_page PASSED [ 50%]
# tests/test_home.py::test_flask_app_running PASSED [100%]
# ============ 2 passed in 0.XX s ============
```

### **Step 4: Test Flask Application**

```bash
# Start Flask development server (run in background or new terminal)
cd src
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### **Step 5: Verify HTTP Response (New Terminal)**

```bash
# In a new terminal, activate environment and test HTTP response
cd "d:\STSA\fitnessclubmembershippyf-starter"
.venv\Scripts\activate

# Test HTTP request
python -c "import requests; response = requests.get('http://127.0.0.1:5000'); print(f'Status: {response.status_code}'); print('Success!' if 'Welcome to Fitness Club' in response.text else 'Failed!')"

# Expected output:
# Status: 200
# Success!
```

### **Step 6: Verify Project Structure**

```bash
# Check project structure
Get-ChildItem -Recurse src, tests | Select-Object FullName

# Expected structure:
# src\app.py ✅
# src\templates\index.html ✅
# tests\test_home.py ✅
```

### **Step 7: Manual Browser Test**

- Open browser to `http://127.0.0.1:5000`
- Verify you see: **"🏋️‍♂️ Welcome to Fitness Club"**
- Verify page loads with Tailwind CSS styling

---

**✅ ALL CHECKS PASSED?** → **Ready for Sprint 1!**  
**❌ ANY FAILURES?** → **Review setup steps and fix issues**

---

## Daily Development Workflow

```bash
# 1. Activate environment (every new terminal session)
.venv\Scripts\activate

# 2. Navigate to appropriate folder
cd src          # For running the app
cd tests        # For running tests

# 3. Run the application
python app.py   # Starts server on localhost:5000

# 4. Run tests (from project root)
python tests/manual_test_sprint1.py
```

## Project Structure Reference

```
fittnessclubmembershippyf/     # Always start here
├── README.md               # Main documentation
├── requirements.txt        # Dependencies (install from here)
├── .venv/                  # Virtual environment
├── src/                   # Source code (run app.py from here)
├── tests/                 # Tests (run tests from here)
└── docs/                  # Documentation
```

## Troubleshooting

**Virtual Environment Issues:**

- Ensure you're in project root when creating venv
- Always activate before installing packages
- Look for `(.venv)` in terminal prompt

**Import Errors:**

- Check you're in correct directory (src/ for app, tests/ for tests)
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

**Database Issues:**

- Delete `src/instance/fitness_club.db` and re-run `init_db.py`
- Check file permissions

**Port 5000 in Use:**

- Change port in app.py: `app.run(port=5001)`
- Or kill process using port: `netstat -ano | findstr :5000`

## Success Indicators

- ✅ `(.venv)` appears in terminal prompt
- ✅ `pip list` shows Flask and dependencies
- ✅ Database file exists: `src/instance/fitness_club.db`
- ✅ App starts without errors
- ✅ Browser shows dashboard at localhost:5000
- ✅ Tests pass without failures
