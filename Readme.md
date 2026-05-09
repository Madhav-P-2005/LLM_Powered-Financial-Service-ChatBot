# 💬 FinSathi AI — Financial Services Chatbot
### (React + Vite + Tailwind + Flask + HuggingFace)

![FinSathi AI Banner](https://img.shields.io/badge/FinSathi_AI-Premium_Financial_Assistant-blue?style=for-the-badge&logo=ai)

An intelligent, responsive financial services chatbot that provides accurate answers with reliable source citations. Features a **dual-provider LLM architecture** (HuggingFace primary + OpenAI fallback), advanced URL generation for Investopedia resources, and a modular, professional backend.

---

## 🚀 Live Demo
- **Frontend (Vercel):** [finsathi-chatbot-madhavp.vercel.app](https://finsathi-chatbot-madhavp.vercel.app)
- **Backend (Render):** [madhavp-financial-service-backend.onrender.com](https://madhavp-financial-service-backend.onrender.com)

---

## ✨ Features
- 🗨️ **Conversational UI**: Real-time chat with message history and auto-scroll.
- 📚 **Curated Knowledge**: Instant, hand-written answers for high-traffic financial topics.
- 🤖 **Mistral-7B LLM**: Powered by HuggingFace's free inference API (Primary) with OpenAI (Fallback).
- 🔗 **Smart Citations**: Always provides verified Investopedia source links.
- 🔄 **Retry Logic**: Built-in "Retry" button for failed messages and exponential backoff for API rate limits.
- 🌓 **Dynamic Themes**: Fully responsive design with automatic Dark/Light mode support.

---

## 🛠️ Local Development Setup

### 1. Backend (Python + Flask)
Navigate to the `financial-service-chatbot-backend/` directory.

#### A. Setup Virtual Environment
**Windows:**
```powershell
python -m venv MyEnvironment
.\MyEnvironment\Scripts\Activate.ps1
```
**Mac/Linux:**
```bash
python3 -m venv MyEnvironment
source MyEnvironment/bin/activate
```

#### B. Install Dependencies
```bash
pip install -r requirements.txt
```

#### C. Configure Environment
Create a file at `config/.env` and add your keys:
```env
# PRIMARY — HuggingFace (FREE)
# Get token at: https://huggingface.co/settings/tokens (Select 'Read')
HF_API_TOKEN=hf_your_actual_token_here

# FALLBACK — OpenAI (PAID, optional)
# OPENAI_API_KEY=sk-your-key-here
```

#### D. Run the Server
```powershell
$env:FLASK_APP="app.py"
python app.py
```
*Backend runs at: http://127.0.0.1:5000*

---

### 2. Frontend (React + Vite)
Navigate to the `financial-service-chatbot-frontend/` directory.

#### A. Install Packages
```bash
npm install
```

#### B. Run Development Server
```bash
npm run dev
```
*Frontend runs at: http://localhost:5173*

---

## 📦 Deployment Sync (Updating your live App)

Since you updated the code and switched to HuggingFace, follow these steps to update your live deployment:

### 1. Push to GitHub
```bash
git add .
git commit -m "Migrated to HuggingFace dual-provider and modular architecture"
git push origin Project-3
```

### 2. Update Render (Backend)
- Go to your **Render Dashboard**.
- Select your Web Service.
- Go to **Environment**.
- **ADD** a new variable: `HF_API_TOKEN` = `your_hf_token_here`.
- Ensure `PORT` is set to `5000` (optional, as Render detects this).
- Click **Save Changes**. Render will auto-redeploy with the new code and token.

### 3. Update Vercel (Frontend)
- Vercel will automatically detect your push and redeploy the frontend.
- If you have a custom backend URL, ensure `VITE_API_BASE` is set in Vercel's Environment Variables.

---

## 🗂️ Project Structure
- `/knowledge`: Curated answers and 200+ canonical URL mappings.
- `/services`: Core logic for LLM providers (HF/OpenAI) and URL generation.
- `/routes`: API endpoints and health checks.
- `/src/pages`: React components for Home and Chat interfaces.

---

## 🤝 Contact
**Madhav P**  
[LinkedIn Profile](https://www.linkedin.com/in/madhav-p-156b9b290/)  
[GitHub Repository](https://github.com/Madhav-P-2005/LLM_Powered-Financial-Service-ChatBot)
