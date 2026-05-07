import os
import django
import sys

sys.path.append('d:/directory/vaidyaGo/vaidyaGo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from prescription_management.ocr_service import OCRService

image_path = 'd:/directory/vaidyaGo/vaidyaGo/media/prescriptions/WhatsApp_Image_2026-04-06_at_9_Vhvdxsm.56.50_AM.jpeg'
if os.path.exists(image_path):
    print("Extracting text...")
    text = OCRService.extract_text_from_image(image_path)
    print("--- RAW TEXT ---")
    print(text)
    print("----------------")
else:
    print(f"File not found: {image_path}")
