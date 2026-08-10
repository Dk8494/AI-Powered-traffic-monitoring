import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

def get_mock_response(query):
    """Fallback rule-based engine if AI API is missing/fails."""
    query = query.lower()
    if 'traffic' in query or 'congestion' in query:
        return "🚗 **Congestion Update:** Based on current models, expect a minor 10-minute delay on major highways. Alternative routes are flowing smoothly."
    elif 'route' in query or 'fastest' in query:
        return "🗺️ **Route Suggestion:** I recommend taking the AI Optimized Route. It bypasses current bottlenecks and improves fuel efficiency."
    elif 'accident' in query or 'crash' in query:
        return "⚠️ **Incident Report:** No major accidents reported on your immediate corridor. Emergency protocols remain on standby."
    else:
        return "🤖 **System Online:** I am your Smart City AI Assistant. I can analyze millions of data points across the city grid. Ask me about *traffic*, *routes*, or *accidents*!"

def get_ai_response(query):
    """Uses Google Gemini Generative AI to respond in real-time."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return get_mock_response(query)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_context = (
            "You are an advanced AI Smart Traffic Assistant for a futuristic city dashboard. "
            "You help users with live traffic analysis, route optimization, smart city concepts, "
            "and commuting advice. Keep responses concise, highly informative, and use a professional "
            "yet slightly futuristic tone. User query: "
        )
        response = model.generate_content(system_context + query)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        return get_mock_response(query)

# NOTE: Streamlit UI removed. Frontend should call `get_ai_response(query)`
# or use the Flask `/api/chat` endpoint implemented in `api.py`.
