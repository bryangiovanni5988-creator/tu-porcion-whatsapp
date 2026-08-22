# config_tu_porcion.py
NEGOCIO = {
    "nombre": "Tu Porción",
    "ciudad": "Hermosillo, Sonora",
    "direccion_origen_reparto": "Matamoros 17, Hermosillo, Sonora",
    "sitio_web": "https://www.tuporcion.com.mx",
}

HORARIOS = {
    "lunes": ("07:30", "17:00"),
    "martes": ("07:30", "17:00"),
    "miercoles": ("07:30", "17:00"),
    "jueves": ("07:30", "17:00"),
    "viernes": ("07:30", "17:00"),
    "sabado": ("10:00", "16:00"),
    "domingo": None,
}

DESAYUNOS = {
    "Huevos con Jamón": {"precio": 105},
    "Huevos rancheros": {"precio": 105},
    "Chilaquiles de Huevos": {"precio": 115},
    "Chilaquiles de pollo": {"precio": 135},
    "Omelette de queso": {"precio": 95},
    "Omelette de queso y Jamón": {"precio": 109},
    "Omelette de queso y Espinaca": {"precio": 109},
    "Machaca con verdura": {"precio": 125},
    "Machaca con huevo": {"precio": 130},
    "Huevos con verdura": {"precio": 95},
    "Avocado Toast": {"precio": 105},
    "Panela Toast": {"precio": 115},
    "Sandwich de jamón": {"precio": 80},
    "Sandwich de pollo": {"precio": 110},
    "HotCakes de avena": {"precio": 120},
    "Pan francés integral": {"precio": 115},
    "Waffles integrales": {"precio": 120},
    "Escamocha": {"precio": 89},
}

BOWL = {
    "regular": 154,
    "supreme": 174,
    "proteinas": ["Pechuga de pollo", "Carne de res", "Atún fresco o sellado", "Camarón"],
    "carbohidratos": ["Arroz al vapor", "Pasta", "Crutones", "Frutos secos", "Aguacate"],
    "aderezos": ["César", "Chipotle", "Ajo y especias", "Ponzu", "Búfalo", "Vinagreta de jamaica", "BBQ", "Teriyaki"],
}

PLATILLOS = {
    "Quesadillas de Marlín": {"fit": 159, "supreme": 189},
    "Pasta Verde": {"fit": 149, "supreme": 174},
    "Pollo con papas": {"fit": 149, "supreme": 174},
    "Teriyaki": {"fit": 154, "supreme": 179, "proteinas": ["Pollo", "Res", "Camarón"]},
    "Pechuga al Grill": {"fit": 149, "supreme": 174},
    "Pechuga Pomodoro": {"fit": 159, "supreme": 184},
    "Wok estilo Mongol": {"fit": 154, "supreme": 179, "proteinas": ["Pollo", "Res", "Camarón"]},
    "Pollo a la mostaza": {"fit": 149, "supreme": 174},
    "Burger Proteica": {"fit": 154, "supreme": 184},
    "Hamburguesa de pollo": {"fit": 149, "supreme": 179},
    "Ceviche de Atún": {"fit": 159, "supreme": 189},
    "Pasta Teriyaki": {"fit": 154, "supreme": 179, "proteinas": ["Pollo", "Res", "Camarón"]},
    "Espagueti Boloñesa": {"fit": 149, "supreme": 174},
}

SUSHI = {
    "Chicken Roll": 149,
    "Sonora Roll": 159,
    "Tuna Roll": 159,
    "Tampico Roll": 159,
}

PLANES = {"5_fit": 675, "5_supreme": 799, "10_fit": 1265, "10_supreme": 1475}

EXTRAS = {
    "Pollo 150 g": 45,
    "Res 150 g": 60,
    "Camarón 110 g": 60,
    "Atún 110 g": 60,
    "Arroz": 20,
    "Pasta": 20,
    "Aderezo 2 oz": 12,
    "Aderezo 4 oz": 18,
    "Aguacate": 20,
}

BEBIDAS = {
    "Limonada natural": 35,
    "Limonada mineral": 45,
    "Limonada de fresa": 45,
    "Limonada de fresa mineral": 55,
    "Jamaica": 30,
    "Té negro": 30,
    "Jugo verde": 55,
    "Mango Splash": 75,
    "Dulce Tentación": 75,
    "Licuado de plátano": 55,
    "Licuado de chocoplátano": 55,
    "Licuado de papaya": 55,
}

NUTRICION = {
    "Bowl Regular": {"kcal": "350-550", "proteina_g": "38-47"},
    "Quesadillas de Marlín": {"kcal": 540, "proteina_g": 44},
    "Pasta Verde": {"kcal": 510, "proteina_g": 47},
    "Pollo con papas": {"kcal": 460, "proteina_g": 43},
    "Teriyaki": {"kcal": 500, "proteina_g": 42},
    "Pechuga al Grill": {"kcal": 430, "proteina_g": 42},
    "Pechuga Pomodoro": {"kcal": 515, "proteina_g": 49},
    "Burger Proteica": {"kcal": 400, "proteina_g": 47},
    "Ceviche de Atún": {"kcal": 545, "proteina_g": 39},
    "Wok estilo Mongol": {"kcal": 500, "proteina_g": 42},
    "Pollo a la mostaza": {"kcal": 480, "proteina_g": 46},
    "Hamburguesa de pollo": {"kcal": 525, "proteina_g": 44},
    "Pasta Teriyaki": {"kcal": 510, "proteina_g": 43},
    "Espagueti Boloñesa": {"kcal": 520, "proteina_g": 41},
    "Chicken Roll": {"kcal": 515, "proteina_g": 43},
    "Sonora Roll": {"kcal": 565, "proteina_g": 45},
    "Tuna Roll": {"kcal": 445, "proteina_g": 40},
    "Tampico Roll": {"kcal": 525, "proteina_g": 39},
}

