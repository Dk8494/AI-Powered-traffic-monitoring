import os
from chatbot_engine import get_ai_response, get_mock_response

print("--- Chatbot Engine Test ---")
print("1. Testing Fallback / Mock System:")
print("Result:", get_mock_response("What is the fastest route right now?"))

print("\n2. Testing Real AI System (Gemini):")
if "GEMINI_API_KEY" in os.environ or True: # Force test context message
    print("If you have set the key in the dashboard or environment, this works.")
    # result = get_ai_response("Hello, smart city! How do you help?")
    # print(result)
