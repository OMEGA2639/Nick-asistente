import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import requests
import datetime

# Inicializa la voz
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0')
engine.setProperty('rate', 165)

nombre_asistente = "Nick"
usuario = "Anderson"

# Memoria para recordatorios
recordatorios = []

# URL de actualización automática
ACTUALIZACION_URL = "https://raw.githubusercontent.com/OMEGA2639/Nick-asistente/main/IA-Nick/Nick.py"

def hablar(texto):
    print(f"{nombre_asistente}: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language="es-ES").lower()
        print(f"Tú: {comando}")
        return comando
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        hablar("Lo siento, hubo un error con el reconocimiento de voz.")
        return ""

def buscar_en_edge(consulta):
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        hablar("No encontré Microsoft Edge en tu computadora.")
        return
    url = f"https://www.bing.com/search?q={consulta.replace(' ', '+')}"
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
    webbrowser.get('edge').open(url)
    hablar(f"Buscando {consulta} en Microsoft Edge")

def descargar_actualizacion():
    try:
        response = requests.get(ACTUALIZACION_URL)
        if response.status_code == 200:
            with open("Nick.py", "wb") as f:
                f.write(response.content)
            hablar("Código actualizado correctamente.")
        else:
            hablar("No se pudo descargar la actualización.")
    except Exception as e:
        hablar("Ocurrió un error al intentar actualizar.")

def procesar_comando(comando):
    if any(palabra in comando for palabra in ["cómo te llamas", "tu nombre"]):
        hablar(f"Me llamo {nombre_asistente}")
    elif "cómo me llamo" in comando:
        hablar(f"Te llamas {usuario}")
    elif "abre el navegador" in comando:
        buscar_en_edge("inicio")
    elif "busca" in comando or "investiga" in comando:
        consulta = comando.replace("busca", "").replace("investiga", "").strip()
        if consulta:
            buscar_en_edge(consulta)
        else:
            hablar("¿Qué deseas que busque?")
    elif any(palabra in comando for palabra in ["detente", "silencio", "para de hablar"]):
        hablar("De acuerdo. Estaré en silencio.")
        return False
    elif "actualiza" in comando or "descarga actualización" in comando:
        descargar_actualizacion()
    elif "recuérdame" in comando:
        recordatorio = comando.split("recuérdame", 1)[-1].strip()
        if recordatorio:
            recordatorios.append(recordatorio)
            hablar(f"He recordado: {recordatorio}")
        else:
            hablar("¿Qué quieres que recuerde?")
    elif "qué me has recordado" in comando:
        if recordatorios:
            hablar("Me pediste que recuerde lo siguiente:")
            for r in recordatorios:
                hablar(r)
        else:
            hablar("Aún no me has pedido que recuerde nada.")
    elif "hora" in comando:
        hora = datetime.datetime.now().strftime("%H:%M")
        hablar(f"Son las {hora}")
    else:
        hablar("No entendí ese comando.")
    return True

# Programa principal
def iniciar_nick():
    hablar(f"Hola {usuario}, soy {nombre_asistente}. ¿En qué puedo ayudarte?")
    activo = True
    while activo:
        comando = escuchar()
        if comando:
            activo = procesar_comando(comando)

if __name__ == "__main__":
    iniciar_nick()


