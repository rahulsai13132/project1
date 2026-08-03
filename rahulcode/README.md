# 🎓 SmartCampus AI – AI Powered College Management System

SmartCampus AI is a production-ready, modular, and responsive Streamlit web application engineered with Python 3.12+. It delivers an end-to-end college management ecosystem featuring a custom JSON database engine, bcrypt password security, glassmorphic UI, Plotly analytics, and an OpenAI-powered career & academic assistant.

---

## 🌟 Key Features

* **🔐 Authentication & Security**:
  * Bcrypt password hashing
  * Multi-field registration validation (Email format, mobile check, duplicate username/email detection)
  * Secure `st.session_state` management
* **📁 Custom JSON Database Engine**:
  * Thread-safe atomic JSON read/write operations
  * Reusable generic CRUD abstraction (`create`, `read`, `update`, `delete`, `find`, `find_all`, `save`, `load`)
  * Auto-creates missing database JSON files & seeds demo data
* **📊 Analytics Dashboard**:
  * Real-time student statistics & system metrics
  * Interactive Plotly charts (Notice priority breakdown, workshop seat allocation, placement deadlines timeline)
  * Quick action shortcuts and activity logging
* **📢 Notice Board (Full CRUD)**:
  * Department & priority badges (High, Medium, Low)
  * Real-time search, priority filtering, and edit/delete controls
* **💼 Placement & Internship Portal (Full CRUD)**:
  * Salary package tracking, location, eligibility, and direct apply links
  * One-click CSV export of placement records
* **🎯 Skill Workshops (Full CRUD)**:
  * Trainer profiles, venue allocation, and live seat registration counters
* **🤖 SmartCampus AI Assistant**:
  * Powered by official OpenAI API (`gpt-4o-mini`)
  * Summarizes campus notices, provides resume feedback, mock interview practice, and generates career roadmaps
  * Robust fallback engine ensuring 100% feature functionality even without an active API key
* **⚙ Preferences & Settings**:
  * Student profile editor, password change, dark/light styling preferences, language selector

---

## 📁 Directory Structure

```
SmartCampusAI/
│── app.py                      # Main Streamlit Application Entrypoint
│── requirements.txt            # Project Dependencies
│── render.yaml                 # Render Cloud Deployment Blueprint
│── README.md                   # Comprehensive Project Documentation
│── .env                        # Environment Variables
│── .env.example                # Template for Environment Setup
│── .gitignore                  # Git Ignore Rules
│
├── assets/
│     ├── logo.svg              # Brand Vector Logo
│     ├── banner.svg            # Hero Section Graphic
│     ├── styles.css            # Master Glassmorphism CSS Design System
│
├── database/
│     ├── users.json            # User Credentials & Profile Database
│     ├── notices.json          # College Notices & Bulletins
│     ├── placements.json       # Job & Internship Listings
│     ├── workshops.json        # Workshop & Event Data
│     ├── settings.json         # Application System Preferences
│     ├── logs.json             # System Audit Logs
│
├── core/
│     ├── config.py             # Config & Environment Parser
│     ├── session.py            # Session Manager
│     ├── security.py           # Bcrypt Security Manager
│     ├── constants.py          # Application Constants & Dropdowns
│
├── database_engine/
│     ├── json_database.py      # JSON IO Engine & Default Seeder
│     ├── crud.py               # Reusable Generic CRUD Engine
│
├── authentication/
│     ├── login.py              # Login Form & Verification
│     ├── register.py           # User Registration & Validation
│     ├── logout.py             # Session Termination
│
├── pages/
│     ├── home.py               # Landing Overview & Quick Actions
│     ├── dashboard.py          # Analytics Dashboard & Plotly Charts
│     ├── notice_board.py       # Notice Board CRUD
│     ├── placements.py         # Placement Portal CRUD & CSV Download
│     ├── workshops.py          # Workshop Catalog & Registration
│     ├── chatbot.py            # Streamlit Chat AI Assistant UI
│     ├── settings.py           # Profile & Preferences Settings
│
├── components/
│     ├── sidebar.py            # Glassmorphic Sidebar Navigation
│     ├── navbar.py             # Header Bar with Date Badge
│     ├── footer.py             # Global Footer
│     ├── cards.py               # Reusable Card Renderers
│
├── services/
│     ├── ai_service.py         # OpenAI Service & Fallback Engine
│     ├── notice_service.py     # Notice Business Logic
│     ├── placement_service.py  # Placement Business Logic
│     ├── workshop_service.py   # Workshop Business Logic
│
└── utils/
      ├── helpers.py            # Date Formatting & CSV Generators
      ├── validators.py         # Regex Form Validators
      ├── logger.py             # Unified App Logging Utility
```

---

## 🛠 Tech Stack

* **Frontend**: Streamlit, Custom Glassmorphism CSS, Plotly Charts
* **Backend**: Python 3.12+, Object-Oriented Architecture, MVC Pattern
* **Database**: Native JSON File Engine
* **AI Engine**: OpenAI API (`gpt-4o-mini`)
* **Security**: Bcrypt Password Hashing

---

## 🚀 Installation & Local Setup

### 1. Clone Repository & Setup Virtual Environment

```bash
# Clone repository
git clone https://github.com/your-username/SmartCampusAI.git
cd SmartCampusAI

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS / Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
SECRET_KEY=smartcampus_secret_key_2026_super_secure_99
APP_NAME=SmartCampus AI
ENVIRONMENT=development
```

### 4. Run Application Locally

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## ☁ Render Deployment

SmartCampus AI is pre-configured for one-click deployment on [Render](https://render.com).

### Deployment Steps:
1. Push your repository to GitHub.
2. Log in to Render Dashboard and select **New + -> Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml`.
4. Add your environment variables (`OPENAI_API_KEY` and `SECRET_KEY`) under **Environment Variables**.
5. Click **Deploy**.

---

## 📷 Default Login Credentials

* **Username**: `alexj`
* **Password**: `password123`

---

## 📄 License

This project is licensed under the MIT License.
