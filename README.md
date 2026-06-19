# 🦇 Alfred: Tactical AI Assistant Station

An advanced, low-latency local virtual assistant inspired by a tactical batcave station. **Alfred** combines real-time biometric verification, localized hardware warm-up, asynchronous dual-camera routing, and high-speed audio telemetry integrated with Language and Vision Models (LLM/VLM) via Groq API.

---

## 🛠️ System Architecture & Key Features

*   **🔒 Immediate Biometric Feedback:** Local facial recognition (`modelo_rostro.xml`) triggers instant audio authorization prior to calling the cloud LLM pipeline, removing perceived dead-silence.
*   **📷 Asynchronous Smart Camera Router:** Features an intent-discriminator that bypasses the VLM for standard audio queries (responding in milliseconds). If visual analysis is requested, it dynamically routes to the appropriate hardware:
    *   **Laptop Camera (Index 0):** Biometrics and user visual assessment.
    *   **GoPro (Index 6):** Desk/bench physical tool inspection.
*   **🏎️ Hardware Pre-warming & Multi-Threading:** To eliminate Windows device initialization lag, video capture streams remain globally persistent at an optimized **480p (480x360, buffer=1)**. Heavy Vision API network requests mask latency using parallel background threads that voice status updates ("Permítame activar los sensores...").
*   **🎙️ Optimized High-Speed Audio:** Utilizing `edge-tts` (`es-US-AlonsoNeural` voice model) bound natively to `pygame.mixer` to bypass Windows file-locking. Configured with a fast, corporate-toned speech rate acceleration of **+48%** and tuned microphone `pause_threshold` at **0.7**.
*   **🧠 Personality & Identity Filtering:** Hardcoded strict behavioral constraints preventing identity-read stuttering (translating shortcuts to literal pronunciations like *"Mister Gerardo"* or *"Señor"*) and filtering formatting noise (parentheses, asterisks).

---

## 🚀 Future Roadmap

- [ ] **Localized Long-Term Memory (RAG):** Migrate from standard text-logging to a vector database layer (ChromaDB/SQLite) for persistent workspace memory.
- [ ] **Smart Lab Automation:** Script hooks to bind peripheral events to voice actions (e.g., triggering developer workspaces, launching local servers, or IDE automation).
- [ ] **Active Perimeter Watch (Security Mode):** Idle state video motion analysis using the GoPro feed to detect unauthorized personnel.
- [ ] **Futuristic HUD GUI:** Graphical terminal overlays utilizing PyQt/OpenCV displaying visual biometric tracking scanners, real-time waveform telemetries, and status matrices.

---

## ⚙️ Tech Stack

*   **Core:** Python 3.10+ (Virtual Environment)
*   **AI Orchestration:** Groq API (LLM & Vision-Language Models)
*   **Computer Vision:** OpenCV (Haar Cascades, Multi-Input Capture)
*   **Audio Pipeline:** SpeechRecognition, `edge-tts`, `pygame.mixer`
