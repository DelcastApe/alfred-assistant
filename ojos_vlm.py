import os
import requests
import base64
import cv2  # Importado a nivel de módulo global

# Cargar las variables de entorno (.env)
from dotenv import load_dotenv
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODELO_VLM = os.getenv("MODELO_VLM", "moondream")

# Crear una sesión persistente de HTTP para ahorrar tiempos de handshake de red local
session_ollama = requests.Session()

def analizar_escena(frame_cv2, es_gopro=False):
    """
    Toma un frame de OpenCV, lo comprime directamente en memoria a JPEG de alta velocidad,
    y consulta al VLM local usando un prompt adaptativo según el hardware de origen.
    """
    try:
        if frame_cv2 is None:
            return "Error: Fotograma vacío."

        # ⚡ OPTIMIZACIÓN CRÍTICA: Compresión directa en memoria (C++ nativo) sin pasar por Pillow
        success, encoded_image = cv2.imencode('.jpg', frame_cv2, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not success:
            return "Error al codificar la matriz visual."
            
        img_str = base64.b64encode(encoded_image).decode("utf-8")
        
        # 🎯 PROMPT ADAPTATIVO: Cambia la directiva según la cámara que llama
        if es_gopro:
            pregunta = (
                "Analyze this workspace camera frame from the bench/desk. "
                "Describe concisely the tools, objects, electronics, or hardware items present on the table."
            )
        else:
            pregunta = (
                "Analyze this camera frame carefully. Identify the person in front of the screen. "
                "Is it Mr. Gerardo, the sole operator and creator? "
                "Describe the person clearly and state explicitly if a man, user, or person is sitting at the desk."
            )
        
        # Estructurar la petición para la API de Ollama
        url_api = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": MODELO_VLM,
            "prompt": pregunta,
            "stream": False,
            "images": [img_str],
            "options": {
                "temperature": 0.4  # Reducido un poco para respuestas de telemetría más precisas y rápidas
            }
        }
        
        # Enviar usando la sesión persistente
        respuesta = session_ollama.post(url_api, json=payload, timeout=30)
        
        if respuesta.status_code == 200:
            return respuesta.json().get("response", "No se obtuvo diagnóstico.")
        else:
            return f"Error de Ollama: Código de estado {respuesta.status_code}"
            
    except Exception as e:
        return f"Error en la conexión con los ojos de la GPU: {str(e)}"