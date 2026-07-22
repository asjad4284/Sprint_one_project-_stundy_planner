# Study Planner

A full-stack study planning application built using FastAPI (backend) and Streamlit (frontend).  
This project helps users organize subjects, create a weekly study schedule, track daily progress, and analyze weekly performance through a simple and interactive web interface.

---

## Overview

The AI Study Planner works as a digital study management system. It allows users to plan their studies in a structured and efficient way while tracking their consistency over time.

Users can:
- Create an account and log in securely
- Add subjects with difficulty level and study hours
- Build a weekly study schedule
- Track daily progress by marking tasks as completed
- View a weekly performance report with detailed statistics

All data is stored in a database, ensuring persistence across sessions.

---

## Key Highlights

- Clean architecture (separation of concerns)
- Secure authentication system
- Real-world CRUD operations
- Interactive frontend using Streamlit
- Fully functional backend APIs
- Weekly analytics and reporting system

---

## Core Functionalities (CRUD Logic)

### User
- Create new user (signup)
- Login with token generation
- Secure password hashing

### Subject
- Add subject
- View subjects
- Delete subject

### Schedule
- Create schedule (day and duration)
- Link schedule with subject
- Automatically create progress record

### Today Tasks
- Fetch today's schedule
- Show completed vs pending tasks

### Progress
- Update task status:
  - pending
  - completed

### Weekly Report
- Total tasks
- Completed tasks
- Pending tasks
- Completion percentage
- Day-wise performance

---

## Authentication System

- JWT-based authentication
- Token generated on login
- Token required for protected routes
- Token expires after 2 hours

---

## How This Project Works

This system is divided into backend and frontend components.

### Backend (FastAPI)

Handles:
- API creation
- Database operations
- Authentication
- Business logic

### Frontend (Streamlit)

Handles:
- User interface
- User interaction
- API communication with backend

---

## Tech Stack

| Layer | Technology | Purpose |
|------|-----------|--------|
| Backend | FastAPI | API development |
| Database | MySQL | Data storage |
| ORM | SQLAlchemy | Database interaction |
| Validation | Pydantic | Data validation |
| Authentication | JWT + bcrypt | Security |
| Frontend | Streamlit | User interface |

---

## Project Structure

```
study-planner/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── auth.py
│   ├── utils.py
│
├── streamlit_app.py
├── requirements.txt
├── images/
│   └── screenshot.png
└── README.md
```

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/saqlainshahx01/Sprint_one_project-_stundy_planner.git
cd Sprint_one_project-_stundy_planner
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```sql
CREATE DATABASE study_planner;
```

### 5. Configure Database Connection

Update in `app/database.py`:
```
DATABASE_URL = "mysql+pymysql://username:password@localhost/study_planner"
```

(Optional: use environment variable)
```bash
export DATABASE_URL="mysql+pymysql://username:password@localhost/study_planner"
```

### 6. Run Backend
```bash
uvicorn app.main:app --reload
```

API Docs:
```
http://127.0.0.1:8000/docs
```

### 7. Run Frontend
```bash
streamlit run streamlit_app.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /user | Create user |
| GET | /login | Login |
| GET | /me | Get current user |
| POST | /subjects | Add subject |
| GET | /subjects/{user_id} | Get subjects |
| DELETE | /subjects/{id} | Delete subject |
| POST | /schedule | Create schedule |
| GET | /schedule/{user_id} | Get schedule |
| GET | /schedule/today/{user_id} | Today's tasks |
| PUT | /progress/{id} | Update progress |
| GET | /report/{user_id} | Weekly report |

---

## Usage

1. Create an account
2. Login
3. Add subjects
4. Create weekly schedule
5. Track daily progress
6. View weekly report

---

## Screenshot

GitHub Repository:  
https://github.com/saqlainshahx01/Sprint_one_project-_stundy_planner

---

## Notes

- Backend runs on http://127.0.0.1:8000
- Frontend runs on http://localhost:8501
- Ensure MySQL is running before starting

---

## Author

Saqlain Shah
