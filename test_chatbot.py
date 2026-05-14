import os
import sys

# Optional: ensure we can see logs
import logging
logging.basicConfig(level=logging.INFO)

from chatbot_engine import get_ai_response, get_mock_response

print("="*50)
print("1. TESTING MOCK FALLBACK SYSTEM (ZERO-CRASH SAFEGUARD)")
print("="*50)
mock_queries = [
    "What is the fastest route?",
    "Is there an accident?",
    "How is the traffic congestion?",
    "I need an ambulance!"
]
for q in mock_queries:
    print(f"User: '{q}'")
    print(f"Bot : {get_mock_response(q)}\n")

print("="*50)
print("2. TESTING LIVE AI SYSTEM (GEMINI API)")
print("="*50)
ai_queries = [
    "What's the best route to avoid traffic today?",
    "Explain why sudden rain causes gridlock."
]
for q in ai_queries:
    print(f"User: '{q}'")
    print(f"Bot : {get_ai_response(q)}\n")

