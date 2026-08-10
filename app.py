"""API launcher and README shim.

This project formerly used Streamlit for the UI. The Streamlit UI has been
removed and replaced by a frontend in `frontend/` (React). The Flask API
backend is implemented in `api.py` and can be started by running this file.
"""

from api import app


if __name__ == "__main__":
    print("Starting Flask API (backend) on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
