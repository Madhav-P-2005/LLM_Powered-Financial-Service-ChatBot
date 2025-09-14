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


# Loading the environment variables
load_dotenv('config/.env')

# Initialize the Flask app
app = Flask(__name__)


# Allow local dev and deployed frontend on Vercel
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
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
    """Return a curated answer for common topics, or None if not matched."""
    q = user_message.lower()
    for item in CURATED_KB:
        if any(k in q for k in item["keywords"]):
            content = f"{item['title']}\n{item['answer']}\nSource: {item['source']}"
            return content
    return None


# Function to guess the Investopedia URL for a user query
def guess_investopedia_url(user_message: str) -> str:
    """Generate Investopedia URL using the actual pattern: /terms/{letter}/{slug}.asp"""
    q = user_message.lower()
    
    # Extract the most relevant financial term
    financial_keywords = [
        'stock', 'bond', 'investment', 'trading', 'portfolio', 'dividend', 'interest',
        'loan', 'mortgage', 'credit', 'debt', 'budget', 'savings', 'retirement',
        'insurance', 'tax', 'fund', 'etf', 'mutual fund', 'broker', 'market',
        'economy', 'inflation', 'recession', 'gdp', 'cryptocurrency', 'bitcoin',
        'forex', 'options', 'futures', 'derivatives', 'asset', 'liability',
        'equity', 'capital', 'yield', 'return', 'risk', 'diversification'
    ]
    
    # Find the best matching financial term
    best_match = None
    for keyword in financial_keywords:
        if keyword in q:
            best_match = keyword
            break
    
    if not best_match:
        # Extract meaningful terms, filtering out stop words
        tokens = re.findall(r"\b[a-zA-Z]+(?:\s+[a-zA-Z]+)*\b", q)
        stop_words = {'what', 'is', 'are', 'how', 'can', 'do', 'does', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'about', 'explain', 'tell', 'me', 'you', 'i', 'my', 'your'}
        meaningful_tokens = [t for t in tokens if t.lower() not in stop_words and len(t) > 2]
        
        if meaningful_tokens:
            best_match = meaningful_tokens[0].lower()
    
    if not best_match:
        return "https://www.investopedia.com/"
    
    # Create proper Investopedia slug (remove spaces, special chars, keep lowercase)
    slug = re.sub(r"[^a-z0-9\s]", "", best_match.lower()).strip()
    slug = re.sub(r"\s+", "", slug)  # Remove all spaces for Investopedia format
    
    if not slug:
        return "https://www.investopedia.com/"
    
    first_letter = slug[0]
    
    # Use the actual Investopedia pattern: /terms/{letter}/{slug}.asp
    return f"https://www.investopedia.com/terms/{first_letter}/{slug}.asp"



# Function to check if a URL exists
def url_exists(url: str, timeout: int = 3) -> bool:
    """Check if a URL likely exists via a HEAD request (<400 considered ok)."""
    try:
         r = requests.head(url, allow_redirects=True, timeout=timeout)

         return r.status_code < 400
    except Exception:
        return False


