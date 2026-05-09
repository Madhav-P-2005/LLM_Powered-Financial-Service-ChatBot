"""
Curated Knowledge Base for the Financial Services Chatbot.

This module contains hand-written, high-quality answers for commonly asked
financial questions. These are served *instantly* (no API call needed) and
always include a verified Investopedia source link.

HOW TO ADD A NEW TOPIC:
    1. Add a new dictionary to the CURATED_KB list below.
    2. Include relevant keywords (lowercase) that a user might type.
    3. Write a concise, bullet-point answer.
    4. Provide a verified Investopedia URL as the source.

WHY THIS EXISTS:
    - Instant responses for popular questions (no API latency).
    - Guaranteed accurate answers with verified citations.
    - Works even if both HuggingFace and OpenAI APIs are down.
"""


# ──────────────────────────────────────────────────────────────────────
# Curated answers for common financial topics
# Each entry has:
#   - keywords : list of trigger phrases (matched against user's query)
#   - title    : heading shown to user
#   - answer   : bullet-point explanation
#   - source   : verified Investopedia URL
# ──────────────────────────────────────────────────────────────────────

CURATED_KB = [
    {
        "keywords": ["credit card", "creditcards", "card limit", "annual fee"],
        "title": "Credit Card — What it is",
        "answer": (
            "• A credit card lets you borrow up to a preset limit to pay for goods/services.\n"
            "• You must repay by the due date; otherwise interest (APR) applies on revolving balance.\n"
            "• Key terms: credit limit, billing cycle, minimum due, interest/finance charges, late fee.\n"
            "• Benefits often include rewards/cashback; watch for annual fee and FX markups.\n"
            "• Responsible use builds credit score; overspending can hurt it."
        ),
        "source": "https://www.investopedia.com/terms/c/creditcard.asp",
    },
    {
        "keywords": ["bank", "what is a bank", "commercial bank", "retail bank"],
        "title": "Bank — What it is",
        "answer": (
            "• A bank is a regulated financial institution that accepts deposits and provides loans.\n"
            "• Core services: savings/current accounts, payments, credit cards, mortgages, business lending.\n"
            "• Makes money via interest spread (lending rate − deposit rate) and fees.\n"
            "• Types: retail, commercial, investment, central banks; each serves different functions."
        ),
        "source": "https://www.investopedia.com/terms/b/bank.asp",
    },
    {
        "keywords": ["phishing", "phish", "fraud email", "scam link"],
        "title": "Phishing — How to stay safe",
        "answer": (
            "• Phishing is a social-engineering attack to steal credentials or money.\n"
            "• Red flags: urgent tone, unknown links/attachments, sender spoofing.\n"
            "• Do not share OTPs/PINs; banks never ask for them.\n"
            "• Type URLs manually; enable 2FA; report suspicious messages to your bank."
        ),
        "source": "https://www.investopedia.com/terms/p/phishing.asp",
    },
    {
        "keywords": ["credit default swap", "cds", "swap credit risk"],
        "title": "Credit Default Swap (CDS) — Plain-English definition",
        "answer": (
            "• A CDS is a derivative contract where a buyer pays a periodic premium to transfer the credit risk of a reference borrower to a seller.\n"
            "• If a defined credit event occurs (e.g., default), the seller compensates the buyer per contract terms.\n"
            "• Used for hedging credit exposure or speculating on a borrower's creditworthiness.\n"
            "• Key terms: reference entity, notional, premium (spread), maturity, credit events."
        ),
        "source": "https://www.investopedia.com/terms/c/creditdefaultswap.asp",
    },
    {
        "keywords": ["credit score", "cibil", "fico"],
        "title": "Credit Score — Why it matters",
        "answer": (
            "• 3‑digit number reflecting your repayment history and credit utilization.\n"
            "• Higher scores generally help you get loans/cards at better interest rates.\n"
            "• Improve by paying on time, keeping utilization <30%, and avoiding hard inquiries."
        ),
        "source": "https://www.investopedia.com/terms/c/credit_score.asp",
    },
    {
        "keywords": ["emi", "equated monthly instalment", "loan payment"],
        "title": "EMI — Equated Monthly Installment",
        "answer": (
            "• Fixed monthly payment covering principal + interest for a loan.\n"
            "• Depends on loan amount, interest rate, and tenure; longer tenure lowers EMI but increases total interest."
        ),
        "source": "https://www.investopedia.com/terms/e/equated-monthly-installment-emi.asp",
    },
]


def get_curated_answer(user_message: str) -> str | None:
    """
    Try to match the user's message against curated knowledge base entries.

    Args:
        user_message: The raw text the user typed in the chat.

    Returns:
        A formatted string with title + answer + source if matched,
        or None if no curated answer is available.
    """
    q = user_message.lower()

    for item in CURATED_KB:
        # Check if any keyword from this entry appears in the user's message
        if any(keyword in q for keyword in item["keywords"]):
            content = f"{item['title']}\n{item['answer']}\nSource: {item['source']}"
            return content

    return None
