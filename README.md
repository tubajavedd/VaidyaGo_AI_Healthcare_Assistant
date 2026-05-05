 ##AI Vernacular Healthcare Assistant

An AI-powered healthcare assistant designed for Indian users that supports Hindi/Hinglish communication, enabling easy access to healthcare services like symptom checking, doctor booking, prescription analysis, and reminders.

##Project Overview

This project aims to build a full-stack healthcare platform with AI integration that helps users:

* Understand symptoms in Hindi
* Book doctor appointments
* Upload prescriptions (OCR-based parsing)
* Get medicine reminders
* Use voice (Speech-to-Text & Text-to-Speech)

 Goal: Make healthcare accessible, simple, and vernacular-friendly

## MVP Features (Minimum Working Product)
* OTP-based Login (Mobile)
* Hindi Symptom Chat (AI-based)
* Doctor Appointment Booking
* Prescription Upload + OCR
* Medicine Reminder System
* Basic Doctor/Admin Dashboard
  
##Tech Stack
*Frontend:
React / Next.js
Tailwind CSS
*Backend:
FastAPI / Django REST Framework
PostgreSQL
#AI & ML :
Hugging Face Models
Whisper (Speech-to-Text)
Tesseract OCR
*Mobile:
React Native / Flutter
#Cloud & DevOps:
AWS / GCP / Azure
Docker
GitHub Actions (CI/CD)

*Core Features Explained:
Symptom Checker (Hindi AI)
User inputs symptoms in Hindi
AI extracts:
Symptoms
Duration
Severity
Returns:
Possible conditions (Top 3)
Suggestions (NOT diagnosis)

* Prescription OCR
Upload image of prescription
Extract:
Medicine name
Dosage
Frequency
Convert into structured data

* Medicine Reminder
Auto-create reminders from prescription
Notifications via:
App
SMS / Email

* Voice Support
Speak symptoms → convert to text
AI response → converted to speech

##Phase Breakdown
Week	Focus
Week 1	Planning, Repo Setup
Week 2	Backend APIs
Week 3	Frontend UI
Week 4	AI Symptom Checker
Week 5	OCR + Voice
Week 6	Video Call + Payments
Week 7	Mobile App
Week 8	Security + Testing
Week 9	Deployment + Beta


AI-Healthcare-Assistant/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   └── services/
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── utils/
│
├── mobile/
│
├── ai/
│   ├── symptom_checker/
│   ├── ocr/
│   └── speech/
│
├── docs/
├── tests/
└── README.md


