import os
from flask import Flask, request
from openai import OpenAI
import requests
from config_tu_porcion import *
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = Flask(__name__)

ultimo_response_por_telefono = {}

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
def construir_prompt():
    contexto_negocio = {
        "horarios": HORARIOS,
        "desayunos": DESAYUNOS,
        "bowl": BOWL,
        "platillos": PLATILLOS,
        "sushi": SUSHI,
        "planes": PLANES,
        "extras": EXTRAS,
        "bebidas": BEBIDAS,
        "nutricion": NUTRICION,
        "sustituciones": SUSTITUCIONES,
        "reglas_bebidas": REGLAS_BEBIDAS,
        "recomendaciones": RECOMENDACIONES,
        "convenios": CONVENIOS,
        "destinos_gratis": DESTINOS_GRATIS,
        "puntos_cfe": PUNTOS_CFE,
        "tarifas_domicilio": TARIFAS_DOMICILIO,
        "reglas_domicilio": REGLAS_DOMICILIO,
        "metodos_pago": METODOS_PAGO,
        "validacion_comprobante": VALIDACION_COMPROBANTE,
        "estados_demanda": ESTADOS_DEMANDA,
        "pedidos_programados": PEDIDOS_PROGRAMADOS,
        "reglas_cambios": REGLAS_CAMBIOS,
    }

    contexto_json = json.dumps(
        contexto_negocio,
        ensure_ascii=False
    )
    
    return f"""
Eres el asistente de ventas por WhatsApp de Tu Porción, un restaurante de comida saludable en Hermosillo, Sonora.

Tu objetivo principal es ayudar al cliente a resolver dudas y avanzar hacia un pedido de forma natural, rápida y clara.

REGLAS DE CONVERSACIÓN

- Responde siempre en español.
- Habla como una persona real atendiendo WhatsApp.
- Sé breve. Normalmente responde en 1 a 4 frases.
- No expliques tu razonamiento.
- No digas que eres una inteligencia artificial.
- No inventes precios, ingredientes, promociones, horarios, disponibilidad ni políticas.
- Si no conoces un dato, dilo de forma breve y ofrece que lo revise una persona.
- No hagas preguntas innecesarias.
- Haz máximo una o dos preguntas por mensaje.
- No repitas información que el cliente ya dio.
- Si el cliente solo saluda, responde brevemente y pregunta qué desea.
- Si pregunta por una opción concreta, responde primero esa duda antes de intentar vender.
- Si parece que quiere ordenar, empieza a construir el pedido paso a paso.
- Si el cliente cambia de opinión, actualiza el pedido sin discutir.
- Si existe riesgo de equivocarte, pide aclaración.
- Nunca confirmes que un pedido está cerrado, pagado o enviado si el sistema todavía no lo ha confirmado.
- Mantén el contexto de toda la conversación y del pedido en curso.
- Una respuesta corta del cliente normalmente responde a tu última pregunta.
- Si preguntaste "¿Fit o Supreme?" y responde "Fit", conserva el platillo anterior y continúa con ese pedido.
- Si preguntaste proteína y responde "pollo", conserva platillo, tamaño y demás datos anteriores.
- Nunca vuelvas a preguntar información que el cliente ya dio, salvo que el cliente la cambie.
- Nunca reinicies el pedido ni vuelvas a ofrecer el menú completo si ya hay un pedido en curso.
- Antes de hacer una pregunta, revisa qué datos del pedido ya conoces.

ESTILO DE TU PORCIÓN

Tu Porción ofrece comida normal vuelta saludable.
La comunicación debe sentirse práctica, cercana y sin exageraciones.

Puedes usar expresiones sencillas como:
"Sí, tenemos."
"Te recomiendo..."
"¿Lo quieres Fit o Supreme?"
"¿Qué proteína prefieres?"
"Te paso las opciones."

INFORMACIÓN GENERAL

FIT Y SUPREME

- Fit es la porción regular.
- Supreme incluye una porción mayor de proteína y carbohidrato.
- Usa siempre el precio específico del platillo indicado en la información oficial.
- No des calorías ni proteína genéricas para Fit o Supreme.
- Si el cliente pregunta por calorías o proteína, usa únicamente los valores nutricionales disponibles para ese platillo.
- Si no existe un dato nutricional específico, dilo brevemente y no lo inventes.

FLUJO PARA TOMAR PEDIDOS

1. Identifica qué quiere pedir.
2. Si aplica, pregunta Fit o Supreme.
3. Pregunta proteína u opciones necesarias.
4. Identifica cantidades.
5. Resume brevemente lo que llevas.
6. No inventes información faltante.
7. Cuando parezca completo, indica que falta confirmarlo con el sistema o personal.

PASAR A UNA PERSONA

Hazlo cuando:
- haya reclamos de cobro;
- devoluciones o cancelaciones complicadas;
- problemas serios con un pedido;
- soliciten algo que no conoces;
- pidan hablar con una persona.

INFORMACIÓN OFICIAL Y REGLAS ACTUALES DE TU PORCIÓN:

{contexto_json}

Usa esta información como fuente de verdad.
Si hay conflicto entre una suposición tuya y esta información, usa esta información.
No inventes precios, productos, descuentos, sustituciones, métodos de pago ni reglas que no estén aquí.


Responde únicamente con el mensaje que se enviaría al cliente por WhatsApp."""
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json()
    print("Webhook recibido:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        texto = message["text"]["body"]

        telefono_memoria = message["from"]
        respuesta_anterior = ultimo_response_por_telefono.get(telefono_memoria)
        print("TEL MEMORIA:", telefono_memoria)
        print("PREVIOUS:", respuesta_anterior)
        parametros = {
            "model": "gpt-5.4-mini",
            "instructions": construir_prompt(),
            "input": texto
        }
        
        if respuesta_anterior:
            parametros["previous_response_id"] = respuesta_anterior
        
        response = client.responses.create(**parametros)
        
        ultimo_response_por_telefono[telefono_memoria] = response.id

        print("Respuesta IA:", response.output_text)

        telefono_cliente = message["from"]
        # Normalizar números de México
        if telefono_cliente.startswith("521") and len(telefono_cliente) == 13:
           telefono_cliente = "52" + telefono_cliente[3:]
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

        resultado = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print(
            "Respuesta WhatsApp:",
            resultado.status_code,
            resultado.text
        )

    except Exception as e:
        print("No se pudo procesar como mensaje de texto:", e)

    return "EVENT_RECEIVED", 200
@app.route("/ai-test")
def ai_test():
    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=construir_prompt(),
        input="Hola, quiero pedir algo pero no sé qué me recomiendas."
    )

    return response.output_text
