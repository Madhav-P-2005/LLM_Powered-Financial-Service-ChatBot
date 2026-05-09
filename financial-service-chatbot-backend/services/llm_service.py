"""
LLM Service for the Financial Services Chatbot.

This module handles all Large Language Model (LLM) API interactions.
It implements a dual-provider strategy:

    PRIMARY  :  HuggingFace Inference API  (FREE — no cost, no expiry)
    FALLBACK :  OpenAI API                 (PAID — used if HF fails or is unavailable)

WHY TWO PROVIDERS?
    - HuggingFace is free forever but has rate limits (~30 req/min).
    - OpenAI is paid but provides the highest quality responses.
    - If HF is down or rate-limited, the system automatically falls back to OpenAI.
    - This gives you experience with BOTH APIs for your portfolio/resume.

MODELS USED:
    - HuggingFace : mistralai/Mistral-7B-Instruct-v0.3  (open-source, great for finance)
    - OpenAI      : gpt-4o-mini                          (cost-effective, high quality)
"""

import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables from config/.env
load_dotenv("config/.env")

# Set up logging for debugging and monitoring
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────
# System prompt that instructs the LLM how to behave
# This is sent with every request to set the AI's personality and format
# ──────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are FinSathi AI, a helpful financial assistant. "
    "If the user greets you or asks how you can help, respond with a very brief (1-2 sentences) friendly greeting. "
    "DO NOT use bullet points for greetings. DO NOT include a 'Source:' for greetings. "
    "Only provide a detailed explanation if the user asks about a specific financial term or concept. "
    "For financial questions: "
    "1. Provide a clear explanation in 5-8 bullet points. "
    "2. Focus on what it is and why it matters. "
    "3. Use '•' for bullet points. "
    "4. Always end with 'Source: [valid Investopedia URL]' on a separate line."
)


# ──────────────────────────────────────────────────────────────────────
# HuggingFace Client Setup (PRIMARY — Free)
# Uses the huggingface_hub library with OpenAI-compatible chat interface
# ──────────────────────────────────────────────────────────────────────

hf_client = None               # Will be initialized below if token exists
HF_MODEL = "Qwen/Qwen2.5-7B-Instruct"   # Open-source model (confirmed on HF Inference Providers free tier)

if os.getenv("HF_API_TOKEN"):
    try:
        from huggingface_hub import InferenceClient
        hf_client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))
        logger.info("✅ HuggingFace client initialized successfully")
    except ImportError:
        logger.warning("⚠️ huggingface_hub not installed. Run: pip install huggingface_hub")
    except Exception as e:
        logger.warning(f"⚠️ HuggingFace client init failed: {e}")
else:
    logger.warning("⚠️ HF_API_TOKEN not found in environment. HuggingFace provider disabled.")


# ──────────────────────────────────────────────────────────────────────
# OpenAI Client Setup (FALLBACK — Paid)
# Only initialized if OPENAI_API_KEY is present in environment
# ──────────────────────────────────────────────────────────────────────

openai_client = None            # Will be initialized below if key exists
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if os.getenv("OPENAI_API_KEY"):
    try:
        from openai import OpenAI
        openai_client = OpenAI()
        logger.info("✅ OpenAI client initialized successfully (fallback ready)")
    except ImportError:
        logger.warning("⚠️ openai not installed. Run: pip install openai")
    except Exception as e:
        logger.warning(f"⚠️ OpenAI client init failed: {e}")
else:
    logger.info("ℹ️ OPENAI_API_KEY not found. OpenAI fallback disabled (this is fine).")


# ──────────────────────────────────────────────────────────────────────
# Public API — called by the chat route
# ──────────────────────────────────────────────────────────────────────

def get_llm_response(user_message: str) -> str:
    """
    Get an AI-generated response for a financial question.

    Strategy:
        1. Try HuggingFace first (free)
        2. If HF fails, try OpenAI (paid fallback)
        3. If both fail, return a helpful error message

    Args:
        user_message: The question the user asked.

    Returns:
        The AI-generated response string.

    Raises:
        RuntimeError: If both providers fail (caught by the route handler).
    """

    # ── Attempt 1: HuggingFace (Primary — Free) ──────────────────────
    if hf_client:
        try:
            response = _call_huggingface(user_message)
            logger.info("✅ Response generated via HuggingFace")
            return response
        except Exception as e:
            logger.warning(f"⚠️ HuggingFace failed: {e}. Trying OpenAI fallback...")

    # ── Attempt 2: OpenAI (Fallback — Paid) ───────────────────────────
    if openai_client:
        try:
            response = _call_openai(user_message)
            logger.info("✅ Response generated via OpenAI (fallback)")
            return response
        except Exception as e:
            logger.error(f"❌ OpenAI fallback also failed: {e}")

    # ── Both providers failed ─────────────────────────────────────────
    raise RuntimeError(
        "Both HuggingFace and OpenAI providers are unavailable. "
        "Please check your API tokens in config/.env"
    )


# ──────────────────────────────────────────────────────────────────────
# Private helpers — one for each LLM provider
# ──────────────────────────────────────────────────────────────────────

def _call_huggingface(user_message: str, max_retries: int = 2) -> str:
    """
    Call the HuggingFace Inference API with retry logic.

    The free tier has rate limits, so we retry with exponential backoff
    if we get a rate limit error (HTTP 429).

    Args:
        user_message: The user's question.
        max_retries : Number of retry attempts for rate limit errors.

    Returns:
        The model's response text.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            # Use the OpenAI-compatible chat.completions interface
            completion = hf_client.chat.completions.create(
                model=HF_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=500,       # Keep responses concise
                temperature=0.3,      # Low temp = more focused, factual answers
            )
            return completion.choices[0].message.content.strip()

        except Exception as e:
            last_error = e
            error_str = str(e).lower()

            # If rate-limited, wait and retry (exponential backoff)
            if "429" in error_str or "rate" in error_str:
                wait_time = 2 ** attempt      # 1s, 2s, 4s
                logger.warning(f"⏳ HF rate limited. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries + 1})")
                time.sleep(wait_time)
            else:
                # For non-rate-limit errors, don't retry
                raise

    # All retries exhausted
    raise last_error


def _call_openai(user_message: str) -> str:
    """
    Call the OpenAI Chat Completions API.

    This is the fallback provider — only called if HuggingFace fails.

    Args:
        user_message: The user's question.

    Returns:
        The model's response text.
    """
    completion = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()


# ──────────────────────────────────────────────────────────────────────
# Utility — check which providers are currently available
# ──────────────────────────────────────────────────────────────────────

def get_provider_status() -> dict:
    """
    Check which LLM providers are configured and ready.

    Returns:
        A dictionary with the status of each provider.
        Useful for health checks and debugging.
    """
    return {
        "huggingface": {
            "configured": hf_client is not None,
            "model": HF_MODEL,
            "role": "primary (free)",
        },
        "openai": {
            "configured": openai_client is not None,
            "model": OPENAI_MODEL,
            "role": "fallback (paid)",
        },
    }
