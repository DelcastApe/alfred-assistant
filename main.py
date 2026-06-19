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

# 🎯 ENLACES CRÍTICOS NATIVOS INTERCONECTADOS CON TU NUEVA CAPA DE INFERENCIA
from cerebro_llm import consultar_alfred_texto, consultar_alfred_vision

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
                time.sleep(0.02)  # 20ms para alta reactividad táctica
            pygame.mixer.music.unload()  # Liberar archivo inmediatamente
            
    except Exception as e:
        print(f"⚠️ [Fallo de audio]: {e}")
    finally:
        if os.path.exists(archivo_audio):
            try: os.remove(archivo_audio)
            except: pass

def hablar_en_paralelo(texto):
    """Lanza una alocución en un hilo independiente para no congelar los sensores o la red."""
    hilo = threading.Thread(target=hablar, args=(texto,))
    hilo.start()
    return hilo

def configurar_opticas(cap):
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def escuchar_operador():
    """Configuración del micrófono AMD optimizada para frases completas sin cortes prematuros."""
    r = sr.Recognizer()
    
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.2          # Espera estable para capturar oraciones completas
    r.non_speaking_duration = 0.5    
    
    INDICE_MIC_AMD = 3  
    
    try:
        with sr.Microphone(device_index=INDICE_MIC_AMD, sample_rate=48000) as source:
            print("\n🎙️ [Escuchando...] Ordene, Señor Gerardo...")
            
            r.adjust_for_ambient_noise(source, duration=0.2)  
            
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            print("📡 [Procesando comandos de voz...]")
            comando = r.recognize_google(audio, language="es-ES")
            print(f"👤 [Mister Gerardo]: {comando}")
            return comando.lower()
            
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
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
            hablar("Entendido, Señor. He registrado esa anotación in los apuntes.")
            return True
    return False

def leer_ultimos_apuntes():
    if os.path.exists(ARCHIVO_NOTAS):
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            return "".join(f.readlines()[-3:])
    return "No hay registros previos anotados hoy."

def realizar_escaneo_biometrico(cap_laptop_global):
    """Verifica identidad local por hardware utilizando el flujo óptico global continuo."""
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

    hilo_voz = hablar_en_paralelo("Iniciando escaneo biométrico. Mire fijamente a la cámara, Señor.")
    
    acceso_concedido = False
    frame_rostro = None
    inicio_busqueda = time.time()
    
    while time.time() - inicio_busqueda < 5.0:
        if not cap_laptop_global.isOpened():
            continue
            
        ret, frame = cap_laptop_global.read()
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
                frame_rostro = frame.copy()
                break
                
        if acceso_concedido:
            break
        time.sleep(0.01)
        
    hilo_voz.join()
    return acceso_concedido, frame_rostro

