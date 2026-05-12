import json
import re

def _extract_json(text):
    if not isinstance(text, str):
        return {"intent": "chat", "message": str(text), "data": {}}

    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r'^```[a-z]*\n', '', cleaned_text)
        cleaned_text = re.sub(r'\n```$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()

    start = cleaned_text.find("{")
    end = cleaned_text.rfind("}") + 1
    
    if start < 0 or end <= start:
        return {"intent": "chat", "message": text, "data": {}}

    json_str = cleaned_text[start:end]

    json_str = re.sub(r'"\s*\+\s*\\n\s*"', '', json_str)
    json_str = re.sub(r'"\s*\+\s*"\s*\n\s*', '', json_str)
    json_str = re.sub(r'"\s*\+\s*', '', json_str)
    json_str = re.sub(r'\s*\+\s*"', '', json_str)

    try:
        payload = json.loads(json_str)
        return payload if isinstance(payload, dict) else {"intent": "chat", "message": text, "data": {}}
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {e}")
        try:
            cleaned = json_str.replace("\n", " ").replace("\r", " ")
            return json.loads(cleaned)
        except Exception as e2:
            print(f"JSON ERROR 2: {e2}")
            return {"intent": "chat", "message": text, "data": {}}

test_text = """```json
{
  "action": "get_prescriptions",
  "action_data": {
    "doctor_id": "testdo",
    "phone_number": "+919936543210"
  },
  "message": "Acha ji, theek hai... toh aap apni prescription ke hisaab se reminder set karna chahte hain, right? Bas ek minute, main aapki latest prescription check kar leti hoon... usme jo medicines hain, unke reminders set kar dete hain. Thoda rukiye na?"
}
```"""

print(json.dumps(_extract_json(test_text), indent=2))
