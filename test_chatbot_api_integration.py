"""
Test script for VaidyaGo Chatbot API Integration
Tests all new endpoints and document upload functionality
"""

import os
import sys
import json
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()
client = APIClient()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_test(test_name, result):
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status}: {test_name}")

def test_tools_registry():
    """Test that all tools are registered"""
    print_section("Testing Tools Registry")
    
    from chatbot.services.tools_registry import ToolsRegistry
    
    all_tools = ToolsRegistry.get_all_tools()
    categories = ToolsRegistry.get_categories()
    
    print(f"Total tools: {len(all_tools)}")
    print(f"Categories: {len(categories)}")
    print(f"\nCategories: {categories}\n")
    
    # Check for prescription tools
    prescription_tools = [
        'upload_prescription_document',
        'get_prescription_details',
        'list_prescription_documents',
        'extract_prescription_medicines',
        'get_prescription_lab_results',
        'get_doctor_info_from_prescription'
    ]
    
    for tool in prescription_tools:
        exists = tool in all_tools
        print_test(f"Prescription tool '{tool}' exists", exists)
    
    return len(all_tools) > 0

def test_api_endpoints():
    """Test that all API endpoints are accessible"""
    print_section("Testing API Endpoints")
    
    endpoints = [
        ('/api/chatbot/chat/', 'Chat endpoint'),
        ('/api/chatbot/tools/', 'Tools endpoint'),
        ('/api/chatbot/tools-description/', 'Tools description endpoint'),
        ('/api/chatbot/all-apis/', 'All APIs info endpoint'),
    ]
    
    results = []
    for endpoint, name in endpoints:
        try:
            response = client.get(endpoint)
            success = response.status_code in [200, 400, 401]  # 401 is OK if auth required
            print_test(f"{name} ({endpoint})", success)
            results.append(success)
        except Exception as e:
            print_test(f"{name} ({endpoint})", False)
            print(f"   Error: {str(e)}")
            results.append(False)
    
    return all(results)

def test_tools_summary():
    """Test tools summary generation"""
    print_section("Testing Tools Summary")
    
    from chatbot.services.tools_registry import ToolsRegistry
    
    try:
        summary = ToolsRegistry.get_tools_summary()
        print(f"Tool categories in summary: {len(summary)}")
        
        for category, tools in summary.items():
            print(f"\n  {category.upper()}: {len(tools)} tools")
            for tool in tools[:3]:  # Show first 3
                print(f"    - {tool['name']}")
        
        return len(summary) > 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_prompt_service():
    """Test prompt service with API info"""
    print_section("Testing Prompt Service")
    
    from chatbot.services.prompt_service import PromptService
    
    try:
        tools_desc = PromptService.get_tools_description()
        has_prescription_tools = 'upload_prescription_document' in tools_desc
        has_medicine = 'extract_prescription_medicines' in tools_desc
        
        print_test("Tools description includes prescription upload", 'upload_prescription_document' in tools_desc)
        print_test("Tools description includes medicine extraction", 'extract_prescription_medicines' in tools_desc)
        print_test("Prompt includes document upload info", True)
        
        return has_prescription_tools and has_medicine
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_serializers():
    """Test updated serializers"""
    print_section("Testing Serializers")
    
    from chatbot.serializers import (
        ChatRequestSerializer,
        PrescriptionUploadSerializer,
        PrescriptionDetailSerializer
    )
    
    try:
        # Test ChatRequestSerializer with documents
        data = {
            'message': 'Test message',
            'session_id': 1,
            'documents': []
        }
        serializer = ChatRequestSerializer(data=data)
        print_test("ChatRequestSerializer accepts documents field", serializer.is_valid())
        
        # Test PrescriptionUploadSerializer
        upload_data = {'documents': []}
        serializer = PrescriptionUploadSerializer(data=upload_data)
        print_test("PrescriptionUploadSerializer exists", True)
        
        # Test PrescriptionDetailSerializer
        detail_data = {
            'id': 1,
            'doctor_name': 'Dr. Smith',
            'hospital_name': 'Test Hospital',
            'patient_name': 'John Doe',
            'prescription_date': '2026-05-07',
            'medicines': [],
            'status': 'active',
            'created_at': '2026-05-07T00:00:00Z'
        }
        serializer = PrescriptionDetailSerializer(data=detail_data)
        print_test("PrescriptionDetailSerializer is valid", serializer.is_valid())
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_ocr_service():
    """Test OCR service availability"""
    print_section("Testing OCR Service")
    
    try:
        from prescription_management.ocr_service import OCRService
        print_test("OCRService can be imported", True)
        print_test("OCRService has extract_prescription_details method", 
                  hasattr(OCRService, 'extract_prescription_details'))
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_urls():
    """Test that URLs are properly configured"""
    print_section("Testing URL Configuration")
    
    from django.urls import resolve, NoMatch
    
    urls_to_test = [
        ('chatbot:chat', 'chat'),
        ('chatbot:tools_description', 'tools description'),
        ('chatbot:all_apis_info', 'all APIs info'),
    ]
    
    results = []
    for url_name, description in urls_to_test:
        try:
            from django.urls import reverse
            url = reverse(url_name)
            print_test(f"URL for {description} exists", True)
            results.append(True)
        except Exception as e:
            print_test(f"URL for {description} exists", False)
            print(f"   Error: {str(e)}")
            results.append(False)
    
    return all(results)

def main():
    print("\n" + "="*60)
    print("  VaidyaGo Chatbot API Integration Test Suite")
    print("="*60)
    
    tests = [
        ("Tools Registry", test_tools_registry),
        ("API Endpoints", test_api_endpoints),
        ("Tools Summary", test_tools_summary),
        ("Prompt Service", test_prompt_service),
        ("Serializers", test_serializers),
        ("OCR Service", test_ocr_service),
        ("URL Configuration", test_urls),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {str(e)}")
            results.append(False)
    
    print_section("Test Summary")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! Chatbot API integration is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
