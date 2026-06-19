import cv2
import time
import os
import sys
import asyncio
import numpy as np
import speech_recognition as sr
from dotenv import load_dotenv
import edge_tts
import pygame  # Control de audio premium nativo
import threading  # Para paralelizar el escaneo por hardware mientras Alfred habla

# 🎯 ENLACE CRÍTICO: Importación del cerebro LLM local
from cerebro_llm import consultar_alfred

load_dotenv()

# 🛡️ FIX CRÍTICO PARA ASYNCIO EN WINDOWS (Evita el error 'Event loop is closed')
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# =====================================================================
# CONFIGURACIÓN TÁCTICA NATIVA EN WINDOWS
# =====================================================================
CAMARA_LAPTOP = 0
FUENTE_GOPRO = 6  # Índice de la GoPro con DirectShow

VOZ_SELECCIONADA = "es-US-AlonsoNeural"    
VELOCIDAD = "+48%"                        # ⚡ Velocidad ultra-fluida optimizada
ARCHIVO_NOTAS = "apuntes_batcueva.txt"     

# Inicializar el mezclador de audio de pygame de forma limpia
pygame.mixer.init()

def hablar(texto):
    """Genera el audio en alta fidelidad y lo reproduce de forma nativa usando pygame."""
    print(f"\n🤵 [ALFRED]: {texto}")
    archivo_audio = "alfred_premium.mp3"
    
    async def generar_audio():
        communicate = edge_tts.Communicate(texto, VOZ_SELECCIONADA, rate=VELOCIDAD)
        await communicate.save(archivo_audio)
        
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generar_audio())
        loop.close()
        
        if os.path.exists(archivo_audio):
            pygame.mixer.music.load(archivo_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            pygame.mixer.music.unload()  # Liberar archivo inmediatamente
            
    except Exception as e:
        print(f"⚠️ [Fallo de audio]: {e}")
    finally:
        if os.path.exists(archivo_audio):
            try: os.remove(archivo_audio)
            except: pass

def configurar_opticas(cap):
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def escuchar_operador():
    """Usa el micrófono de AMD explícitamente configurado en el Índice 3."""
    r = sr.Recognizer()
    
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    r.non_speaking_duration = 0.4
    
    INDICE_MIC_AMD = 3  
    
    try:
        with sr.Microphone(device_index=INDICE_MIC_AMD, sample_rate=48000) as source:
            print("\n🎙️ [Escuchando...] Ordene, Señor Gerardo...")
            
            r.adjust_for_ambient_noise(source, duration=0.2)
            
            audio = r.listen(source, timeout=4, phrase_time_limit=6)
            print("📡 [Procesando comandos de voz...]")
            comando = r.recognize_google(audio, language="es-ES")
            print(f"👤 [Mister Gerardo]: {comando}")
            return comando.lower()
            
    except sr.WaitTimeoutError:
        print("⏳ [Micrófono]: Silencio detectado (Tiempo de espera agotado).")
        return ""
    except sr.UnknownValueError:
        print("❓ [Micrófono]: Ruido detectado pero la frase no fue inteligible.")
        return ""
    except Exception as e:
        print(f"⚠️ [Error de micrófono]: {e}")
        return ""

def gestionar_apuntes(texto_comando):
    palabras_clave = ["anota", "recuerda", "escribe", "apunta", "guarda un apunte", "escribe un apunte"]
    if any(palabra in texto_comando for palabra in palabras_clave):
        nota = texto_comando
        for palabra in palabras_clave:
            nota = nota.replace(palabra, "")
        nota = nota.strip()
        
        if nota:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(ARCHIVO_NOTAS, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] - {nota}\n")
            hablar("Entendido, Señor. He registrado esa anotación en los apuntes.")
            return True
    return False

def leer_ultimos_apuntes():
    if os.path.exists(ARCHIVO_NOTAS):
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            return "".join(f.readlines()[-3:])
    return "No hay registros previos anotados hoy."

def realizar_escaneo_biometrico():
    """Verifica identidad local por hardware y retorna el estado junto al fotograma capturado."""
    print("\n🔒 [PROTOCOLO DE SEGURIDAD]: Matriz Bloqueada. Verificando identidad local...")
    
    if not os.path.exists('modelo_rostro.xml'):
        print("🚨 [CRÍTICO]: No se encuentra 'modelo_rostro.xml'. Ejecute primero el entrenamiento facial.")
        hablar("Alerta, Señor. No he detectado la base de datos de su rostro en el sistema local.")
        return False, None

    try:
        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.read('modelo_rostro.xml')
    except AttributeError:
        print("🚨 [ERROR]: Requiere módulos contrib. Ejecute en su consola: pip install opencv-contrib-python")
        hablar("Error de dependencias de hardware. Revise la consola, Señor.")
        return False, None

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    hilo_voz = threading.Thread(target=hablar, args=("Iniciando escaneo biométrico. Mire fijamente a la cámara, Señor.",))
    hilo_voz.start()
    
    cap0 = cv2.VideoCapture(CAMARA_LAPTOP)
    configurar_opticas(cap0)
    
    acceso_concedido = False
    frame_rostro = None
    inicio_busqueda = time.time()
    
    while time.time() - inicio_busqueda < 5.0:
        if not cap0.isOpened():
            continue
            
        ret, frame = cap0.read()
        if not ret or frame is None:
            continue
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            rostro_recortado = gray[y:y+h, x:x+w]
            rostro_recortado = cv2.resize(rostro_recortado, (150, 150))
            
            label, confianza = reconocedor.predict(rostro_recortado)
            
            if label == 1 and confianza < 75:
                print(f"🎯 [Sistemas]: Identidad confirmada por hardware local (Confianza: {confianza:.2f})")
                acceso_concedido = True
                frame_rostro = frame.copy()  # Preservamos el frame exacto de su rostro para el VLM
                break
                
        if acceso_concedido:
            break
        time.sleep(0.03)
        
    cap0.release()
    hilo_voz.join()
    return acceso_concedido, frame_rostro

def bucle_principal():
    print("🦇 [Protocolo Alfred Windows]: Inicializando sistemas interactivos...")
    
    acceso, frame_inicial = realizar_escaneo_biometrico()
    if not acceso:
        print("\n🚨 [ALERTA DE SEGURIDAD]: Identidad no verificada.")
        hablar("Acceso denegado. Apagando los sistemas.")
        sys.exit()
        
    print("\n🔓 [ACCESO CONCEDIDO]: Identidad confirmada.\n")
    hablar("Acceso concedido, identidad confirmada.")
    
    telemetria_animo = "No se pudo determinar el estado visual del operador."
    if frame_inicial is not None:
        print("🧠 [Biometría Avanzada]: Consultando VLM para analizar la expresión de Mister Gerardo...")
        try:
            from ojos_vlm import analizar_escena
            telemetria_animo = analizar_escena(frame_inicial)
            print(f"[TELEMETRÍA EMOCIONAL NATIVA]: '{telemetria_animo}'\n")
        except Exception as e:
            print(f"⚠️ [Error de VLM en inicio]: {e}")

    prompt_saludo = (
        f"Actúa estrictamente como Alfred, el ingenioso, sarcástico pero sumamente leal mayordomo virtual de Mister Gerardo. "
        f"Él se acaba de autenticar con éxito mediante escaneo facial. Lo que estás viendo en su rostro o estado físico actual "
        f"a través del lente de la laptop según tus sensores visuales es: {telemetria_animo}. "
        f"Dale una bienvenida formal, pero haz un comentario divertido, irónico o bromea abiertamente sobre cómo se ve hoy. "
        f"Sé expresivo y conciso."
    )
    
    print("🧠 [Cerebro LLM]: Formulando saludo interactivo en Groq...")
    respuesta_saludo = consultar_alfred(prompt_saludo, rostro_detectado="Confirmado")
    hablar(respuesta_saludo)
    
    # 📡 ENLAZAR LA GOPRO EN EL ÍNDICE 6 FORZANDO EL BACKEND DIRECTSHOW DE WINDOWS
    cap_gopro = cv2.VideoCapture(FUENTE_GOPRO, cv2.CAP_DSHOW)
    if not cap_gopro.isOpened():
        print("🔍 [Sistemas]: GoPro no detectada en índice 6 con DirectShow. Probando apertura estándar...")
        cap_gopro = cv2.VideoCapture(FUENTE_GOPRO)
        
    configurar_opticas(cap_gopro)

    try:
        while True:
            orden = escuchar_operador()
            if not orden:
                continue
                
            if any(parar in orden for parar in ["apagar sistemas", "descansa alfred", "apágate"]):
                hablar("Desconectando matriz operativa de forma segura. Descanse, Mister Gerardo.")
                break

            if gestionar_apuntes(orden):
                continue

            # 🎯 ENRUTADOR INTELIGENTE DE CÁMARAS Y CONTEXTO VISUAL
            palabras_gopro = ["mesa", "gopro", "go pro", "objetos", "tengo en", "ves en la"]
            palabras_laptop = ["me veo", "mi cara", "mi rostro", "cómo luzco", "mi aspecto", "sobre mí"]
            
            requiere_gopro = any(p in orden for p in palabras_gopro)
            requiere_laptop = any(p in orden for p in palabras_laptop)

            telemetria_contexto = "Análisis visual omitido (El comando no requiere inspección por cámara)."

            # CASO A: Análisis de la Mesa mediante la GoPro
            if requiere_gopro:
                ret, frame_gopro = False, None
                if cap_gopro.isOpened():
                    # Limpiar buffer leyendo un par de frames
                    for _ in range(2): cap_gopro.read()
                    ret, frame_gopro = cap_gopro.read()

                if ret and frame_gopro is not None:
                    print("👀 [Ojos VLM]: Capturando y procesando entorno desde la GoPro (Mesa)...")
                    from ojos_vlm import analizar_escena
                    telemetria_contexto = f"Telemetría actual de la MESA vista por la GoPro: {analizar_escena(frame_gopro)}"
                else:
                    telemetria_contexto = "Error de hardware: La GoPro no devolvió señal de video válida."

            # CASO B: Análisis del Rostro/Físico del operador mediante la Laptop
            elif requiere_laptop:
                print("📸 [Sensores Locales]: Activando cámara de la laptop para inspección de aspecto...")
                cap_lap = cv2.VideoCapture(CAMARA_LAPTOP)
                configurar_opticas(cap_lap)
                ret_l, frame_lap = False, None
                if cap_lap.isOpened():
                    time.sleep(0.1)  # Breve latencia para exposición de luz
                    ret_l, frame_lap = cap_lap.read()
                cap_lap.release()

                if ret_l and frame_lap is not None:
                    print("🧠 [Ojos VLM]: Procesando fotograma facial del operador desde la laptop...")
                    from ojos_vlm import analizar_escena
                    telemetria_contexto = f"Telemetría actual del ASPECTO/ROSTRO de Mister Gerardo visto por la laptop: {analizar_escena(frame_lap)}"
                else:
                    telemetria_contexto = "Error de hardware: La cámara de la laptop no pudo ser inicializada."

            memoria_trabajo = leer_ultimos_apuntes()

            prompt_inyectado = (
                f"Actúa estrictamente como Alfred, el ingenioso, sarcástico pero sumamente leal mayordomo virtual de Mister Gerardo. "
                f"Él te acaba de decir por comando de voz: '{orden}'. "
                f"Entorno visual capturado: {telemetria_contexto}. "
                f"Las últimas notas del laboratorio son: {memoria_trabajo}. "
                f"Responde de manera carismática, directa y con tu característico sentido del humor británico. "
                f"Usa los datos visuales provistos únicamente si corresponden al contexto de la pregunta de Mister Gerardo. "
                f"Si el análisis visual indica que fue omitido, responde directamente sin inventar objetos en el entorno. Sé breve y fluido."
            )

            print("🧠 [Cerebro LLM]: Procesando comando en Groq...")
            respuesta_alfred = consultar_alfred(prompt_inyectado, rostro_detectado="Confirmado")
            
            hablar(respuesta_alfred)
            print("-" * 50)
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n🛑 Desactivando sistemas de forma manual.")
    finally:
        if cap_gopro.isOpened():
            cap_gopro.release()

if __name__ == "__main__":
    bucle_principal()