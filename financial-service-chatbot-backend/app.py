"""
Flask API for the Financial Services Chatbot.

Responsibilities :- 
- Serve a POST /chat endpoint that first tries curated answers, then falls back to OpenAI.
- Always append a reliable "Source:" link (validated Investopedia URL or search page).
- Enable CORS for local dev and the deployed Vercel frontend.
- Expose GET / health endpoint for uptime checks.

"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

import os
import re
import requests
from urllib.parse import quote_plus


# Loading the environment variables
load_dotenv('config/.env')

# Initialize the Flask app
app = Flask(__name__)


# Allow local dev and deployed frontend on Vercel
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://madhavp-financial-service-chatbot.vercel.app",
    "https://finsathi-chatbot-madhavp.vercel.app",
]}})


# OpenAI client (expects OPENAI_API_KEY in environment)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found. Please set it in config/.env or environment.")
client = OpenAI()


# Curated topics with trusted citations for predictable questions
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



# Function to get a curated answer for a user query
def get_curated_answer(user_message: str):
    q = user_message.lower()
    for item in CURATED_KB:
        if any(k in q for k in item["keywords"]):
            content = f"{item['title']}\n{item['answer']}\nSource: {item['source']}"
            return content
    return None


# Function to guess the Investopedia URL for a user query
def guess_investopedia_url(user_message: str) -> str:
    """
    Heuristically map a term to an Investopedia URL (best-effort).

    This is not guaranteed to exist; caller should validate with a HEAD request
    before returning to the user.

    """
    # pick a keyword-like token
    q = user_message.lower()

    # simple noun-ish extraction: take last meaningful word
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\- ]+", q)

    if not tokens:
        return "https://www.investopedia.com/"

    phrase = tokens[-1].strip()
    slug = re.sub(r"[^a-z0-9\- ]", "", phrase.lower()).strip()
    slug = re.sub(r"\s+", "-", slug)
    first = slug[0] if slug else 'a'
    return f"https://www.investopedia.com/terms/{first}/{slug}.asp"




# Function to check if a URL exists
def _url_exists(url: str, timeout: int = 3) -> bool:
    try:
         r = requests.head(url, allow_redirects=True, timeout=timeout)

         return r.status_code < 400
    except Exception:
        return False


# OpenAI client
CANONICAL_INVESTOPEDIA = {

    "credit default swap" : "https://www.investopedia.com/terms/c/creditdefaultswap.asp",
    "credit card" : "https://www.investopedia.com/terms/c/creditcard.asp",
    "bank" : "https://www.investopedia.com/terms/b/bank.asp",
    "phishing" : "https://www.investopedia.com/terms/p/phishing.asp",
    "credit score" : "https://www.investopedia.com/terms/c/credit_score.asp",
    "emi" : "https://www.investopedia.com/terms/e/equated-monthly-installment-emi.asp",
}


# Function to build the source link for the response
def build_investopedia_source_link(query: str) -> str:
    """
    Return the best-effort Investopedia URL for a user query.

    Priority :- 
    1) Canonical curated mapping
    2) Heuristic guess (validated)
    3) Investopedia search (never 404s)

    """

    # If canonical mapping exists, return it
    q = query.lower()
    for key, url in CANONICAL_INVESTOPEDIA.items():
        if key in q:
            return url
    
    # If canonical mapping fails, try heuristic guess
    guessed = guess_investopedia_url(query)
    if guessed and _url_exists(guessed):
        return guessed

    # If all else fails, return a search URL
    return f"https://www.investopedia.com/search.asp?q={quote_plus(query)}"



# Routes
@app.route('/chat', methods=['POST'])
def chat():

    # Getting the data
    data = request.json

    try : 
        # Get the user's message from the request
        user_message = data.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # First try curated knowledge for higher quality + citation
        curated = get_curated_answer(user_message)
        if curated:
            return jsonify({"response": curated})

        # Otherwise, ask OpenAI for a concise, cited answer
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        chat = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial assistant. Answer in simple language using 3-6 bullet points. "
                        "Always add a final line starting with 'Source:' followed by a reputable URL."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        message = chat.choices[0].message.content.strip()

        # If the model didn't produce a Source line, append a best-effort URL
        if "Source:" not in message:
            source_url = build_investopedia_source_link(user_message)
            message = message + f"\nSource: {source_url}"


        # Returning the response
        return jsonify({"response": message})
    except Exception as e:

        # Returning the error
        return jsonify({"error": str(e)}), 500


# Health Check Endpoint
@app.route('/', methods=['GET'])
def health():

    """
    Simple health check endpoint for Railway/Vercel probes.
    
    Returns :- 
    - JSON response with status "ok" and HTTP status code 200.

    """
    return jsonify({"status": "ok"}), 200

# Running the app
if __name__ == "__main__":
         app.run(debug=True)