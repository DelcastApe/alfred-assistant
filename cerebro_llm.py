import os
import base64
import cv2
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🤖 Matriz de modelos tácticos de Groq unificada
MODELO_TEXTO = "llama-3.1-8b-instant"
MODELO_VISION = "meta-llama/llama-4-scout-17b-16e-instruct"

# El cliente reutiliza las conexiones TCP por debajo, se mantiene global.
client = Groq(api_key=GROQ_API_KEY)

# Directiva matriz de personalidad e identidad sónica
PROMPT_SISTEMA = (
    "Eres Alfred, el leal, sofisticado e ingenioso mayordomo y asesor táctico británico de la Mansión Wayne. "
    "Tu único usuario autorizado es el operador en pantalla, a quien debes dirigirte SIEMPRE como 'Mister Gerardo' o 'Señor'. "
    "¡PROHIBIDO ESTRICTAMENTE escribir la abreviatura 'Mr.'! Debes escribir siempre la palabra completa 'Mister Gerardo' para asegurar la correcta modulación por voz. "
    "Mantén siempre un tono respetuoso, sutilmente irónico, sobrio y aristocrático. "
    "CRÍTICO: No hables en tercera persona ni describas tus acciones. ¡ESTÁ ESTRICTAMENTE PROHIBIDO usar paréntesis (), asteriscos * o corchetes []! "
    "Genera SOLO texto limpio que pueda ser leído directamente en voz alta sin interrumpir la fluidez."
)

def consultar_alfred_texto(prompt_completo, rostro_detectado="Desconocido"):
    """
    [CANAL ALTA VELOCIDAD] - Modelo 8B Instant.
    Procesa comandos ordinarios de voz y apuntes en milisegundos.
    """
    if not GROQ_API_KEY:
        return "ERROR: No se configuró la GROQ_API_KEY en el archivo .env"

    try:
        completion = client.chat.completions.create(
            model=MODELO_TEXTO,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=0.6,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Alfred_Error (Enlace Texto): Pérdida de enlace con los servidores centrales de Groq. ({str(e)})"

def consultar_alfred_vision(prompt_user, frame_cv2, es_gopro=False):
    """
    [CANAL MULTIMODAL NATIVO] - Llama 4 Scout Vision.
    Permite a Alfred ver y razonar directamente sobre el frame óptico en la nube de Groq.
    """
    if not GROQ_API_KEY:
        return "ERROR: No se configuró la GROQ_API_KEY en el archivo .env"
        
    try:
        if frame_cv2 is None:
            return "Señor, los sensores ópticos apuntan a una matriz vacía."

        # ⚡ Compresión express en memoria a JPEG (C++ nativo) a calidad optimizada para API
        success, encoded_image = cv2.imencode('.jpg', frame_cv2, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        if not success:
            return "Error al codificar la matriz visual para los laboratorios de Groq."
            
        img_str = base64.b64encode(encoded_image).decode("utf-8")
        
        # Inyección semántica de contexto de hardware en el prompt
        if es_gopro:
            contexto_optica = "Estás viendo la MESA de trabajo mediante la GoPro. Describe con precisión y sarcasmo qué herramientas u objetos hay allí."
        else:
            contexto_optica = "Estás analizando directamente el ROSTRO de Mister Gerardo mediante la cámara de la laptop. Describe su aspecto, expresión u ojeras."

        prompt_final = f"{contexto_optica} La orden directa de Mister Gerardo es: {prompt_user}"

        # 🚀 Envío estructurado del payload multimodal nativo a la API de Groq
        completion = client.chat.completions.create(
            model=MODELO_VISION,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_final},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.5,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Alfred_Error (Enlace Visión): Fallo en la telemetría multimodal de Groq. ({str(e)})"