# Canonical Investopedia URL mappings for common financial terms
CANONICAL_INVESTOPEDIA = {
    "credit default swap" : "https://www.investopedia.com/terms/c/creditdefaultswap.asp",
    "credit card" : "https://www.investopedia.com/terms/c/creditcard.asp",
    "bank" : "https://www.investopedia.com/terms/b/bank.asp",
    "phishing" : "https://www.investopedia.com/terms/p/phishing.asp",
    "credit score" : "https://www.investopedia.com/terms/c/credit_score.asp",
    "emi" : "https://www.investopedia.com/terms/e/equated-monthly-installment-emi.asp",
    "stock": "https://www.investopedia.com/terms/s/stock.asp",
    "stocks": "https://www.investopedia.com/terms/s/stock.asp",
    "equity": "https://www.investopedia.com/terms/e/equity.asp",
    "trading": "https://www.investopedia.com/trading-4427765",
    "how to trade": "https://www.investopedia.com/trading-4427765",
    "crypto": "https://www.investopedia.com/cryptocurrency-4427699",
    "what is cryptocurrency": "https://www.investopedia.com/cryptocurrency-4427699",
    "crypocurrency": "https://www.investopedia.com/cryptocurrency-4427699",
    "what is crypto": "https://www.investopedia.com/cryptocurrency-4427699",
    "etf": "https://www.investopedia.com/terms/e/etf.asp",
    "etfs": "https://www.investopedia.com/terms/e/etf.asp",
    "exchange traded fund": "https://www.investopedia.com/terms/e/etf.asp",
    "mutual fund": "https://www.investopedia.com/terms/m/mutualfund.asp",
    "mutual funds": "https://www.investopedia.com/terms/m/mutualfund.asp",
    "bond": "https://www.investopedia.com/terms/b/bond.asp",
    "bonds": "https://www.investopedia.com/terms/b/bond.asp",
    "broker": "https://www.investopedia.com/terms/b/broker.asp",
    "brokers": "https://www.investopedia.com/terms/b/broker.asp",
    "budget": "https://www.investopedia.com/terms/b/budget.asp",
    "budgeting": "https://www.investopedia.com/terms/b/budget.asp",
    "financing": "https://www.investopedia.com/terms/f/financing.asp",
    "diversification": "https://www.investopedia.com/terms/d/diversification.asp",
    "investment": "https://www.investopedia.com/terms/i/investment.asp",
    "investing": "https://www.investopedia.com/terms/i/investment.asp",
    "portfolio": "https://www.investopedia.com/terms/p/portfolio.asp",
    "risk": "https://www.investopedia.com/terms/r/risk.asp",
    "return": "https://www.investopedia.com/terms/r/return.asp",
    "compound interest": "https://www.investopedia.com/terms/c/compoundinterest.asp",
    "inflation": "https://www.investopedia.com/terms/i/inflation.asp",
    "recession": "https://www.investopedia.com/terms/r/recession.asp",
    "gdp": "https://www.investopedia.com/terms/g/gdp.asp",
    "cryptocurrency": "https://www.investopedia.com/cryptocurrency-4427699",
    "bitcoin": "https://www.investopedia.com/terms/b/bitcoin.asp",
    "blockchain": "https://www.investopedia.com/terms/b/blockchain.asp",
    "forex": "https://www.investopedia.com/terms/f/forex.asp",
    "derivatives": "https://www.investopedia.com/terms/d/derivative.asp",
    "options": "https://www.investopedia.com/terms/o/option.asp",
    "futures": "https://www.investopedia.com/terms/f/futures.asp",
    "insurance": "https://www.investopedia.com/terms/i/insurance.asp",
    "401k": "https://www.investopedia.com/terms/1/401kplan.asp",
    "ira": "https://www.investopedia.com/terms/i/ira.asp",
    "roth ira": "https://www.investopedia.com/terms/r/rothira.asp",
    "mortgage": "https://www.investopedia.com/terms/m/mortgage.asp",
    "loan": "https://www.investopedia.com/terms/l/loan.asp",
    "interest rate": "https://www.investopedia.com/terms/i/interestrate.asp",
    "apr": "https://www.investopedia.com/terms/a/apr.asp",
    "dividend": "https://www.investopedia.com/terms/d/dividend.asp",
    "dividends": "https://www.investopedia.com/terms/d/dividend.asp",
    "market cap": "https://www.investopedia.com/terms/m/marketcapitalization.asp",
    "pe ratio": "https://www.investopedia.com/terms/p/price-earningsratio.asp",
    "bull market": "https://www.investopedia.com/terms/b/bullmarket.asp",
    "bear market": "https://www.investopedia.com/terms/b/bearmarket.asp",
    "volatility": "https://www.investopedia.com/terms/v/volatility.asp",
    "liquidity": "https://www.investopedia.com/terms/l/liquidity.asp",
    "asset": "https://www.investopedia.com/terms/a/asset.asp",
    "liability": "https://www.investopedia.com/terms/l/liability.asp",
    "net worth": "https://www.investopedia.com/terms/n/networth.asp",
    "cash flow": "https://www.investopedia.com/terms/c/cashflow.asp",
    "balance sheet": "https://www.investopedia.com/terms/b/balancesheet.asp",
    "income statement": "https://www.investopedia.com/terms/i/incomestatement.asp",
    "financial planning": "https://www.investopedia.com/terms/f/financial_plan.asp",
    "retirement planning": "https://www.investopedia.com/terms/r/retirement-planning.asp",
    "emergency fund": "https://www.investopedia.com/terms/e/emergency_fund.asp",
    "savings account": "https://www.investopedia.com/terms/s/savingsaccount.asp",
    "checking account": "https://www.investopedia.com/terms/c/checkingaccount.asp",
    "debit card": "https://www.investopedia.com/terms/d/debitcard.asp",
    "credit limit": "https://www.investopedia.com/terms/c/credit_limit.asp",
    "credit utilization": "https://www.investopedia.com/terms/c/credit-utilization-rate.asp",
    "debt": "https://www.investopedia.com/terms/d/debt.asp",
    "bankruptcy": "https://www.investopedia.com/terms/b/bankruptcy.asp",
    "tax": "https://www.investopedia.com/terms/t/taxes.asp",
    "taxes": "https://www.investopedia.com/terms/t/taxes.asp",
    "capital gains": "https://www.investopedia.com/terms/c/capitalgain.asp",
    "tax deduction": "https://www.investopedia.com/terms/t/tax-deduction.asp",
    "reit": "https://www.investopedia.com/terms/r/reit.asp",
    "reits": "https://www.investopedia.com/terms/r/reit.asp",
    "real estate": "https://www.investopedia.com/terms/r/realestate.asp",
    "commodity": "https://www.investopedia.com/terms/c/commodity.asp",
    "commodities": "https://www.investopedia.com/terms/c/commodity.asp",
    "gold": "https://www.investopedia.com/terms/g/gold.asp",
    "silver": "https://www.investopedia.com/terms/s/silver.asp",
    "oil": "https://www.investopedia.com/terms/c/crude-oil.asp",
    "nasdaq": "https://www.investopedia.com/terms/n/nasdaq.asp",
    "nyse": "https://www.investopedia.com/terms/n/nyse.asp",
    "s&p 500": "https://www.investopedia.com/terms/s/sp500.asp",
    "dow jones": "https://www.investopedia.com/terms/d/djia.asp",
    "index fund": "https://www.investopedia.com/terms/i/indexfund.asp",
    "index funds": "https://www.investopedia.com/terms/i/indexfund.asp",
    "expense ratio": "https://www.investopedia.com/terms/e/expenseratio.asp",
    "yield": "https://www.investopedia.com/terms/y/yield.asp",
    "bond yield": "https://www.investopedia.com/terms/b/bond-yield.asp",
    "treasury": "https://www.investopedia.com/terms/t/treasurybond.asp",
    "fed": "https://www.investopedia.com/terms/f/federalreservebank.asp",
    "federal reserve": "https://www.investopedia.com/terms/f/federalreservebank.asp",
    "monetary policy": "https://www.investopedia.com/terms/m/monetarypolicy.asp",
    "fiscal policy": "https://www.investopedia.com/terms/f/fiscalpolicy.asp",
    "economics": "https://www.investopedia.com/terms/e/economics.asp",
    "supply and demand": "https://www.investopedia.com/terms/l/law-of-supply-demand.asp",
    "market": "https://www.investopedia.com/terms/m/market.asp",
    "stock market": "https://www.investopedia.com/terms/s/stockmarket.asp",
    "financial market": "https://www.investopedia.com/terms/f/financial-market.asp",
    "capital market": "https://www.investopedia.com/terms/c/capitalmarkets.asp",
    "money market": "https://www.investopedia.com/terms/m/moneymarket.asp",
    "hedge fund": "https://www.investopedia.com/terms/h/hedgefund.asp",
    "private equity": "https://www.investopedia.com/terms/p/privateequity.asp",
    "venture capital": "https://www.investopedia.com/terms/v/venturecapital.asp",
    "ipo": "https://www.investopedia.com/terms/i/ipo.asp",
    "merger": "https://www.investopedia.com/terms/m/merger.asp",
    "acquisition": "https://www.investopedia.com/terms/a/acquisition.asp",
    "valuation": "https://www.investopedia.com/terms/v/valuation.asp",
    "dcf": "https://www.investopedia.com/terms/d/dcf.asp",
    "financial statement": "https://www.investopedia.com/terms/f/financial-statements.asp",
    "audit": "https://www.investopedia.com/terms/a/audit.asp",
    "accounting": "https://www.investopedia.com/terms/a/accounting.asp",
    "bookkeeping": "https://www.investopedia.com/terms/b/bookkeeping.asp",
    "cpa": "https://www.investopedia.com/terms/c/cpa.asp",
    "financial advisor": "https://www.investopedia.com/terms/f/financial-advisor.asp",
    "fiduciary": "https://www.investopedia.com/terms/f/fiduciary.asp",
    "robo advisor": "https://www.investopedia.com/terms/r/roboadvisor-roboadviser.asp",
    "asset allocation": "https://www.investopedia.com/terms/a/assetallocation.asp",
    "rebalancing": "https://www.investopedia.com/terms/r/rebalancing.asp",
    "dollar cost averaging": "https://www.investopedia.com/terms/d/dollarcostaveraging.asp",
    "compound growth": "https://www.investopedia.com/terms/c/compoundgrowth.asp",
    "time value of money": "https://www.investopedia.com/terms/t/timevalueofmoney.asp",
    "present value": "https://www.investopedia.com/terms/p/presentvalue.asp",
    "future value": "https://www.investopedia.com/terms/f/futurevalue.asp",
    "annuity": "https://www.investopedia.com/terms/a/annuity.asp",
    "pension": "https://www.investopedia.com/terms/p/pensionplan.asp",
    "social security": "https://www.investopedia.com/terms/s/socialsecurity.asp",
    "medicare": "https://www.investopedia.com/terms/m/medicare.asp",
    "medicaid": "https://www.investopedia.com/terms/m/medicaid.asp",
    "health insurance": "https://www.investopedia.com/terms/h/healthinsurance.asp",
    "life insurance": "https://www.investopedia.com/terms/l/lifeinsurance.asp",
    "disability insurance": "https://www.investopedia.com/terms/d/disability-insurance.asp",
    "auto insurance": "https://www.investopedia.com/terms/a/auto-insurance.asp",
    "home insurance": "https://www.investopedia.com/terms/h/homeowners-insurance.asp",
    "umbrella insurance": "https://www.investopedia.com/terms/u/umbrella-insurance-policy.asp",
    "deductible": "https://www.investopedia.com/terms/d/deductible.asp",
    "premium": "https://www.investopedia.com/terms/p/premium.asp",
    "copay": "https://www.investopedia.com/terms/c/copay.asp",
    "coinsurance": "https://www.investopedia.com/terms/c/coinsurance.asp",
    "out of pocket": "https://www.investopedia.com/terms/o/outofpocket.asp",
    "hsa": "https://www.investopedia.com/terms/h/hsa.asp",
    "fsa": "https://www.investopedia.com/terms/f/flexiblespendingaccount.asp",
    "529 plan": "https://www.investopedia.com/terms/1/529plan.asp",
    "coverdell esa": "https://www.investopedia.com/terms/c/coverdellesa.asp",
    "student loan": "https://www.investopedia.com/terms/s/student-debt.asp",
    "fafsa": "https://www.investopedia.com/terms/f/federal-application-of-student-aid-fafsa.asp",
    "pell grant": "https://www.investopedia.com/terms/p/pell-grant.asp",
    "subsidized loan": "https://www.investopedia.com/terms/s/subsidized-loan.asp",
    "unsubsidized loan": "https://www.investopedia.com/terms/u/unsubsidized-loan.asp",
    "consolidation": "https://www.investopedia.com/terms/s/student-loan-consolidation.asp",
    "refinancing": "https://www.investopedia.com/terms/r/refinance.asp",
    "amortization": "https://www.investopedia.com/terms/a/amortization.asp",
    "escrow": "https://www.investopedia.com/terms/e/escrow.asp",
    "closing costs": "https://www.investopedia.com/terms/c/closingcosts.asp",
    "down payment": "https://www.investopedia.com/terms/d/down_payment.asp",
    "pmi": "https://www.investopedia.com/terms/p/private-mortgage-insurance.asp",
    "home equity": "https://www.investopedia.com/terms/h/home_equity.asp",
    "heloc": "https://www.investopedia.com/terms/h/homeequityloan.asp",
    "reverse mortgage": "https://www.investopedia.com/terms/r/reverse-mortgage.asp",
    "foreclosure": "https://www.investopedia.com/terms/f/foreclosure.asp",
    "short sale": "https://www.investopedia.com/terms/s/shortsale.asp",
    "real estate agent": "https://www.investopedia.com/terms/r/realestateagent.asp",
    "realtor": "https://www.investopedia.com/terms/r/realtor.asp",
    "mls": "https://www.investopedia.com/terms/m/multiple-listing-service.asp",
    "appraisal": "https://www.investopedia.com/terms/a/appraisal.asp",
    "home inspection": "https://www.investopedia.com/terms/h/home-inspection.asp",
    "title insurance": "https://www.investopedia.com/terms/t/title_insurance.asp",
    "deed": "https://www.investopedia.com/terms/d/deed.asp",
    "lien": "https://www.investopedia.com/terms/l/lien.asp",
    "property tax": "https://www.investopedia.com/terms/p/propertytax.asp",
    "hoa": "https://www.investopedia.com/terms/h/hoa.asp",
    "condo": "https://www.investopedia.com/terms/c/condominium.asp",
    "townhouse": "https://www.investopedia.com/terms/t/townhome.asp",
    "co-op": "https://www.investopedia.com/terms/c/co_op.asp",
    "rental property": "https://www.investopedia.com/terms/r/residentialrentalproperty.asp",
    "landlord": "https://www.investopedia.com/terms/l/landlord.asp",
    "tenant": "https://www.investopedia.com/terms/l/lessee.asp",
    "lease": "https://www.investopedia.com/terms/l/lease.asp",
    "security deposit": "https://www.investopedia.com/terms/s/security-deposit.asp",
    "eviction": "https://www.investopedia.com/terms/e/eviction.asp",
    "rent control": "https://www.investopedia.com/terms/r/rent-control.asp",
    "cap rate": "https://www.investopedia.com/terms/c/capitalizationrate.asp",
    "cash on cash return": "https://www.investopedia.com/terms/c/cashoncashreturn.asp",
    "gross rental yield": "https://www.investopedia.com/terms/g/gross-rental-yield.asp",
    "net operating income": "https://www.investopedia.com/terms/n/noi.asp",
    "depreciation": "https://www.investopedia.com/terms/d/depreciation.asp",
    "1031 exchange": "https://www.investopedia.com/terms/1/1031exchange.asp",
}


