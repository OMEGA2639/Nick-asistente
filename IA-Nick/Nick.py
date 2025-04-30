import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser

# Inicializar motor de voz
voz = pyttsx3.init()
voz.setProperty('rate', 170)
voz.setProperty('volume', 1.0)

# Cambiar a voz masculina
def cambiar_voz_masculina():
    for v in voz.getProperty('voices'):
        if "David" in v.name or "Mark" in v.name or "male" in v.name.lower():
            voz.setProperty('voice', v.id)
            break

cambiar_voz_masculina()

# Función para hablar
def hablar(texto):
    print("NICK:", texto)
    voz.say(texto)
    voz.runAndWait()

# Función para escuchar
def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Ajustar el umbral de ruido para que Nick ignore ruidos de fondo
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Escuchando... (Solo escuchará cuando hables)")

        try:
            audio = recognizer.listen(source, timeout=5)  # Timeout para no quedarse esperando por siempre
            comando = recognizer.recognize_google(audio, language="es-ES")
            print("Tú:", comando)
            return comando.lower()
        except sr.UnknownValueError:
            return ""  # No dice nada si no entendió lo que dijiste
        except sr.RequestError:
            hablar("Hubo un problema de conexión.")
            return ""
        except sr.WaitTimeoutError:
            return ""  # Si no escuchó nada en el tiempo dado

# Guardar recordatorio
def guardar_recordatorio(texto):
    with open("recordatorios.txt", "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
    hablar("He recordado eso.")

# Leer recordatorios
def leer_recordatorios():
    if os.path.exists("recordatorios.txt"):
        with open("recordatorios.txt", "r", encoding="utf-8") as archivo:
            recordatorios = archivo.readlines()
        if recordatorios:
            hablar("Esto es lo que recuerdo:")
            for r in recordatorios:
                hablar(r.strip())
        else:
            hablar("No tengo nada guardado todavía.")
    else:
        hablar("Aún no tengo nada que recordar.")

# Buscar en internet
def buscar_en_internet(consulta):
    if not consulta or len(consulta.strip()) == 0:
        hablar("¿Qué deseas que busque?")
        nueva_consulta = escuchar()
        if nueva_consulta:
            buscar_en_internet(nueva_consulta)
        else:
            hablar("No entendí lo que quieres que busque.")
        return

    url = f"https://www.bing.com/search?q={consulta.replace(' ', '+')}"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        hablar(f"Buscando {consulta} en Microsoft Edge.")
        os.system(f'"{edge_path}" "{url}"')
    else:
        hablar("No encontré Microsoft Edge instalado.")

# Procesar comandos
def procesar_comando(comando):
    # Recordar algo
    if comando.startswith("recuérdame que") or comando.startswith("recuerda que") or comando.startswith("apunta que"):
        recordatorio = comando.replace("recuérdame que", "").replace("recuerda que", "").replace("apunta que", "").strip()
        guardar_recordatorio(recordatorio)

    # Leer lo recordado
    elif "qué me has recordado" in comando or "qué recuerdas" in comando or "qué recordaste" in comando or "qué sabes de mí" in comando:
        leer_recordatorios()

    elif "hora" in comando:
        ahora = datetime.datetime.now().strftime("%H:%M")
        hablar(f"Son las {ahora}.")

    elif "navegador" in comando and ("abre" in comando or "abrir" in comando):
        hablar("Abriendo Microsoft Edge.")
        os.system("start msedge")

    elif "busca" in comando or "buscar" in comando:
        palabras = comando.split()
        try:
            indice = palabras.index("busca") if "busca" in palabras else palabras.index("buscar")
            consulta = " ".join(palabras[indice + 1:])
            buscar_en_internet(consulta)
        except:
            hablar("No entendí bien qué quieres que busque.")

    elif "cómo te llamas" in comando or "cuál es tu nombre" in comando:
        hablar("Mi nombre es Nick, tu asistente personal.")

    elif "cómo me llamo" in comando or "cuál es mi nombre" in comando:
        hablar("Tú te llamas Anderson.")

    elif any(p in comando for p in ["salir", "adiós", "me voy", "nos vemos"]):
        hablar("Hasta luego, Anderson.")
        exit()

    elif any(p in comando for p in ["detente", "parar", "ya basta", "silencio", "detén la conversación"]):
        hablar("Conversación detenida. Hasta luego.")
        exit()

    else:
        hablar("No reconozco ese comando todavía.")

# INICIO DEL ASISTENTE
hablar("Hola Anderson. Soy Nick, tu asistente personal. ¿Qué quieres que recuerde o haga hoy?")
while True:
    comando = escuchar()
    if comando:
        procesar_comando(comando)
