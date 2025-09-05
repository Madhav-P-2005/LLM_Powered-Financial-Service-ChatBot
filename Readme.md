# Financial Services Chatbot - Internship Assignment 2

## Project Overview
Build a simple LLM-powered chatbot for financial services queries using React.js + Vite + Tailwind CSS for frontend and Python Flask for backend. The chatbot answers questions like "What is a phishing scam?" or "Explain credit default swap" in simple terms. Includes conversation history, loading animations, and source citations for bonuses.

**Submission Deadline**: September 6th, 12 PM.  
**Timeline**: 1-2 days (start backend first as per plan).

## Tech Stack
- **Frontend**: React.js + Vite + Tailwind CSS
- **Backend**: Python Flask (for API proxying to OpenAI)
- **LLM**: OpenAI GPT-3.5/4 API
- **Hosting**: Frontend on Vercel/Netlify, Backend on Railway
- **Tools**: GitHub for repo, Node.js for frontend, Python for backend

## Project Structure
```
chatbot-assignment/
├── backend/
│   ├── app.py (Flask server)
│   ├── requirements.txt
│   └── .env (API keys)
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env
├── README.md (this file)
└── .gitignore
```

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



