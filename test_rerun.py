"""Streamlit-specific test helper removed.

This file previously attempted to call `st.rerun()`. Streamlit has been
removed from the project; to rerun tests use your normal test runner,
e.g. `pytest` or `python -m pytest`.
"""

if __name__ == "__main__":
    print("test_rerun: Streamlit removed. Use pytest or your preferred runner.")
