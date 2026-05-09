"""
Chat Routes for the Financial Services Chatbot.

This module defines the Flask Blueprint for all chat-related endpoints:

    POST /chat   →  Main chat endpoint (curated KB → HuggingFace → OpenAI)
    GET  /       →  Health check (used by Render/Vercel for uptime monitoring)

REQUEST/RESPONSE FORMAT:
    Request:  { "message": "What is a credit card?" }
    Response: { "response": "• A credit card lets you..." }

ERROR HANDLING:
    - 400: Missing or empty message
    - 500: Both LLM providers failed (returns helpful error text)
"""

import os
import logging
from flask import Blueprint, request, jsonify

# Import our service modules
from knowledge.curated_kb import get_curated_answer
from services.llm_service import get_llm_response, get_provider_status
from services.url_service import ensure_source_in_response

# Set up logging
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────
# Create a Flask Blueprint for chat routes
# A Blueprint is like a mini-app that gets registered with the main app
# This keeps routes separate from app initialization (clean architecture)
# ──────────────────────────────────────────────────────────────────────

chat_bp = Blueprint("chat", __name__)


# ──────────────────────────────────────────────────────────────────────
# POST /chat — Main chat endpoint
# ──────────────────────────────────────────────────────────────────────

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint that answers financial questions.

    Processing order:
        1. Check curated knowledge base (instant, no API call)
        2. If not curated, call LLM (HuggingFace → OpenAI fallback)
        3. Ensure the response has a valid Source link

    Returns:
        JSON: { "response": "..." } on success
        JSON: { "error": "..." }    on failure
    """
    # ── Parse the request ─────────────────────────────────────────────
    data = request.json

    try:
        # Validate that a message was provided
        user_message = data.get("message") if data else None
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # ── Step 1: Try curated knowledge base (instant response) ─────
        # The USE_CURATED env var allows disabling this for testing
        if os.getenv("USE_CURATED", "true").lower() == "true":
            curated = get_curated_answer(user_message)
            if curated:
                logger.info(f"📚 Curated answer served for: '{user_message[:50]}...'")
                return jsonify({"response": curated})

        # ── Step 2: Call LLM (HuggingFace primary → OpenAI fallback) ──
        llm_response = get_llm_response(user_message)

        # ── Step 3: Ensure response has a valid Source link ───────────
        final_response = ensure_source_in_response(llm_response, user_message)

        logger.info(f"🤖 LLM response served for: '{user_message[:50]}...'")
        return jsonify({"response": final_response})

    except Exception as e:
        # Log the full error for debugging
        logger.error(f"❌ Chat error: {str(e)}", exc_info=True)

        # Return a user-friendly error message
        return jsonify({
            "error": f"Sorry, I couldn't process your question right now. Error: {str(e)}"
        }), 500


# ──────────────────────────────────────────────────────────────────────
# GET / — Health check endpoint
# ──────────────────────────────────────────────────────────────────────

@chat_bp.route("/", methods=["GET"])
def health():
    """
    Health check endpoint for Render/Vercel uptime monitoring probes.

    Also returns the status of configured LLM providers,
    which is useful for debugging deployment issues.

    Returns:
        JSON: { "status": "ok", "providers": { ... } }
    """
    return jsonify({
        "status": "ok",
        "providers": get_provider_status(),
    }), 200
