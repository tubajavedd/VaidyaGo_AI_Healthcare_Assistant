import os
import json
from groq import Groq
from django.conf import settings

class AIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def analyze_symptoms(self, body_part, sub_region, symptoms, duration, severity):
        prompt = f"""
        As a medical AI diagnostic assistant, analyze the following:
        Body Part: {body_part}
        Sub-Region: {sub_region}
        Symptoms: {', '.join(symptoms)}
        Duration: {duration}
        Severity: {severity}

        Provide a detailed diagnostic report in JSON format with the following keys:
        - possible_diseases: (list of strings)
        - confidence_score: (float between 0 and 100)
        - recommendations: (list of strings)
        - precautions: (list of strings)
        - consultation_advice: (string)
        - summary: (string)

        Ensure the response is ONLY the JSON object.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful medical assistant. Always return JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            # Fallback or log error
            raise Exception(f"AI Service Error: {str(e)}")
