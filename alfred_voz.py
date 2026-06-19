import subprocess
import shlex

def hablar(texto):
    """
    Hace que Alfred dicte un mensaje llamando a la PowerShell de Windows
    desde WSL. Evita cuelgues y usa las voces nativas del sistema host.
    """
    print(f"\n🗣️ [ALFRED VOZ]: {texto}")
    
    # Escapar comillas para evitar errores de sintaxis en el comando de PowerShell
    texto_escapado = texto.replace('"', '`"').replace("'", "`'")
    
    # Comando de PowerShell para inicializar el sintetizador y forzar idioma español si está disponible
    ps_command = (
        f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$voice = $synth.GetInstalledVoices() | Where-Object {{ $_.VoiceInfo.Culture.TwoLetterISOLanguageName -eq 'es' }} | Select-Object -First 1; "
        f"if ($voice) {{ $synth.SelectVoice($voice.VoiceInfo.Name) }}; "
        f"$synth.Rate = 1; " # Velocidad elegante
        f"$synth.Speak('{texto_escapado}')"
    )
    
    try:
        # Ejecutar el binario de Windows de manera silenciosa desde WSL
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", ps_command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"⚠️ [Fallo de puente de audio Windows]: {e}")