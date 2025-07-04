# 🎨 Sprint 2: Frontend Templates (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 2**

```text
Create a complete responsive frontend for the fitness club system using modern styling:

TEMPLATES NEEDED:
1. base.html - Navigation with Tailwind, responsive design, footer
2. index.html - Dashboard with 8 key metrics (members, sessions, revenue, growth)
3. members/list.html - Member list with search, filters, export button
4. members/create.html - Member registration form with validation
5. members/detail.html - Member profile with plan assignment
6. members/edit.html - Member edit form with validation
7. plans/list.html - Membership plans with pricing cards
8. sessions/list.html - Session list with booking functionality
9. sessions/schedule.html - Session scheduling form

TEMPLATE STRUCTURE:
- All templates should extend base.html using Jinja2 inheritance
- Use consistent block structure: title, content, scripts
- Implement breadcrumb navigation for sub-pages
- Include flash message display for user feedback

STYLING RESOURCES:
- TailwindCSS: https://cdn.tailwindcss.com
- Font Awesome: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css
- Google Fonts: https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap

FEATURES TO INCLUDE:
- Mobile-responsive navigation with hamburger menu
- Professional Tailwind CSS styling (blue/gray theme)
- Font Awesome icons for UI elements
- Google Fonts typography (Inter for body, Poppins for headings)
- Form validation with error messages
- Data tables with hover effects
- Button styling (primary, secondary, danger)
- Card layouts for plans and statistics
- Export functionality (CSV buttons)
- Progress bars for analytics
- Professional footer with contact info

All forms should connect to existing Flask routes
Include proper error handling and success messages
```

## ✅ **VALIDATION COMMANDS**

### **Windows PowerShell:**

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Navigate to src and start application
Set-Location src
python app.py
# Visit <http://localhost:5000> - verify all pages
# Check responsive design on different screen sizes
# Verify forms are styled properly
```

### **Alternative: Command Prompt (cmd):**

```cmd
REM Activate virtual environment
.venv\Scripts\activate.bat

REM Navigate to src and run application
cd src
python app.py
```

## 🎯 **EXPECTED DELIVERABLES**

- ✅ 9 professional HTML templates with Jinja2 inheritance
- ✅ Responsive Tailwind CSS design with Font Awesome icons
- ✅ Complete navigation system with breadcrumbs
- ✅ Forms with client-side validation styling and error display
- ✅ Dashboard with analytics layout and visual metrics
- ✅ Mobile-first responsive design across all templates
- ✅ Professional typography with Google Fonts integration

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🔧 Setup & Environment
- [3_Sprint1-Backend.md](3_Sprint1-Backend.md) - 🛠 Backend Development
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 🎯 **NEXT STEP**

After completing Sprint 2, proceed to: **[5_Sprint3-Integration.md](5_Sprint3-Integration.md)** - Integration & Polish