# Function to build the source link for the response
def get_safe_source_link(query: str) -> str:
    """Return a safe Investopedia URL for a query: canonical → validated guess → search."""

    # If canonical mapping exists, return it (prioritize exact matches first)
    q = query.lower()
    
    # First try exact matches
    if q in CANONICAL_INVESTOPEDIA:
        return CANONICAL_INVESTOPEDIA[q]
    
    # Then try partial matches, prioritizing longer matches
    matches = []
    for key, url in CANONICAL_INVESTOPEDIA.items():
        if key in q:
            matches.append((len(key), url))
    
    if matches:
        # Return the URL for the longest matching key
        matches.sort(reverse=True)
        return matches[0][1]
    
    # If canonical mapping fails, try multiple heuristic guesses
    guessed_urls = []
    
    # Try the primary guess
    primary_guess = guess_investopedia_url(query)
    if primary_guess:
        guessed_urls.append(primary_guess)
    
    # Try heuristic URL generation for extracted financial terms
    financial_terms = extract_financial_terms(query)
    for term in financial_terms:
        slug = re.sub(r"[^a-z0-9\s]", "", term.lower()).strip()
        slug = re.sub(r"\s+", "", slug)
        if slug:
            first_letter = slug[0]
            guessed_urls.append(f"https://www.investopedia.com/terms/{first_letter}/{slug}.asp")
    
    # Test each guessed URL
    for url in guessed_urls:
        if url_exists(url):
            return url

    # Final fallback: use Investopedia's alphabetical directory
    search_term = extract_search_term(query)
    if search_term:
        main_term = search_term.split()[0] if search_term else ""
        if main_term and main_term[0].isalpha():
            first_letter = main_term[0].lower()
            return f"https://www.investopedia.com/terms-beginning-with-{first_letter}-{4769351 + ord(first_letter) - ord('a')}"
    
    return "https://www.investopedia.com/"

