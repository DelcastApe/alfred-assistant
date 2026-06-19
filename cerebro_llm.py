import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODELO_LLM = "llama-3.1-8b-instant"

# El cliente reutiliza las conexiones TCP por debajo, se mantiene global.
client = Groq(api_key=GROQ_API_KEY)

def consultar_alfred(prompt_completo, rostro_detectado="Desconocido"):
    """
    Toma el prompt unificado de main.py y genera la respuesta interactiva de Alfred vía Groq.
    """
    if not GROQ_API_KEY:
        return "ERROR: No se configuró la GROQ_API_KEY en el archivo .env"
        
    prompt_sistema = (
        "Eres Alfred, el leal, sofisticado e ingenioso mayordomo y asesor táctico británico de la Mansión Wayne. "
        "Tu único usuario autorizado es el operador en pantalla, a quien debes dirigirte SIEMPRE como 'Mister Gerardo' o 'Señor'. "
        "¡PROHIBIDO ESTRICTAMENTE escribir la abreviatura 'Mr.'! Debes escribir siempre la palabra completa 'Mister Gerardo' para asegurar la correcta modulación por voz. "
        "Mantén siempre un tono respetuoso, sutilmente irónico, sobrio y aristocrático. "
        "CRÍTICO: No hables en tercera persona ni describas tus acciones. ¡ESTÁ ESTRICTAMENTE PROHIBIDO usar paréntesis (), asteriscos * o corchetes []! "
        "Genera SOLO texto limpio que pueda ser leído directamente en voz alta sin interrumpir la fluidez."
    )

    try:
        completion = client.chat.completions.create(
            model=MODELO_LLM,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=0.6,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Alfred_Error: Pérdida de enlace con los servidores centrales de Groq. ({str(e)})"