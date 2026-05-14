import streamlit as st

def get_bot_response(query):
    """
    Returns predefined smart traffic responses based on keywords.
    """
    query = query.lower()
    if 'congestion' in query or 'traffic' in query:
        return "🚗 **Congestion Update:** Based on current models, traffic is expected to peak soon. Avoid main highways and expect a 15-minute delay."
    elif 'route' in query or 'suggestion' in query or 'fastest' in query:
        return "🗺️ **Route Suggestion:** I recommend the 'AI Recommended ✨' route. It saves time and balances fuel efficiency by bypassing major tolls."
    elif 'accident' in query or 'crash' in query:
        return "⚠️ **Accident Report:** A minor collision was reported nearby. Emergency protocols are active, and routes have been automatically adjusted."
    elif 'emergency' in query or 'ambulance' in query:
        return "🚨 **Emergency Active:** Priority lanes are being monitored. Fastest routes are locked for emergency vehicles."
    else:
        return "🤖 Hello! I am your AI Traffic Assistant. Ask me about *congestion*, *route suggestions*, or *accidents*!"

def display_chatbot():
    """
    Renders a lightweight, interactive chat interface in Streamlit.
    """
    st.subheader("💬 AI Traffic Assistant")
    st.markdown("Ask me anything about current traffic conditions or get quick route advice.")
    
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "🤖 Hello! Use the input below to ask me about congestion, routes, or accidents."}
        ]
        
    # Create a container with fixed height for the chat if desired, or just let it expand
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages from history
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    # React to user input
    if prompt := st.chat_input("E.g., 'What is the fastest route?' or 'Any accidents?'"):
        # Add and display user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Add and display assistant response
            response = get_bot_response(prompt)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