def extract_financial_terms(query: str) -> list:
    """Extract potential financial terms from a query."""
    q = query.lower()
    
    # Common financial term patterns
    financial_patterns = [
        r'\b(?:stock|bond|investment|trading|portfolio|dividend|interest|loan|mortgage|credit|debt|budget|savings|retirement|insurance|tax|fund|etf|broker|market|economy|inflation|recession|gdp|cryptocurrency|crypocurrency|crypto|bitcoin|forex|options|futures|derivatives|asset|liability|equity|capital|yield|return|risk|diversification)\b',
        r'\b(?:401k|ira|roth|hsa|fsa|529|pmi|heloc|reit|ipo|pe ratio|market cap|bull market|bear market)\b',
        r'\b(?:mutual fund|index fund|hedge fund|private equity|venture capital|real estate|emergency fund|checking account|savings account|credit card|debit card)\b'
    ]
    
    terms = []
    for pattern in financial_patterns:
        matches = re.findall(pattern, q)
        terms.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)
    
    return unique_terms[:3]  # Limit to top 3 terms

def extract_search_term(query: str) -> str:
    """Extract the most relevant search term from a query."""
    q = query.lower()
    
    # Remove common question words
    stop_words = {'what', 'is', 'are', 'how', 'can', 'do', 'does', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'about', 'explain', 'tell', 'me', 'you', 'i', 'my', 'your', 'should', 'would', 'could'}
    
    tokens = re.findall(r'\b[a-zA-Z]+\b', q)
    meaningful_tokens = [t for t in tokens if t.lower() not in stop_words and len(t) > 2]
    
    if meaningful_tokens:
        return ' '.join(meaningful_tokens[:3])  # Use first 3 meaningful words
    
    return query.strip()