def bucle_principal():
    print("🦇 [Protocolo Alfred Windows]: Inicializando periféricos globales de la estación...")
    
    cap_laptop = cv2.VideoCapture(CAMARA_LAPTOP)
    configurar_opticas(cap_laptop)
    
    cap_gopro = cv2.VideoCapture(FUENTE_GOPRO, cv2.CAP_DSHOW)
    if not cap_gopro.isOpened():
        print("🔍 [Sistemas]: GoPro no detectada en índice 6 con DirectShow. Probando apertura estándar...")
        cap_gopro = cv2.VideoCapture(FUENTE_GOPRO)
    configurar_opticas(cap_gopro)
    
    acceso, frame_inicial = realizar_escaneo_biometrico(cap_laptop)
    if not acceso:
        print("\n🚨 [ALERTA DE SEGURIDAD]: Identidad no verificada.")
        hablar("Acceso denegado. Apagando los sistemas.")
        cap_laptop.release()
        if cap_gopro.isOpened(): cap_gopro.release()
        sys.exit()
        
    print("\n🔓 [ACCESO CONCEDIDO]: Identidad confirmada.\n")
    hablar("Acceso concedido, identidad confirmada.")
    
    # Saludo inicial inyectando el frame directo a Groq Vision (Canal Llama 4 Scout)
    respuesta_saludo = "Señor, no se pudo enlazar la telemetría multimodal inicial."
    if frame_inicial is not None:
        print("🧠 [Groq Multimodal]: Transmitiendo frame facial de bienvenida a Llama-4-Scout...")
        respuesta_saludo = consultar_alfred_vision("Dame una bienvenida formal y analiza mi rostro o estado físico actual.", frame_inicial, es_gopro=False)
    else:
        respuesta_saludo = consultar_alfred_texto("Dale una bienvenida formal a Mister Gerardo e infórmale que la cámara falló.")
        
    hablar(respuesta_saludo)

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

            # 🎯 ENRUTADOR INTELIGENTE ASIMÉTRICO DE CANALES (OPTIMIZADO CON FILTROS DE INDUMENTARIA Y ÓPTICAS)
            palabras_gopro = ["mesa", "gopro", "go pro", "objetos", "tengo en", "ves en la", "cámara secundaria"]
            palabras_laptop = ["me veo", "mi cara", "mi rostro", "cómo luzco", "mi aspecto", "sobre mí", "mírame", "camiseta", "ropa", "traigo puesto", "cámara principal", "cámara de la laptop", "laptop"]
            palabras_vision_general = ["mira", "observa", "qué ves", "analiza", "inspecciona"]

            requiere_gopro = any(p in orden for p in palabras_gopro)
            requiere_laptop = any(p in orden for p in palabras_laptop)
            requiere_vision_general = any(p in orden for p in palabras_vision_general)

            # CASO A: Canal Visión Nativo Groq - Óptica GoPro (Mesa)
            if requiere_gopro:
                hilo_espera = hablar_en_paralelo("Por supuesto. Permítame enfocar los sensores de la GoPro hacia la mesa de trabajo.")
                
                ret, frame_gopro = False, None
                if cap_gopro.isOpened():
                    for _ in range(2): cap_gopro.read()  # Vaciado veloz del búfer de hardware
                    ret, frame_gopro = cap_gopro.read()
                
                hilo_espera.join()

                if ret and frame_gopro is not None:
                    print("🧠 [Groq Visión]: Transmitiendo fotograma de la mesa a Llama-4-Scout...")
                    respuesta_alfred = consultar_alfred_vision(orden, frame_gopro, es_gopro=True)
                else:
                    respuesta_alfred = "Error de telemetría, Señor. La GoPro no devolvió señal de video válida."

            # CASO B: Canal Visión Nativo Groq - Óptica Laptop (Rostro, Camiseta, Ropa o Visión General por defecto)
            elif requiere_laptop or requiere_vision_general:
                hilo_espera = hablar_en_paralelo("Un momento, Señor. Procedo a capturar la matriz óptica de su aspecto.")
                
                ret_l, frame_lap = False, None
                if cap_laptop.isOpened():
                    for _ in range(2): cap_laptop.read()  # Vaciado veloz del búfer
                    ret_l, frame_lap = cap_laptop.read()
                
                hilo_espera.join()

                if ret_l and frame_lap is not None:
                    print("🧠 [Groq Visión]: Transmitiendo fotograma facial/corporal a Llama-4-Scout...")
                    respuesta_alfred = consultar_alfred_vision(orden, frame_lap, es_gopro=False)
                else:
                    respuesta_alfred = "Error de hardware, Señor. La cámara de la laptop no devolvió señal."

            # CASO C: Canal Texto Express Groq - Llama 3.1 8B Instant (Comandos sin cámara)
            else:
                memoria_trabajo = leer_ultimos_apuntes()
                prompt_inyectado = (
                    f"Orden del operador: '{orden}'. "
                    f"Las últimas notas del laboratorio son: '{memoria_trabajo}'. "
                )
                print("🧠 [Cerebro LLM]: Procesando comando de voz veloz en Llama-3.1-8b...")
                respuesta_alfred = consultar_alfred_texto(prompt_inyectado)

            # Salida sónica unificada por los altavoces
            hablar(respuesta_alfred)
            print("-" * 50)
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n🛑 Desactivando sistemas de forma manual.")
    finally:
        print("🔌 Clausurando flujos de hardware óptico de forma limpia...")
        if cap_laptop.isOpened(): cap_laptop.release()
        if cap_gopro.isOpened(): cap_gopro.release()

if __name__ == "__main__":
    bucle_principal()