#!/usr/bin/env python3
"""
A minimal, extensible ChatGPT-like chatbot web app in a single file.

Features:
  1. ChatGPT-like conversational UI.
  2. Model selection (e.g. online OpenAI GPT‑3.5‑turbo, local DialoGPT, dummy fallback).

Dependencies:
  - flask
  - openai
  - transformers, torch  (for local model)
  
Set your OpenAI API key in the environment variable OPENAI_API_KEY if using GPT‑3.5‑turbo.
"""

import os
from flask import Flask, render_template_string, request, jsonify
import openai

# Try importing transformers. If not installed, mark local model as unavailable.
try:
    from transformers import pipeline, Conversation
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

app = Flask(__name__)

# --- Initialize local model pipelines ---
if TRANSFORMERS_AVAILABLE:
    # Using a conversational pipeline with DialoGPT (local model).
    dialoGPT_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")
else:
    dialoGPT_pipeline = None

# --- Define model interface functions ---
def chat_with_openai(conversation, prompt):
    """
    Call the OpenAI ChatCompletion API with the conversation history.
    Expects conversation as a list of dicts like {"role": "user"/"assistant", "content": "..."}.
    """
    messages = conversation + [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Error calling OpenAI API: {e}"
    return reply

def chat_with_dialoGPT(conversation, prompt):
    """
    Call the local DialoGPT model via transformers.
    For simplicity we concatenate the conversation history.
    """
    if not dialoGPT_pipeline:
        return "DialoGPT model not available. Please install transformers."
    # Combine conversation history into one prompt.
    combined_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
    combined_input = (combined_history + "\nuser: " + prompt) if combined_history else prompt
    conv = Conversation(combined_input)
    result = dialoGPT_pipeline(conv)
    reply = result.generated_responses[-1] if result.generated_responses else "No response."
    return reply

def chat_with_dummy(conversation, prompt):
    """A dummy echo model."""
    return f"Dummy response to: {prompt}"

# Mapping model names to handler functions.
MODEL_FUNCTIONS = {
    "OpenAI GPT-3.5-turbo": chat_with_openai,
    "DialoGPT": chat_with_dialoGPT,
    "Dummy": chat_with_dummy
}

AVAILABLE_MODELS = list(MODEL_FUNCTIONS.keys())

# --- HTML + JavaScript for the Chat UI ---
INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ChatGPT Replica</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
        .chat-container { max-width: 800px; margin: 20px auto; padding: 20px; }
        .chat-log { border: 1px solid #ddd; padding: 10px; background: #fff; height: 500px; overflow-y: scroll; }
        .message { margin: 10px 0; }
        .user { text-align: right; }
        .assistant { text-align: left; }
        .message p { display: inline-block; padding: 10px; border-radius: 5px; max-width: 70%; }
        .user p { background-color: #0084ff; color: #fff; }
        .assistant p { background-color: #e5e5ea; color: #000; }
        .input-area { margin-top: 10px; display: flex; }
        .input-area select, .input-area input { padding: 10px; font-size: 16px; }
        .input-area select { margin-right: 10px; }
        .input-area input { flex: 1; }
        .input-area button { padding: 10px 20px; font-size: 16px; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>ChatGPT Replica</h2>
        <div class="chat-log" id="chat-log"></div>
        <div class="input-area">
            <select id="model-select">
                {% for model in models %}
                <option value="{{model}}">{{model}}</option>
                {% endfor %}
            </select>
            <input type="text" id="user-input" placeholder="Type your message here..." autocomplete="off" />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
<script>
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const modelSelect = document.getElementById('model-select');
    let conversation = [];  // Holds the conversation as an array of {role, content}

    function appendMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ' + role;
        const p = document.createElement('p');
        p.innerText = text;
        msgDiv.appendChild(p);
        chatLog.appendChild(msgDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        appendMessage('user', text);
        conversation.push({role: 'user', content: text});
        userInput.value = '';
        // Add a temporary typing indicator.
        appendMessage('assistant', '...');
        const model = modelSelect.value;
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({conversation: conversation, prompt: text, model: model})
            });
            const data = await response.json();
            // Remove the temporary message.
            chatLog.removeChild(chatLog.lastChild);
            appendMessage('assistant', data.reply);
            conversation.push({role: 'assistant', content: data.reply});
        } catch (err) {
            console.error(err);
            chatLog.removeChild(chatLog.lastChild);
            appendMessage('assistant', 'Error: ' + err);
        }
    }

    // Allow Enter key to send message.
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
</script>
</body>
</html>
'''

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template_string(INDEX_HTML, models=AVAILABLE_MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    conversation_history = data.get('conversation', [])
    prompt = data.get('prompt', '')
    model_name = data.get('model', 'Dummy')
    # Select the handler; default to dummy if not found.
    model_func = MODEL_FUNCTIONS.get(model_name, chat_with_dummy)
    reply = model_func(conversation_history, prompt)
    return jsonify({'reply': reply})

# --- Main entry point ---
if __name__ == '__main__':
    # Set OpenAI API key from environment variable if available.
    openai.api_key = os.getenv("OPENAI_API_KEY")
    app.run(host="0.0.0.0", port=5000, debug=True)