SUSTITUCIONES = {
    "permitidas": [
        "Quitar ingrediente",
        "Ingrediente aparte",
        "Sushi sin alga",
        "Arroz por pasta sin costo",
        "Pasta por arroz sin costo",
        "Cambiar aderezo cuando aplique",
    ],
    "no_especificadas": "Consultar cocina antes de confirmar",
    "doble_proteina": "Cobrar extra según tabla",
    "extra_marlin": "Cobrar internamente como atún; no explicarlo al cliente",
    "dos_carbohidratos": "Si dividen una sola porción entre dos opciones, cobrar media porción extra cuando aplique; ejemplo confirmado: frutos secos + pasta = +$10",
}

REGLAS_BEBIDAS = {
    "jamaica_y_limonada": "Splenda",
    "te_negro": "Stevia",
    "licuados": "Splenda",
    "jugo_verde": "Sin endulzante añadido; naranja y piña",
    "mango_splash": "Sin endulzante añadido",
    "dulce_tentacion": "Lleva miel",
}

RECOMENDACIONES = {
    "pollo": ["Pasta Verde", "Pollo con papas"],
    "res": ["Teriyaki de Res", "Espagueti Boloñesa"],
    "atun": ["Ceviche de Atún", "Quesadillas de Marlín"],
    "camaron": ["Tampico Roll", "Pasta Teriyaki de Camarón"],
    "llenador": ["Wok estilo Mongol", "Espagueti Boloñesa"],
    "natural": ["Arma tu Bowl", "Pechuga al Grill"],
    "alto_proteina": ["Pechuga Pomodoro", "Pasta Verde", "Burger Proteica", "Pollo a la mostaza", "Sonora Roll"],
}

CONVENIOS = {
    "CFST": {
        "descuento": 0.20,
        "aplica": ["platillos", "desayunos"],
        "no_aplica": ["bebidas", "extras", "aderezos", "domicilio"],
    }
}

DESTINOS_GRATIS = ["CT", "Bomberos", "NGX"]

PUNTOS_CFE = {
    "Con Don Isma": ["Con Don Isma", "Don Isma", "Matamoros", "entrada por Matamoros"],
    "Cajeros / Atención al cliente": ["Cajeros", "Atención al cliente"],
    "Glorieta": ["Glorieta"],
    "Juárez / Guardia": ["Juárez", "Juarez", "guardia", "con el guardia"],
    "Utec": ["Utec"],
}

TARIFAS_DOMICILIO = [
    (0, 2, 25),
    (2, 3, 30),
    (3, 4, 35),
    (4, 5, 40),
    (5, 6, 45),
    (6, 7, 50),
    (7, 8, 55),
]

REGLAS_DOMICILIO = {
    "usar_distancia_conduccion": True,
    "8_a_10_km": {"pedido_minimo": 300, "costo": 60},
    "mas_de_10_km": "No entregar",
}

METODOS_PAGO = {
    "domicilio_normal": ["transferencia"],
    "recoger": ["efectivo", "tarjeta", "transferencia"],
    "destino_gratis": ["efectivo", "tarjeta", "transferencia"],
}

VALIDACION_COMPROBANTE = {
    "faltante_maximo": 1,
    "excedente_maximo": 30,
    "si_cumple": "Aceptar operativamente",
    "si_no_legible": "Revisión manual",
}

ESTADOS_DEMANDA = {
    "normal": {"recoger": "5-20 min", "domicilio": "20-40 min"},
    "alta_demanda": {"recoger": "30-45 min", "domicilio": "45-60+ min"},
    "saturado": {"recoger": "45-60 min", "domicilio": "60+ min"},
}

PEDIDOS_PROGRAMADOS = {
    "recoger": "Listo a la hora solicitada",
    "domicilio": "Listo 30 min antes; ventana de entrega ±15 min",
}

REGLAS_CAMBIOS = {
    "antes_de_cocina": "Permitir cambios y recalcular el pedido.",
    "en_preparacion": "Los cambios requieren revisión humana.",

    "cancelacion_en_construccion": "Permitir cancelación automática sin revisión humana.",
    "cancelacion_confirmado": "Pasar a revisión humana.",
    "cancelacion_en_preparacion": "Pasar a revisión humana.",
    "cancelacion_listo": "Pasar a revisión humana.",

    "reglas_cancelacion": [
        "El estado real del pedido se determina por el campo estado del pedido.",
        "No afirmar que el pedido está en cocina o en proceso si el estado no lo indica.",
        "Si el estado es en_construccion y el cliente pide cancelar, aceptar la cancelación sin revisión humana.",
        "Si el cliente dice no lo canceles o siempre sí antes de que avance a cocina, conservar o reactivar el pedido.",
        "Si el estado es confirmado, en_preparacion o listo, la cancelación debe pasar a revisión humana."
    ]
}

REGLAS_PLANES_MVP = "Si el cliente menciona que tiene plan, tomar pedido y marcar REVISIÓN DE PLAN."

REGLAS_AGOTADOS = "Informar con disculpa breve y recomendar solo alternativas realmente similares."

REGLAS_CONVERSACION = [
    "Responder siempre en español",
    "Ser breve, normalmente 1 a 4 frases",
    "No inventar precios ni disponibilidad",
    "Hacer máximo una o dos preguntas por mensaje",
    "Si algo no está contemplado, consultar cocina o revisión humana",
]
