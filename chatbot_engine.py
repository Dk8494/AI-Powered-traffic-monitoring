import streamlit as st
import time
import os
import logging

logger = logging.getLogger(__name__)

# --- Optional AI API Integration ---
# Try importing google.generativeai for actual AI. 
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

def get_mock_response(query):
    """
    FALLBACK RULE-BASED ENGINE: 
    Returns predefined smart traffic responses based on keywords if AI API fails or is not configured.
    Ensures 0% crash rate during hackathon demos.
    """
    query = query.lower()
    if 'congestion' in query or 'traffic' in query:
        return "🚗 **Congestion Update:** Based on current telemetry models, traffic is expected to peak in 12 minutes. Avoid I-95 main highways and expect a 15-minute delay."
    elif 'route' in query or 'suggestion' in query or 'fastest' in query:
        return "🗺️ **Route Suggestion:** I recommend the 'AI Recommended ✨' route. It bypasses the congestion zone and saves 22% fuel efficiency by skipping major tolls."
    elif 'accident' in query or 'crash' in query:
        return "⚠️ **Accident Report:** A minor collision was reported near the downtown bridge. Emergency protocols are active, and routes have been automatically adjusted."
    elif 'emergency' in query or 'ambulance' in query:
        return "🚨 **Emergency Active:** Priority lanes are being monitored. Signal synchronization is locking fastest routes for emergency vehicles."
    else:
        return "🤖 **System Online:** I am your AI Smart City Assistant. I am analyzing millions of data points across the city grid. Ask me about *congestion*, *routes*, or *accidents*."

def get_ai_response(query):
    """
    Attempts to use Google Gemini AI for intelligent conversation. 
    Falls back to mock responses gracefully if API keys are missing or limits reached.
    """
    
    # Check for API Key in environment or Streamlit secrets
    api_key = os.getenv("GEMINI_API_KEY") 
    try:
        if not api_key:
            api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
        
    if not HAS_GENAI or not api_key:
        time.sleep(1) # Fake loading latency for realism
        return get_mock_response(query)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Inject System Prompt Persona
        prompt_with_persona = f"""
        You are a highly advanced Smart City Traffic AI Assistant. 
        You monitor live congestion, routes, and emergency alerts. 
        Keep your answer under 3 sentences. Be highly professional, futuristic, and helpful. 
        Use emojis.
        
        User Query: {query}
        """
        
        response = model.generate_content(prompt_with_persona)
        
        # If API returns something empty, fallback safely
        if not response.text:
            return get_mock_response(query)
            
        return response.text
        
    except Exception as e:
        logger.error(f"AI Chatbot API Error: {e}")
        return get_mock_response(query) # Zero-crash fallback!

def display_chatbot():
    """
    Renders a futuristic, premium chat interface in Streamlit.
    """
    st.markdown("### <span style='color: #00F0FF;'>💬 AI Neural Assistant</span>", unsafe_allow_html=True)
    st.markdown("<p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Real-time AI querying connected to the city grid. Ask for routes, alerts, or insights.</p>", unsafe_allow_html=True)
    
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "🤖 **System Initialized.** The smart city grid is online. How can I assist your routing today?"}
        ]
        
    # Styling container
    st.markdown("<div style='border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 12px; padding: 15px; background: rgba(10,10,12,0.6); backdrop-filter: blur(10px); min-height: 300px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
    # Display chat messages from history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # React to user input
    if prompt := st.chat_input("E.g., 'What is the fastest route right now?' or 'Any accidents locally?'"):
        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Get AI Response with Loading Spinner
        with st.spinner("🧠 Synthesizing live city data..."):
            response = get_ai_response(prompt)
        
        # Save to history       
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Force a refresh to properly render the new messages in the persistent container
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
