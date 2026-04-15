# Telecom BSS System

## 📌 Overview
This project is a Telecom BSS (Business Support System) built using Django and Django REST Framework.  
It handles UDR ingestion, rating, and invoice generation.

---

## 🚀 Features
- UDR (Usage Data Record) ingestion
- Rating engine for usage calculation
- Invoice generation system
- REST APIs for integration
- Admin dashboard support

---

## 🛠 Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (can be extended to PostgreSQL)
- HTML (for templates)

---

## 📂 Project Structure
- `bss_project1/` → Main project settings
- `rating/` → Core business logic (rating, billing, APIs)
- `templates/` → HTML templates

---

## 🔗 APIs
- UDR ingestion API
- Rating calculation API
- Invoice generation API

---

## ▶️ How to Run
```bash
git clone https://github.com/serajsid786/telecom_bss.git
cd telecom_bss
python -m venv telecomvenv
.\telecomvenv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
