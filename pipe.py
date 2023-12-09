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
import os
import csv

mp_hands = mp.solutions.hands
hands_detector  = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
hands_connections = mp.solutions.hands.HAND_CONNECTIONS

# Variáveis globais
coordenadas_mao_em_tempo_real = []
etapas_completas = []
lista_palavras = []
tempo_ultima_palavra = 0
pasta_anterior = ""
tempo_ultimo_sinal = 0

MINIMO_CORRESPONDENCIA_PERCENTUAL_UNICO = 0.75 # 0.85
MINIMO_CORRESPONDENCIA_PERCENTUAL_MULTIPLAS = 0.70 # 0.76

PASTA_PRINCIPAL = './sinais'

def process_frame(frame):
    resultado = hands_detector.process(frame)
    coordenadas_mao_em_tempo_real = []

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            coordenadas_mao = []
            for landmark in hand_landmarks.landmark:
                coordenadas_mao.extend([landmark.x, landmark.y])
            coordenadas_mao_em_tempo_real = coordenadas_mao
    
    return coordenadas_mao_em_tempo_real

def verificar_correspondencia(coordenadas_mao_em_tempo_real):
    global pasta_anterior
    global lista_palavras

    for pasta_sinal in os.listdir(PASTA_PRINCIPAL):
        if os.path.isdir(os.path.join(PASTA_PRINCIPAL, pasta_sinal)):
            for arquivo_csv in os.listdir(os.path.join(PASTA_PRINCIPAL, pasta_sinal)):
                if arquivo_csv.endswith(".csv"):
                    nome_pasta = pasta_sinal
                    caminho_csv = os.path.join(PASTA_PRINCIPAL, pasta_sinal, arquivo_csv)

                    # Lê os arquivos .csv
                    with open(caminho_csv, newline='') as csvfile:
                        csv_lido = csv.reader(csvfile)
                        next(csv_lido)
                        correspondencia_encontrada = True
                        etapas_completas = []
                        numero_de_etapas = sum(1 for row in csv_lido)
                        csvfile.seek(0)
                        next(csv_lido)
                        for row in csv_lido:
                             # Compare coordenadas de mão em tempo real com o arquivo CSV
                            for ponto_idx in range(0, 20):
                                x_csv = float(row[ponto_idx * 2 + 2])
                                y_csv = float(row[ponto_idx * 2 + 3])
                                x_real = coordenadas_mao_em_tempo_real[ponto_idx * 2]
                                y_real = coordenadas_mao_em_tempo_real[ponto_idx * 2 + 1]

                                # Calcula distâncias entre pontos
                                distancia_entre_pontos = ((x_csv - x_real) ** 2 + (y_csv - y_real) ** 2) ** 0.5

                                distancia_maxima_possivel = 1.0
                                # Defina os critérios com base no número de etapas
                                if numero_de_etapas == 1:
                                    limite_correspondencia_percentual = MINIMO_CORRESPONDENCIA_PERCENTUAL_UNICO
                                else:  # Outro critério para mais de 1 etapa
                                    limite_correspondencia_percentual = MINIMO_CORRESPONDENCIA_PERCENTUAL_MULTIPLAS

                                # Calcular a correspondência percentual
                                correspondencia_percentual = 1 - (distancia_entre_pontos / distancia_maxima_possivel)
                                if isinstance(correspondencia_percentual, complex):
                                    correspondencia_percentual = correspondencia_percentual.real
                                if correspondencia_percentual < limite_correspondencia_percentual:
                                    correspondencia_encontrada = False
                                    break
                            etapas_completas.append(correspondencia_encontrada)
                                
                            if all(etapas_completas) and nome_pasta != pasta_anterior:
                                pasta_anterior = nome_pasta
                                return nome_pasta


    return None

def process_and_verify(frame):

    coordenadas_mao = process_frame(frame)
    if coordenadas_mao:
        palavra = verificar_correspondencia(coordenadas_mao)
        return palavra if palavra else None
    return None
#def process_and_verify(frame):
#    global lista_palavras
#
#    coordenadas_mao = process_frame(frame)
#    if coordenadas_mao:
#        lista_palavras = verificar_correspondencia(coordenadas_mao)
#        if len(lista_palavras) >= 3:
#            lista_atual = lista_palavras.copy()
#            lista_palavras.clear()
#            return True, list(set(lista_atual))
#    return True, []