# Routes
@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint: curated-first (optional), else OpenAI; always append valid Source."""

    # Getting the data
    data = request.json

    try : 
        # Get the user's message from the request
        user_message = data.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # First try curated knowledge (toggle via USE_CURATED)
        if os.getenv("USE_CURATED", "true").lower() == "true":
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
                        "You are a financial assistant that explains concepts in simple language. "
                        "Provide a clear, concise explanation in 2-4 sentences. "
                        "Focus on what the concept is, why it matters, and practical information. "
                        "Always end with 'Source: [valid URL]' on a separate line."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        message = chat.choices[0].message.content.strip()

        # Ensure we have a valid Source line. If model provided an invalid URL, repair it.
        src_match = re.search(r"(?im)^\s*Source:\s*(\S+)", message)
        if src_match:
            provided_url = src_match.group(1).strip()
            if not url_exists(provided_url):
                system_prompt = (
                    "You are a financial assistant that explains concepts in simple language. "
                    "Provide a clear, concise explanation in 2-4 sentences. "
                    "Focus on what the concept is, why it matters, and practical information. "
                    "Always end with 'Source: [valid URL]' on a separate line."
                )
                safe_url = get_safe_source_link(user_message)
                message = re.sub(r"(?im)^\s*Source:.*$", f"Source: {safe_url}", message)
        else:
            # If the model didn't produce a Source line, append a best-effort URL
            source_url = get_safe_source_link(user_message)
            message = message + f"\nSource: {source_url}"


        # Returning the response
        return jsonify({"response": message})
    except Exception as e:

        # Returning the error
        return jsonify({"error": str(e)}), 500


# Health Check Endpoint
@app.route('/', methods=['GET'])
def health():
    """Simple health check endpoint for Railway/Vercel probes."""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)