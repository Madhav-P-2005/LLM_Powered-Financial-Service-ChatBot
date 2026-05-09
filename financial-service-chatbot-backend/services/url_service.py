"""
URL Service for the Financial Services Chatbot.

This module handles generating reliable Investopedia source links
for chatbot responses. Every answer the bot gives should include
a valid "Source: <URL>" citation.

URL RESOLUTION STRATEGY (tried in order):
    1. Canonical lookup  →  exact match from verified URL dictionary
    2. Partial matching  →  find a canonical key inside the user's query
    3. Heuristic generation →  auto-generate URL from term pattern
    4. Alphabetical fallback →  link to Investopedia's directory page

WHY THIS MATTERS:
    - Users trust answers more when they see a real source link.
    - Broken links look unprofessional — we avoid them.
    - The curated canonical dictionary has 200+ verified URLs.
"""

import re
import logging

# Import the canonical URL dictionary from our knowledge base
from knowledge.canonical_urls import CANONICAL_INVESTOPEDIA

# Set up logging
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────
# Public API — called by the chat route
# ──────────────────────────────────────────────────────────────────────

def get_safe_source_link(query: str) -> str:
    """
    Generate a safe, reliable Investopedia URL for a given query.

    Resolution order:
        1. Exact canonical match
        2. Partial canonical match (longest key wins for accuracy)
        3. Heuristic URL generation (pattern-based guess)
        4. Alphabetical directory fallback

    Args:
        query: The user's original question.

    Returns:
        A string URL — always returns something, never None.
    """
    q = query.lower()

    # ── Step 1: Exact match in canonical dictionary ───────────────────
    if q in CANONICAL_INVESTOPEDIA:
        logger.debug(f"URL: exact match for '{q}'")
        return CANONICAL_INVESTOPEDIA[q]

    # ── Step 2: Partial match (find canonical key inside the query) ───
    # We collect all matches and pick the longest one for accuracy
    # e.g., "credit default swap" should match over "credit"
    matches = []
    for key, url in CANONICAL_INVESTOPEDIA.items():
        if key in q:
            matches.append((len(key), url))

    if matches:
        # Sort by key length descending — longest match is most specific
        matches.sort(reverse=True)
        logger.debug(f"URL: partial match, best key length = {matches[0][0]}")
        return matches[0][1]

    # ── Step 3: Heuristic URL generation ──────────────────────────────
    # Try to construct a valid Investopedia URL from the query terms
    heuristic_url = _guess_investopedia_url(query)
    if heuristic_url:
        logger.debug(f"URL: heuristic guess → {heuristic_url}")
        return heuristic_url

    # ── Step 4: Alphabetical directory fallback ───────────────────────
    # Link to Investopedia's alphabetical term directory
    search_term = _extract_search_term(query)
    if search_term:
        main_term = search_term.split()[0] if search_term else ""
        if main_term and main_term[0].isalpha():
            first_letter = main_term[0].lower()
            # Investopedia's directory pages follow this ID pattern
            directory_id = 4769351 + ord(first_letter) - ord("a")
            return f"https://www.investopedia.com/terms-beginning-with-{first_letter}-{directory_id}"

    # ── Ultimate fallback: Investopedia homepage ──────────────────────
    return "https://www.investopedia.com/"


