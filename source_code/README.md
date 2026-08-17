# Unified Students & Employment Lifecycle Portal

This package contains a Django 5.2 academic web application for managing student lifecycle records, employee lifecycle records, company/HR mappings, salary records, salary queries, rule-based verification, dashboards, reports, and printable resumes.

## Quick Start

1. Open a terminal in `source_code`.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it on Windows: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and adjust values if needed.
6. Run migrations: `python manage.py migrate`
7. Load demo data: `python manage.py seed_demo_data`
8. Start the server: `python manage.py runserver`
9. Open `http://127.0.0.1:8000`.

Demo accounts are created by the seed command: `admin/Admin@12345`, `hr_demo/Hr@12345`, `student_demo/Student@12345`, and `employee_demo/Employee@12345`.
