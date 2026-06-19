# 🦇 Alfred: Tactical Asymmetric AI Assistant Station

An advanced, ultra-low-latency local virtual assistant station inspired by a tactical batcave interface. **Alfred** operates under a high-performance **Asymmetric Computing Architecture**, shifting visual and text workloads dynamically across specialized cloud pipelines via Groq API, while maintaining ultra-fast local biometric hardware control.

---

## ⚡ Asymmetric System Architecture

The core station intelligence is decoupled into two parallel pipelines to maximize fluid conversational response while executing heavy Vision-Language tasks:

1.  **🚀 High-Speed Text Pipeline (`llama-3.1-8b-instant`):** Handles all standard ambient voice commands, laboratory note-taking, and conversational responses in milliseconds.
2.  **👁️ Multimodal Native Vision Pipeline (`meta-llama/llama-4-scout-17b-16e-instruct`):** Triggered exclusively when the intelligent intent-router detects camera commands. It processes live high-definition frames compressed in memory alongside the user's voice prompt in a single cloud transaction.

---

## 🛠️ Key Technical Features

* **🔒 Local Biometric Gatekeeping:** Real-time local facial recognition (`modelo_rostro.xml` via OpenCV LBPH) triggers instantaneous hardware authorization and parallel voice confirmation before exposing any cloud endpoints.
* **📡 Intelligent Dynamic Intent Router:** Uses advanced semantic keyword filtering to route data pipelines. It intercepts clothing, environment, and physical queries, automatically switching between dedicated optics:
    * **Laptop Face Camera (Index 0):** Used for initial biometrics, facial expressions, and clothing/appearance assessment.
    * **GoPro Desk Camera (Index 6):** Enforced via Windows DirectShow for precise physical inspection of tools, electronics, or lab bench components.
* **🏎️ Global Hardware Pre-Warming & Express Flushing:** To completely eradicate device initialization lag on Windows, camera capture objects are persistent globally. Fast-flushing loops clean the hardware buffers continuously, ensuring Groq receives an instantaneous frame at **480p (640x480, buffer=1)**.
* **🎙️ Uncut Premium Audio Pipeline:** Built using `edge-tts` (`es-US-AlonsoNeural`) bound natively to `pygame.mixer` to bypass Windows file-locking bottlenecks. Speech recognition is tuned with an expanded `phrase_time_limit=15` and a relaxed `pause_threshold=1.2` to allow complex instructions without premature truncation.
* **🧵 Non-Blocking Threads:** Latency from heavy cloud API requests is masked by throwing parallel background threads that handle tactical voice status alerts (*"Un momento, Señor..."*) while the main thread pipes data.

---

## 🚀 Future Roadmap

- [ ] **HUD Tactical Overlay Interface:** Project live video streams onto an OpenCV cyberpunk window, drawing scanning laser geometries, facial tracking matrices, and audio-reactive waveforms.
- [ ] **Persistent Workspace Vector Memory (RAG):** Integrate a localized `ChromaDB` layer to replace raw text notes, granting Alfred historical memory retrieval capabilities.
- [ ] **Subprocess Lab Automation:** Bind voice commands to native Windows scripts via `subprocess` to launch developer environments, active terminals, and hardware diagnostic readouts.

---

## ⚙️ Tech Stack

* **Core Environment:** Python 3.10+ (Windows venv)
* **Inference Cloud:** Groq LPU API (Llama 3.1 8B & Llama 4 Scout 17B Multimodal)
* **Computer Vision:** OpenCV (Haar Cascades, Multi-Optic Capture, Native Memory Encoding)
* **Audio Pipeline:** SpeechRecognition, `edge-tts` (+48% Speed Acceleration), `pygame.mixer`
