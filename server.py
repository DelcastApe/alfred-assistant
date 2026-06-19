import os
import cv2
import numpy as np
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 🎯 ENLACES CRÍTICOS MULTIMODALES DE TU CEREBRO
from cerebro_llm import consultar_alfred_texto, consultar_alfred_vision

load_dotenv()

app = FastAPI(
    title="Alfred Tactical MR Server",
    description="Centro de computación asimétrica para Meta Quest 3",
    version="1.0.0"
)

# Constante de almacenamiento de apuntes
ARCHIVO_NOTAS = "apuntes_batcueva.txt"

def leer_ultimos_apuntes():
    if os.path.exists(ARCHIVO_NOTAS):
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            return "".join(f.readlines()[-3:])
    return "No hay registros previos anotados hoy."

@app.get("/")
def estado_estacion():
    """Verificación de enlace de la Batcueva."""
    return {"status": "ONLINE", "peripherals": "Awaiting Quest 3 Connection"}

@app.post("/api/v1/alfred/comando")
async def procesar_comando_tactico(
    orden: str = Form(...),
    frame: UploadFile = File(None)
):
    """
    Endpoint Matriz: Recibe la orden por voz (transcrita o en texto) y el frame 
    opcional del Passthrough de las Meta Quest 3.
    """
    orden_clean = orden.lower().strip()
    print(f"\n📡 [Quest 3 Incoming]: '{orden_clean}'")

    # 🎯 ENRUTADOR INTELIGENTE ADAPTADO PARA REALIDAD MIXTA
    palabras_vision = [
        "mira", "observa", "qué ves", "analiza", "inspecciona", 
        "este", "esto", "mesa", "objeto", "camiseta", "ropa", "traigo puesto"
    ]
    requiere_vision = any(p in orden_clean for p in palabras_vision)

    # CASO A: El comando requiere procesamiento visual y las Quest enviaron un frame
    if requiere_vision and frame is not None:
        try:
            print("👁️ [Servidor VLM]: Decodificando matriz óptica del passthrough...")
            # Leer el archivo binario enviado por red por las Quest
            contents = await frame.read()
            nparr = np.frombuffer(contents, np.uint8)
            # Decodificar a formato OpenCV (BGR)
            frame_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame_cv2 is None:
                raise ValueError("Matriz de imagen corrupta o no legible.")

            print("🧠 [Groq Visión]: Transmitiendo entorno de realidad mixta a Llama-4-Scout...")
            # Mandamos a Alfred Visión indicando que es la cámara principal de las gafas (es_gopro=False para descripción general)
            respuesta_alfred = consultar_alfred_vision(orden_clean, frame_cv2, es_gopro=False)
            
        except Exception as e:
            print(f"🚨 [Fallo Óptico]: {e}")
            respuesta_alfred = f"Señor, mis sensores ópticos han sufrido una anomalía de red al procesar el entorno. (Error: {str(e)})"

    # CASO B: Comando ordinario de voz/texto (Llama 3.1 8B Instant)
    else:
        memoria_trabajo = leer_ultimos_apuntes()
        prompt_inyectado = (
            f"Orden del operador desde el visor: '{orden_clean}'. "
            f"Las últimas notas del laboratorio son: '{memoria_trabajo}'."
        )
        print("🧠 [Cerebro LLM]: Despachando consulta de texto express a Llama-3.1-8b...")
        respuesta_alfred = consultar_alfred_texto(prompt_inyectado)

    print(f"🤵 [ALFRED]: {respuesta_alfred}\n" + "-"*50)
    
    # Retornamos JSON limpio. Unity leerá este texto para pintarlo en las pizarras holográficas
    return JSONResponse(content={
        "alfred_response": respuesta_alfred,
        "mode_executed": "VISION_L4" if (requiere_vision and frame is not None) else "TEXT_8B"
    })

if __name__ == "__main__":
    import uvicorn
    # Levantamos el servidor en el puerto 8000 visible para toda tu red local (0.0.0.0)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)