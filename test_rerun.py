import streamlit as st
try:
    st.rerun()
except Exception as e:
    st.write("Caught exception:", e)
