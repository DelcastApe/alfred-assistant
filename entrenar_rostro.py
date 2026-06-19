import cv2
import os
import time
import numpy as np

print("🤖 [Sistemas]: Iniciando módulo de configuración facial...")

# Asegurar que existan los directorios
if not os.path.exists('data_rostro'):
    os.makedirs('data_rostro')

cap = cv2.VideoCapture(0)
# Usamos el detector de rostros clásico de Haar de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("📸 Estabilizando cámara... Mire fijamente al lente.")
time.sleep(2)

count = 0
while count < 30:
    ret, frame = cap.read()
    if not ret:
        continue
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        count += 1
        rostro_recortado = gray[y:y+h, x:x+w]
        rostro_recortado = cv2.resize(rostro_recortado, (150, 150))
        # Guardar muestra
        cv2.imwrite(f'data_rostro/user_{count}.jpg', rostro_recortado)
        print(f"Captured sample {count}/30")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    cv2.imshow('Registrando Rostro de Mr. Gerardo', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if count >= 30:
    print("\n🧠 Entrenando modelo matemático LBPH...")
    # Creamos el reconocedor LBPH nativo
    reconocedor = cv2.face.LBPHFaceRecognizer_create()
    
    imagenes = []
    labels = []
    
    for archivo in os.listdir('data_rostro'):
        if archivo.endswith('.jpg'):
            img_path = os.path.join('data_rostro', archivo)
            imagen = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            imagenes.append(imagen)
            labels.append(1) # ID 1 para Mr. Gerardo
            
    reconocedor.train(imagenes, np.array(labels))
    reconocedor.write('modelo_rostro.xml')
    print("🔒 [ÉXITO]: Modelo 'modelo_rostro.xml' guardado. ¡Identidad blindada!")
else:
    print("🚨 Error: No se capturaron suficientes muestras.")