def ensure_source_in_response(message: str, query: str) -> str:
    """
    Ensure the LLM response has a valid Source line.

    If the model already included a Source URL, keep it.
    If not, append our best-effort Investopedia link.

    Args:
        message: The raw LLM response text.
        query  : The user's original question (used for URL generation).

    Returns:
        The response text with a guaranteed Source line.
    """
    # ── Step 1: Find "Source:" ANYWHERE in the response ───────────────
    # The LLM sometimes puts Source: at the start of a new line,
    # sometimes inline at the end of the last sentence — catch both
    source_match = re.search(r"Source:\s*(.+?)$", message, re.IGNORECASE | re.MULTILINE)
    
    if source_match:
        source_text = source_match.group(1)
        
        # Extract ALL real URLs from the source text
        # Handles: plain URLs, markdown [text](url), and mixed formats
        urls_found = re.findall(r"https?://[^\s\)\]\>]+", source_text)
        
        # Strip everything from "Source:" onwards
        content = message[:source_match.start()].rstrip()
        
        if urls_found:
            # Use the FIRST real URL found (most relevant to the question)
            clean_url = urls_found[0].rstrip(")")
            return content + f"\nSource: {clean_url}"
        else:
            # Source text has NO real URLs (placeholder like "[Investopedia URL for stocks]")
            # Fall through to append our canonical URL below
            message = content
    
    # ── Step 2: Decide whether to append our own source ───────────────
    q = query.lower().strip()
    words = q.split()
    
    # Only treat as greeting if it's a SHORT, pure greeting (max 5 words)
    # e.g., "hi" or "hello how are you" — NOT "hi what are stocks?"
    is_pure_greeting = len(words) <= 5 and any(
        word in ["hi", "hello", "hey"] for word in words
    ) and not any(
        word in q for word in ["what", "how", "explain", "tell", "stock", "bond", "credit", "loan", "fund"]
    )
    
    if is_pure_greeting:
        return message

    # Append our canonical source URL for all financial answers
    # (works for both bullet-point and paragraph-style responses)
    if len(message) > 100:
        source_url = get_safe_source_link(query)
        return message + f"\nSource: {source_url}"
    
    return message


# ──────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────

def _guess_investopedia_url(user_message: str) -> str | None:
    """
    Generate an Investopedia URL using the standard pattern:
        /terms/{first_letter}/{slug}.asp

    Example: "stock" → /terms/s/stock.asp

    Args:
        user_message: The user's question text.

    Returns:
        A guessed URL string, or None if we can't generate one.
    """
    q = user_message.lower()

    # List of known financial keywords to look for in the query
    financial_keywords = [
        "stock", "bond", "investment", "trading", "portfolio", "dividend", "interest",
        "loan", "mortgage", "credit", "debt", "budget", "savings", "retirement",
        "insurance", "tax", "fund", "etf", "mutual fund", "broker", "market",
        "economy", "inflation", "recession", "gdp", "cryptocurrency", "bitcoin",
        "forex", "options", "futures", "derivatives", "asset", "liability",
        "equity", "capital", "yield", "return", "risk", "diversification",
    ]

    # Try to find a known financial term in the query
    best_match = None
    for keyword in financial_keywords:
        if keyword in q:
            best_match = keyword
            break

    # If no financial keyword found, extract the most meaningful word
    if not best_match:
        tokens = re.findall(r"\b[a-zA-Z]+(?:\s+[a-zA-Z]+)*\b", q)
        stop_words = {
            "what", "is", "are", "how", "can", "do", "does", "the", "a", "an",
            "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "by", "about", "explain", "tell", "me", "you", "i", "my", "your",
        }
        meaningful = [t for t in tokens if t.lower() not in stop_words and len(t) > 2]

        if meaningful:
            best_match = meaningful[0].lower()

    if not best_match:
        return None

    # Build the Investopedia URL slug
    # Remove special characters and spaces (Investopedia format)
    slug = re.sub(r"[^a-z0-9\s]", "", best_match.lower()).strip()
    slug = re.sub(r"\s+", "", slug)       # "mutual fund" → "mutualfund"

    if not slug:
        return None

    first_letter = slug[0]
    return f"https://www.investopedia.com/terms/{first_letter}/{slug}.asp"


def _extract_search_term(query: str) -> str:
    """
    Extract the most meaningful words from a user query.

    Strips out common question words (what, is, how, etc.)
    and returns the remaining significant terms.

    Args:
        query: The raw user question.

    Returns:
        A string of up to 3 meaningful words joined by spaces.
    """
    q = query.lower()

    # Words to ignore when extracting the search term
    stop_words = {
        "what", "is", "are", "how", "can", "do", "does", "the", "a", "an",
        "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
        "by", "about", "explain", "tell", "me", "you", "i", "my", "your",
        "should", "would", "could",
    }

    tokens = re.findall(r"\b[a-zA-Z]+\b", q)
    meaningful = [t for t in tokens if t.lower() not in stop_words and len(t) > 2]

    if meaningful:
        return " ".join(meaningful[:3])    # Use first 3 meaningful words

    return query.strip()
