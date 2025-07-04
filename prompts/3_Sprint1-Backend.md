# 🏗️ Sprint 1: Backend API Foundation (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 1**

````text
Build Flask backend API endpoints for a fitness club membership system with the following requirements:

PYTHON VERSION REQUIREMENT:
- Python 3.13.5 (ensure compatibility with Flask 3.0.0 and SQLAlchemy 2.0.41 features)

SPRINT 1 FOCUS: BACKEND API ONLY
- Keep the existing welcome page (/) unchanged from pre-sprint setup
- Add JSON API endpoints that return data (no HTML templates)
- NO UI/Templates in Sprint 1 - that's Sprint 2's job
- Focus purely on backend functionality and data structure

APPROACH:
1. Keep existing src\app.py welcome page route (/) unchanged
2. Add new API routes that return JSON responses
3. Use mock data for Sprint 1 (no database required yet)
4. Prepare data structure for Sprint 2 frontend consumption

REQUIRED API ENDPOINTS:
- GET / - Keep existing welcome page (pre-sprint, unchanged)
- GET /test - Backend verification endpoint (JSON)
- GET /api/members - Get all members (JSON)
- POST /api/members - Create new member (JSON)
- GET /api/plans - Get membership plans (JSON)
- GET /api/sessions - Get workout sessions (JSON)
- GET /api/trainers - Get trainers list (JSON)
- GET /api/stats - Get dashboard statistics (JSON)
- POST /api/sessions/schedule - Schedule session (JSON)

REQUIRED APP.PY STRUCTURE:
```python
from flask import Flask, render_template, jsonify, request
import config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config.Config)

# Keep the original welcome page from pre-sprint (no changes)
@app.route('/')
def home():
    return render_template('index.html')

# Sprint 1: Backend API endpoints only (return JSON, no HTML/templates)

@app.route('/test')
def test():
    """Test endpoint to verify backend is working"""
    return jsonify({
        'status': 'success',
        'message': 'Flask Backend is Working!',
        'endpoint': '/test',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/members', methods=['GET'])
def api_members():
    """API: Get all members"""
    return jsonify({
        'status': 'success',
        'data': [],
        'count': 0,
        'message': 'Members API endpoint ready'
    })

@app.route('/api/members', methods=['POST'])
def api_create_member():
    """API: Create new member"""
    return jsonify({
        'status': 'success',
        'message': 'Member creation API ready',
        'received_data': request.get_json() if request.is_json else None
    })

# Continue with other API endpoints...

@app.route('/api/plans', methods=['GET'])
def api_plans():
    """API: Get all membership plans"""
    return jsonify({
        'status': 'success',
        'data': [],
        'count': 0,
        'message': 'Plans API endpoint ready'
    })

@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    """API: Get all workout sessions"""
    return jsonify({
        'status': 'success',
        'data': [],
        'count': 0,
        'message': 'Sessions API endpoint ready'
    })

@app.route('/api/trainers', methods=['GET'])
def api_trainers():
    """API: Get all trainers"""
    return jsonify({
        'status': 'success',
        'data': [],
        'count': 0,
        'message': 'Trainers API endpoint ready'
    })

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API: Get dashboard statistics"""
    stats = {
        'total_members': 0,
        'active_sessions': 0,
        'total_plans': 0,
        'monthly_revenue': 0,
        'new_members': 0
    }
    return jsonify({
        'status': 'success',
        'data': stats,
        'message': 'Stats API endpoint ready'
    })

@app.route('/api/sessions/schedule', methods=['POST'])
def api_schedule_session():
    """API: Schedule a new session"""
    return jsonify({
        'status': 'success',
        'message': 'Session scheduling API ready',
        'received_data': request.get_json() if request.is_json else None
    })

if __name__ == '__main__':
    app.run(debug=True)
```

SPRINT 1 API ENDPOINTS SUMMARY:

✅ **Keep Unchanged:**
- GET / - Welcome page from pre-sprint (HTML)

✅ **Add New API Endpoints:**
- GET /test - Backend verification (JSON)
- GET /api/members - Get all members (JSON)
- POST /api/members - Create new member (JSON)
- GET /api/plans - Get membership plans (JSON)
- GET /api/sessions - Get workout sessions (JSON)
- GET /api/trainers - Get trainers list (JSON)
- GET /api/stats - Get dashboard statistics (JSON)
- POST /api/sessions/schedule - Schedule session (JSON)

