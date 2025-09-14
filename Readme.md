# 💬 LLM‑Powered Financial Services Chatbot (React + Vite + Tailwind + Flask)

![React 18.x](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=white&style=for-the-badge)
![Vite 5.x](https://img.shields.io/badge/Vite-5.x-646CFF?logo=vite&logoColor=white&style=for-the-badge)
![Tailwind CSS 3.x](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge)
![Flask 3.x](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white&style=for-the-badge)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white&style=for-the-badge)

An intelligent, responsive financial services chatbot that provides accurate answers with reliable source citations. Features advanced URL generation for Investopedia resources and comprehensive financial knowledge coverage.

**Example queries:**

- "What is cryptocurrency?"
- "Explain credit default swap in simple terms"
- "How does compound interest work?"
- "What are the risks of trading stocks?"

The bot provides clear, concise explanations and **always includes valid Investopedia source links** for further reading.

## 🚀 Live App

- Frontend (Vercel): [finsathi-chatbot-madhavp.vercel.app](https://finsathi-chatbot-madhavp.vercel.app)
- Backend (Render): [madhavp-financial-service-backend.onrender.com](https://madhavp-financial-service-backend.onrender.com)
- GitHub Repo: [Madhav-P-2005/LLM_Powered-Financial-Service-ChatBot](https://github.com/Madhav-P-2005/LLM_Powered-Financial-Service-ChatBot)

## ✨ Features

- 🗨️ Conversational chat UI with history
- ⏳ Loading indicator while the model generates
- 📚 Answers in simple financial language
- 🔗 **Smart URL Generation**: Always provides valid Investopedia links using:
  - Canonical URL mappings for 200+ financial terms
  - Heuristic URL generation with validation
  - Alphabetical directory fallback system
- 🌓 Dark/Light theme (auto-applies based on saved or system preference)
- 🧹 "Clear chat" and "Home" buttons on chat page
- 📱 Fully responsive UI (mobile-first)
- 🔒 OpenAI key loaded securely from backend `.env` (never exposed to browser)
- 🧩 Custom favicon and branding (`public/finsathi.svg`) replacing default Vite icon

## 🧠 How It Works

- **Curated Knowledge First**: Common topics like "cryptocurrency", "credit default swap", "bank", "phishing" return high-quality answers with verified Investopedia citations from a curated knowledge base.
- **OpenAI Fallback**: For other queries, the backend calls OpenAI with optimized prompts for concise, educational responses.
- **Advanced URL Resolution**: Multi-tier system ensures valid Investopedia links:
  1. Exact canonical mapping lookup
  2. Partial matching with priority scoring
  3. Heuristic URL generation with validation
  4. Alphabetical directory fallback
- **No Broken Links**: System validates URLs before returning them to users.

## 🗂️ Project Structure

```text
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

Backend runs at: <http://127.0.0.1:5000>

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

Frontend runs at: <http://localhost:5173>

Open the app, go to "Chat" and ask:

- What is a credit default swap?
- What is cryptocurrency?
- What is a bank?

You should get clear explanations with valid Investopedia source URLs.

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

CORS is configured for local development and production deployment.

## 📦 Deployment

### Backend (Render)

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

## 🤝 Contributing

PRs and suggestions welcome. Open an issue for bugs or improvements.

## 🪪 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Built with 💙 by [Madhav P](https://www.linkedin.com/in/madhav-p-156b9b290/)
