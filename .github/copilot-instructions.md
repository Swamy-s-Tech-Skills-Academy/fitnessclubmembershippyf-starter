# 🤖 GitHub Copilot Instructions: Fitness Club Membership System

Welcome to the **Fitness Club Membership System** – a 45-minute live coding demo using **Flask**, **Tailwind CSS**, and **SQLite**. This project is structured into sprints with clear instructions to help GitHub Copilot Agent provide contextual suggestions aligned with the development flow.

---

## 📦 Project Summary

| Key Detail         | Value                      |
| ------------------ | -------------------------- |
| Language           | Python                     |
| Backend Framework  | Flask                      |
| ORM                | SQLAlchemy                 |
| Forms Library      | Flask-WTF                  |
| Frontend Framework | Tailwind CSS (CDN)         |
| Icons              | Font Awesome (CDN)         |
| Typography         | Google Fonts (CDN)         |
| Database           | SQLite (in `src/instance`) |
| Mode               | Live coding demo           |
| Duration           | ~45 minutes                |

---

## 📁 Project Structure (Expected)

```
.
├── src/
│   ├── app.py
│   ├── config.py
│   ├── init_db.py
│   ├── models.py
│   ├── templates/
│   ├── static/
│   └── instance/
├── requirements.txt
├── README.md
├── .gitignore
├── .copilot/settings.json
└── .github/
    └── copilot-instructions.md
```

---

## � Coding Standards

- `camelCase` → variables, functions
- `PascalCase` → class and component names
- `ALL_CAPS` → constants
- `_prefix` → private class members
- Prefer explicit error handling (`try/except`)
- Use contextual logging for debugging

---

## 🧠 Contextual Path Awareness

Copilot Agent must remember:

- The project structure is focused on development with Flask app in `src/` folder
- All application code resides in the `src/` directory
- Database files are stored in `src/instance/`
- Templates are in `src/templates/` and static files in `src/static/`

---

## 🚦 Workflow and Sprint Files

### 🛠 Sprint Files (Sequential)

| Sprint Step | File Name                  | Duration | Summary                          |
| ----------- | -------------------------- | -------- | -------------------------------- |
| 1️⃣          | `2_Pre-Sprint-Setup.md`    | 5 min    | Setup virtual env, Flask, layout |
| 2️⃣          | `3_Sprint1-Backend.md`     | 15 min   | SQLAlchemy models & routes       |
| 3️⃣          | `4_Sprint2-Frontend.md`    | 15 min   | Jinja2 templates & Tailwind UI   |
| 4️⃣          | `5_Sprint3-Integration.md` | 15 min   | Booking logic, CSV export        |

### 📚 Reference Files

_Note: Reference files have been removed to focus on core sprint workflow_

---

## ⚙️ Copilot Agent Expectations

Copilot Agent should:

- Follow file flow: `2_`, `3_`, `4_`, `5_`
- Suggest model creation using SQLAlchemy
- Recommend routes/views using Flask decorators
- Generate Tailwind-based HTML templates
- Propose Flask-WTF forms
- Use `cat <<EOF` format for writing files
- Follow `settings.json` configuration
- Focus on development workflow (no test file generation)

---

## ✅ Deliverables by End

- Fully working Flask web app
- CRUD + booking features with relationships
- Professional UI with TailwindCSS
- Data export capability
- Clean, modular source layout
- Browser-testable endpoints

---

## 🔁 Developer Commands (Validation)

```bash
# Setup
python -m venv .venv
source .venv/bin/activate       # or .venv\Scripts\activate
pip install -r requirements.txt

# Run database init
cd src
python init_db.py

# Start app
python app.py
# Open: http://localhost:5000
```

---

## 💡 Reminder to Copilot Agent

If the user invokes a prompt:

- Identify the current sprint file (based on file name)
- Generate or complete relevant code
- Respect coding standards and folder structure
- Provide context-aware completions, not global changes
- **Do not move to the next sprint unless the user (Swamy) confirms the current sprint is complete and correct**

### 🧪 Sprint Review Process (Agile-style)

Copilot should:

1. **Generate code for the current sprint**
2. **Wait for Swamy to test and validate**
3. **Incorporate any feedback**
4. **Proceed to the next sprint only after Swamy explicitly agrees**

This ensures quality, clarity, and a smooth live demo flow.

---

## 📂 Folder Purpose Clarification

### 💡 `prompts/` – Sprint Prompts for Copilot Agent

- Contains `.md` prompt files used **exclusively** for **coding guidance during live sprints**.
- Copilot should **rely only on files inside `prompts/`** for generating code during the live demo.
- Each file is self-contained, follows the naming pattern `2_`, `3_`, `4_`, etc.
- Focus on development workflow and live coding demonstrations.

---
