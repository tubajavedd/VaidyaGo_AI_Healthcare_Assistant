"""
Quick Start Guide for Vado AI Chatbot

This script helps set up and test the chatbot integration.
Run: python manage.py shell < setup_chatbot.py
"""

from chatbot.services.tools_registry import ToolsRegistry
from chatbot.services.prompt_service import PromptService

# Print available tools
print("=" * 80)
print("VADO AI CHATBOT - AVAILABLE TOOLS")
print("=" * 80)

registry = ToolsRegistry()

# Print by category
for category in registry.get_categories():
    tools = registry.get_tools_by_category(category)
    print(f"\n{category.upper()} ({len(tools)} tools):")
    for tool_name, tool in tools.items():
        print(f"  • {tool_name}")
        print(f"    {tool['description']}")

print("\n" + "=" * 80)
print("TOTAL TOOLS:", len(registry.get_all_tools()))
print("=" * 80)

# Test prompt generation
print("\nTesting prompt generation...")
test_message = "Book an appointment with a doctor"
prompt = PromptService.build_prompt(test_message)
print(f"\nGenerated prompt (first 500 chars):\n{prompt[:500]}...\n")

print("✓ Chatbot setup complete!")
print("\nTo test the chatbot API:")
print("1. Start Django server: python manage.py runserver")
print("2. Send POST request to: http://localhost:8000/api/vado/chat/")
print("3. Example payload: {'message': 'Book an appointment'}")
