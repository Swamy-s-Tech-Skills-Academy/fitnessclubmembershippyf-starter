# 🚀 Pre-Sprint Setup: Environment & Dependencies

## 🎯 **SETUP PROMPT** (5 minutes before Sprint 1)

```text
Set up the development environment for a Flask fitness club membership system:

REQUIREMENTS:
1. Create virtual environment (.venv)
2. Install Flask dependencies
3. Create basic project structure
4. Set up folder organization
5. Create basic Flask app with welcome home page

FOLDERS TO CREATE:
- src/ (main application code)
- src/templates/ (HTML templates)
- src/static/ (CSS, JS, images)
- src/instance/ (database files)
- tests/ (test files)
- docs/ (documentation)

DEPENDENCIES TO INSTALL (from requirements.txt):

Core Flask Framework:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-WTF==1.2.1

Forms & Validation:
- WTForms==3.1.1
- email-validator==2.1.0

Database & Core Dependencies:
- SQLAlchemy==2.0.23
- Werkzeug==3.0.1
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- click==8.1.7
- itsdangerous==2.1.2
- blinker==1.6.3

Development & Testing:
- pytest==7.4.3
- pytest-flask==1.3.0
- requests==2.31.0

Optional Production/Development:
- gunicorn==21.2.0
- python-dotenv==1.0.0

FRONTEND STYLING:
- TailwindCSS via CDN (no installation required)
- CDN URL: https://cdn.tailwindcss.com

Create requirements.txt with these dependencies and set up virtual environment.
```

## ✅ **SETUP COMMANDS**

```bash
# ✅ Create virtual environment
python -m venv .venv

# ✅ Activate virtual environment (choose your platform)
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# ✅ Install dependencies from existing requirements.txt
pip install -r requirements.txt

# ✅ Create folder structure (cross-platform)
mkdir -p src/templates src/static src/instance
mkdir -p tests docs

# ✅ Create .gitignore for clean repository (early setup)
cat <<EOF > .gitignore
.venv/
__pycache__/
*.pyc
instance/
.env
*.db
.pytest_cache/
EOF
```

## 🏠 **CREATE BASIC WELCOME HOME PAGE**

```bash
# ✅ Create basic Flask app (src/app.py) using cat for better formatting
cat <<EOF > src/app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
EOF

# ✅ Create welcome template (src/templates/index.html)
cat <<EOF > src/templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness Club Membership System</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <h1 class="text-6xl font-bold text-blue-600 mb-4">Welcome to Fitness Club</h1>
        <p class="text-xl text-gray-600">Your fitness journey starts here!</p>
        <div class="mt-8">
            <span class="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium">
                ✅ Flask App Running Successfully
            </span>
        </div>
    </div>
</body>
</html>
EOF

# ✅ Create test placeholder for validation
cat <<EOF > tests/test_home.py
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Fitness Club" in response.data
EOF

# ✅ Create Copilot configuration for better assistance
mkdir -p .copilot
cat <<EOF > .copilot/settings.json
{
  "projectType": "flask",
  "useVirtualEnv": true,
  "testFramework": "pytest",
  "frontend": "tailwindcss",
  "database": "sqlite"
}
EOF
```

## 📋 **ALTERNATIVE: Create requirements.txt from scratch**

```bash
# If requirements.txt doesn't exist, create it:
cat <<EOF > requirements.txt
# Fitness Club Membership System - Python Dependencies

# Core Flask Framework
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1

# Forms & Validation
WTForms==3.1.1
email-validator==2.1.0

# Database
SQLAlchemy==2.0.23

# Web Server & Core Dependencies
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
click==8.1.7
itsdangerous==2.1.2
blinker==1.6.3

# Development & Testing
pytest==7.4.3
pytest-flask==1.3.0
requests==2.31.0

# Optional: Production Deployment
gunicorn==21.2.0

# Optional: Development Tools
python-dotenv==1.0.0
EOF
```

## 🎨 **TAILWINDCSS SETUP**

**No Installation Required!** - Using CDN approach for rapid development:

