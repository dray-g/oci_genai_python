from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI(title="Gemini Chatbot")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    response = model.generate_content(req.message)
    return ChatResponse(reply=response.text)


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .chat-container { width: 100%; max-width: 700px; background: #16213e; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); overflow: hidden; display: flex; flex-direction: column; height: 90vh; }
        .header { padding: 20px; background: linear-gradient(135deg, #0f3460, #533483); text-align: center; font-size: 1.4rem; font-weight: 600; }
        .messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .msg { max-width: 80%; padding: 12px 16px; border-radius: 12px; line-height: 1.5; white-space: pre-wrap; }
        .msg.user { align-self: flex-end; background: #533483; }
        .msg.bot { align-self: flex-start; background: #0f3460; }
        .input-area { display: flex; padding: 16px; gap: 10px; background: #0f3460; }
        .input-area input { flex: 1; padding: 12px 16px; border: none; border-radius: 8px; font-size: 1rem; background: #1a1a2e; color: #eee; outline: none; }
        .input-area button { padding: 12px 24px; border: none; border-radius: 8px; background: #533483; color: #fff; font-size: 1rem; cursor: pointer; }
        .input-area button:hover { background: #6a42a0; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">💬 Gemini Chatbot</div>
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Type your message..." autocomplete="off" />
            <button onclick="send()">Send</button>
        </div>
    </div>
    <script>
        const input = document.getElementById('input');
        const messages = document.getElementById('messages');
        input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
        async function send() {
            const text = input.value.trim();
            if (!text) return;
            addMsg(text, 'user');
            input.value = '';
            try {
                const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({message: text}) });
                const data = await res.json();
                addMsg(data.reply, 'bot');
            } catch(e) { addMsg('Error: ' + e.message, 'bot'); }
        }
        function addMsg(text, type) {
            const div = document.createElement('div');
            div.className = 'msg ' + type;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""
