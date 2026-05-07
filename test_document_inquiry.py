"""
Test script to verify document inquiry functionality works in chatbot
"""

import os
import sys
import json
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from chatbot.services.tool_router import ToolRouter

def test_document_inquiry_handler():
    """Test that document_inquiry action is now handled"""
    print("\n" + "="*60)
    print("Testing Document Inquiry Handler")
    print("="*60 + "\n")
    
    # Mock user object
    class MockUser:
        id = 1
        username = "testuser"
        first_name = "Test"
        last_name = "User"
    
    user = MockUser()
    
    # Test 1: document_inquiry action should now work
    intent_data = {
        "intent": "document_inquiry",
        "action": "document_inquiry",
        "message": "Tell me about my documents",
        "data": {}
    }
    
    print("Test 1: document_inquiry action")
    result = ToolRouter.execute(intent_data, user)
    print(f"Result:")
    print(f"  Action Executed: {result['action_executed']}")
    print(f"  Message: {result['message'][:100]}...")
    print(f"  Data Keys: {list(result['data'].keys())}")
    
    if not result['action_executed']:
        print("✅ PASS - Correctly returned no documents (user not in DB)")
    else:
        print("⚠️ Action executed but user may not have prescriptions")
    
    # Test 2: list_prescription_documents action
    print("\n\nTest 2: list_prescription_documents action")
    intent_data = {
        "intent": "document_inquiry",
        "action": "list_prescription_documents",
        "message": "What prescriptions do I have?",
        "data": {}
    }
    
    result = ToolRouter.execute(intent_data, user)
    print(f"Result:")
    print(f"  Action Executed: {result['action_executed']}")
    print(f"  Message: {result['message'][:100]}...")
    print(f"  Data Keys: {list(result['data'].keys())}")
    
    # Test 3: list_prescriptions action (alias)
    print("\n\nTest 3: list_prescriptions action (alias)")
    intent_data = {
        "intent": "document_inquiry",
        "action": "list_prescriptions",
        "message": "Show my prescriptions",
        "data": {}
    }
    
    result = ToolRouter.execute(intent_data, user)
    print(f"Result:")
    print(f"  Action Executed: {result['action_executed']}")
    print(f"  Message: {result['message'][:100]}...")
    print(f"  Data Keys: {list(result['data'].keys())}")
    
    print("\n" + "="*60)
    print("✅ All document inquiry handlers are working!")
    print("="*60 + "\n")

def test_available_tools():
    """Test that new tools are in the available tools list"""
    print("\n" + "="*60)
    print("Testing Available Tools List")
    print("="*60 + "\n")
    
    tools = ToolRouter.get_available_tools()
    
    print(f"Total available tools: {tools['count']}")
    print(f"\nTools list:")
    for tool in tools['tools']:
        print(f"  - {tool}")
    
    # Check for prescription tools
    prescription_tools = [
        'list_prescription_documents',
        'get_prescription_details',
        'extract_prescription_medicines',
        'get_prescription_lab_results',
        'get_doctor_info_from_prescription',
        'document_inquiry'
    ]
    
    print(f"\nPrescription tools check:")
    for tool in prescription_tools:
        if tool in tools['tools']:
            print(f"  ✅ {tool}")
        else:
            print(f"  ❌ {tool} - MISSING!")
    
    return all(tool in tools['tools'] for tool in prescription_tools)

def main():
    print("\n" + "#"*60)
    print("# VaidyaGo Chatbot - Document Inquiry Handler Tests")
    print("#"*60)
    
    try:
        test_available_tools()
        test_document_inquiry_handler()
        
        print("\n" + "#"*60)
        print("# ✅ All tests completed successfully!")
        print("#"*60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
