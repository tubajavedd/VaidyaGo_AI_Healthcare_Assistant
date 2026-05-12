from ..models import Diagnostic
from .ai_service import AIService
import json

class DiagnosticService:
    def __init__(self):
        self.ai_service = AIService()

    def get_or_create_diagnosis(self, user, body_part, sub_region, symptoms, duration, severity):
        # 1. Search for existing diagnosis (cache check)
        sorted_symptoms = sorted(symptoms)
        
        # SQLite doesn't support __contains for JSON lists, so we use a more compatible approach
        # For small databases, filtering by body_part and then checking symptoms in Python is safe
        existing_list = Diagnostic.objects.filter(
            body_part=body_part,
            sub_region=sub_region
        )
        
        existing = None
        for diag in existing_list:
            if sorted(diag.symptoms) == sorted_symptoms:
                existing = diag
                break

        if existing:
            return existing, True

        # 2. Call AI Service if not found
        ai_data = self.ai_service.analyze_symptoms(
            body_part, sub_region, symptoms, duration, severity
        )

        # 3. Save new diagnosis
        diagnosis = Diagnostic.objects.create(
            user=user,
            body_part=body_part,
            sub_region=sub_region,
            symptoms=symptoms,
            duration=duration,
            severity=severity,
            possible_diseases=ai_data.get('possible_diseases', []),
            recommendations=ai_data.get('recommendations', []),
            precautions=ai_data.get('precautions', []),
            consultation_advice=ai_data.get('consultation_advice', ''),
            confidence_score=ai_data.get('confidence_score', 0.0),
            ai_response=json.dumps(ai_data)
        )

        return diagnosis, False