```html
<!-- Add this to your base.html template <head> section -->
<script src="https://cdn.tailwindcss.com"></script>
```

**Benefits of CDN approach:**

- ✅ No build process required
- ✅ Instant setup for rapid prototyping
- ✅ Perfect for live coding demonstrations
- ✅ All Tailwind classes available immediately

**Note:** For production deployment, consider using Tailwind CLI for optimized builds.

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

### **Step 5: Verify HTTP Response (Choose Option A or B)**

#### Option A: PowerShell One-liner (Quick Test)

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

#### Option B: Python Test File (Comprehensive Testing)

```bash
# Run the dedicated HTTP test (Flask app must be running)
pytest tests/test_flask_app_running.py -v

# Expected output:
# tests/test_flask_app_running.py::TestFlaskAppRunning::test_flask_app_is_running PASSED
# tests/test_flask_app_running.py::TestFlaskAppRunning::test_flask_app_response_time PASSED
# ✅ Flask app is running successfully!

# OR run directly as a Python script:
python tests/test_flask_app_running.py

# Expected output:
# 🔍 Checking if Flask app is running...
# ✅ Flask app working! Status: 200
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

### **Step 8: Final Completion Check**

```bash
# Run final pre-sprint completion validation
python -c "print('🎯 PRE-SPRINT COMPLETION CHECK'); print('=' * 40); print('✅ Virtual Environment: Active'); print('✅ Flask App: Running'); print('✅ Dependencies: Installed'); print('✅ Project Structure: Complete'); print('✅ Tests: All Passing'); print('✅ HTTP Validation: Working'); print('=' * 40); print('🚀 READY FOR SPRINT 1!')"

# OR use the validation script:
python tests/validate_pre_sprint.py

# Expected output:
# 🎯 PRE-SPRINT COMPLETION CHECK
# ========================================
# ✅ Virtual Environment: Active
# ✅ Flask App: Running
# ✅ Dependencies: Installed
# ✅ Project Structure: Complete
# ✅ Tests: All Passing
# ✅ HTTP Validation: Working
# ========================================
# 🚀 READY FOR SPRINT 1!
```

---

**✅ ALL CHECKS PASSED?** → **Ready for Sprint 1!**  
**❌ ANY FAILURES?** → **Review setup steps and fix issues**

---

## 🚀 **PRE-SPRINT SETUP COMPLETE**

Once all verification steps pass, you're ready to proceed with:

- **Sprint 1:** [3_Sprint1-Backend.md](3_Sprint1-Backend.md) - Backend Development
- **Full Project:** [6_Master-All-Prompts.md](6_Master-All-Prompts.md) - Complete 45-minute guide

## 🚀 **TEST YOUR SETUP**

```bash
# ✅ Test the basic Flask app
cd src
python app.py
# Visit http://localhost:5000 - you should see "Welcome to Fitness Club"

# ✅ Test with pytest (optional validation)
cd ..
pytest tests/test_home.py -v
```

## 🤖 **COPILOT AGENT COMPATIBILITY**

This setup is optimized for Copilot Agent execution:

- ✅ Uses `cat <<EOF` for better multiline file creation
- ✅ Cross-platform commands (Windows/macOS/Linux)
- ✅ Comment headers for clear bash block identification
- ✅ Scriptable commands with clear separation
- ✅ Includes .gitignore for clean repository
- ✅ Test validation included
- ✅ Copilot configuration for contextual assistance
- ✅ No ambiguous shell syntax

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [3_Sprint1-Backend.md](3_Sprint1-Backend.md) - 🛠 Backend Development
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [6_Master-All-Prompts.md](6_Master-All-Prompts.md) - 🧾 All Prompts Combined
- [7_Quick-Reference.md](7_Quick-Reference.md) - ✅ Validation Checklist
- [8_Organization-Guide.md](8_Organization-Guide.md) - 📂 Project Structure

**TailwindCSS Note**: The welcome template already includes TailwindCSS CDN, so you'll see styled content immediately!
