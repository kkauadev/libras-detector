# ------------------------------------------ #
#              Libras Detector               #
# ------------------------------------------ #
#               Programadores:               #
#         Fernando Martins Ferreira          #
#           Kaua Alves Nascimento            #
#             Steffany Medeiros              #
# ------------------------------------------ #
#        Samsung Innovation Campus           #
# ------------------------------------------ #
import mediapipe as mp
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from itertools import chain
import pipe
import threading
import openai
import re
import pyttsx3

mp_draw_landmarks = mp.solutions.drawing_utils.draw_landmarks
hand_connections = mp.solutions.hands.HAND_CONNECTIONS
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands()

openai.api_key = #sua api do chatgpt aqui
fala = pyttsx3.init()

def formatar_com_gpt3(lista_palavras, resultado_label):
    print("Chat GPT em execução!")
    print(lista_palavras)
    if not lista_palavras:
        resultado_label.config(text="A lista de palavras está vazia.")
        return
    
    #prompt = "Formate a lista em uma pequena frase correspondente de acordo com a lingua portuguesa utilizando apenas as palavras fornecidas na lista e coloque a frase entre aspas: " + ", ".join(lista_palavras)
    prompt = "Formate a seguinte lista em uma frase, não acrescente palavras não existentes, coloque entre aspas: " + ", ".join(lista_palavras)
    
    resposta_gpt3 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

    texto_completo = resposta_gpt3.choices[0].text.strip()
    print(texto_completo)

    texto_entre_aspas = re.findall(r'"([^"]*)"', texto_completo)
    texto_formatado = ', '.join(texto_entre_aspas) 

    resultado_label.config(text=texto_formatado)
    fala.say(texto_formatado)

    fala.runAndWait()
    
    resultado_label.config(text="")
    
def formatar_sem_api(lista_palavras, resultado_label):
    lista_texto = " ".join(lista_palavras)
    resultado_label.config(text=lista_texto)
    print(lista_texto)
    fala.say(lista_texto)

    fala.runAndWait()
    resultado_label.config(text="")

def open_camera(frame: tk.Frame, button: tk.Button):
    cap = cv2.VideoCapture(0)
    button.place_forget()
    
    def show_frame():
        ret, frame = cap.read()
        if ret:
            # Process hands on frame
            hands_results = hands_detector.process(frame)
            
            # draw hands landmarks
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    mp_draw_landmarks(frame, hand_landmarks, hand_connections)
                    
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            panel.imgtk = img
            panel.config(image=img)
            panel.after(10, show_frame) 
        
    def process_frames():
        lista_atual = []
        tempo_processado = 0
        
        while True:
            ret, new_frame = cap.read()
            if ret:
                palavra = pipe.process_and_verify(new_frame) 
                tempo_processado += 1
                if palavra:
                    print(palavra)
                if tempo_processado == 0:
                    print("tempo ok")
                
                if palavra and palavra not in lista_atual:
                    lista_atual.append(palavra)

                if len(lista_atual) >= 1 and tempo_processado > 50:
                    print("lista e tempo ok")
                    tempo_processado = 0
                    if len(lista_atual) > 2:
                        print("COM CHAT")
                        print(lista_atual)
                        formatar_com_gpt3(lista_atual, resultado_label)
                        lista_atual = []
                    else:
                        print("SEM CHAT")
                        formatar_sem_api(lista_atual, resultado_label)
                        lista_atual = []

                    
    panel = tk.Label(frame)
    panel.place(relx=0.5, rely=0.48, anchor="center")
        
    resultado_label = tk.Label(frame, text="", bg="#111", fg="white", padx=8, pady=2, font=("SamsungOne-400", 12))
    resultado_label.place(relx=0.5, rely=0.8, anchor="center")   
    
    process_thread = threading.Thread(target=process_frames)
    process_thread.daemon = True 
    process_thread.start()
    
    show_frame()  
    frame.mainloop()

def create_screen(root):
    frame = tk.Frame(root, bg="#1428A0")

    image = Image.open("img/person-video.png")  
    image = image.resize((160, 120))
    photo = ImageTk.PhotoImage(image)
    
    label_image = tk.Label(frame, bg="#1428A0", image=photo)
    label_image.image = photo
    label_image.place(relx=0.5, rely=0.33, anchor="center")
    
    label_message = tk.Label(frame, text="Posicione-se no centro da câmera\npara que seja possível a melhor captação do sinal", bg="#1428A0", fg="white", width=50, font=("Samsung Sharp Sans Bold", 18))
    label_message.place(relx=0.5,rely=0.4855,anchor="center")
    
    label_message = tk.Label(frame, text="Fique em um lugar iluminado para melhorar a visibilidade das mãos", bg="#1428A0", fg="#AAA", font=("SamsungOne-400", 12))
    label_message.place(relx=0.5,rely=0.55,anchor="center")
    
    botao_iniciar = tk.Button(frame, text="Ok, Vamos começar!", bg="white", fg="#1428A0", padx=8, pady=2, borderwidth=0, cursor="hand2", font=("Samsung Sharp Sans Bold", 12),command=lambda: open_camera(frame, botao_iniciar))
    botao_iniciar.place(relx=0.5, rely=0.61, anchor="center")

    image = Image.open("img/samsung-white.png")
    image = image.resize((200, 50))
    photo = ImageTk.PhotoImage(image)
  
    label_image = tk.Label(frame, width=200, height=50, bg="#1428A0", image=photo)
    label_image.image = photo
    label_image.place(relx=0.5, rely=0.92, anchor="center")

    return frame
