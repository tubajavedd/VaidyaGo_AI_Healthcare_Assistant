"""
VaidyaGo Knowledge Base

Comprehensive information about the VaidyaGo healthcare platform.
Used by the chatbot to answer questions about the platform, features, and usage.
"""


class VaidyaGoKnowledge:
    """
    Knowledge base for VaidyaGo platform information.
    """

    PLATFORM_INFO = {
        "name": "VaidyaGo",
        "tagline": "AI-powered conversational healthcare management platform",
        "description": (
            "VaidyaGo is a healthcare platform where patients can discover doctors, "
            "book appointments, manage healthcare through natural conversation, "
            "view prescriptions, and access notifications. Instead of filling forms, "
            "users interact with an AI assistant named Vado."
        ),
        "vision": "Make healthcare more accessible and conversational",
    }

    CORE_FEATURES = {
        "discover_doctors": {
            "title": "Discover Doctors",
            "description": "Find and browse healthcare professionals",
            "examples": [
                "Show me cardiologists",
                "Find dermatologists near me",
                "Who are the available doctors?",
            ],
        },
        "book_appointments": {
            "title": "Book Appointments",
            "description": "Schedule appointments with doctors conversationally",
            "examples": [
                "Book an appointment with Dr. Smith on Monday at 10 AM",
                "Schedule a consultation with a dentist tomorrow",
                "I need to see a doctor this week",
            ],
        },
        "manage_appointments": {
            "title": "Manage Appointments",
            "description": "Cancel, reschedule, or view your appointments",
            "examples": [
                "Show my appointments",
                "Cancel my appointment for Friday",
                "Reschedule my appointment to next Monday",
            ],
        },
        "view_prescriptions": {
            "title": "View Prescriptions",
            "description": "Access your active prescriptions and medication history",
            "examples": [
                "Show my prescriptions",
                "What medicines am I currently taking?",
                "Get my prescription history",
            ],
        },
        "notifications": {
            "title": "Get Notifications",
            "description": "Receive appointment reminders and healthcare updates",
            "examples": [
                "Show my notifications",
                "Do I have any upcoming reminders?",
                "Alert me before my appointment",
            ],
        },
        "conversation": {
            "title": "Natural Conversation",
            "description": "Interact with healthcare through chat instead of forms",
            "examples": [
                "What is VaidyaGo?",
                "How do I book an appointment?",
                "Tell me about the platform",
            ],
        },
    }

    CORE_MODULES = {
        "authentication": {
            "name": "Authentication System",
            "purpose": "User signup, login, and role management",
            "user_types": ["Patient", "Doctor", "Admin"],
            "technologies": ["JWT", "Django Auth"],
        },
        "doctor_management": {
            "name": "Doctor Management",
            "purpose": "Store and manage doctor profiles and specializations",
            "features": [
                "Doctor profiles",
                "Specialization",
                "Availability",
                "Contact information",
            ],
        },
        "doctor_slots": {
            "name": "Doctor Slots System",
            "purpose": "Manage doctor availability and time slots",
            "details": (
                "Doctors define availability windows with time slots. "
                "Example: Available Feb 4-7, 11:00-16:00, 15-minute slots"
            ),
        },
        "appointments": {
            "name": "Appointment System",
            "purpose": "Book, cancel, reschedule, and manage appointments",
            "capabilities": [
                "Create appointments",
                "Cancel appointments",
                "Reschedule appointments",
                "List user appointments",
            ],
        },
        "conversational_ai": {
            "name": "Conversational AI Layer",
            "purpose": "Natural language interface for all healthcare operations",
            "differentiator": (
                "Instead of UI-heavy workflows, users interact through chat. "
                "Example: 'Book dentist tomorrow evening' instead of clicking 8 buttons."
            ),
        },
    }

    VADO_ASSISTANT = {
        "name": "Vado",
        "role": "AI Healthcare Assistant for VaidyaGo",
        "responsibilities": [
            "Understand user healthcare needs through conversation",
            "Execute appointment actions (book, cancel, reschedule)",
            "Provide healthcare information and guidance",
            "Remember user context and preferences",
            "Answer questions about VaidyaGo",
        ],
        "capabilities": [
            "Conversational support and Q&A",
            "Appointment management",
            "Doctor discovery",
            "Prescription access",
            "Personalized memory and context",
        ],
        "personality": "Warm, friendly, empathetic healthcare assistant",
        "example_interactions": [
            {
                "user": "I need to see a dermatologist tomorrow",
                "vado": "I can help with that! Let me find available dermatologists for tomorrow. What time works best for you?",
            },
            {
                "user": "Show my appointments",
                "vado": "You have 2 upcoming appointments: [list]",
            },
            {
                "user": "Cancel my Friday appointment",
                "vado": "I've cancelled your appointment with Dr. Smith on Friday. Confirmed.",
            },
        ],
    }

    TARGET_USERS = {
        "patients": {
            "needs": [
                "Easy appointment booking",
                "Healthcare access",
                "Medication management",
                "Appointment reminders",
            ],
        },
        "doctors": {
            "needs": [
                "Availability management",
                "Appointment scheduling",
                "Patient management",
            ],
        },
        "administrators": {
            "needs": [
                "System oversight",
                "User management",
                "Platform configuration",
            ],
        },
    }

    TECHNICAL_STACK = {
        "backend": ["Python", "Django", "Django REST Framework"],
        "ai_layer": ["Mistral LLM", "AutoGen Framework", "Intent Detection"],
        "authentication": ["JWT"],
        "architecture": [
            "Conversational AI pipeline",
            "Tool routing system",
            "Memory service",
            "Multi-language support",
        ],
    }

    CONVERSATIONAL_FLOW = (
        "User → Chat endpoint → ChatbotEngine → PromptService → LLM → "
        "IntentService → ToolRouter → Backend APIs → Response"
    )

    WHY_VAIDYAGO_STANDS_OUT = [
        "Conversational interface reduces friction",
        "Natural language healthcare interaction",
        "AI-powered intent detection",
        "Combines healthcare workflows with conversational AI",
        "Built on modern, scalable architecture",
        "Focus on user experience over forms",
    ]

    FUTURE_POSSIBILITIES = {
        "symptom_triage": "AI assistant helps diagnose symptoms and recommend care",
        "prescription_assistant": "Smart medication reminders and refill management",
        "multi_language": "Support for Hindi, English, and other languages",
        "multi_agent": "Specialized agents for booking, symptoms, escalation",
        "reminders": "Appointment and medication reminders",
    }

    FAQ = {
        "what_is_vaidyago": {
            "question": "What is VaidyaGo?",
            "answer": (
                "VaidyaGo is an AI-powered conversational healthcare management platform. "
                "It allows patients to discover doctors, book appointments, manage healthcare, "
                "view prescriptions, and interact with an AI assistant named Vado through natural conversation "
                "instead of traditional forms."
            ),
        },
        "how_to_book": {
            "question": "How do I book an appointment?",
            "answer": (
                "Simply tell Vado what you need. Example: 'Book an appointment with Dr. Smith on Monday at 10 AM'. "
                "You can also say 'I need to see a dentist tomorrow' and Vado will handle the rest, "
                "extracting doctor details, date, and time automatically."
            ),
        },
        "vado_features": {
            "question": "What can Vado do?",
            "answer": (
                "Vado can: book and cancel appointments, reschedule appointments, show your appointments, "
                "help you discover doctors, access your prescriptions, provide healthcare information, "
                "answer questions about VaidyaGo, and remember your preferences for personalized assistance."
            ),
        },
        "how_different": {
            "question": "How is VaidyaGo different from other healthcare apps?",
            "answer": (
                "Most healthcare apps require clicking through menus and filling forms. VaidyaGo is different because "
                "you interact through natural conversation. Instead of 8 clicks and forms, you just say what you need, "
                "and Vado handles everything. It's like texting with your healthcare assistant."
            ),
        },
        "vaidyago_users": {
            "question": "Who uses VaidyaGo?",
            "answer": (
                "VaidyaGo is designed for: Patients who want easy healthcare access and appointment booking, "
                "Doctors who need to manage their availability and appointments, and Administrators who oversee the platform."
            ),
        },
        "vaidyago_features_list": {
            "question": "What features does VaidyaGo have?",
            "answer": (
                "VaidyaGo offers: Doctor discovery and browsing, Conversational appointment booking, "
                "Appointment management (cancel, reschedule, list), Prescription viewing and management, "
                "Appointment and medication reminders, Personalized AI assistant (Vado), Natural language interface, "
                "Multi-language support, and more features coming soon."
            ),
        },
        "what_is_vado": {
            "question": "What is Vado?",
            "answer": (
                "Vado is your AI healthcare assistant on VaidyaGo. She's designed to be warm, friendly, and empathetic. "
                "Vado can help you book appointments, manage your healthcare, answer questions about VaidyaGo, "
                "remember your preferences, and provide healthcare guidance. Think of her as your personal healthcare assistant."
            ),
        },
        "is_vaidyago_safe": {
            "question": "Is VaidyaGo safe and secure?",
            "answer": (
                "Yes. VaidyaGo uses modern security practices including JWT authentication, secure API endpoints, "
                "and follows healthcare data protection standards. Your personal and health information is protected."
            ),
        },
        "languages_supported": {
            "question": "What languages does VaidyaGo support?",
            "answer": (
                "VaidyaGo currently supports English. Multi-language support for Hindi and other languages is coming soon."
            ),
        },
        "how_to_cancel_appointment": {
            "question": "How do I cancel an appointment?",
            "answer": (
                "You can cancel an appointment by telling Vado. Example: 'Cancel my appointment for Friday' "
                "or 'Cancel appointment ID 123'. Vado will handle the cancellation and confirm."
            ),
        },
        "symptom_fever": {
            "question": "I have a fever",
            "answer": (
                "I'm sorry to hear you have a fever. It's important to rest and stay hydrated. "
                "For persistent or high fever, I recommend consulting a General Physician. "
                "Would you like me to find an available doctor for you?"
            ),
        },
        "symptom_headache": {
            "question": "I have a headache",
            "answer": (
                "Headaches can be caused by stress, dehydration, or other factors. "
                "If it's severe or persistent, you should consult a General Physician or a Neurologist. "
                "Shall I check for available appointments?"
            ),
        },
        "symptom_stomach_pain": {
            "question": "My stomach hurts",
            "answer": (
                "Stomach pain can range from mild indigestion to more serious issues. "
                "I recommend seeing a General Physician or a Gastroenterologist for a proper evaluation. "
                "Would you like to book an appointment?"
            ),
        },
        "emergency_chest_pain": {
            "question": "I have chest pain",
            "answer": (
                "🚨 IMPORTANT: If you are experiencing chest pain, difficulty breathing, or severe bleeding, "
                "this may be a medical emergency. Please contact emergency services immediately or head to the "
                "nearest hospital emergency department. Do not wait for an online consultation."
            ),
        },
        "doctor_recommendation_skin": {
            "question": "Which doctor for skin allergy?",
            "answer": (
                "For skin allergies, rashes, or other skin-related issues, you should consult a Dermatologist. "
                "I can help you find top-rated dermatologists on VaidyaGo. Should I show you a list?"
            ),
        },
        "medicine_inquiry": {
            "question": "Can I take paracetamol?",
            "answer": (
                "I cannot provide specific medical prescriptions. However, common over-the-counter medicines "
                "should be taken only according to the dosage on the package or as advised by a doctor. "
                "Would you like to speak with a doctor about your symptoms?"
            ),
        },
        "account_help": {
            "question": "Account assistance",
            "answer": (
                "You can manage your profile, reset your password, or update your phone number in the 'Account Settings'. "
                "If you're having trouble with OTPs or login, please wait a minute and retry, or contact our support team."
            ),
        },
        "trust_and_privacy": {
            "question": "Is VaidyaGo legit and safe?",
            "answer": (
                "Yes, VaidyaGo is a fully legit and secure healthcare platform. We use end-to-end encryption for all chats, "
                "follow HIPAA-compliant data practices, and ensure your medical history is shared only with your chosen doctors. "
                "We are available across India and never sell user data."
            ),
        },
        "pricing_and_payments": {
            "question": "Pricing and payment methods",
            "answer": (
                "The VaidyaGo platform is free to use. Doctor consultation fees are set by the professionals and displayed upfront. "
                "We support UPI, credit cards, and net banking. Refunds for cancellations are processed within 5-7 business days. "
                "Invoices are available after every paid consultation."
            ),
        },
        "insurance_info": {
            "question": "Insurance and claims",
            "answer": (
                "We support various insurance providers for reimbursement claims. You can upload your insurance or health card "
                "(including Ayushman Bharat or corporate cards) to your profile. We are actively working on direct cashless tie-ups."
            ),
        },
        "diagnostics_and_lab": {
            "question": "Lab tests and diagnostics",
            "answer": (
                "You can book blood tests (CBC, Sugar, Thyroid), MRI, CT scans, and X-rays. We partner with certified labs "
                "for home sample collection. Once ready, you can upload and share your reports with your doctor via the app."
            ),
        },
        "mental_health": {
            "question": "Mental health support",
            "answer": (
                "VaidyaGo provides access to experienced psychologists and therapists for anxiety, depression, stress, "
                "and sleep issues. Counseling is private and available via chat or video consultation."
            ),
        },
        "womens_and_child_health": {
            "question": "Pregnancy and Child health",
            "answer": (
                "We have specialized Gynecologists for pregnancy and women's health, and Pediatricians for newborn "
                "and child care, including vaccination schedules and common childhood illnesses like fever and cold."
            ),
        },
        "medical_specialties": {
            "question": "Specialized departments",
            "answer": (
                "We have doctors for every specialty: Cardiology (Heart), Neurology (Brain/Nerves), Orthopedics (Bones/Joints), "
                "Dermatology (Skin), ENT, Dentistry, and Gastroenterology. Just tell Vado your symptoms to find the right expert."
            ),
        },
        "pharmacy_and_medicines": {
            "question": "Pharmacy and medicine logistics",
            "answer": (
                "Order medicines online by uploading your prescription. We offer home delivery, refills, and generic "
                "medicine substitutes to help you manage your healthcare costs effectively."
            ),
        },
        "emotional_support": {
            "question": "Angry or frustrated users",
            "answer": (
                "I'm very sorry you're having a bad experience. Whether it's a technical glitch, a booking failure, "
                "or a payment issue, I'm here to help you fix it. Please provide details, or I can connect you to human support."
            ),
        },
        "random_and_silly": {
            "question": "Random questions",
            "answer": (
                "I am Vado, your AI assistant! I don't sleep, I don't eat, and I'm always here to help you. "
                "I can tell jokes, but my primary mission is your health! How can I assist you today?"
            ),
        },
        "system_and_accessibility": {
            "question": "App features and help",
            "answer": (
                "VaidyaGo supports dark mode, voice commands, and accessibility features like larger text. "
                "Check the 'Help' section for tutorials or contact our 24/7 customer care for technical support."
            ),
        },
        "greetings": {
            "question": "Greetings",
            "answer": "Hello! I'm Vado, your VaidyaGo healthcare assistant. How can I help you today?",
        },
    }

    @classmethod
    def get_answer(cls, question_keyword):
        """
        Get answer from FAQ based on keyword with word-boundary awareness.
        """
        question_lower = question_keyword.lower()
        # Clean the question and split into words for precise matching
        import re
        words = re.findall(r'\w+', question_lower)

        # Final Priority-Ordered Keyword Map
        keyword_map = {
            # 1. EMERGENCY (Top Priority)
            ("chest pain", "breathe", "emergency", "heart attack", "unconscious", "bleeding"): "emergency_chest_pain",

            # 2. GREETINGS
            ("hi", "hello", "hey", "greetings", "morning", "evening"): "greetings",
            
            # 3. SPECIFIC TRUST & SECURITY
            ("legit", "trust", "approved", "safe", "secure", "encrypt", "private", "hipaa"): "trust_and_privacy",
            
            # 4. PRICING & PAYMENTS
            ("refund", "payment", "upi", "card", "invoice", "charge", "fee", "cost", "price", "paid", "free", "subscription"): "pricing_and_payments",
            
            # 5. INSURANCE
            ("insurance", "ayushman", "cashless", "claim", "policy"): "insurance_info",
            
            # 6. DIAGNOSTICS & REPORTS
            ("lab", "blood", "cbc", "sugar", "thyroid", "mri", "scan", "xray", "report", "analyze", "cholesterol"): "diagnostics_and_lab",
            
            # 7. MENTAL HEALTH
            ("anxiety", "anxious", "depression", "depressed", "panic", "stress", "stressed", "mental", "therapist", "counseling"): "mental_health",
            
            # 8. WOMEN & CHILD HEALTH
            ("pregnancy", "pregnant", "gynecologist", "period", "pcos", "child", "pediatric", "baby", "vaccination", "vaccine"): "womens_and_child_health",
            
            # 9. PHARMACY & LOGISTICS
            ("medicine", "order", "refill", "pharmacy", "generic"): "pharmacy_and_medicines",
            
            # 10. MEDICAL SPECIALTIES & SYMPTOMS
            ("heart", "cardio", "bp", "ecg", "brain", "nerve", "neurologist", "migraine", "seizure", "bone", "joint", "ortho", "back", "knee", "fracture", "tooth", "teeth", "dental", "dentist", "eye", "vision", "ear", "nose", "throat", "ent", "sinus", "skin", "allergy", "rash", "acne", "hair", "surgery", "surgeon", "diabetes", "hypertension", "asthma"): "medical_specialties",
            ("fever", "cough", "cold", "headache", "dizzy", "stomach", "hurts", "abdominal", "acidity"): "medical_specialties",
            
            # 11. EMOTIONAL & SYSTEM HELP
            ("bad", "hate", "working", "failed", "crash", "angry", "frustrated"): "emotional_support",
            ("password", "login", "signup", "otp", "account", "profile", "forgot"): "account_help",
            ("dark", "text", "voice", "help", "support"): "system_and_accessibility",
            
            # 12. RANDOM & SILLY
            ("joke", "marry", "laugh", "robot", "human", "real", "name"): "random_and_silly",
            
            # 13. GENERAL PLATFORM (Lowest priority)
            ("what is vaidyago", "about vaidyago", "platform"): "what_is_vaidyago",
            ("book", "appointment", "schedule", "bok", "make"): "how_to_book",
            ("vado", "who is vado", "who are you"): "what_is_vado",
            ("cancel", "delete", "cncl"): "how_to_cancel_appointment",
            ("hindi", "hinglish", "language"): "languages_supported",
            ("vaidyago",): "what_is_vaidyago",
        }

        for keywords, faq_key in keyword_map.items():
            for kw in keywords:
                # If keyword is multiple words, check if it's in the full string
                if ' ' in kw:
                    if kw in question_lower:
                        return cls.FAQ[faq_key]["answer"]
                # If keyword is a single word, check if it's a whole word in the question
                elif kw in words:
                    return cls.FAQ[faq_key]["answer"]

        return None

    @classmethod
    def search_knowledge(cls, query):
        """
        Search knowledge base for relevant information.
        Returns matching information from knowledge base.
        """
        query_lower = query.lower()
        results = []

        if any(term in query_lower for term in ["book", "appointment", "schedule"]):
            results.append(cls.CORE_FEATURES["book_appointments"])

        if any(term in query_lower for term in ["doctor", "find", "discover", "specialist"]):
            results.append(cls.CORE_FEATURES["discover_doctors"])

        if any(term in query_lower for term in ["cancel", "reschedule", "manage", "appointment"]):
            results.append(cls.CORE_FEATURES["manage_appointments"])

        if any(term in query_lower for term in ["prescription", "medicine", "medication"]):
            results.append(cls.CORE_FEATURES["view_prescriptions"])

        if any(term in query_lower for term in ["vado", "assistant", "ai"]):
            results.append(cls.VADO_ASSISTANT)

        if any(term in query_lower for term in ["feature", "can do", "what can"]):
            results.append(cls.CORE_FEATURES)
            
        if any(term in query_lower for term in ["emergency", "chest pain", "breathe"]):
            results.append({"title": "EMERGENCY PROTOCOL", "description": cls.FAQ["emergency_chest_pain"]["answer"]})

        return results if results else [cls.PLATFORM_INFO]

    @classmethod
    def get_all_faq(cls):
        """
        Get all FAQ items.
        """
        return cls.FAQ

    @classmethod
    def get_platform_overview(cls):
        """
        Get comprehensive platform overview.
        """
        return {
            "platform": cls.PLATFORM_INFO,
            "core_features": cls.CORE_FEATURES,
            "modules": cls.CORE_MODULES,
            "vado": cls.VADO_ASSISTANT,
            "target_users": cls.TARGET_USERS,
            "tech_stack": cls.TECHNICAL_STACK,
            "why_special": cls.WHY_VAIDYAGO_STANDS_OUT,
            "future": cls.FUTURE_POSSIBILITIES,
        }
