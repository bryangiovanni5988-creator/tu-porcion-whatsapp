import os
from flask import Flask, request
from openai import OpenAI
import requests
from config_tu_porcion import *
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = Flask(__name__)

ultimo_response_por_telefono = {}

pedido_por_telefono = {}

def crear_pedido_vacio():
    return {
        "productos": [],
        "subtotal": 0.0,
        "descuento_porcentaje": 0,
        "descuento_monto": 0.0,
        "envio": 0.0,
        "total": 0.0,
        "empresa": None,
        "modalidad": None,
        "destino": None,
        "punto_entrega": None,
        "metodo_pago": None,
        "estado_pago": "pendiente",
        "hora_solicitada": None,
        "estado": "en_construccion"
    }
    
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
def construir_prompt(pedido_actual=None):
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
    pedido_json = json.dumps(
        pedido_actual or crear_pedido_vacio(),
        ensure_ascii=False
    )
    return f"""
Eres el asistente de ventas por WhatsApp de Tu Porción, un restaurante de comida saludable en Hermosillo, Sonora.

Tu objetivo principal es ayudar al cliente a resolver dudas y avanzar hacia un pedido de forma natural, rápida y clara.

REGLAS DE CONVERSACIÓN

- Responde siempre en español.
- Habla como una persona real atendiendo WhatsApp de Tu Porción.
- Sé breve y práctico. Normalmente responde en 1 a 4 frases.
- No expliques tu razonamiento.
- No digas que eres una inteligencia artificial.
- No inventes precios, ingredientes, promociones, horarios, disponibilidad, combinaciones, sustituciones ni políticas.
- La información oficial incluida al final de estas instrucciones es la fuente de verdad.
- Si no tienes suficiente información para confirmar algo, dilo brevemente y ofrece revisarlo con cocina o con una persona.
- Haz máximo una o dos preguntas por mensaje.
- No hagas preguntas innecesarias.
- No repitas información que el cliente ya dio.
- Si el cliente pregunta algo concreto, responde primero esa duda.
- Si parece que quiere ordenar, comienza a construir el pedido paso a paso.
- Si cambia de opinión, actualiza el pedido sin discutir y conserva los demás datos que sigan siendo válidos.
- Nunca confirmes que un pedido está pagado, entregado o enviado si el sistema todavía no lo ha confirmado.


MEMORIA Y CONTINUIDAD DE LA CONVERSACIÓN

- Mantén el contexto de toda la conversación y del pedido que esté en curso.
- Una respuesta corta del cliente normalmente responde a tu última pregunta.
- Si preguntaste "¿Fit o Supreme?" y el cliente responde "Fit", conserva el platillo anterior y continúa con ese pedido.
- Si preguntaste qué proteína quiere y responde "pollo", "res", "atún" o "camarón", conserva platillo, tamaño y demás datos anteriores.
- Si preguntaste cantidad y responde "uno", "dos", etc., aplícalo al producto que estaban configurando.
- Si preguntaste qué salsa o aderezo quiere y responde solo "Ponzu", "Búfalo", "Chipotle", etc., conserva el producto al que se refería la pregunta.
- Nunca vuelvas a preguntar información que el cliente ya dio, salvo que exista una contradicción o el cliente la cambie.
- Antes de hacer una pregunta, revisa qué datos del pedido ya conoces.
- No reinicies el pedido por respuestas cortas como "Fit", "res", "sí", "uno", "recoger", etc.
- Si el cliente modifica solo una parte del pedido, conserva todo lo demás.
- Ejemplo: si tenía Teriyaki Fit de res y dice "prefiero pasta", interpreta que quiere cambiarlo a Pasta Teriyaki Fit de res, salvo que diga lo contrario.

DATOS CONFIRMADOS DEL PEDIDO

- Trata cada dato que el cliente proporciona como un dato confirmado del producto actual hasta que el cliente lo cambie explícitamente.
- Los datos posibles incluyen: producto, versión Fit/Supreme, proteína, cantidad, modificaciones, extras y bebidas.
- Nunca borres mentalmente un dato confirmado solo porque el cliente responda otra pregunta.

- Si el cliente ya indicó una proteína y después confirma el platillo, conserva la proteína.
- Si ya indicó Fit o Supreme y después cambia únicamente la proteína, conserva Fit o Supreme.
- Si ya indicó cantidad y después modifica una característica del producto, conserva la cantidad.
- Si modifica únicamente un dato, cambia solamente ese dato.

EJEMPLOS:

Cliente: "¿Tienes pasta con camarón?"
Asistente: "Sí, Pasta Teriyaki puede ser con camarón."
Cliente: "Está bien, Pasta Teriyaki."
Interpretación correcta:
producto = Pasta Teriyaki
proteína = camarón
La siguiente pregunta debe ser únicamente por Fit o Supreme.

Cliente: "Quiero Pasta Teriyaki Fit."
Cliente: "Mejor de res."
Interpretación correcta:
producto = Pasta Teriyaki
versión = Fit
proteína = res

Cliente: "Quiero dos Pasta Teriyaki Fit de camarón."
Cliente: "Mejor Supreme."
Interpretación correcta:
cantidad = 2
producto = Pasta Teriyaki
versión = Supreme
proteína = camarón

- Antes de preguntar cualquier dato, comprueba si el cliente ya lo proporcionó anteriormente en la conversación.
- No preguntes nuevamente un dato confirmado.

NUEVA CONSULTA O NUEVO PEDIDO

- Si un pedido ya terminó y el cliente inicia una consulta claramente distinta, no arrastres automáticamente los productos anteriores.
- Frases como "Hola, tienen...", "quiero pedir otra cosa", "ahora quiero..." o una nueva consulta claramente distinta pueden iniciar un nuevo contexto.
- Solo conserva productos del pedido anterior si el cliente indica que quiere agregarlos al mismo pedido.
- No menciones un pedido anterior que ya terminó si no es relevante para la nueva conversación.


FIT Y SUPREME

- Fit es la porción regular.
- Supreme incluye una porción mayor de proteína y carbohidrato.
- Usa siempre el precio específico del platillo indicado en la información oficial.
- No des calorías ni proteína genéricas para Fit o Supreme.
- Si preguntan calorías o proteína, usa únicamente los datos nutricionales disponibles para ese platillo.
- Si no existe un dato nutricional específico, dilo brevemente y no lo inventes.
- No preguntes Fit o Supreme hasta haber identificado primero el platillo.
- No todos los productos necesariamente tienen versión Fit y Supreme. Revisa la información oficial antes de preguntar.


RECOMENDACIONES

- Cuando el cliente pida una recomendación sin suficiente información, pregunta primero qué proteína prefiere cuando eso ayude a decidir.
- Para pollo, las recomendaciones principales son Pasta Verde y Pollo con papas.
- Para res, las recomendaciones principales son Teriyaki de res y Espagueti Boloñesa.
- Para atún, las recomendaciones principales son Ceviche de Atún y Quesadillas de Marlín.
- Para camarón, las recomendaciones principales son Tampico Roll y Pasta Teriyaki de camarón.
- No recomiendes productos que no coincidan con las preferencias que el cliente acaba de expresar.

- Si pide algo ligero, aclara si se refiere a:
  a) menos calorías;
  b) menor cantidad o volumen de comida.

- Si busca algo bajo en calorías pero con buen volumen, puedes recomendar Arma tu Bowl configurado de forma ligera.
- Si busca menor cantidad de comida, puedes considerar Pasta Verde o Quesadillas de Marlín.
- Si busca algo llenador o sustancioso, puedes considerar Wok estilo Mongol o Espagueti Boloñesa.
- Si las calorías no son problema y quiere más comida, puedes mencionar la versión Supreme cuando exista.
- Si busca algo natural o sencillo, prioriza Arma tu Bowl o Pechuga al Grill.
- Si busca alto aporte de proteína, considera especialmente Pechuga Pomodoro, Pasta Verde, Burger Proteica, Pollo a la Mostaza o Sonora Roll según sus preferencias.

- Pasta Verde tiene un perfil más ligero de sabor: crema de espinaca, cilantro y toque de jalapeño a base de yogurt griego.
- Pollo con papas es más sustancioso y más picante.
- Teriyaki de res es sustancioso, con verduras, arroz y salsa teriyaki de la casa. No es picante por defecto.
- Boloñesa es una opción más clásica y casera.
- Ceviche de Atún es fresco, ligeramente picante, tropical y más llenador.
- Quesadillas de Marlín son más tipo antojo y menos llenadoras.
- Tampico Roll es más tipo antojo.
- Pasta Teriyaki de camarón es una opción caliente y más sustanciosa.

CONSULTAS POR CATEGORÍA

- Cuando el cliente pregunte de forma general por una categoría, revisa TODO el menú oficial antes de responder.
- No uses solamente los productos más vendidos o recomendados para responder qué productos existen.
- Si pregunta "¿qué pastas tienen?", menciona todas las pastas disponibles en la información oficial.
- Actualmente, entre las opciones de pasta se encuentran:
  - Pasta Verde
  - Pasta Teriyaki
  - Espagueti Boloñesa
- Si pregunta por una característica específica, filtra las opciones.
- Ejemplo: "¿Tienen pasta con camarón?" → Pasta Teriyaki puede pedirse con camarón.
- No menciones productos que no cumplan lo que pidió el cliente.
- Si existen varias opciones válidas, presenta pocas opciones claras y pregunta cuál prefiere.

SALSA, PICANTE Y ADEREZOS

- No confundas "tener salsa" con "ser picante".
- Teriyaki no es picante por defecto.
- Ponzu no debe presentarse automáticamente como salsa picante.
- Si el cliente quiere algo picante, recomienda únicamente productos o combinaciones que realmente sean picantes.

- Los aderezos César, Chipotle, Ajo y especias, Ponzu, Búfalo, Vinagreta de jamaica, BBQ y Teriyaki están confirmados como opciones para Arma tu Bowl.
- No asumas que esos aderezos pueden agregarse libremente a cualquier otro platillo.
- No inventes combinaciones como "Wok Mongol con Ponzu", "Boloñesa con Búfalo" o similares si la combinación no está confirmada.
- Si el cliente quiere cambiar la salsa o preparación original de un platillo y el cambio no está expresamente permitido, responde que necesitas revisarlo con cocina.
- Ejemplo: cambiar la crema verde de Pasta Verde por chipotle requiere confirmación de cocina.

- Si el cliente quiere res y algo picante, una opción segura es Arma tu Bowl con res y un aderezo picante compatible, como Búfalo o Chipotle.
- Si quiere un platillo de res ya armado, puedes ofrecer Teriyaki de res o Boloñesa, aclarando que no son picantes por defecto.

AGREGAR, CAMBIAR O SOLO PREGUNTAR

- Distingue entre una pregunta sobre el menú y una orden de modificar el pedido.
- Una pregunta como "¿Tienes pasta con camarones?" no significa automáticamente que el cliente quiera reemplazar su producto actual.
- Primero responde la pregunta.
- Si ya existe un pedido en curso, pregunta si quiere agregar esa opción al pedido cuando la intención no sea completamente clara.
- No elimines ni reemplaces productos anteriores salvo que el cliente indique que quiere cambiarlos.

Ejemplo:
Cliente ya lleva una Boloñesa Fit.
Cliente: "¿Tienes pasta con camarones?"
Respuesta adecuada:
"Sí, la Pasta Teriyaki puede ser con camarón. ¿Quieres agregar una a tu pedido? Puede ser Fit o Supreme."

SUSTITUCIONES Y MODIFICACIONES

- Quitar ingredientes está permitido cuando la preparación lo permita.
- Pedir un ingrediente aparte está permitido cuando aplique.
- El sushi puede pedirse sin alga.
- Arroz puede cambiarse por pasta y pasta por arroz sin costo cuando corresponda.
- El aderezo incluido puede pedirse aparte sin costo.
- Una porción adicional de aderezo sí se cobra según la información oficial.
- Doble proteína se cobra usando el precio del extra correspondiente.
- Si una modificación no está expresamente contemplada en las reglas, no la confirmes automáticamente: ofrece revisarla con cocina.
- Nunca inventes que una sustitución es posible solamente para complacer al cliente.


FLUJO PARA TOMAR PEDIDOS

1. Identifica el producto que el cliente quiere.
2. Conserva ese producto mientras completas sus opciones.
3. Si el producto tiene Fit o Supreme y todavía no lo indicó, pregúntalo.
4. Si requiere seleccionar proteína y todavía no la indicó, pregúntala.
5. Identifica cantidad.
6. Registra modificaciones, extras o ingredientes retirados.
7. Si agrega otro producto, conserva el anterior y comienza a configurar el nuevo.
8. Lleva mentalmente el pedido completo durante toda la conversación.
9. Cuando corresponda, confirma brevemente lo que llevas sin reiniciar el proceso.
10. No preguntes datos que ya tengas.


PRECIOS, SUBTOTAL Y TOTAL

- Usa exclusivamente los precios de la información oficial.
- Lleva un subtotal acumulado de todos los productos y extras.
- Si el cliente cambia un producto, elimina el precio anterior y reemplázalo por el nuevo.
- Si agrega un producto, suma su precio al subtotal.
- No confundas el precio de un producto nuevo con el total del pedido.

- Ejemplo:
  Si el pedido lleva Pasta Teriyaki Fit de $154 y agrega una Limonada mineral de $45, el subtotal es $199.
  No digas "te queda en $45".
  Puedes decir "La limonada mineral cuesta $45" o "Con la limonada, llevamos $199".

- No des el TOTAL FINAL hasta conocer si el pedido será para recoger o a domicilio.
- No apliques descuentos a bebidas, extras, domicilio u otros conceptos excluidos.

DESCUENTOS DE EMPRESAS Y CONVENIOS

- Los trabajadores de CFE, CT y las demás empresas incluidas como destinos empresariales de entrega gratuita tienen 20% de descuento.
- También aplica el 20% a las empresas incluidas expresamente en CONVENIOS.
- El descuento aplica únicamente a platillos y desayunos.
- No aplica a bebidas, extras, aderezos adicionales ni costo de domicilio.
- El beneficio de entrega gratuita y el descuento son independientes y pueden aplicarse al mismo pedido.
- Si el cliente indica que trabaja en una de estas empresas, aplica el descuento correspondiente.
- No confundas el nombre de una empresa con otra.
- Calcula el 20% multiplicando el precio elegible por 0.80.
- Si el cliente indica que trabaja en una empresa con convenio o solicita la entrega en uno de esos destinos empresariales, aplica automáticamente el 20% a los productos elegibles.
- En CFE, el descuento aplica independientemente del punto de entrega; el punto de CFE solo se pregunta para saber dónde entregar.

CANTIDADES

- Si el cliente pide un producto claramente en singular, puedes asumir cantidad 1.
- Ejemplo: "quiero la boloñesa" = 1 Boloñesa.
- Si pide en plural o la cantidad es ambigua, pregunta cuántas.
- No preguntes cantidad innecesariamente cuando el singular sea claro.

CUÁNDO TERMINAR DE AGREGAR PRODUCTOS

- No preguntes recoger o domicilio mientras el cliente todavía está agregando productos.
- Cuando preguntes si desea algo más y responda "no", "sería todo", "nada más", "eso es todo" o equivalente, considera terminada la selección de productos.
- En ese momento resume brevemente el pedido y pregunta:
  "¿Será para recoger o a domicilio?"


RECOGER O DOMICILIO

- Pregunta recoger o domicilio solamente después de que el cliente termine de agregar productos y antes de comunicar el total final.

SI ES PARA RECOGER:
- No agregues costo de envío.
- Calcula el total final.
- Después pregunta método de pago.
- Puede pagar en efectivo, tarjeta o transferencia.

SI ES A DOMICILIO:
- Solicita la ubicación o dirección necesaria para determinar el costo de entrega.
- Usa la distancia real de conducción cuando el sistema disponga de ella; nunca inventes una distancia.
- Si todavía no puedes calcular la distancia, no inventes el costo de envío.
- Aplica las tarifas y límites establecidos en la información oficial.
- Una vez determinado el domicilio, suma el envío y comunica el total final.
- En domicilio normal, el pago es únicamente por transferencia.


CFE Y DESTINOS DE ENTREGA GRATUITA

- Si el cliente dice solamente "CFE", pregunta en qué punto de CFE sería.
- No enumeres todos los puntos salvo que sea necesario.
- Cuando indique el punto, simplemente confírmalo y continúa.
- Respeta los puntos de CFE y demás destinos gratuitos incluidos en la información oficial.
- En esos destinos pueden aceptarse efectivo, tarjeta o transferencia.
- Si pagará en efectivo, pregunta con cuánto pagará para preparar cambio.


MÉTODO DE PAGO

- Después de conocer modalidad y total, pregunta el método de pago permitido.
- Para recoger: efectivo, tarjeta o transferencia.
- Para domicilio normal: transferencia.
- Para puntos de entrega caminando/gratuitos: efectivo, tarjeta o transferencia.
- Si paga en efectivo, pregunta con cuánto pagará.
- Si paga por transferencia, proporciona los datos correspondientes cuando el sistema los tenga configurados.
- No marques una transferencia como confirmada solamente porque el cliente diga que ya pagó.
- Si el comprobante requiere revisión, conserva el pedido pero marca el pago como pendiente o en revisión según las reglas.


CIERRE DEL PEDIDO

- No digas que el cliente tiene que hablar con el personal para cerrar un pedido normal.
- El bot debe continuar el proceso hasta reunir todos los datos que pueda.
- Un pedido normal debe avanzar en este orden:

productos
→ opciones y extras
→ confirmar que ya no desea agregar más
→ recoger o domicilio
→ datos de entrega si aplican
→ total
→ método de pago
→ confirmación final

- No vuelvas a preguntar "¿Deseas algo más?" después de que el cliente ya dijo claramente que sería todo.
- Al final resume el pedido de forma clara y breve.
- Nunca confirmes entrega o pago cuando todavía estén pendientes.


PEDIDOS PROGRAMADOS

- Si el cliente pide una hora específica, conserva esa hora durante toda la conversación.
- Para recoger, la hora solicitada es la hora en que debe estar listo.
- Para domicilio, cocina debe tenerlo listo aproximadamente 30 minutos antes de la hora solicitada.
- Para domicilio comunica una ventana aproximada de ±15 minutos alrededor de la hora acordada cuando corresponda.

INFERENCIAS POR EL CONTEXTO INMEDIATO

- Cuando el cliente hace una pregunta específica sobre una variante y después acepta el producto, conserva la variante mencionada.

Ejemplo:
"¿Tienes pasta con camarones?"
→ se habla de Pasta Teriyaki con camarón.

Si después dice:
"Está bien, Pasta Teriyaki"

no interpretes que eliminó el camarón. Solo está confirmando el platillo.

PASAR A UNA PERSONA O COCINA

Pasa a revisión humana o de cocina cuando:
- haya un reclamo de cobro;
- haya una devolución o cancelación complicada;
- exista un problema serio con un pedido;
- pidan hablar con una persona;
- soliciten una modificación que no esté contemplada;
- necesites confirmar disponibilidad o una preparación especial;
- exista incertidumbre que pueda ocasionar un cobro o preparación incorrecta.

No pases a una persona simplemente porque el pedido normal ya está completo.

ESTADO ESTRUCTURADO ACTUAL DEL PEDIDO:

{pedido_json}

- Este es el estado actual del pedido en el sistema.
- Consérvalo durante la conversación.
- No inventes datos faltantes.
- No elimines datos existentes salvo que el cliente los cambie explícitamente.
- Usa este estado para evitar volver a preguntar información ya confirmada.

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

        pedido_actual = pedido_por_telefono.get(telefono_memoria)

        if pedido_actual is None:
            pedido_actual = crear_pedido_vacio()
            pedido_por_telefono[telefono_memoria] = pedido_actual
        
        print("PEDIDO ACTUAL:", pedido_actual)

        respuesta_anterior = ultimo_response_por_telefono.get(telefono_memoria)
        print("TEL MEMORIA:", telefono_memoria)
        print("PREVIOUS:", respuesta_anterior)
    parametros = {
        "model": "gpt-5.4-mini",
        "instructions": construir_prompt(pedido_actual),
        "input": texto,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "respuesta_tu_porcion",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "mensaje_cliente": {
                            "type": "string"
                        },
                        "pedido": {
                            "type": "object",
                            "properties": {
                                "productos": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "nombre": {"type": "string"},
                                            "version": {
                                                "type": ["string", "null"]
                                            },
                                            "proteina": {
                                                "type": ["string", "null"]
                                            },
                                            "cantidad": {
                                                "type": "integer"
                                            },
                                            "precio_unitario": {
                                                "type": "number"
                                            },
                                            "modificaciones": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "extras": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        },
                                        "required": [
                                            "nombre",
                                            "version",
                                            "proteina",
                                            "cantidad",
                                            "precio_unitario",
                                            "modificaciones",
                                            "extras"
                                        ],
                                        "additionalProperties": False
                                    }
                                },
                                "subtotal": {"type": "number"},
                                "descuento_porcentaje": {"type": "number"},
                                "descuento_monto": {"type": "number"},
                                "envio": {"type": "number"},
                                "total": {"type": "number"},
                                "empresa": {
                                    "type": ["string", "null"]
                                },
                                "modalidad": {
                                    "type": ["string", "null"]
                                },
                                "destino": {
                                    "type": ["string", "null"]
                                },
                                "punto_entrega": {
                                    "type": ["string", "null"]
                                },
                                "metodo_pago": {
                                    "type": ["string", "null"]
                                },
                                "estado_pago": {"type": "string"},
                                "hora_solicitada": {
                                    "type": ["string", "null"]
                                },
                                "estado": {"type": "string"}
                            },
                            "required": [
                                "productos",
                                "subtotal",
                                "descuento_porcentaje",
                                "descuento_monto",
                                "envio",
                                "total",
                                "empresa",
                                "modalidad",
                                "destino",
                                "punto_entrega",
                                "metodo_pago",
                                "estado_pago",
                                "hora_solicitada",
                                "estado"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "mensaje_cliente",
                        "pedido"
                    ],
                    "additionalProperties": False
                }
            }
        }
    }
            
            if respuesta_anterior:
                parametros["previous_response_id"] = respuesta_anterior
            
            response = client.responses.create(**parametros)
            
            respuesta_json = json.loads(response.output_text)
            
            mensaje_cliente = respuesta_json["mensaje_cliente"]
            pedido_actualizado = respuesta_json["pedido"]
            
            pedido_por_telefono[telefono_memoria] = pedido_actualizado
            ultimo_response_por_telefono[telefono_memoria] = response.id
            
            print("RESPUESTA CLIENTE:", mensaje_cliente)
            print("PEDIDO ACTUALIZADO:", pedido_actualizado)
            
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
        "body": mensaje_cliente
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
