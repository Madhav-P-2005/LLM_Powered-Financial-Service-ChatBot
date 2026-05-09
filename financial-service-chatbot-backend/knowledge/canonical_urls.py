"""
Canonical Investopedia URL Mappings for the Financial Services Chatbot.

This module contains 200+ verified Investopedia URLs mapped to common
financial terms. These are used as the primary source for generating
reliable citation links in chatbot responses.

HOW URL RESOLUTION WORKS (Priority Order):
    1. Exact match  →  user query matches a key exactly
    2. Partial match →  a key is found inside the user query (longest wins)
    3. Heuristic     →  auto-generate URL from the term pattern
    4. Fallback      →  Investopedia alphabetical directory page

HOW TO ADD A NEW MAPPING:
    Add a new key-value pair below. The key should be lowercase.
    The URL should be verified (test it in your browser first!).
"""


# ──────────────────────────────────────────────────────────────────────
# Verified Investopedia URL mappings
# Key   : lowercase financial term (what the user might ask about)
# Value : verified Investopedia URL for that topic
# ──────────────────────────────────────────────────────────────────────

CANONICAL_INVESTOPEDIA = {
    # ── Credit & Banking ──────────────────────────────────────────────
    "credit default swap":  "https://www.investopedia.com/terms/c/creditdefaultswap.asp",
    "credit card":          "https://www.investopedia.com/terms/c/creditcard.asp",
    "bank":                 "https://www.investopedia.com/terms/b/bank.asp",
    "phishing":             "https://www.investopedia.com/terms/p/phishing.asp",
    "credit score":         "https://www.investopedia.com/terms/c/credit_score.asp",
    "emi":                  "https://www.investopedia.com/terms/e/equated-monthly-installment-emi.asp",
    "credit limit":         "https://www.investopedia.com/terms/c/credit_limit.asp",
    "credit utilization":   "https://www.investopedia.com/terms/c/credit-utilization-rate.asp",
    "debit card":           "https://www.investopedia.com/terms/d/debitcard.asp",
    "checking account":     "https://www.investopedia.com/terms/c/checkingaccount.asp",
    "savings account":      "https://www.investopedia.com/terms/s/savingsaccount.asp",

    # ── Stocks & Equities ─────────────────────────────────────────────
    "stock":                "https://www.investopedia.com/terms/s/stock.asp",
    "stocks":               "https://www.investopedia.com/terms/s/stock.asp",
    "equity":               "https://www.investopedia.com/terms/e/equity.asp",
    "dividend":             "https://www.investopedia.com/terms/d/dividend.asp",
    "dividends":            "https://www.investopedia.com/terms/d/dividend.asp",
    "market cap":           "https://www.investopedia.com/terms/m/marketcapitalization.asp",
    "pe ratio":             "https://www.investopedia.com/terms/p/price-earningsratio.asp",
    "bull market":          "https://www.investopedia.com/terms/b/bullmarket.asp",
    "bear market":          "https://www.investopedia.com/terms/b/bearmarket.asp",
    "ipo":                  "https://www.investopedia.com/terms/i/ipo.asp",
    "stock market":         "https://www.investopedia.com/terms/s/stockmarket.asp",

    # ── Trading & Markets ─────────────────────────────────────────────
    "trading":              "https://www.investopedia.com/trading-4427765",
    "how to trade":         "https://www.investopedia.com/trading-4427765",
    "volatility":           "https://www.investopedia.com/terms/v/volatility.asp",
    "liquidity":            "https://www.investopedia.com/terms/l/liquidity.asp",
    "market":               "https://www.investopedia.com/terms/m/market.asp",
    "financial market":     "https://www.investopedia.com/terms/f/financial-market.asp",
    "capital market":       "https://www.investopedia.com/terms/c/capitalmarkets.asp",
    "money market":         "https://www.investopedia.com/terms/m/moneymarket.asp",
    "nasdaq":               "https://www.investopedia.com/terms/n/nasdaq.asp",
    "nyse":                 "https://www.investopedia.com/terms/n/nyse.asp",
    "s&p 500":              "https://www.investopedia.com/terms/s/sp500.asp",
    "dow jones":            "https://www.investopedia.com/terms/d/djia.asp",

    # ── Cryptocurrency & Blockchain ───────────────────────────────────
    "crypto":               "https://www.investopedia.com/cryptocurrency-4427699",
    "cryptocurrency":       "https://www.investopedia.com/cryptocurrency-4427699",
    "crypocurrency":        "https://www.investopedia.com/cryptocurrency-4427699",   # common typo
    "what is cryptocurrency": "https://www.investopedia.com/cryptocurrency-4427699",
    "what is crypto":       "https://www.investopedia.com/cryptocurrency-4427699",
    "bitcoin":              "https://www.investopedia.com/terms/b/bitcoin.asp",
    "blockchain":           "https://www.investopedia.com/terms/b/blockchain.asp",

    # ── Bonds & Fixed Income ──────────────────────────────────────────
    "bond":                 "https://www.investopedia.com/terms/b/bond.asp",
    "bonds":                "https://www.investopedia.com/terms/b/bond.asp",
    "bond yield":           "https://www.investopedia.com/terms/b/bond-yield.asp",
    "yield":                "https://www.investopedia.com/terms/y/yield.asp",
    "treasury":             "https://www.investopedia.com/terms/t/treasurybond.asp",

    # ── Funds & Investing ─────────────────────────────────────────────
    "etf":                  "https://www.investopedia.com/terms/e/etf.asp",
    "etfs":                 "https://www.investopedia.com/terms/e/etf.asp",
    "exchange traded fund": "https://www.investopedia.com/terms/e/etf.asp",
    "mutual fund":          "https://www.investopedia.com/terms/m/mutualfund.asp",
    "mutual funds":         "https://www.investopedia.com/terms/m/mutualfund.asp",
    "index fund":           "https://www.investopedia.com/terms/i/indexfund.asp",
    "index funds":          "https://www.investopedia.com/terms/i/indexfund.asp",
    "hedge fund":           "https://www.investopedia.com/terms/h/hedgefund.asp",
    "expense ratio":        "https://www.investopedia.com/terms/e/expenseratio.asp",
    "investment":           "https://www.investopedia.com/terms/i/investment.asp",
    "investing":            "https://www.investopedia.com/terms/i/investment.asp",
    "portfolio":            "https://www.investopedia.com/terms/p/portfolio.asp",
    "diversification":      "https://www.investopedia.com/terms/d/diversification.asp",
    "asset allocation":     "https://www.investopedia.com/terms/a/assetallocation.asp",
    "rebalancing":          "https://www.investopedia.com/terms/r/rebalancing.asp",
    "dollar cost averaging": "https://www.investopedia.com/terms/d/dollarcostaveraging.asp",
    "risk":                 "https://www.investopedia.com/terms/r/risk.asp",
    "return":               "https://www.investopedia.com/terms/r/return.asp",
    "broker":               "https://www.investopedia.com/terms/b/broker.asp",
    "brokers":              "https://www.investopedia.com/terms/b/broker.asp",
    "robo advisor":         "https://www.investopedia.com/terms/r/roboadvisor-roboadviser.asp",

    # ── Derivatives & Forex ───────────────────────────────────────────
    "forex":                "https://www.investopedia.com/terms/f/forex.asp",
    "derivatives":          "https://www.investopedia.com/terms/d/derivative.asp",
    "options":              "https://www.investopedia.com/terms/o/option.asp",
    "futures":              "https://www.investopedia.com/terms/f/futures.asp",

    # ── Loans & Mortgages ─────────────────────────────────────────────
    "loan":                 "https://www.investopedia.com/terms/l/loan.asp",
    "mortgage":             "https://www.investopedia.com/terms/m/mortgage.asp",
    "interest rate":        "https://www.investopedia.com/terms/i/interestrate.asp",
    "apr":                  "https://www.investopedia.com/terms/a/apr.asp",
    "compound interest":    "https://www.investopedia.com/terms/c/compoundinterest.asp",
    "refinancing":          "https://www.investopedia.com/terms/r/refinance.asp",
    "amortization":         "https://www.investopedia.com/terms/a/amortization.asp",
    "escrow":               "https://www.investopedia.com/terms/e/escrow.asp",
    "closing costs":        "https://www.investopedia.com/terms/c/closingcosts.asp",
    "down payment":         "https://www.investopedia.com/terms/d/down_payment.asp",
    "pmi":                  "https://www.investopedia.com/terms/p/private-mortgage-insurance.asp",
    "home equity":          "https://www.investopedia.com/terms/h/home_equity.asp",
    "heloc":                "https://www.investopedia.com/terms/h/homeequityloan.asp",
    "reverse mortgage":     "https://www.investopedia.com/terms/r/reverse-mortgage.asp",
    "foreclosure":          "https://www.investopedia.com/terms/f/foreclosure.asp",
    "student loan":         "https://www.investopedia.com/terms/s/student-debt.asp",
    "fafsa":                "https://www.investopedia.com/terms/f/federal-application-of-student-aid-fafsa.asp",
    "pell grant":           "https://www.investopedia.com/terms/p/pell-grant.asp",
    "subsidized loan":      "https://www.investopedia.com/terms/s/subsidized-loan.asp",
    "unsubsidized loan":    "https://www.investopedia.com/terms/u/unsubsidized-loan.asp",
    "consolidation":        "https://www.investopedia.com/terms/s/student-loan-consolidation.asp",

    # ── Budgeting & Personal Finance ──────────────────────────────────
    "budget":               "https://www.investopedia.com/terms/b/budget.asp",
    "budgeting":            "https://www.investopedia.com/terms/b/budget.asp",
    "financing":            "https://www.investopedia.com/terms/f/financing.asp",
    "financial planning":   "https://www.investopedia.com/terms/f/financial_plan.asp",
    "emergency fund":       "https://www.investopedia.com/terms/e/emergency_fund.asp",
    "net worth":            "https://www.investopedia.com/terms/n/networth.asp",
    "cash flow":            "https://www.investopedia.com/terms/c/cashflow.asp",
    "debt":                 "https://www.investopedia.com/terms/d/debt.asp",
    "bankruptcy":           "https://www.investopedia.com/terms/b/bankruptcy.asp",
    "financial advisor":    "https://www.investopedia.com/terms/f/financial-advisor.asp",
    "fiduciary":            "https://www.investopedia.com/terms/f/fiduciary.asp",

    # ── Accounting & Financial Statements ─────────────────────────────
    "asset":                "https://www.investopedia.com/terms/a/asset.asp",
    "liability":            "https://www.investopedia.com/terms/l/liability.asp",
    "balance sheet":        "https://www.investopedia.com/terms/b/balancesheet.asp",
    "income statement":     "https://www.investopedia.com/terms/i/incomestatement.asp",
    "financial statement":  "https://www.investopedia.com/terms/f/financial-statements.asp",
    "audit":                "https://www.investopedia.com/terms/a/audit.asp",
    "accounting":           "https://www.investopedia.com/terms/a/accounting.asp",
    "bookkeeping":          "https://www.investopedia.com/terms/b/bookkeeping.asp",
    "cpa":                  "https://www.investopedia.com/terms/c/cpa.asp",
    "depreciation":         "https://www.investopedia.com/terms/d/depreciation.asp",

    # ── Taxes ─────────────────────────────────────────────────────────
    "tax":                  "https://www.investopedia.com/terms/t/taxes.asp",
    "taxes":                "https://www.investopedia.com/terms/t/taxes.asp",
    "capital gains":        "https://www.investopedia.com/terms/c/capitalgain.asp",
    "tax deduction":        "https://www.investopedia.com/terms/t/tax-deduction.asp",

    # ── Insurance ─────────────────────────────────────────────────────
    "insurance":            "https://www.investopedia.com/terms/i/insurance.asp",
    "health insurance":     "https://www.investopedia.com/terms/h/healthinsurance.asp",
    "life insurance":       "https://www.investopedia.com/terms/l/lifeinsurance.asp",
    "disability insurance": "https://www.investopedia.com/terms/d/disability-insurance.asp",
    "auto insurance":       "https://www.investopedia.com/terms/a/auto-insurance.asp",
    "home insurance":       "https://www.investopedia.com/terms/h/homeowners-insurance.asp",
    "umbrella insurance":   "https://www.investopedia.com/terms/u/umbrella-insurance-policy.asp",
    "deductible":           "https://www.investopedia.com/terms/d/deductible.asp",
    "premium":              "https://www.investopedia.com/terms/p/premium.asp",
    "copay":                "https://www.investopedia.com/terms/c/copay.asp",
    "coinsurance":          "https://www.investopedia.com/terms/c/coinsurance.asp",
    "out of pocket":        "https://www.investopedia.com/terms/o/outofpocket.asp",
    "hsa":                  "https://www.investopedia.com/terms/h/hsa.asp",
    "fsa":                  "https://www.investopedia.com/terms/f/flexiblespendingaccount.asp",

    # ── Retirement & Savings ──────────────────────────────────────────
    "retirement planning":  "https://www.investopedia.com/terms/r/retirement-planning.asp",
    "401k":                 "https://www.investopedia.com/terms/1/401kplan.asp",
    "ira":                  "https://www.investopedia.com/terms/i/ira.asp",
    "roth ira":             "https://www.investopedia.com/terms/r/rothira.asp",
    "annuity":              "https://www.investopedia.com/terms/a/annuity.asp",
    "pension":              "https://www.investopedia.com/terms/p/pensionplan.asp",
    "social security":      "https://www.investopedia.com/terms/s/socialsecurity.asp",
    "medicare":             "https://www.investopedia.com/terms/m/medicare.asp",
    "medicaid":             "https://www.investopedia.com/terms/m/medicaid.asp",
    "529 plan":             "https://www.investopedia.com/terms/1/529plan.asp",
    "coverdell esa":        "https://www.investopedia.com/terms/c/coverdellesa.asp",

    # ── Economics ─────────────────────────────────────────────────────
    "inflation":            "https://www.investopedia.com/terms/i/inflation.asp",
    "recession":            "https://www.investopedia.com/terms/r/recession.asp",
    "gdp":                  "https://www.investopedia.com/terms/g/gdp.asp",
    "economics":            "https://www.investopedia.com/terms/e/economics.asp",
    "supply and demand":    "https://www.investopedia.com/terms/l/law-of-supply-demand.asp",
    "fed":                  "https://www.investopedia.com/terms/f/federalreservebank.asp",
    "federal reserve":      "https://www.investopedia.com/terms/f/federalreservebank.asp",
    "monetary policy":      "https://www.investopedia.com/terms/m/monetarypolicy.asp",
    "fiscal policy":        "https://www.investopedia.com/terms/f/fiscalpolicy.asp",

    # ── Financial Math & Valuation ────────────────────────────────────
    "compound growth":      "https://www.investopedia.com/terms/c/compoundgrowth.asp",
    "time value of money":  "https://www.investopedia.com/terms/t/timevalueofmoney.asp",
    "present value":        "https://www.investopedia.com/terms/p/presentvalue.asp",
    "future value":         "https://www.investopedia.com/terms/f/futurevalue.asp",
    "valuation":            "https://www.investopedia.com/terms/v/valuation.asp",
    "dcf":                  "https://www.investopedia.com/terms/d/dcf.asp",

    # ── Corporate Finance ─────────────────────────────────────────────
    "private equity":       "https://www.investopedia.com/terms/p/privateequity.asp",
    "venture capital":      "https://www.investopedia.com/terms/v/venturecapital.asp",
    "merger":               "https://www.investopedia.com/terms/m/merger.asp",
    "acquisition":          "https://www.investopedia.com/terms/a/acquisition.asp",

    # ── Real Estate ───────────────────────────────────────────────────
    "reit":                 "https://www.investopedia.com/terms/r/reit.asp",
    "reits":                "https://www.investopedia.com/terms/r/reit.asp",
    "real estate":          "https://www.investopedia.com/terms/r/realestate.asp",
    "short sale":           "https://www.investopedia.com/terms/s/shortsale.asp",
    "real estate agent":    "https://www.investopedia.com/terms/r/realestateagent.asp",
    "realtor":              "https://www.investopedia.com/terms/r/realtor.asp",
    "mls":                  "https://www.investopedia.com/terms/m/multiple-listing-service.asp",
    "appraisal":            "https://www.investopedia.com/terms/a/appraisal.asp",
    "home inspection":      "https://www.investopedia.com/terms/h/home-inspection.asp",
    "title insurance":      "https://www.investopedia.com/terms/t/title_insurance.asp",
    "deed":                 "https://www.investopedia.com/terms/d/deed.asp",
    "lien":                 "https://www.investopedia.com/terms/l/lien.asp",
    "property tax":         "https://www.investopedia.com/terms/p/propertytax.asp",
    "hoa":                  "https://www.investopedia.com/terms/h/hoa.asp",
    "condo":                "https://www.investopedia.com/terms/c/condominium.asp",
    "townhouse":            "https://www.investopedia.com/terms/t/townhome.asp",
    "co-op":                "https://www.investopedia.com/terms/c/co_op.asp",
    "rental property":      "https://www.investopedia.com/terms/r/residentialrentalproperty.asp",
    "landlord":             "https://www.investopedia.com/terms/l/landlord.asp",
    "tenant":               "https://www.investopedia.com/terms/l/lessee.asp",
    "lease":                "https://www.investopedia.com/terms/l/lease.asp",
    "security deposit":     "https://www.investopedia.com/terms/s/security-deposit.asp",
    "eviction":             "https://www.investopedia.com/terms/e/eviction.asp",
    "rent control":         "https://www.investopedia.com/terms/r/rent-control.asp",
    "cap rate":             "https://www.investopedia.com/terms/c/capitalizationrate.asp",
    "cash on cash return":  "https://www.investopedia.com/terms/c/cashoncashreturn.asp",
    "gross rental yield":   "https://www.investopedia.com/terms/g/gross-rental-yield.asp",
    "net operating income": "https://www.investopedia.com/terms/n/noi.asp",
    "1031 exchange":        "https://www.investopedia.com/terms/1/1031exchange.asp",

    # ── Commodities ───────────────────────────────────────────────────
    "commodity":            "https://www.investopedia.com/terms/c/commodity.asp",
    "commodities":          "https://www.investopedia.com/terms/c/commodity.asp",
    "gold":                 "https://www.investopedia.com/terms/g/gold.asp",
    "silver":               "https://www.investopedia.com/terms/s/silver.asp",
    "oil":                  "https://www.investopedia.com/terms/c/crude-oil.asp",
}
