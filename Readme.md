# 💬 LLM‑Powered Financial Services Chatbot (React + Vite + Tailwind + Flask)

![React 18.x](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=white&style=for-the-badge)
![Vite 5.x](https://img.shields.io/badge/Vite-5.x-646CFF?logo=vite&logoColor=white&style=for-the-badge)
![Tailwind CSS 3.x](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge)
![Flask 3.x](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white&style=for-the-badge)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white&style=for-the-badge)

A simple, responsive financial services chatbot that answers queries like:
- “What is a phishing scam?”
- “Explain credit default swap in simple terms.”
- “How can I secure my online banking?”

The bot replies in clear bullet points and includes a “Source:” link for citation (bonus requirement).

### 🚀 Live App
- Frontend (Vercel/Netlify): [link-here]
- Backend (Render/Railway): [link-here]
- GitHub Repo: [link-here]

## ✨ Features

- 🗨️ Conversational chat UI with history
- ⏳ Loading indicator while the model generates
- 📚 Answers in simple financial language
- 🔗 Always appends “Source:” with a reputable link (Investopedia/OpenAI-provided)
- 🌓 Dark/Light theme (auto-applies based on saved or system preference)
- 🧹 “Clear chat” and “Home” buttons on chat page
- 📱 Fully responsive UI (mobile-first)
- 🔒 OpenAI key loaded securely from backend `.env` (never exposed to browser)

## 🧠 How It Works

- Curated knowledge first: Common topics like “credit default swap”, “bank”, “phishing”, “credit score”, “EMI” return high-quality, bullet-point answers with Investopedia citations from a curated knowledge base in `financial-service-chatbot-backend/app.py`.
- OpenAI fallback: For other queries, the backend calls OpenAI (Chat Completions). The prompt enforces concise bullets and a final “Source:” line.
- Safety net: If the model forgets the “Source:”, the backend appends a best-effort Investopedia URL guess.

## 🗂️ Project Structure

```
LLM-Powered Financial Services Chatbot/
├── financial-service-chatbot-backend/
│   ├── app.py                  # Flask API (curated KB + OpenAI fallback)
│   ├── config/.env             # OPENAI_API_KEY and optional OPENAI_MODEL
│   ├── requirements.txt        # Backend dependencies
│   └── MyEnvironment/          # Python venv (ignored)
├── financial-service-chatbot-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx      # Header (auto theme application)
│   │   │   └── Footer.jsx      # Themed footer with socials
│   │   ├── pages/
│   │   │   ├── HomePage.jsx    # Landing
│   │   │   └── ChatPage.jsx    # Chat UI with Clear/Home buttons
│   │   ├── App.jsx, main.jsx, index.css
│   ├── tailwind.config.js      # darkMode: 'class'
│   └── package.json
├── Readme.md                   # This file
└── .gitignore                  # Includes config/.env, __pycache__/, etc.
```

## 🚀 Quick Start (Local)

### Prerequisites
- Node.js (LTS) and npm
- Python 3.11+ (venv recommended)

### 1) Backend (Flask)

From: `financial-service-chatbot-backend/`

- Create and activate venv (Windows PowerShell):
```powershell
python -m venv MyEnvironment
./MyEnvironment/Scripts/Activate.ps1
```

- Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

- Configure environment: Create `config/.env` with:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

- Run Flask:
```powershell
$Env:FLASK_APP = "app.py"
$Env:FLASK_ENV = "development"
flask run --host 127.0.0.1 --port 5000
```

Backend runs at: http://127.0.0.1:5000

### 2) Frontend (Vite + React)

From: `financial-service-chatbot-frontend/`

- Install:
```bash
npm install
```

- Run dev:
```bash
npm run dev
```

Frontend runs at: http://localhost:5173

Open the app, go to “Chat” and ask:
- What is a credit default swap?
- What is a bank?
You should get 3–6 bullet points and a “Source:” URL.

## 🔧 Technologies & Key Dependencies

- React 18, Vite 5
- Tailwind CSS 3
- Axios, React Router, React Icons
- Python Flask 3, Flask-CORS
- OpenAI Python SDK

Backend `requirements.txt` (core):
- Flask, flask-cors
- openai
- python-dotenv
- requests
- (Optional legacy: transformers, torch; can be removed if not using local HF models)

## 🔐 Environment Variables

Backend: `financial-service-chatbot-backend/config/.env`
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```
Do not commit `.env`. It is already gitignored.

## 🔗 API Contract

Endpoint:
- POST `/chat`
- Request JSON:
```json
{ "message": "What is a credit default swap?" }
```
- Response JSON:
```json
{ "response": "- • Short, simple bullet points...\n- ...\nSource: https://..." }
```
CORS is configured to allow `http://localhost:5173` in development.

## 📦 Deployment

### Backend (Render / Railway)

- Push repo to GitHub.
- Create a new Web Service.
- Environment variables:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL` (optional; default `gpt-4o-mini`)
- Start command:
```bash
gunicorn app:app
```
- After deploy, note your backend URL (e.g., `https://your-backend.onrender.com`).

### Frontend (Vercel / Netlify)

- Build command:
```bash
npm run build
```
- Publish directory:
```bash
dist
```
- Ensure your frontend Axios points to your backend URL for production (if needed, add an env or simple conditional).

### Update Links

- Replace Live links at the top of this README.

## 🧪 Testing Scenarios

- “What is a credit default swap?” → curated bullets + Investopedia link.
- “What is a phishing scam?” → curated bullets + Investopedia link.
- “How can I secure my online banking?” → OpenAI fallback bullets + Source line.
- “What is a bank?” → curated bullets + Investopedia link.
- Network/Key errors → graceful frontend message.

## 🛣️ Roadmap

- Add more curated topics:
  - APR vs APY, Debit vs Credit Card, Mutual Funds vs ETFs, KYC/AML.
- Optional: rate limiting and logging middleware on backend.
- Optional: message persistence (localStorage or server).

## 📚 Learnings

- Curated-first approach ensures consistent, high-quality, cited answers for expected queries.
- OpenAI fallback broadens coverage while enforcing a “Source:” line via prompt and backend guard.
- Frontend keeps messages readable with `whitespace-pre-line` and a clean, responsive UI.

## 🤝 Contributing

PRs and suggestions welcome. Open an issue for bugs or improvements.

## 🪪 License

MIT License. See LICENSE if included.

---

Built with 💙 by [Madhav P](https://www.linkedin.com/in/madhav-p-156b9b290/)