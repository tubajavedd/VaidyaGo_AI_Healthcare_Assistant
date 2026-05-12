#!/usr/bin/env python3
"""
Test script to verify medication suggestions in prompt service
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from chatbot.services.prompt_service import PromptService
from chatbot.services.vaidyago_knowledge_base import VaidyaGoKnowledge

def test_medication_knowledge():
    """Test that medication knowledge is loaded"""
    print("Testing Medication Knowledge Base...")

    med_kb = VaidyaGoKnowledge.MEDICATION_SUGGESTIONS
    print(f"Available medication categories: {list(med_kb.keys())}")

    # Test headache suggestions
    headache = med_kb.get('headache', {})
    print(f"Headache suggestions: {headache.get('suggestions', [])}")

    return len(med_kb) > 0

def test_prompt_includes_medication():
    """Test that prompt includes medication knowledge"""
    print("\nTesting Prompt Service...")

    # Build a test prompt
    prompt = PromptService.build_prompt("I have a headache", user=None)

    # Check if medication knowledge is included
    has_medication = "MEDICATION KNOWLEDGE BASE" in prompt
    print(f"Prompt includes medication knowledge: {has_medication}")

    # Check if specific medication is mentioned
    has_paracetamol = "Paracetamol" in prompt
    print(f"Prompt includes Paracetamol: {has_paracetamol}")

    return has_medication and has_paracetamol

if __name__ == "__main__":
    print("VaidyaGo Medication Suggestions Test")
    print("=" * 50)

    test1_pass = test_medication_knowledge()
    test2_pass = test_prompt_includes_medication()

    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Medication Knowledge: {'PASS' if test1_pass else 'FAIL'}")
    print(f"Prompt Integration: {'PASS' if test2_pass else 'FAIL'}")

    if test1_pass and test2_pass:
        print("✅ All tests passed! Medication suggestions are working.")
    else:
        print("❌ Some tests failed. Check the implementation.")