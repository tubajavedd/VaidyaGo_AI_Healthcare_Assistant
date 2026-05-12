#!/usr/bin/env python3
"""
Test script to simulate chatbot response with medication suggestions
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

def test_chatbot_prompt_for_headache():
    """Test that the prompt includes medication suggestions for headache"""
    print("Testing Chatbot Prompt for Headache...")

    # Build prompt for headache query
    prompt = PromptService.build_prompt("I have a headache", user=None)

    # Check if medication suggestions are in the prompt
    has_headache_section = "headache" in prompt.lower()
    has_paracetamol = "paracetamol" in prompt.lower()
    has_crocin = "crocin" in prompt.lower()

    print(f"Prompt contains headache info: {has_headache_section}")
    print(f"Prompt contains Paracetamol: {has_paracetamol}")
    print(f"Prompt contains Crocin: {has_crocin}")

    # Show a snippet of the medication knowledge section
    if "MEDICATION KNOWLEDGE BASE" in prompt:
        start = prompt.find("MEDICATION KNOWLEDGE BASE")
        end = prompt.find("--- CONVERSATION CONTEXT ---")
        med_section = prompt[start:end][:500]  # First 500 chars
        print(f"\nMedication Knowledge Section (first 500 chars):\n{med_section}...")

    return has_headache_section and has_paracetamol

if __name__ == "__main__":
    print("VaidyaGo Chatbot Medication Response Test")
    print("=" * 50)

    test_pass = test_chatbot_prompt_for_headache()

    print("\n" + "=" * 50)
    print("Test Result:")
    print(f"Medication suggestions in prompt: {'PASS' if test_pass else 'FAIL'}")

    if test_pass:
        print("✅ The chatbot should now suggest medications like Paracetamol (Crocin) for headaches!")
    else:
        print("❌ Medication suggestions not found in prompt.")