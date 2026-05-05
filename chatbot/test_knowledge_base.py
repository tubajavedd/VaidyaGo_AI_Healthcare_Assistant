"""
VaidyaGo Knowledge Base Integration - Test and Usage Guide

This demonstrates how the knowledge base is integrated into the chatbot.
"""

from chatbot.services.vaidyago_knowledge_base import VaidyaGoKnowledge


def test_knowledge_base():
    """
    Test VaidyaGo knowledge base queries.
    """
    
    test_queries = [
        "What is VaidyaGo?",
        "Tell me about VaidyaGo",
        "Who are you?",
        "What is Vado?",
        "What are VaidyaGo features?",
        "How do I book an appointment?",
        "How do I cancel an appointment?",
        "Is VaidyaGo safe?",
        "Why is VaidyaGo different?",
        "What languages does VaidyaGo support?",
    ]

    print("=" * 80)
    print("VAIDYAGO KNOWLEDGE BASE - TEST QUERIES")
    print("=" * 80)

    for query in test_queries:
        print(f"\nUser: {query}")
        answer = VaidyaGoKnowledge.get_answer(query)
        if answer:
            print(f"Vado: {answer[:150]}...")  # Print first 150 chars
        else:
            print("Vado: [No direct answer, would use fallback]")

    print("\n" + "=" * 80)
    print("PLATFORM OVERVIEW")
    print("=" * 80)
    
    overview = VaidyaGoKnowledge.get_platform_overview()
    print(f"\nPlatform Name: {overview['platform']['name']}")
    print(f"Tagline: {overview['platform']['tagline']}")
    print(f"\nCore Features: {len(overview['core_features'])} features")
    for feature_key, feature in overview['core_features'].items():
        print(f"  - {feature['title']}: {feature['description']}")

    print(f"\nCore Modules: {len(overview['modules'])} modules")
    for module_key, module in overview['modules'].items():
        print(f"  - {module['name']}: {module['purpose']}")

    print(f"\nWhy VaidyaGo Stands Out:")
    for reason in overview['why_special']:
        print(f"  - {reason}")

    print(f"\nFuture Possibilities:")
    for feature_key, feature_desc in overview['future'].items():
        print(f"  - {feature_key.replace('_', ' ').title()}: {feature_desc}")


def test_faq():
    """
    Display all FAQ items.
    """
    print("\n" + "=" * 80)
    print("VAIDYAGO FAQ")
    print("=" * 80)
    
    faqs = VaidyaGoKnowledge.get_all_faq()
    for idx, (key, faq) in enumerate(faqs.items(), 1):
        print(f"\n{idx}. Q: {faq['question']}")
        print(f"   A: {faq['answer'][:100]}...")


def test_search():
    """
    Test knowledge base search functionality.
    """
    print("\n" + "=" * 80)
    print("VAIDYAGO KNOWLEDGE BASE - SEARCH")
    print("=" * 80)
    
    search_queries = [
        "appointment booking",
        "doctor search",
        "vado assistant",
        "features",
    ]

    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        results = VaidyaGoKnowledge.search_knowledge(query)
        if results:
            for result in results[:2]:  # Show first 2 results
                if isinstance(result, dict) and 'title' in result:
                    print(f"  - {result['title']}: {result['description']}")
                elif isinstance(result, dict) and 'name' in result:
                    print(f"  - {result['name']}")


if __name__ == "__main__":
    test_knowledge_base()
    test_faq()
    test_search()
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
