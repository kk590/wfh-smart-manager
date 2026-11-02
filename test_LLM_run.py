from src.app import llm_1, llm_2, llm_3, llm_4, llm_5

def test_llm(name, llm_instance):
    print(f"Testing {name} (Model: {llm_instance.model})...")
    try:
        response = llm_instance.call("Say exactly: 'Hello, API is working!'")
        print(f"  Result: {response}")
    except Exception as e:
        print(f"  FAILED: {e}")
    print("-" * 50)

if __name__ == "__main__":
    print("=== Testing All LLMs Individually (sequential) ===\n")

    test_llm("Agent 1 (Parser)", llm_1)
    test_llm("Agent 2 (Generator)", llm_2)
    test_llm("Agent 3 (Critique)", llm_3)
    test_llm("Agent 4 (Loop)", llm_4)
    test_llm("Agent 5 (Sequence)", llm_5)


    print("=== LLM Test Complete ===")
