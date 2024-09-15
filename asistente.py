import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext

# Configura la clave de API
openai.api_key = 'Enter your Api Key'

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Función para convertir texto a voz
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Función para capturar entrada de audio y convertirla a texto
def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No pude entender el audio."
        except sr.RequestError as e:
            return f"Error al conectar con el servicio de reconocimiento de voz; {e}"

# Función para hacer una consulta al API de OpenAI
def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"

# Función para manejar el botón de enviar pregunta
def on_ask_button_click():
    question = entry.get()
    if question.lower() == "salir":
        root.quit()
    else:
        # Haz la consulta a OpenAI
        response = ask_openai(question)
        output_text.configure(state='normal')
        output_text.insert(tk.END, f"Tú: {question}\n")
        output_text.insert(tk.END, f"OpenAI: {response}\n\n")
        output_text.configure(state='disabled') 
        speak_text(response)
        entry.delete(0, tk.END)

# Función para manejar el botón de escuchar pregunta
def on_listen_button_click():
    question = get_audio_input()
    if question.lower() == "salir":
        root.quit()
    else:
        # Haz la consulta a OpenAI
        response = ask_openai(question)
        output_text.configure(state='normal') 
        output_text.insert(tk.END, f"Tú: {question}\n")
        output_text.insert(tk.END, f"OpenAI: {response}\n\n")
        output_text.configure(state='disabled') 
        speak_text(response)

# Función para eliminar la conversación
def on_clear_button_click():
    output_text.configure(state='normal')
    output_text.delete(1.0, tk.END) 
    output_text.configure(state='disabled') 

# Configura la interfaz gráfica
root = tk.Tk()
root.title("Asistente de Voz con OpenAI")

# Crea los widgets
entry = tk.Entry(root, width=50)
ask_button = tk.Button(root, text="Preguntar", command=on_ask_button_click)
listen_button = tk.Button(root, text="Escuchar", command=on_listen_button_click)
clear_button = tk.Button(root, text="Eliminar Conversación", command=on_clear_button_click)
output_text = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')

# Organiza los widgets en la ventana
entry.pack(pady=10)
ask_button.pack(pady=5)
listen_button.pack(pady=5)
clear_button.pack(pady=5)
output_text.pack(pady=10)

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()
