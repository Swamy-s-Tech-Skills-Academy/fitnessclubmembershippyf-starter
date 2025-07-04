# 🚀 Pre-Sprint Setup: Environment & Dependencies

## 🎯 **COPY-PASTE PROMPT FOR PRE-SPRINT**

```text
Set up the development environment for a Flask fitness club membership system:

STARTER PROJECT INCLUDES:
✅ requirements.txt - All Python dependencies with specific versions
✅ .gitignore - Python/Flask optimized ignore rules
✅ .copilot/settings.json - GitHub Copilot configuration
✅ .github/copilot-instructions.md - Copilot Agent instructions
✅ docs/ folder - Documentation and images
✅ prompts/ folder - All sprint .md files with copy-paste prompts
✅ LICENSE - Project license
✅ README.md - Project documentation

SETUP TASKS:
1. Create virtual environment (.venv)
2. Install dependencies from provided requirements.txt
3. Create src/ folder structure
4. Set up basic Flask app with welcome home page

FOLDERS TO CREATE:
- src\ (main application code)
- src\templates\ (HTML templates)
- src\static\ (CSS, JS, images)
- src\instance\ (database files - ensure this exists to prevent database path issues)

DEPENDENCIES (already defined in requirements.txt):

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

✅ All configuration files are included in the starter project - no manual creation needed!
```

## 🏠 **CREATE BASIC WELCOME HOME PAGE**

### **PowerShell File Creation Commands:**

```powershell
# ✅ Create basic Flask app (src\app.py)
@"
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"@ | Out-File -FilePath "src\app.py" -Encoding UTF8

# ✅ Create welcome template (src\templates\index.html)
@"
<!DOCTYPE html>
<html lang=`"en`">
<head>
    <meta charset=`"UTF-8`">
    <meta name=`"viewport`" content=`"width=device-width, initial-scale=1.0`">
    <title>Fitness Club Membership System</title>
    <!-- TailwindCSS CDN -->
    <script src=`"https://cdn.tailwindcss.com`"></script>
    <!-- Font Awesome CDN -->
    <link rel=`"stylesheet`" href=`"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`">
    <!-- Google Fonts -->
    <link href=`"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap`" rel=`"stylesheet`">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-poppins { font-family: 'Poppins', sans-serif; }
    </style>
</head>
<body class=`"bg-gray-100 min-h-screen flex items-center justify-center`">
    <div class=`"text-center`">
        <div class=`"mb-6`">
            <i class=`"fas fa-dumbbell text-6xl text-blue-600 mb-4`"></i>
        </div>
        <h1 class=`"text-6xl font-bold text-blue-600 mb-4 font-poppins`">Welcome to Fitness Club</h1>
        <p class=`"text-xl text-gray-600 mb-6`">Your fitness journey starts here!</p>
        <div class=`"flex justify-center gap-4 mb-8`">
            <div class=`"flex items-center gap-2 text-gray-700`">
                <i class=`"fas fa-users text-blue-500`"></i>
                <span>Members</span>
            </div>
            <div class=`"flex items-center gap-2 text-gray-700`">
                <i class=`"fas fa-calendar-alt text-green-500`"></i>
                <span>Bookings</span>
            </div>
            <div class=`"flex items-center gap-2 text-gray-700`">
                <i class=`"fas fa-chart-line text-purple-500`"></i>
                <span>Analytics</span>
            </div>
        </div>
        <div class=`"mt-8`">
            <span class=`"inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium`">
                <i class=`"fas fa-check-circle mr-2`"></i>Flask App Running Successfully
            </span>
        </div>
    </div>
</body>
</html>
"@ | Out-File -FilePath "src\templates\index.html" -Encoding UTF8
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

## 🎯 **EXPECTED DELIVERABLES**

- ✅ Virtual environment created and activated
- ✅ All Flask dependencies installed (Flask, SQLAlchemy, Flask-WTF, etc.)
- ✅ Project folder structure created (src\, templates\, static\, instance\)
- ✅ Basic Flask app with professional welcome page
- ✅ CDN resources integrated (Tailwind CSS, Font Awesome, Google Fonts)
- ✅ HTTP responses working and styled content visible

## 🧪 **PRE-SPRINT VERIFICATION CHECKLIST**

**Manual verification steps for the user to confirm setup is working:**

### **Step 1: Activate Virtual Environment**

```powershell
# Navigate to your project root directory
Set-Location "path\to\your\project"

# Activate virtual environment (PowerShell)
.venv\Scripts\activate

# Verify you see (.venv) in your prompt
```

### **Step 2: Verify Python Environment**

```powershell
# Check Python version
python --version

# List installed packages (should show Flask, SQLAlchemy, etc.)
pip list

# Verify Flask is installed
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

### **Step 3: Test Flask Application**

```powershell
# Start Flask development server
Set-Location src
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### **Step 4: Verify Project Structure**

```powershell
# Check project structure exists (PowerShell)
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

```powershell
# Simple completion validation (PowerShell)
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

This setup is optimized for Copilot Agent execution on Windows:

- ✅ Uses PowerShell `@"..."@` syntax for better multiline file creation
- ✅ Windows-specific PowerShell commands
- ✅ Comment headers for clear PowerShell block identification
- ✅ Scriptable commands with Windows path separators (\)
- ✅ .gitignore already included in starter project
- ✅ Copilot configuration already included in starter project
- ✅ No Unix-specific shell syntax
- ✅ Development-focused workflow optimized for Windows 11

## � **IMPORTANT NOTES FOR SPRINT 1**

**Database Configuration:** The `src\instance\` folder created during setup is crucial for Sprint 1 database initialization. Sprint 1 will use absolute paths to prevent "unable to open database file" errors.

## �📚 **QUICK ACCESS TO OTHER PROMPTS**

- [3_Sprint1-Backend.md](3_Sprint1-Backend.md) - 🛠 Backend Development
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

**Styling Resources Note**: The welcome template already includes TailwindCSS CDN, Font Awesome icons, and Google Fonts, so you'll see professional styling immediately!
