import os
import gradio as gr
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDrx7j5XPIztMz274t-ItjxSE55sr6Q39g")
model = genai.GenerativeModel('gemini-2.5-flash')

# Chat logic using OpenAI-style messages
def chat_with_astrologer(messages, message):
    try:
        full_prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                full_prompt += f"User: {content}\n"
            elif role == "assistant":
                full_prompt += f"Astrologer: {content}\n"

        full_prompt += f"User: {message}\nAstrologer:"

        response = model.generate_content(full_prompt)
        return messages + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response.text}
        ]
    except Exception as e:
        return messages + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": f"Error: {str(e)}"}
        ]

# Gradio UI
with gr.Blocks(css="""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

body {
    background: #1e1e2f;
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
}

.gradio-container {
    max-width: 750px;
    margin: auto;
    padding: 20px;
    background: #2e2e3e;
    border-radius: 20px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

h1 {
    color: #ffcc70 !important;
    font-weight: 600;
    text-align: center;
}

.gr-chatbot {
    background-color: #1e1e2f !important;
    color: #ffffff !important;
    border-radius: 12px;
}

textarea, input {
    background-color: #1e1e2f !important;
    color: #ffffff !important;
    border: 1px solid #555 !important;
    border-radius: 12px !important;
    padding: 10px !important;
    font-size: 15px !important;
}

button {
    background-color: #6e40c9;
    color: white;
    border: none;
    font-size: 16px;
    font-weight: 600;
    padding: 12px 20px;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.3s ease;
}

button:hover {
    background-color: #8e5ee0;
    transform: scale(1.03);
}
""") as demo:

    gr.Markdown("<h1>🔮 Gemini Astrology Chat</h1>")
    gr.Markdown("Chat with your personal AI astrologer. Ask anything about your future, zodiac, or horoscope.")

    chatbot = gr.Chatbot(label="🌠 Astrology Chat", type='messages')
    msg = gr.Textbox(placeholder="Ask your astrologer anything...", label="Your Message", show_label=False)
    send_btn = gr.Button("Send")

    send_btn.click(chat_with_astrologer, [chatbot, msg], chatbot)
    msg.submit(chat_with_astrologer, [chatbot, msg], chatbot)

demo.launch()
