import pygame
import random
from config import gravidade, forca_pulo, velocidade_tubo, largura_tubo, espaco_tubo

def criar_jogador(x, y):
    return {
        "x" : x,
        "y" : y,
        "largura" : 50,
        "altura" : 50,
        "velocidade" : 0
    }

def aplicar_gravidade(jogador):
    jogador["velocidade"] += gravidade
    jogador["y"] += jogador["velocidade"]


def pular(jogador):
    jogador["velocidade"] = forca_pulo


def checar_colisao_bordas(jogador, altura_tela):
    if jogador["y"] >= altura_tela - jogador["altura"] or jogador["y"] <= 0:
        return True
    return False


def desenhar_jogador(tela, imagem, jogador):
    angulo = jogador["velocidade"] * -3
    
    angulo = max(-90, min(angulo, 30))
    
    imagem_rotacionada = pygame.transform.rotate(imagem, angulo)
    
    centro_x = jogador["x"] + jogador["largura"] // 2
    centro_y = jogador["y"] + jogador["altura"] // 2
    retangulo_imagem = imagem_rotacionada.get_rect(center=(centro_x, centro_y))
    
    tela.blit(imagem_rotacionada, retangulo_imagem.topleft)


def mover_fundo(x_atual, largura_imagem, velocidade):
    
    x_atual -= velocidade

    if x_atual <= -largura_imagem:
        x_atual = 0
    
    return x_atual


def criar_tubo(x, altura_tela):
    altura_minima = 50
    altura_maxima = altura_tela - espaco_tubo - 50

    pos_y_abertura = random.randint(altura_minima, altura_maxima)

    return {
        "x" : x,
        "y_abertura" : pos_y_abertura,
        "passou" : False 
    }


def mover_tubos(tubos, velocidade):
    for tubo in tubos:
        tubo["x"] -= velocidade
    
    return [tubo for tubo in tubos if tubo["x"] > - largura_tubo]


def desenhar_tubos(tela, tubos, altura_tela, sprites_tubo):
    img_cima = sprites_tubo["cima"]
    img_baixo = sprites_tubo["baixo"]

    altura_img = img_cima.get_height()

    for tubo in tubos:
        y_cima = tubo["y_abertura"] - altura_img
        tela.blit(img_cima, (tubo["x"], y_cima))

        y_base = tubo["y_abertura"] + espaco_tubo
        tela.blit(img_baixo, (tubo["x"], y_base))

def desenhar_tubos_retangulos(tela, tubos, altura_tela, cor):
    for tubo in tubos:
        rect_cima = pygame.Rect(tubo["x"], 0, largura_tubo, tubo["y_abertura"])
        pygame.draw.rect(tela, cor, rect_cima)

        y_base = tubo["y_abertura"] + espaco_tubo
        altura_base = altura_tela - y_base
        rect_baixo = pygame.Rect(tubo["x"], y_base, largura_tubo, altura_base)
        pygame.draw.rect(tela, cor, rect_baixo)

def checar_colisao_tubos(jogador, tubos, altura_tela):

    rect_jogador = pygame.Rect(jogador["x"], jogador["y"], jogador["largura"], jogador["altura"])

    for tubo in tubos:
        rect_cima = pygame.Rect(tubo["x"], 0, largura_tubo, tubo["y_abertura"])
        y_base = tubo["y_abertura"] + espaco_tubo
        altura_base = altura_tela - y_base
        rect_baixo = pygame.Rect(tubo["x"], y_base, largura_tubo, altura_base)

        if rect_jogador.colliderect(rect_cima) or rect_jogador.colliderect(rect_baixo):
            return True
        
    return False
    

def atualizar_pontuacao(jogador, tubos, pontuaca_atual):

    for tubo in tubos:
        if tubo["x"] + largura_tubo < jogador["x"] and not tubo["passou"]:
            tubo["passou"] = True 
            return pontuaca_atual + 1
        
    return pontuaca_atual

