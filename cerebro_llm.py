import os
from groq import Groq
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Configuramos el modelo de producción elegido de tu lista
MODELO_LLM = "llama-3.1-8b-instant"

# Inicializar cliente de Groq
client = Groq(api_key=GROQ_API_KEY)

def consultar_alfred(prompt_completo, rostro_detectado="Desconocido"):
    """
    Toma el prompt táctico unificado de main.py (VLM + Micrófono + Notas)
    y genera la respuesta interactiva con la personalidad de Alfred.
    """
    if not GROQ_API_KEY:
        return "ERROR: No se configuró la GROQ_API_KEY en el archivo .env"
        
    # Instrucciones base de personalidad del sistema
# Instrucciones base de personalidad del sistema (ACTUALIZADO)
# Instrucciones base de personalidad del sistema (ACTUALIZADO - REGLA DE PRONUNCIACIÓN)
    prompt_sistema = (
        "Eres Alfred, el leal, sofisticado e ingenioso mayordomo y asesor táctico británico de la Mansión Wayne. "
        "Tu único usuario autorizado es el operador en pantalla, a quien debes dirigirte SIEMPRE como 'Mister Gerardo' (escrito completo) o 'Señor'. "
        "¡PROHIBIDO ESTRÍCTAMENTE escribir la abreviatura 'Mr.'! Debes escribir siempre la palabra completa 'Mister Gerardo' para asegurar que el sintetizador de voz lo pronuncie correctamente. "
        "Mantén siempre un tono respetuoso, sutilmente irónico, sobrio y aristocrático. "
        "CRÍTICO: No hables en tercera persona ni describas tus acciones. ¡ESTÁ ESTRICTAMENTE PROHIBIDO usar paréntesis (), asteriscos * o corchetes [] para describir expresiones, gestos, pausas o emociones! "
        "Genera SOLO texto limpio que pueda ser leído directamente en voz alta sin interrumpir la fluidez."
    )

    try:
        completion = client.chat.completions.create(
            model=MODELO_LLM,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=0.6, # Un toque extra de creatividad para las bromas
            max_tokens=150   # Espacio suficiente para respuestas completas
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Alfred_Error: Pérdida de enlace con los servidores centrales de Groq. ({str(e)})"