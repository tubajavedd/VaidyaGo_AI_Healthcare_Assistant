import base64
import json
import logging
import os
import re
import sys
import time
import requests

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class OCRService:

    _vision_rate_limit_count = 0
    _vision_rate_limit_threshold = 2
    @staticmethod
    def normalize_extracted_data(data):
        """
        Universal medical document normalizer.
        Supports:
        - prescription
        - lab report
        - scan report
        - ultrasound
        - discharge summary
        """

        default_response = {
            "document_type": None,
            "doctor_name": None,
            "hospital_name": None,
            "report_date": None,
            "patient_name": None,
            "summary": None,
            "findings": [],
            "medicines": [],
            "test_results": [],
            "recommendations": []
        }

        if not data:
            return default_response

        if "doctor_name" in data or "hospital_name" in data:
            data.setdefault("document_type", "medical_document")
            data.setdefault("report_date", data.get("prescription_date"))
            data.setdefault("summary", "Medical document analyzed successfully.")
            data.setdefault("findings", [])
            data.setdefault("test_results", [])
            data.setdefault("recommendations", [])

            return data

        report = data.get("prescription_details", data)

        doctor = (
            report.get("doctor", {})
            or report.get("doctor_info", {})
            or report.get("doctor_details", {})
        )

        patient = (
            report.get("patient", {})
            or report.get("patient_info", {})
            or report.get("patient_details", {})
        )

        clinic = (
            report.get("clinic", {})
            or report.get("clinic_info", {})
            or report.get("clinic_details", {})
        )

        raw_medicines = (
            report.get("prescriptions")
            or report.get("prescription")
            or report.get("prescribed_medicines")
            or report.get("treatment_advised")
            or []
        )

        medicines = []

        for med in raw_medicines:
            medicines.append({
                "name": (
                    med.get("medicine_name")
                    or med.get("medicine")
                    or med.get("medication")
                    or med.get("name")
                    or "Unknown"
                ),
                "dosage": med.get("dosage"),
                "frequency": (
                    med.get("frequency")
                    or med.get("frequency_and_timing")
                ),
                "duration_days": OCRService.extract_number(
                    med.get("duration") or med.get("instructions")
                ),
                "instructions": (
                    med.get("instructions")
                    or med.get("timing")
                )
            })

        findings = report.get("impressions") or []
        if isinstance(findings, str):
            findings = [findings]

        recommendations = (
            report.get("doctor_advice")
            or report.get("advice")
            or report.get("notes")
            or []
        )

        if isinstance(recommendations, str):
            recommendations = [recommendations]

        test_results = []

        ultrasound = report.get("ultrasound_findings", {})
        if ultrasound:
            for key, value in ultrasound.items():
                test_results.append({
                    "test": key,
                    "result": str(value)
                })

        return {
            "document_type": OCRService.detect_document_type(report),
            "doctor_name": doctor.get("name"),
            "hospital_name": doctor.get("hospital") or clinic.get("name"),
            "report_date": (
                patient.get("date")
                or patient.get("episode_date")
            ),
            "patient_name": patient.get("name"),

            "summary": OCRService.generate_summary(report),

            "findings": findings,
            "medicines": medicines,
            "test_results": test_results,
            "recommendations": recommendations
        }
######ADD DCOTUMENT DETECTOR
    @staticmethod
    def detect_document_type(data):

        if data.get("ultrasound_findings"):
            return "scan_report"

        if data.get("impressions"):
            return "lab_report"

        if data.get("prescriptions") or data.get("prescribed_medicines"):
            return "prescription"

        return "medical_document"
