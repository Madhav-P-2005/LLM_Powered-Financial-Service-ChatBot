# Importing the required libraries

from flask import request,jsonify

from flask_cors import CORS

from flask import Flask 

from dotenv import load_dotenv

from openai import OpenAI

import os
import re

# Loading the environment variables
load_dotenv('config/.env')

# Creating the Flask app
app = Flask(__name__)

# Allow local dev and deployed frontend on Vercel
CORS(app , resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://madhavp-financial-service-chatbot.vercel.app",
    "https://madhavp-finsathi-chatbot.vercel.app",
]}})

# OpenAI client (expects OPENAI_API_KEY in environment)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found. Please set it in config/.env or environment.")
client = OpenAI()

# Curated FAQ with citations (keyword -> (title, answer, source_url))
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


def curated_answer(user_message: str):
    q = user_message.lower()
    for item in CURATED_KB:
        if any(k in q for k in item["keywords"]):
            content = f"{item['title']}\n{item['answer']}\nSource: {item['source']}"
            return content
    return None


def investopedia_url_guess(user_message: str) -> str:
    """Heuristically map a term to an Investopedia URL (best-effort)."""
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

# Creating the OpenAI client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Defining the route for the chatbot
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
        curated = curated_answer(user_message)
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

        # Getting the response
        # response = model(conv)

        # Sources Dictionary  
        sources = {
            "credit default swap" : "Investopedia - Credit Default Swap",
            "phishing" : "Investopedia - Phishing",
            "fraud": "Investopedia - Financial Fraud", 
        }

        # Query 
        query = user_message.lower()

        source = "General Knowledge" 


        for key in sources:
            if key in query:
                source = sources[key]
                break

        # If the model didn't produce a Source line, append a best-effort one
        if "Source:" not in message:
            guessed = investopedia_url_guess(user_message)
            message = message + f"\nSource: {source if source != 'General Knowledge' else guessed}"


        # Returning the response
        return jsonify({"response": message})
    except Exception as e:

        # Returning the error
        return jsonify({
            "error" : str(e) 
        })


@app.route('/', methods=['GET'])
def health():
    """Simple health check endpoint for Railway/Vercel probes."""
    return jsonify({"status": "ok"}), 200

# Running the app
if __name__ == "__main__":
         app.run(debug=True)