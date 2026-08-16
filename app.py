import os
from flask import Flask, request
from openai import OpenAI
import requests

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
           input=f"""
Eres el asistente de ventas de Tu Porción, un restaurante en Hermosillo.

Responde siempre en español.
Habla como una persona atendiendo WhatsApp.
Sé breve, natural y directo.
No expliques tu razonamiento.
No digas que eres una inteligencia artificial.
No inventes precios, ingredientes ni información que no conozcas.
Tu objetivo es ayudar a tomar el pedido del cliente.

Mensaje del cliente:
{texto}

Responde únicamente con el mensaje que se le enviaría al cliente.
"""
        )

        print("Respuesta IA:", response.output_text)
telefono_cliente = message["from"]

phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"

headers = {
    "Authorization": f"Bearer {whatsapp_token}",
    "Content-Type": "application/json"
}

payload = {
    "messaging_product": "whatsapp",
    "to": telefono_cliente,
    "type": "text",
    "text": {
        "body": response.output_text
    }
}

resultado = requests.post(url, headers=headers, json=payload)

print("Respuesta WhatsApp:", resultado.status_code, resultado.text)
    
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
