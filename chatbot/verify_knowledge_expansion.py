import json
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from chatbot.services.llm_service import LLMService

def test_query(message):
    print(f"\nQUERY: {message}")
    # We simulate the prompt structure that the actual view uses
    prompt = f"--- USER MESSAGE ---\n{message}\n"
    response_json = LLMService.generate_response(prompt)
    response = json.loads(response_json)
    try:
        print(f"REPLY: {response.get('message')}")
    except UnicodeEncodeError:
        print(f"REPLY: {response.get('message').encode('ascii', 'ignore').decode('ascii')} (Note: Emojis stripped for terminal display)")
    print(f"INTENT: {response.get('intent')}")
    return response

test_cases = [
    "Hi",
    "what is vaidyago",
    "Is VaidyaGo legit?",
    "Do you accept Ayushman insurance?",
    "How much does consultation cost?",
    "I feel anxious and need help.",
    "Can I book a blood test?",
    "analyze my report",
    "bok apointment",
    "i have chest pain",
    "Are you a robot?"
]

print("=" * 50)
print("VERIFYING VAIDYAGO KNOWLEDGE EXPANSION")
print("=" * 50)

for case in test_cases:
    test_query(case)

print("\n" + "=" * 50)
print("VERIFICATION COMPLETE")
print("=" * 50)
