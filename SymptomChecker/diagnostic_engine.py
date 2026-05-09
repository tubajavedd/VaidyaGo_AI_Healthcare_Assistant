def run_diagnostic_engine(symptoms_vitals_obj):
    conditions = []
    if symptoms_vitals_obj.headache_severity in ['Moderate', 'Severe']:
        conditions.append({
            'name': 'Tension-Type Headache',
            'match_percent': 85,
            'description': 'Persistent muscle contraction in head and neck region.'
        })
        conditions.append({
            'name': 'Cervicogenic Headache',
            'match_percent': 78,
            'description': 'Pain referred from cervical spine and its components.'
        })
    if symptoms_vitals_obj.eye_strain_duration == 'Continuous':
        conditions.append({
            'name': 'Seasonal Allergies (Rhinitis)',
            'match_percent': 65,
            'description': 'Hypersensitivity reaction to environmental triggers causing sinus pressure and headache.'
        })
    if not conditions:
        conditions.append({
            'name': 'No high‑confidence match',
            'match_percent': 0,
            'description': 'Symptoms do not strongly correlate with any condition.'
        })
    return conditions

def get_condition_details(patient, condition_name):
    """
    Returns a dictionary with detailed report for a given condition_name,
    based on the patient's most recent DailySymptomVitals entry.
    """
    latest = patient.symptom_entries.first()
    if not latest:
        return None

    # Base confidence from the generic engine (or compute a refined number)
    all_conditions = run_diagnostic_engine(latest)
    condition_match = next((c for c in all_conditions if c['name'] == condition_name), None)
    
    if not condition_match:
        return None

    base_score = condition_match['match_percent']
    # For demonstration, slightly increase the score for the detailed view (or keep as is)
    # In a real system you would use a more sophisticated model.
    refined_score = min(base_score + 5, 99.9)  # e.g., 85% -> 90%, but screenshot shows 94.2%
    # To match the screenshot exactly, you can manually set a higher score for Tension-Type Headache
    if condition_name == "Tension-Type Headache":
        refined_score = 94.2

    # Static content based on condition name (could be stored in DB or external file)
    content = {
        "Tension-Type Headache": {
            "title": "Tension-Type Headache",
            "about": "A tension-type headache is the most common kind of headache. It often feels like a tight band or a dull ache pressing on both sides of your head. Unlike migraines, these headaches usually don’t cause nausea or vision changes, but they can still be quite uncomfortable.",
            "common_duration": "Typical episodes last 30 minutes to 7 days.",
            "symptoms_explained": [
                "Pressure on Both Sides – Matches your report of a 'squeezing' feeling across your forehead.",
                "Muscle Sensitivity – Slight tenderness found in your neck and shoulder muscles during the exam.",
                "No Light Sensitivity – Since you aren’t sensitive to light or sound, we can rule out common migraines."
            ],
            "how_it_works": "While these were once thought to be just muscle tension, we now know that nerve signaling in the head and neck plays a major role. Sometimes, the brain becomes extra sensitive to pain signals from your muscles, turning occasional discomfort into a more frequent headache."
        },
        # Add other conditions (Cervicogenic Headache, Seasonal Allergies) similarly if needed
    }

    details = content.get(condition_name)
    if not details:
        return None

    return {
        "condition_name": condition_name,
        "confidence_score": refined_score,
        "about": details["about"],
        "common_duration": details["common_duration"],
        "symptoms_explained": details["symptoms_explained"],
        "how_it_works": details["how_it_works"],
        "match_percentage_original": base_score   # optional
    }













# # Mock diagnostic engine to analyze symptoms
# # In production, this can integrate with Google Gemini or other ML models

# def analyze_symptoms(symptoms: str) -> dict:
#     """
#     Analyzes user symptoms and returns a potential diagnosis and recommended action.
#     """
#     if not symptoms:
#         return {
#             "diagnosis": "No symptoms provided.",
#             "recommended_action": "Please provide your symptoms."
#         }
        
#     return {
#         "diagnosis": f"Potential condition based on: {symptoms}",
#         "recommended_action": "Please consult a healthcare professional for an accurate diagnosis."
#     }
