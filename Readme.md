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

## Step-by-Step Plan
Follow this order to avoid confusion. Work on one step at a time. If stuck, ask for help.

### Phase 1: Backend Setup (Start Here)
1. **Create Backend Directory**: In your project folder, run `mkdir backend && cd backend`.
2. **Set Up Python Environment**: Run `python -m venv venv` and `venv\Scripts\activate` (Windows).
3. **Install Flask**: `pip install flask python-dotenv openai`.
4. **Create app.py**: Build a simple Flask app to proxy OpenAI API calls.
   - Handle POST requests for chat queries.
   - Use few-shot prompts for financial context.
   - Return responses with sources if possible.
5. **Add Environment Variables**: Create `.env` for OpenAI API key.
6. **Test Locally**: Run `flask run` and test with Postman or curl.
7. **Deploy Backend**: Push to GitHub, deploy on Railway.

### Phase 2: LLM Integration
1. **Integrate OpenAI**: In app.py, use OpenAI client to generate responses.
2. **Prompt Engineering**: Craft prompts like "Answer as a financial advisor in simple terms. Cite sources."
3. **Error Handling**: Add try-except for API failures.
4. **Test Queries**: Ensure responses are accurate and cited.

### Phase 3: Frontend Setup
1. **Create Frontend Directory**: In project root, `mkdir frontend && cd frontend`.
2. **Init React + Vite**: `npm create vite@latest . -- --template react`.
3. **Install Tailwind**: `npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p`.
4. **Configure Tailwind**: Update tailwind.config.js and src/index.css.
5. **Run Dev Server**: `npm run dev`.

### Phase 4: Build Chat UI
1. **Create Components**: Build ChatWindow, Message, Input components.
2. **Add State Management**: Use useState for messages, loading.
3. **Styling**: Use Tailwind for responsive design.
4. **Features**: Input field, send button, message history, loading spinner.

### Phase 5: Integration
1. **Connect Frontend to Backend**: Use fetch/axios to call Flask API.
2. **Handle Responses**: Display bot replies with history.
3. **Security**: Ensure API keys are not exposed.

### Phase 6: Bonuses
1. **Source Citations**: Modify backend to include links (e.g., Investopedia).
2. **Conversation History**: Persist messages (localStorage or backend).

### Phase 7: Testing
1. **Unit Tests**: Test components and API calls.
2. **E2E Tests**: Simulate user interactions.
3. **Edge Cases**: Handle empty inputs, API errors.

### Phase 8: Deployment and Submission
1. **Deploy Frontend**: Push to GitHub, deploy on Vercel.
2. **Deploy Backend**: Use Railway for Flask.
3. **Prepare Deliverables**: Live link, GitHub repo with README (include this plan).
4. **Submit**: Ensure all works before 12 PM on 6th.

## Timeline Breakdown (Real-Time)
- **Day 1 (Today)**: Backend setup and LLM integration (4-6 hours).
- **Day 1 Evening**: Frontend setup and basic UI (4-6 hours).
- **Day 2 Morning**: Integration and bonuses (4-6 hours).
- **Day 2 Afternoon**: Testing, deployment, polish (4-6 hours).

## Tips
- Commit to GitHub after each phase.
- Use console.log for debugging.
- If stuck, check Flask/React docs or ask here.
- Focus on learning: Understand why each part works.

Let's start with Phase 1: Backend Setup!




Setup :- 

PS E:\LLM-Powered Financial Services Chatbot\financial-service-chatbot-backend> python -m venv MyEnvironment
PS E:\LLM-Powered Financial Services Chatbot\financial-service-chatbot-backend> .\MyEnvironment\Scripts\Activate.ps1


pip install flask dotenv openai

pip freeze > requirements.txt



not open ai use FinancialBERT :- 

pip install transformers torch -> done 



npm create vite@latest . -- --template react

npm install 

npm run dev

npm i -D tailwindcss @tailwindcss/vite


npm i react-router-dom  axios  react-icons 


python -m pip install flask-cors==4.0.0


npm i axios

