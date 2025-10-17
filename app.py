# 🌐 OmniWave — Intelligent Email Marketing Bot
# Author: You 🚀
# Runs perfectly on Render, Colab, or Hugging Face
# Powered by Gemini + Brevo (free-tier friendly)

import os
import gradio as gr
import google.generativeai as genai
import requests
from datetime import datetime

# ---- CONFIGURATION ----
# 🧩 Add your API keys here or as environment variables on Render
GEMINI_API_KEY = os.getenv("AIzaSyB3tx9wPJ8jiWUJek9zJd-JzrHkKr-9s48", "")
BREVO_API_KEY = os.getenv("xsmtpsib-f260a892429bc23902c6795b41e70942bcc344cebc71b6f5f667b858c57336c5-il7b6OWJhj6gOhbN", "")

# ---- Initialize Gemini ----
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---- SYSTEM PROMPT ----
SYSTEM_PROMPT = """
You are OmniWave — a futuristic email marketing AI.
You specialize in writing, analyzing, and improving email campaigns.
Your style: persuasive, professional, and emotionally engaging.
Use structured, clear formatting with bullet points and short paragraphs.
Never mention being an AI. Focus on brand growth and conversion power.
"""


# ---- EMAIL GENERATION ----
def generate_email(subject, goal, tone, product_info):
    prompt = f"""{SYSTEM_PROMPT}

Task: Write a professional marketing email.
Subject: {subject}
Goal: {goal}
Tone: {tone}
Product or Service: {product_info}

Structure:
1. Catchy subject line
2. Engaging opening
3. Body that connects emotionally
4. Strong CTA (Call to Action)
5. Optional signature
"""

    try:
        response = model.generate_content(prompt)
        text = response.text if hasattr(response, "text") else "⚠️ No response generated."
        return text.strip()
    except Exception as e:
        return f"⚠️ Error generating email: {e}"


# ---- EMAIL SENDER (via Brevo API) ----
def send_email(recipient, subject, content):
    if not BREVO_API_KEY:
        return "⚠️ Brevo API key missing. Please add it in your environment variables."

    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"name": "OmniWave", "email": "no-reply@omniwave.ai"},
        "to": [{"email": recipient}],
        "subject": subject,
        "htmlContent": f"<html><body>{content}</body></html>",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return f"✅ Email sent successfully to {recipient} at {datetime.now().strftime('%H:%M:%S')}!"
    else:
        return f"⚠️ Failed to send email. Error: {response.text}"


# ---- GRADIO INTERFACE ----
with gr.Blocks(title="OmniWave AI") as demo:
    gr.Markdown(
        """
        # 🌊 **OmniWave AI**
        ### Smart Email Marketing Assistant — Generate & Send Campaigns Instantly  
        Powered by Gemini ✨ + Brevo 💌
        """
    )

    with gr.Tab("✉️ Generate Email"):
        subject = gr.Textbox(label="Email Subject")
        goal = gr.Textbox(label="Marketing Goal (e.g. Increase signups, announce sale, etc.)")
        tone = gr.Dropdown(["Friendly", "Professional", "Exciting", "Urgent"], label="Tone", value="Professional")
        product = gr.Textbox(label="Product or Service Info")
        output = gr.Textbox(label="Generated Email", lines=12)

        generate_btn = gr.Button("⚡ Generate Email")
        generate_btn.click(generate_email, inputs=[subject, goal, tone, product], outputs=output)

    with gr.Tab("🚀 Send Email"):
        recipient = gr.Textbox(label="Recipient Email")
        subject2 = gr.Textbox(label="Email Subject")
        content2 = gr.Textbox(label="Email Content", lines=10)
        send_btn = gr.Button("📤 Send Now")
        status = gr.Textbox(label="Status")

        send_btn.click(send_email, inputs=[recipient, subject2, content2], outputs=status)

    gr.Markdown("© 2025 OmniWave AI — Built for effortless marketing ⚡")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
