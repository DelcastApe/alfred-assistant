import os
import requests
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Cargar las variables de entorno (.env)
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODELO_VLM = os.getenv("MODELO_VLM", "moondream")

def analizar_escena(frame_cv2):
    """
    Toma un frame de OpenCV, lo convierte a base64 y le hace una 
    pregunta analítica a Moondream para identificar de forma exclusiva a Mr. Gerardo
    o describir minuciosamente el entorno de la GoPro.
    """
    try:
        # 1. Convertir el frame de OpenCV (BGR) a una imagen de Pillow (RGB)
        import cv2
        frame_rgb = cv2.cvtColor(frame_cv2, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(frame_rgb)
        
        # 2. CORREGIDO PARA WINDOWS: Comprimir en memoria y limpiar la cadena Base64
        buffered = BytesIO()
        imagen_pil.save(buffered, format="JPEG", quality=80)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8").replace("\n", "")
        
        # 3. DIRECTIVA TÁCTICA MEJORADA: Enfoque absoluto en la confirmación de identidad
        pregunta = (
            "Analyze this camera frame carefully. Identify the person in front of the screen. "
            "Is it Mr. Gerardo, the sole operator and creator? "
            "Describe the person clearly and state explicitly if a man, user, or person is sitting at the desk."
        )
        
        # 4. Estructurar la petición para la API de Ollama
        url_api = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": MODELO_VLM,
            "prompt": pregunta,
            "stream": False,  # Respuesta completa de un solo golpe
            "images": [img_str],
            "options": {
                "temperature": 0.5  # Incrementada sutilmente para evitar rigidez en el reconocimiento
            }
        }
        
        # 5. Enviar la telemetría visual al servidor local de Ollama en Windows
        respuesta = requests.post(url_api, json=payload, timeout=90)
        
        if respuesta.status_code == 200:
            return respuesta.json().get("response", "No se obtuvo diagnóstico.")
        else:
            return f"Error de Ollama: Código de estado {respuesta.status_code}"
            
    except Exception as e:
        return f"Error en la conexión con los ojos de la GPU: {str(e)}"

# Bloque de prueba autónomo para el protocolo Alfred
if __name__ == "__main__":
    print("👀 [Alfred - Sistemas]: Probando el módulo de visión local en Windows...")
    print(f"📡 Apuntando a Ollama en: {OLLAMA_HOST}")
    print(f"🧠 Usando el modelo: {MODELO_VLM}")
    
    import numpy as np
    import cv2
    
    imagen_test = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(imagen_test, "Prueba Alfred Windows", (70, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    resultado = analizar_escena(imagen_test)
    print("\n[RESULTADO DE LA TELEMETRÍA VISUAL]:")
    print(resultado)