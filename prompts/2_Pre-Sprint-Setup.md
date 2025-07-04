# 🚀 Pre-Sprint Setup: Environment & Dependencies

## 🎯 **COPY-PASTE PROMPT FOR PRE-SPRINT**

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
- src/instance/ (database files - ensure this exists to prevent database path issues)

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

Optional Production/Development:
- gunicorn==21.2.0
- python-dotenv==1.0.0

FRONTEND STYLING:
- TailwindCSS via CDN (no installation required)
- CDN URL: https://cdn.tailwindcss.com
- Font Awesome via CDN (icons and graphics)
- CDN URL: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css
- Google Fonts (Inter & Poppins)
- CDN URL: https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap

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

# ✅ Create .gitignore for clean repository (early setup)
cat <<EOF > .gitignore
.venv/
__pycache__/
*.pyc
instance/
.env
*.db
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
    <!-- TailwindCSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-poppins { font-family: 'Poppins', sans-serif; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <div class="mb-6">
            <i class="fas fa-dumbbell text-6xl text-blue-600 mb-4"></i>
        </div>
        <h1 class="text-6xl font-bold text-blue-600 mb-4 font-poppins">Welcome to Fitness Club</h1>
        <p class="text-xl text-gray-600 mb-6">Your fitness journey starts here!</p>
        <div class="flex justify-center gap-4 mb-8">
            <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-users text-blue-500"></i>
                <span>Members</span>
            </div>
            <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-calendar-alt text-green-500"></i>
                <span>Bookings</span>
            </div>
            <div class="flex items-center gap-2 text-gray-700">
                <i class="fas fa-chart-line text-purple-500"></i>
                <span>Analytics</span>
            </div>
        </div>
        <div class="mt-8">
            <span class="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium">
                <i class="fas fa-check-circle mr-2"></i>Flask App Running Successfully
            </span>
        </div>
    </div>
</body>
</html>
EOF

# ✅ Create Copilot configuration for better assistance
mkdir -p .copilot
cat <<EOF > .copilot/settings.json
{
  "projectType": "flask",
  "useVirtualEnv": true,
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

# Optional: Production Deployment
gunicorn==21.2.0

# Optional: Development Tools
python-dotenv==1.0.0
EOF
```

## 🎨 **FRONTEND STYLING SETUP**

**No Installation Required!** - Using CDN approach for rapid development:

```html
<!-- Add these to your base.html template <head> section -->

<!-- TailwindCSS CDN -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Font Awesome CDN -->
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
/>

<!-- Google Fonts -->
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

**Benefits of CDN approach:**

- ✅ No build process required
- ✅ Instant setup for rapid prototyping
- ✅ Perfect for live coding demonstrations
- ✅ All styling resources available immediately
- ✅ Professional typography with Google Fonts
- ✅ Rich icon library with Font Awesome

**Available Resources:**

- **TailwindCSS**: Complete utility-first CSS framework
- **Font Awesome**: 1,000+ icons for UI elements
- **Inter Font**: Clean, readable body text
- **Poppins Font**: Modern headings and display text

**Note:** For production deployment, consider using build tools for optimized assets.

## ✅ **VALIDATION COMMANDS**

```bash
# Activate virtual environment
.venv\Scripts\activate
cd src
python app.py
# Visit http://localhost:5000 - should show welcome page
```

## 🎯 **EXPECTED DELIVERABLES**

- ✅ Virtual environment created and activated
- ✅ All dependencies installed
- ✅ Project folder structure created
- ✅ Basic Flask app with welcome page
- ✅ HTTP responses working

## 🧪 **PRE-SPRINT VERIFICATION CHECKLIST**

**If the setup is already complete, run these commands to verify everything is working:**

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
# Check Python version
python --version

# List installed packages (should show Flask, SQLAlchemy, etc.)
pip list

# Verify Flask is installed
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

### **Step 3: Test Flask Application**

```bash
# Start Flask development server
cd src
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### **Step 4: Verify Project Structure**

```bash
# Check project structure exists
Get-ChildItem -Recurse src | Select-Object FullName

# Expected structure:
# src\app.py ✅
# src\templates\index.html ✅
```

### **Step 5: Manual Browser Test**

- Open browser to `http://127.0.0.1:5000`
- Verify you see: **"Welcome to Fitness Club"**
- Verify page loads with Tailwind CSS styling (blue header, centered layout)

### **Step 6: Final Completion Check**

```bash
# Simple completion validation
python -c "print('🎯 PRE-SPRINT COMPLETION CHECK'); print('=' * 40); print('✅ Virtual Environment: Active'); print('✅ Flask App: Running'); print('✅ Dependencies: Installed'); print('✅ Project Structure: Complete'); print('✅ HTTP Validation: Working'); print('=' * 40); print('🚀 READY FOR SPRINT 1!')"

# Expected output:
# 🎯 PRE-SPRINT COMPLETION CHECK
# ========================================
# ✅ Virtual Environment: Active
# ✅ Flask App: Running
# ✅ Dependencies: Installed
# ✅ Project Structure: Complete
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
- **Live Demo Guide:** [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - Complete presentation guide

## 🤖 **COPILOT AGENT COMPATIBILITY**

This setup is optimized for Copilot Agent execution:

- ✅ Uses `cat <<EOF` for better multiline file creation
- ✅ Cross-platform commands (Windows/macOS/Linux)
- ✅ Comment headers for clear bash block identification
- ✅ Scriptable commands with clear separation
- ✅ Includes .gitignore for clean repository
- ✅ Copilot configuration for contextual assistance
- ✅ No ambiguous shell syntax
- ✅ Development-focused workflow

## � **IMPORTANT NOTES FOR SPRINT 1**

**Database Configuration:** The `src/instance/` folder created during setup is crucial for Sprint 1 database initialization. Sprint 1 will use absolute paths to prevent "unable to open database file" errors.

## �📚 **QUICK ACCESS TO OTHER PROMPTS**

- [3_Sprint1-Backend.md](3_Sprint1-Backend.md) - 🛠 Backend Development
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

**Styling Resources Note**: The welcome template already includes TailwindCSS CDN, Font Awesome icons, and Google Fonts, so you'll see professional styling immediately!
