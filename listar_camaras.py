import cv2

print("📡 Buscando dispositivos de video activos en Windows...")
for i in range(8):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # Forzar DirectShow en Windows
    if cap.isOpened():
        print(f"✅ [DISPOSITIVO DETECTADO]: Índice {i} está activo.")
        cap.release()
    else:
        print(f"❌ Índice {i}: Fuera de rango / Inactivo.")