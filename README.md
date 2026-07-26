# 📚 StudyTrack - Student Study Monitoring System

A Django-based study management system for students and educational consultants to track daily study sessions.

---

## 🚀 Features

### Students
- Register/Login with authentication
- Create daily study reports
- Add study sessions with:
  - Subject
  - Start/End time
  - Number of practice questions
  - Optional notes
- View all reports and session details
- Edit/Delete sessions

### Consultants
- Dashboard with assigned students list
- Check daily student activity (reported today or not)
- View complete study history for each student
- Detailed session breakdown per report

---

## 🛠️ Tech Stack

- **Backend**: Django 5.1
- **Database**: MySQL
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Icons**: Font Awesome 6
- **Authentication**: Django Auth System

---

## 🗂️ Database Schema

| Table | Description |
|-------|-------------|
| `auth_user` | User accounts (Django default) |
| `accounts_profile` | Extended user profile with role & consultant |
| `study_log_dailyreport` | Daily reports per student |
| `study_log_studysession` | Study sessions within each report |

**Relationships**:
- `Profile` → `User` (OneToOne)
- `DailyReport` → `Student` (ForeignKey)
- `StudySession` → `DailyReport` (ForeignKey)
- `Profile.consultant` → `Profile` (Self ForeignKey)