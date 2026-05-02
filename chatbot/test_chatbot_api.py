"""
Test Script for Vado AI Chatbot API

Usage:
    python test_chatbot_api.py
"""

import requests
import json
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/vado/chat/"
TOOLS_ENDPOINT = f"{BASE_URL}/api/vado/tools/"
TOOLS_DESCRIPTION_ENDPOINT = f"{BASE_URL}/api/vado/tools-description/"


class ChatbotTester:
    """Test helper for Vado AI Chatbot API"""

    @staticmethod
    def send_message(message: str) -> Dict[str, Any]:
        """Send a message to the chatbot"""
        print(f"\n📝 Sending: {message}")
        print("-" * 60)

        try:
            response = requests.post(
                CHAT_ENDPOINT,
                json={"message": message},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✓ Response received")
                print(json.dumps(data, indent=2))
                return data
            else:
                print(f"✗ Error: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return None

    @staticmethod
    def get_available_tools(category: str = None) -> Dict[str, Any]:
        """Get available tools/actions"""
        url = TOOLS_ENDPOINT
        if category:
            url += f"?category={category}"

        print(f"\n🔧 Fetching available tools{f' ({category})' if category else ''}...")
        print("-" * 60)

        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                data = response.json()
                print(f"✓ Tools retrieved")
                print(json.dumps(data, indent=2))
                return data
            else:
                print(f"✗ Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return None

    @staticmethod
    def get_tools_description() -> Dict[str, Any]:
        """Get detailed description of all tools"""
        print(f"\n📚 Fetching tools description...")
        print("-" * 60)

        try:
            response = requests.get(TOOLS_DESCRIPTION_ENDPOINT, timeout=30)

            if response.status_code == 200:
                data = response.json()
                print(f"✓ Description retrieved")
                print(json.dumps(data, indent=2))
                return data
            else:
                print(f"✗ Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return None


def main():
    """Run test suite"""
    print("=" * 60)
    print("VADO AI CHATBOT API TEST SUITE")
    print("=" * 60)

    # Test 1: Get available tools
    print("\n[TEST 1] Getting available tools...")
    ChatbotTester.get_available_tools()

    # Test 2: Get tools description
    print("\n[TEST 2] Getting tools description...")
    ChatbotTester.get_tools_description()

    # Test 3: Chat with simple message
    print("\n[TEST 3] Simple chat message...")
    ChatbotTester.send_message("Hello, how can you help me?")

    # Test 4: Appointment booking
    print("\n[TEST 4] Book appointment request...")
    ChatbotTester.send_message(
        "I want to book an appointment with Dr. Smith on Monday at 10 AM"
    )

    # Test 5: Get prescriptions
    print("\n[TEST 5] Get prescriptions request...")
    ChatbotTester.send_message("What are my active prescriptions?")

    # Test 6: Medication reminder
    print("\n[TEST 6] Set medication reminder...")
    ChatbotTester.send_message(
        "Set a reminder for my aspirin at 8 AM every morning"
    )

    # Test 7: Get notifications
    print("\n[TEST 7] Get notifications...")
    ChatbotTester.send_message("Show me my recent notifications")

    # Test 8: Specific category tools
    print("\n[TEST 8] Get appointment tools only...")
    ChatbotTester.get_available_tools("appointments")

    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
