# 💬 LLM‑Powered Financial Services Chatbot

![React 18.x](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=white&style=for-the-badge)
![Vite 7.x](https://img.shields.io/badge/Vite-7.x-646CFF?logo=vite&logoColor=white&style=for-the-badge)
![Tailwind CSS 4.x](https://img.shields.io/badge/TailwindCSS-4.x-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge)
![Flask 3.x](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white&style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Inference_API-FFD21E?logo=huggingface&logoColor=black&style=for-the-badge)
![OpenAI API](https://img.shields.io/badge/OpenAI-Fallback-412991?logo=openai&logoColor=white&style=for-the-badge)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel&logoColor=white&style=for-the-badge)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render&logoColor=white&style=for-the-badge)

An intelligent, responsive financial services chatbot built with **React + Vite + Tailwind** on the frontend and **Flask + HuggingFace** on the backend. Delivers concise, cited answers to financial questions with a **dual-provider LLM architecture** — HuggingFace (free, primary) and OpenAI (paid, fallback).

**Try asking:**
- "What is cryptocurrency?"
- "Explain credit default swap in simple terms"
- "How does compound interest work?"
- "What are the risks of trading stocks?"

Every answer includes **valid Investopedia source links** for further reading.

---

## 🚀 Live App

| Service | URL |
|---------|-----|
| **Frontend** (Vercel) | [finsathi-chatbot-madhavp.vercel.app](https://finsathi-chatbot-madhavp.vercel.app) |
| **Backend** (Render) | [madhavp-financial-service-backend.onrender.com](https://madhavp-financial-service-backend.onrender.com) |
| **GitHub** | [Madhav-P-2005/LLM_Powered-Financial-Service-ChatBot](https://github.com/Madhav-P-2005/LLM_Powered-Financial-Service-ChatBot) |

---

## ✨ Features

- 🗨️ **Conversational Chat UI** — Real-time chat with message history and auto-scroll
- 📚 **Curated Knowledge Base** — Instant, hand-written answers for high-traffic topics (no API call needed)
- 🤖 **Qwen2.5-7B LLM** — Powered by HuggingFace's free Inference API (Qwen2.5-7B-Instruct)
- 🔄 **OpenAI Fallback** — Automatic fallback to OpenAI (gpt-4o-mini) if HuggingFace is down
- 🔗 **Smart Citations** — 200+ verified Investopedia URLs with multi-tier fallback resolution
- ⚡ **Retry Button** — Failed messages show a styled retry button for better UX
- 🌓 **Dark/Light Mode** — Auto-applies based on saved or system preference
- 🧹 **Clear Chat & Home** — Quick-action toolbar buttons
- 📱 **Fully Responsive** — Mobile-first design with Tailwind CSS
- 🔒 **Secure** — API keys loaded from backend `.env`, never exposed to the browser

---

## 🧠 How It Works

### Dual-Provider LLM Architecture

```
User Question
     │
     ▼
┌────────────────────┐
│  Curated KB        │ ──→ Instant response (no API call)
│  (6 topics)        │     Hand-written, verified answers
└───────┬────────────┘
        │ Not found
        ▼
┌────────────────────┐
│  HuggingFace       │ ──→ FREE (Qwen2.5-7B-Instruct)
│  (Primary)         │     With retry + exponential backoff
└───────┬────────────┘
        │ Failed / rate-limited
        ▼
┌────────────────────┐
│  OpenAI            │ ──→ PAID fallback (gpt-4o-mini)
│  (Fallback)        │     Only if OPENAI_API_KEY is set
└────────────────────┘
```

### Smart URL Resolution (4-tier)

1. **Exact match** — Direct lookup from 200+ verified Investopedia URLs
2. **Partial match** — Longest canonical key found inside the user's query
3. **Heuristic** — Auto-generate URL from financial term patterns
4. **Directory fallback** — Link to Investopedia's alphabetical term pages

---

## 🗂️ Project Structure

```text
LLM-Powered Financial Services Chatbot/
│
├── financial-service-chatbot-backend/
│   ├── app.py                          # Flask entry point (~70 lines)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py                     # /chat and / endpoints (Blueprint)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py             # HuggingFace + OpenAI dual-provider
│   │   └── url_service.py             # Investopedia URL generation
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── curated_kb.py              # Hand-written answers (6 topics)
│   │   └── canonical_urls.py          # 200+ verified Investopedia URLs
│   ├── config/
│   │   └── .env                       # HF_API_TOKEN + OPENAI_API_KEY
│   ├── requirements.txt               # Python dependencies
│   ├── Procfile                       # Render start command
│   ├── Dockerfile                     # Container config (optional)
│   └── MyEnvironment/                 # Python venv (gitignored)
│
├── financial-service-chatbot-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx             # Header with theme toggle
│   │   │   └── Footer.jsx            # Footer with social links
│   │   ├── pages/
│   │   │   ├── HomePage.jsx           # Landing page
│   │   │   └── ChatPage.jsx          # Chat UI (Retry/Clear/Home)
│   │   ├── App.jsx                    # Router setup
│   │   ├── main.jsx                   # React entry point
│   │   └── index.css                  # Global styles
│   ├── public/
│   │   └── finsathi.svg               # Custom favicon
│   ├── tailwind.config.js             # darkMode: 'class'
│   ├── vite.config.js                 # Vite configuration
│   └── package.json                   # Node dependencies
│
├── Readme.md                          # This file
├── LICENSE                            # MIT License
└── .gitignore                         # Ignores .env, __pycache__, node_modules, etc.
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Node.js** (v18+) and **npm**
- **Python 3.11+**
- A free [HuggingFace account](https://huggingface.co/) (for API token)

---

### 1️⃣ Backend Setup (Flask)

Open a terminal and navigate to `financial-service-chatbot-backend/`:

#### A. Create & Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv MyEnvironment
.\MyEnvironment\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv MyEnvironment
source MyEnvironment/bin/activate
```

#### B. Install Dependencies

```bash
pip install -r requirements.txt
```

#### C. Configure Environment Variables

Create the file `config/.env` with your keys:

```env
# PRIMARY — HuggingFace Inference API (FREE, no expiry)
# Get your token at: https://huggingface.co/settings/tokens
# Click "Create new token" → Select "Read" access → Copy the hf_... token
HF_API_TOKEN=hf_your_actual_token_here

# FALLBACK — OpenAI API (PAID, optional)
# Only needed if you want OpenAI as a backup when HuggingFace is down
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-4o-mini
```

> ⚠️ **Never commit `.env` to GitHub!** It is already listed in `.gitignore`.

#### D. Run the Backend Server

```powershell
python app.py
```

Backend runs at: **http://127.0.0.1:5000**

You can verify it's working by visiting `http://127.0.0.1:5000/` in your browser — you should see:
```json
{ "status": "ok", "providers": { "huggingface": { "configured": true, ... } } }
```

---

### 2️⃣ Frontend Setup (React + Vite)

Open a **second terminal** and navigate to `financial-service-chatbot-frontend/`:

#### A. Install Packages

```bash
npm install
```

#### B. Run the Development Server

```bash
npm run dev
```

Frontend runs at: **http://localhost:5173**

Open `http://localhost:5173` in your browser, click **"Get Started"**, and try asking:
- "What is a credit card?" → Curated answer (instant)
- "What is dollar cost averaging?" → HuggingFace LLM answer

---

## 🔧 Tech Stack & Dependencies

### Frontend

| Package | Version | Purpose |
|---------|---------|---------|
| React | 18.x | UI library |
| Vite | 7.x | Build tool & dev server |
| Tailwind CSS | 4.x | Utility-first styling |
| Axios | 1.x | HTTP client for API calls |
| React Router | 6.x | Client-side routing |
| React Icons | 5.x | Icon library (FaPaperPlane, FaSpinner, etc.) |

### Backend

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.x | Web framework |
| Flask-CORS | 4.x | Cross-origin support for frontend |
| huggingface_hub | 0.25+ | **Primary LLM** — HuggingFace Inference API |
| openai | 1.x | **Fallback LLM** — OpenAI API (optional) |
| python-dotenv | 1.x | Load `.env` variables |
| gunicorn | 23.x | Production WSGI server (Render) |

---

## 🔐 Environment Variables

### Backend (`config/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_API_TOKEN` | ✅ Yes | Free HuggingFace Inference API token |
| `OPENAI_API_KEY` | ❌ Optional | Paid OpenAI API key (fallback only) |
| `OPENAI_MODEL` | ❌ Optional | OpenAI model name (default: `gpt-4o-mini`) |

### Frontend (Vercel Environment Variables)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE` | ✅ For production | Backend URL (e.g., `https://madhavp-financial-service-backend.onrender.com`) |

---

## 🔗 API Contract

### Health Check

```
GET /
```

**Response:**
```json
{
  "status": "ok",
  "providers": {
    "huggingface": { "configured": true, "model": "Qwen/Qwen2.5-7B-Instruct", "role": "primary (free)" },
    "openai": { "configured": false, "model": "gpt-4o-mini", "role": "fallback (paid)" }
  }
}
```

### Chat

```
POST /chat
Content-Type: application/json
```

**Request:**
```json
{ "message": "What is a credit default swap?" }
```

**Response:**
```json
{ "response": "Credit Default Swap (CDS) — Plain-English definition\n• A CDS is a derivative contract...\nSource: https://www.investopedia.com/terms/c/creditdefaultswap.asp" }
```

**Error Response (500):**
```json
{ "error": "Sorry, I couldn't process your question right now. Error: ..." }
```

CORS is configured for `http://localhost:5173` (dev) and `https://finsathi-chatbot-madhavp.vercel.app` (production).

---

## 📦 Deployment Guide

### Backend → Render

1. **Create a new Web Service** on [Render](https://render.com/).
2. **Connect your GitHub repository** and select the branch (`Project-3`).
3. **Configure the service:**

| Setting | Value |
|---------|-------|
| **Name** | `madhavp-financial-service-backend` |
| **Runtime** | Python 3 |
| **Root Directory** | `financial-service-chatbot-backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

4. **Set Environment Variables** in the Render dashboard:

| Key | Value |
|-----|-------|
| `HF_API_TOKEN` | `hf_your_token_here` |
| `OPENAI_API_KEY` | *(optional — only if you have one)* |

5. Click **Deploy**. Render will build and start your backend.
6. **Verify**: Visit your Render URL — you should see the health check JSON.

> 💡 **Tip**: Render's free tier spins down after 15 min of inactivity. The first request after sleep may take ~30s (cold start).

---

### Frontend → Vercel

1. **Import your repository** on [Vercel](https://vercel.com/).
2. **Configure the project:**

| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `financial-service-chatbot-frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

3. **Set Environment Variables** in Vercel dashboard:

| Key | Value |
|-----|-------|
| `VITE_API_BASE` | `https://madhavp-financial-service-backend.onrender.com` |

> ⚠️ **Important**: Vite environment variables must start with `VITE_` to be accessible in the frontend code.

4. Click **Deploy**. Vercel will build the React app and serve it.
5. **Verify**: Open your Vercel URL → Click "Get Started" → Ask a question.

---

### Updating the Live App

Whenever you push new code to GitHub, both Render and Vercel will **auto-redeploy**. If you change environment variables (like API tokens), update them in the respective dashboards and trigger a manual redeploy.

---

## 🤝 Contributing

PRs and suggestions welcome. Open an issue for bugs or improvements.

## 🪪 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Built with 💙 by [Madhav P](https://www.linkedin.com/in/madhav-p-156b9b290/)
