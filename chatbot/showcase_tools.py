"""
Interactive Tool Showcase
Run this to see all available tools and their descriptions
"""

from chatbot.services.tools_registry import ToolsRegistry
import json

def display_tools_by_category():
    """Display tools organized by category"""
    registry = ToolsRegistry()
    summary = registry.get_tools_summary()
    
    print("\n" + "="*80)
    print("VADO AI CHATBOT - AVAILABLE TOOLS & APIS")
    print("="*80)
    
    for category in sorted(summary.keys()):
        tools = summary[category]
        print(f"\n📂 {category.upper()} ({len(tools)} tools)")
        print("-" * 80)
        
        for i, tool in enumerate(tools, 1):
            print(f"\n  {i}. {tool['name']}")
            print(f"     Description: {tool['description']}")
            
            # Get full tool details
            full_tool = ToolsRegistry.get_tool(tool['name'])
            if full_tool:
                print(f"     Endpoint: {full_tool.get('endpoint')}")
                print(f"     Method: {full_tool.get('method')}")
                
                if full_tool.get('parameters'):
                    params = full_tool['parameters']
                    print(f"     Parameters: {', '.join(params.keys())}")
    
    print("\n" + "="*80)
    print(f"TOTAL AVAILABLE TOOLS: {len(registry.get_all_tools())}")
    print("="*80)
    
    # Print categories summary
    categories = registry.get_categories()
    print(f"\nCATEGORIES: {', '.join(categories)}\n")


def display_example_prompts():
    """Show example user prompts that chatbot can handle"""
    print("\n" + "="*80)
    print("EXAMPLE USER PROMPTS & CHATBOT RESPONSES")
    print("="*80)
    
    examples = [
        {
            "prompt": "Book an appointment with Dr. Smith on Monday at 10 AM",
            "intent": "book_appointment",
            "tool": "book_appointment"
        },
        {
            "prompt": "What are my active prescriptions?",
            "intent": "prescriptions",
            "tool": "get_prescriptions"
        },
        {
            "prompt": "Cancel my appointment on Friday",
            "intent": "cancel_appointment",
            "tool": "cancel_appointment"
        },
        {
            "prompt": "Show me available slots for Dr. Johnson",
            "intent": "slots",
            "tool": "get_doctor_slots"
        },
        {
            "prompt": "Set a reminder for my aspirin at 8 AM daily",
            "intent": "reminder",
            "tool": "set_reminder"
        },
        {
            "prompt": "What are my recent notifications?",
            "intent": "notifications",
            "tool": "get_notifications"
        },
        {
            "prompt": "I want to pay for my last appointment",
            "intent": "payment",
            "tool": "make_payment"
        },
        {
            "prompt": "Update my profile with new phone number",
            "intent": "profile",
            "tool": "update_user_profile"
        },
        {
            "prompt": "Get my payment history",
            "intent": "payment",
            "tool": "get_payment_history"
        },
        {
            "prompt": "Rate my last appointment with Dr. Smith",
            "intent": "feedback",
            "tool": "submit_feedback"
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"\n{i}. User: \"{ex['prompt']}\"")
        print(f"   Intent: {ex['intent']}")
        print(f"   Tool Called: {ex['tool']}")
        print(f"   Result: ✓ Executed automatically")


def display_llm_backends():
    """Display LLM backend options and their priorities"""
    print("\n" + "="*80)
    print("LLM BACKEND SUPPORT - AUTOMATIC FALLBACK CHAIN")
    print("="*80)
    
    backends = [
        {
            "name": "Local TinyLlama Model",
            "priority": 1,
            "pros": ["No API key needed", "Fastest", "Works offline", "No rate limits"],
            "cons": ["Requires GPU memory", "Lower quality"],
            "setup": "pip install torch transformers"
        },
        {
            "name": "OpenAI API (GPT-3.5/GPT-4)",
            "priority": 2,
            "pros": ["High quality", "Fastest response", "Best accuracy"],
            "cons": ["Requires API key", "Costs money", "Rate limited"],
            "setup": "pip install openai && export OPENAI_API_KEY=sk-..."
        },
        {
            "name": "HuggingFace API",
            "priority": 3,
            "pros": ["Free tier available", "No local resources needed"],
            "cons": ["Your current setup (404 issue)", "Rate limited", "Slower"],
            "setup": "Already configured (HF_API_KEY in .env)"
        },
        {
            "name": "Fallback JSON Parser",
            "priority": 4,
            "pros": ["Always works", "No external calls"],
            "cons": ["Limited intelligence"],
            "setup": "Built-in, no setup needed"
        }
    ]
    
    for backend in backends:
        print(f"\n[Priority {backend['priority']}] {backend['name']}")
        print(f"Setup: {backend['setup']}")
        print(f"Pros: {', '.join(backend['pros'])}")
        print(f"Cons: {', '.join(backend['cons'])}")


def display_flow_diagram():
    """Show how the chatbot processes requests"""
    print("\n" + "="*80)
    print("CHATBOT REQUEST FLOW")
    print("="*80)
    
    print("""
    
    ┌──────────────────────────────┐
    │   User Message               │
    │ "Book appointment Monday 10"  │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Prompt Service              │
    │ - Add system prompt           │
    │ - Add available tools         │
    │ - Add context                 │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   LLM Service                 │
    │ Try: Local → OpenAI → HF → ?  │
    │ Returns: JSON response        │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Intent Service              │
    │ Parse JSON:                   │
    │ - Extract "action"            │
    │ - Extract "data"              │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Tool Router                 │
    │ - Check if tool exists        │
    │ - Validate parameters         │
    │ - Call API endpoint           │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Your API Endpoint           │
    │ /api/appointments/create/     │
    │ [Django View]                 │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Database                    │
    │ Appointment Created ✓         │
    └──────────────┬───────────────┘
                   │
                   ↓
    ┌──────────────────────────────┐
    │   Response to User            │
    │ "Appointment booked at 10 AM" │
    └──────────────────────────────┘
    """)


if __name__ == "__main__":
    print("\n\n")
    display_tools_by_category()
    display_example_prompts()
    display_llm_backends()
    display_flow_diagram()
    
    print("\n" + "="*80)
    print("✨ CHATBOT INTEGRATION COMPLETE ✨")
    print("="*80)
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Test: python chatbot/test_chatbot_api.py")
    print("3. Read: CHATBOT_INTEGRATION_GUIDE.md")
    print("\n")