IMPORTANT: NO TEMPLATES IN SPRINT 1
- Sprint 1 = Backend API endpoints (JSON responses)
- Sprint 2 = Frontend templates and UI
- Sprint 3 = Integration and polish

CONFIG.PY REQUIREMENTS (OPTIONAL FOR SPRINT 1):
```python
import os

class Config:
    SECRET_KEY = 'fitness-club-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance", "fitness_club.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

SPRINT 1 DATA STRUCTURE (Mock Data for API Responses):
Each API endpoint should return JSON with this structure:

```json
{
    "status": "success",
    "data": [],
    "count": 0,
    "message": "Endpoint description"
}
```

For /api/stats endpoint:
```json
{
    "status": "success",
    "data": {
        "total_members": 0,
        "active_sessions": 0,
        "total_plans": 0,
        "monthly_revenue": 0,
        "new_members": 0
    },
    "message": "Stats API endpoint ready"
}
```

NO DATABASE REQUIRED FOR SPRINT 1:
- Use mock data (empty arrays, zero counts)
- Database and models will be added in Sprint 2
- Focus purely on API endpoint structure

## 🎯 **EXPECTED DELIVERABLES**

✅ **Sprint 1 Backend API Deliverables:**

- **src\app.py** - Flask app with API endpoints (keeps existing welcome page)
- **src\config.py** - Basic Flask configuration (optional for Sprint 1)
- **API Endpoints** - All endpoints return JSON responses, not HTML
- **Welcome Page** - Original welcome page unchanged from pre-sprint

✅ **API Endpoints Working:**

- `GET /` - Welcome page (HTML, unchanged from pre-sprint)
- `GET /test` - Backend verification (JSON)
- `GET /api/members` - Members API (JSON)
- `POST /api/members` - Create member API (JSON)
- `GET /api/plans` - Plans API (JSON)
- `GET /api/sessions` - Sessions API (JSON)
- `GET /api/trainers` - Trainers API (JSON)
- `GET /api/stats` - Dashboard stats API (JSON)
- `POST /api/sessions/schedule` - Schedule session API (JSON)

## 🧪 **SPRINT 1 VERIFICATION CHECKLIST**

**Manual verification steps for Sprint 1 backend API:**

### **Step 1: Start Flask Application**

```powershell
# Navigate to src folder and start Flask app
Set-Location src
python app.py
```

### **Step 2: Test Welcome Page (Should Remain Unchanged)**

- Open browser to `http://127.0.0.1:5000`
- ✅ Verify welcome page displays correctly (same as pre-sprint)
- ✅ Confirm TailwindCSS, Font Awesome, and favicon still work

### **Step 3: Test API Endpoints (New for Sprint 1)**

Open browser or use curl to test these JSON API endpoints:

- `http://127.0.0.1:5000/test` - Should return JSON backend verification
- `http://127.0.0.1:5000/api/members` - Should return JSON members response
- `http://127.0.0.1:5000/api/plans` - Should return JSON plans response
- `http://127.0.0.1:5000/api/sessions` - Should return JSON sessions response
- `http://127.0.0.1:5000/api/trainers` - Should return JSON trainers response
- `http://127.0.0.1:5000/api/stats` - Should return JSON stats response

### **Step 4: Verify JSON Responses**

Each API endpoint should return JSON format like:

```json
{
    "status": "success",
    "data": [],
    "message": "Endpoint description"
}
```

---

## ✅ **SPRINT 1 COMPLETION CRITERIA**

**✅ ALL CHECKS PASSED?** → **Ready for Sprint 2!**
**❌ ANY FAILURES?** → **Review API endpoints and fix issues**

**Sprint 1 Success Indicators:**
- Welcome page unchanged from pre-sprint (HTML with styling)
- All API endpoints return JSON responses
- No HTML templates required (that's Sprint 2)
- Backend structure ready for frontend integration

---

## 🚀 **SPRINT 1 COMPLETE - NEXT STEPS**

Once Sprint 1 verification passes, you're ready for:

**Sprint 2: Frontend Templates** - Create HTML templates that consume these APIs
**Sprint 3: Integration & Polish** - Connect frontend with backend, add validation

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🛠 Environment Setup
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🔧 Setup & Environment
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 🎯 **NEXT STEP**

After completing Sprint 1, proceed to: **[4_Sprint2-Frontend.md](4_Sprint2-Frontend.md)** - Frontend Templates
````
