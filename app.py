import os
from flask import Flask, request
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = Flask(__name__)

@app.route("/")
def home():
    return "Tu Porcion backend funcionando"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    verify_token = os.environ.get("VERIFY_TOKEN")

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return challenge, 200

    return "Forbidden", 403
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json()
    print("Webhook recibido:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        texto = message["text"]["body"]

        response = client.responses.create(
            model="gpt-5.4-mini",
            input=f"El cliente escribió por WhatsApp: {texto}"
        )

        print("Respuesta IA:", response.output_text)

    except Exception as e:
        print("No se pudo procesar como mensaje de texto:", e)

    return "EVENT_RECEIVED", 200
@app.route("/ai-test")
def ai_test():
    response = client.responses.create(
        model="gpt-5.4-mini",
        input="Responde únicamente: OpenAI conectado correctamente"
    )
    return response.output_text