###ADD patient friendly summary generator
    @staticmethod
    def generate_summary(data):

        if data.get("diagnosis"):
            return f"Patient diagnosed with {data.get('diagnosis')}."

        if data.get("impressions"):
            findings = data.get("impressions")
            if isinstance(findings, list):
                findings = ", ".join(findings)
            return f"Report shows: {findings}"

        return "Medical document analyzed successfully."
    @staticmethod
    def extract_number(value):
        if not value:
            return None

        import re
        match = re.search(r"\d+", str(value))
        return int(match.group()) if match else None
    # =========================================================
    # MAIN ENTRY POINT (FIXED - THIS WAS YOUR ERROR)
    # =========================================================
    @staticmethod
    def extract_prescription_details(image_path: str):

        print("\n========== OCR PIPELINE START ==========")
        print("IMAGE PATH:", image_path)

        # ---------------- VISION ----------------
        print("\n[STEP 1] TRYING VISION API")

        vision_result = OCRService.extract_prescription_details_via_vision(image_path)

        print("\nVISION RESULT:")
        print(vision_result)

        if vision_result:
            print("\nVISION SUCCESS")

            normalized = OCRService.normalize_extracted_data(vision_result)

            print("\nNORMALIZED RESULT:")
            print(normalized)

            return normalized

        print("\nVISION FAILED")

        # ---------------- OCR ----------------
        print("\n[STEP 2] TRYING OCR")

        raw_text = OCRService.extract_text_from_image(image_path)

        print("\nRAW OCR TEXT:")
        print(raw_text)

        if not raw_text:
            print("\nOCR FAILED")
            return None

        print("\nOCR SUCCESS")

        # ---------------- LLM ----------------
        print("\n[STEP 3] TRYING LLM PARSER")

        llm_result = OCRService._extract_via_llm(raw_text)

        print("\nLLM RESULT:")
        print(llm_result)

        if llm_result:
            print("\nLLM SUCCESS")

            normalized = OCRService.normalize_extracted_data(llm_result)

            print("\nNORMALIZED RESULT:")
            print(normalized)

            return normalized

        print("\nLLM FAILED")
        print("\n========== OCR PIPELINE END ==========")

        return None
    # =========================================================
    # VISION EXTRACTION
    # =========================================================
    @staticmethod
    def extract_prescription_details_via_vision(image_path: str):

        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            return None

        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()

        except Exception as e:
            logger.error(f"Image read error: {e}")
            return None

        payload = {
            "model": "pixtral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract prescription in structured JSON format."
                        }
                    ]
                }
            ],
            "temperature": 0
        }

        try:
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )

            if not response.ok:
                return None

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            return OCRService._parse_json_response(content)

        except Exception as e:
            logger.error(f"Vision error: {e}")
            return None

    # =========================================================
    # OCR FALLBACK (TESSERACT)
    # =========================================================
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:

        try:
            import cv2
            import pytesseract
            from PIL import Image

            if sys.platform == "win32":
                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            img = cv2.imread(image_path)

            if img is None:
                image = Image.open(image_path)
                return pytesseract.image_to_string(image)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)

            _, thresh = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            text = pytesseract.image_to_string(
                thresh,
                config="--oem 3 --psm 6"
            )

            logger.info("OCR extracted text successfully")

            print("\nRAW OCR TEXT:\n", text)

            return text

        except Exception as e:
            logger.error(f"OCR error: {e}")
            return ""

    # =========================================================
    # OCR + LLM PIPELINE
    # =========================================================
    @staticmethod
    def extract_prescription_details_via_ocr(image_path: str):

        raw_text = OCRService.extract_text_from_image(image_path)

        if not raw_text:
            return None

        return OCRService._extract_via_llm(raw_text)

    # =========================================================
    # SIMPLE LLM PARSER (PLACEHOLDER SAFE)
    # =========================================================
    @staticmethod
    def _extract_via_llm(raw_text: str):

        from chatbot.services.mistral_service import MistralService

        prompt = f"""
        You are a medical document analysis system.

        The uploaded file can be ANY of:
        - prescription
        - blood test
        - ultrasound
        - scan report
        - discharge summary
        - lab report

        Return ONLY valid JSON.

        IMPORTANT:
        1. Detect document type.
        2. Extract important medical findings.
        3. If medicines exist, extract medicines.
        4. Convert difficult medical report into patient-friendly summary.

        Return EXACTLY this schema:

        {{
            "document_type": null,
            "doctor_name": null,
            "hospital_name": null,
            "report_date": null,
            "patient_name": null,
            "summary": null,
            "findings": [],
            "special_instructions": null,
            "medicines": [],
            "test_results": [],
            "recommendations": []
        }}

        Document text:
        {raw_text}
        """
        response = MistralService.generate_raw_response(prompt)

        return OCRService._parse_json_response(response)

    # =========================================================
    # JSON PARSER SAFETY
    # =========================================================
    @staticmethod
    def _parse_json_response(text: str):
        try:
            import json
            import re

            if not text:
                return None

            cleaned = text.strip()

            # remove markdown
            cleaned = re.sub(r"```json", "", cleaned)
            cleaned = re.sub(r"```", "", cleaned)

            # extract JSON block safely
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                cleaned = match.group()

            return json.loads(cleaned)

        except Exception as e:
            logger.error(f"JSON parse failed: {e}")
            logger.error(f"Raw response was: {text}")
            return None

    # =========================================================
    # VALIDATION
    # =========================================================
    @staticmethod
    def _validate_and_enrich(data: dict):

        if not isinstance(data, dict):
            return None

        # -------- possible key variations ----------
        doctor_data = (
            data.get("doctor")
            or data.get("doctor_info")
            or data.get("doctor_details")
            or {}
        )

        patient_data = (
            data.get("patient")
            or data.get("patient_info")
            or data.get("patient_details")
            or {}
        )

        clinic_data = (
            data.get("clinic")
            or data.get("clinic_info")
            or data.get("hospital")
            or {}
        )

        medicines_source = (
            data.get("prescription")
            or data.get("medicines")
            or data.get("treatment_advised")
            or []
        )

        medicines = []

        import re

        for med in medicines_source:
            duration_raw = med.get("duration") or med.get("duration_days")

            duration_number = None
            if duration_raw:
                match = re.search(r"\d+", str(duration_raw))
                if match:
                    duration_number = int(match.group())

            medicines.append({
                "name": (
                    med.get("medicine")
                    or med.get("medication")
                    or med.get("name")
                ),
                "dosage": med.get("dosage"),
                "frequency": med.get("frequency") or med.get("dosage"),
                "duration_days": duration_number,
                "instructions": (
                    med.get("instructions")
                    or med.get("timing")
                )
            })

        return {
            "doctor_name": doctor_data.get("name"),
            "hospital_name": clinic_data.get("name"),
            "prescription_date": (
                patient_data.get("date")
                or patient_data.get("episode_date")
            ),
            "patient_name": patient_data.get("name"),
            "special_instructions": (
                data.get("remarks")
                or data.get("consultant_notes")
                or data.get("notes")
            ),
            "medicines": medicines
        }