# 🎨 Sprint 2: Frontend Templates (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 2**

```text
Create a complete responsive frontend for the fitness club system using Tailwind CSS:

PREREQUISITE: Verify Sprint 1 backend is working with all required model properties:
- member.full_name, member.age, member.current_plans
- plan.price, plan.duration_months
- session.duration_minutes, session.available_spots, session.bookings
- All routes: /, /members, /members/create, /members/<id>, /members/<id>/edit, /plans, /sessions, /sessions/schedule

TEMPLATES NEEDED (must use exact model properties):
1. base.html - Navigation with Tailwind, responsive design, footer
2. index.html - Dashboard with 8 key metrics using stats object
3. members/list.html - Member list using member.full_name, member.status, pagination
4. members/create.html - Registration form posting to /members/create
5. members/detail.html - Member profile using member.age, member.current_plans
6. plans/list.html - Plans using plan.name, plan.price, plan.description
7. sessions/list.html - Sessions using session.title, session.duration_minutes, session.available_spots
8. sessions/schedule.html - Session form posting to /sessions/schedule

CRITICAL TEMPLATE REQUIREMENTS:
- Use ONLY existing model properties (member.full_name NOT member.name)
- Use plan.price NOT plan.monthly_price in templates
- Use session.duration_minutes for display
- Link to /members/<id>/edit (route must exist from Sprint 1)
- Forms must have proper name attributes matching model fields
- Include CSRF tokens: {{ csrf_token() }}
- Use url_for() for all internal links

STYLING REQUIREMENTS:
- Mobile-responsive navigation with hamburger menu
- Professional Tailwind CSS (blue/gray theme: primary-600, gray-50)
- Form validation styling with error message display
- Data tables with hover effects and status badges
- Button styling (btn-primary, btn-secondary, btn-danger classes)
- Card layouts for plans and statistics
- Export buttons (prepare for Sprint 3 CSV functionality)
- Progress bars for dashboard analytics
- Professional footer with contact info

NAVIGATION STRUCTURE:
- Logo: "🏋️‍♂️ FitClub"
- Menu: Dashboard, Members, Plans, Sessions
- Mobile hamburger menu for small screens
- Active link highlighting (prepare for Sprint 3)

Use CDN: https://cdn.tailwindcss.com with custom config for primary colors
All forms connect to existing Flask routes from Sprint 1
Include flash message display areas for Sprint 3 notifications
```

## ✅ **VALIDATION COMMANDS**

```bash
# ✅ Verify Sprint 1 backend is complete first
cd src
python app.py
# Test these URLs work: /, /members, /members/create, /plans, /sessions

# ✅ Create templates using exact model properties
# - member.full_name (NOT member.name)
# - plan.price (NOT plan.monthly_price)
# - session.duration_minutes
# - All routes from Sprint 1 must exist

# ✅ Test responsive design
# - Desktop: Full navigation menu
# - Mobile: Hamburger menu
# - Forms: Proper validation styling
# - Tables: Responsive on small screens

# ✅ Validation checklist
# - All 8 templates created
# - Navigation links work (no 404 errors)
# - Forms submit to correct routes
# - Mobile responsiveness verified
# - Tailwind styling applied consistently
```

## 🎯 **EXPECTED DELIVERABLES**

- ✅ 8 professional HTML templates using correct model properties
- ✅ Responsive Tailwind CSS design (mobile-first)
- ✅ Complete navigation system with hamburger menu
- ✅ Forms with validation styling and CSRF tokens
- ✅ Dashboard with analytics layout using stats object
- ✅ All links work (no BuildError exceptions)
- ✅ Ready for Sprint 3 JavaScript integration

## 🚨 **CRITICAL SUCCESS CRITERIA**

- ✅ No template errors (UndefinedError, BuildError)
- ✅ member.full_name displays correctly (not member.name)
- ✅ plan.price shows monetary values (not plan.monthly_price)
- ✅ session.duration_minutes calculates and displays
- ✅ All url_for() calls reference existing routes
- ✅ Mobile responsive design verified
- ✅ Ready for Sprint 3 advanced features integration
