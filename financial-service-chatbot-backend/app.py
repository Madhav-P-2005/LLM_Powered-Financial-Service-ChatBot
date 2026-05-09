"""
Flask Application Entry Point for the Financial Services Chatbot.

This is the main entry point that:
    1. Creates and configures the Flask app
    2. Enables CORS for frontend access
    3. Registers the chat routes Blueprint
    4. Configures logging for debugging

ARCHITECTURE OVERVIEW:
    app.py (this file)
        ├── routes/chat.py          →  API endpoints (/chat, /)
        ├── services/llm_service.py →  HuggingFace + OpenAI integration
        ├── services/url_service.py →  Investopedia URL generation
        ├── knowledge/curated_kb.py →  Curated answers for common questions
        └── knowledge/canonical_urls.py → 200+ verified Investopedia URLs

HOW TO RUN:
    Development:
        flask run --host 127.0.0.1 --port 5000

    Production (Render):
        gunicorn app:app
"""

import logging
from flask import Flask
from flask_cors import CORS

# Import the chat routes Blueprint
from routes.chat import chat_bp


# ──────────────────────────────────────────────────────────────────────
# Configure logging
# This helps you debug issues in development and on Render
# ──────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ──────────────────────────────────────────────────────────────────────
# Create and configure the Flask app
# ──────────────────────────────────────────────────────────────────────

app = Flask(__name__)


# ──────────────────────────────────────────────────────────────────────
# Enable CORS (Cross-Origin Resource Sharing)
# This allows the frontend (on a different domain) to call our API
#
# Allowed origins:
#   - http://localhost:5173      → local Vite dev server
#   - Vercel deployment URL      → production frontend
# ──────────────────────────────────────────────────────────────────────

CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://finsathi-chatbot-madhavp.vercel.app",
]}})


# ──────────────────────────────────────────────────────────────────────
# Register the chat Blueprint
# This adds all routes from routes/chat.py to our app
# ──────────────────────────────────────────────────────────────────────

app.register_blueprint(chat_bp)


# ──────────────────────────────────────────────────────────────────────
# Run the app (development server)
# In production (Render), gunicorn handles this instead
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)