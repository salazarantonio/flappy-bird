import pygame
import sys
from config import *
import logica

def main():
    pygame.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Zelda Flappy")
    relogio = pygame. time.Clock()

    
    link_original = pygame.image.load("assets/link.png").convert_alpha()
    img_link = pygame.transform.scale(link_original, (50, 50))


    jogador = logica.criar_jogador(50, altura_tela // 2)
    fundo_x = 0
    largura_fundo = 3000
    lista_tubos = []
    temporizador_tubos = 0
    pontuacao = 0

    pygame.font.init()
    pygame.mixer.init()



    try:
        pygame.mixer.music.load("assets/sons/musica_fundo.mp3")
        pygame.mixer.music.set_volume(0.4) 
        pygame.mixer.music.play(-1) 
    except:
        print("Trilha sonora não encontrada.")

    try:
        som_ponto = pygame.mixer.Sound("assets/sons/ponto.wav")
        som_hit = pygame.mixer.Sound("assets/sons/hit.wav")
    except:
        print("Efeitos sonoros não encontrados.")
        som_ponto = som_hit = None



    try:
        fonte_pontuacao = pygame.font.Font("assets/fonte_zelda.ttf", 40)
        fonte_menu = pygame.font.Font("assets/fonte_zelda.ttf", 25)
        fonte_titulo = pygame.font.Font("assets/fonte_zelda.ttf", 60) # Uma fonte maior pro título
    except:
        print("Fonte customizada não encontrada, usando a padrão.")
        fonte_pontuacao = pygame.font.SysFont("Arial", 40, bold=True)
        fonte_menu = pygame.font.SysFont("Arial", 25, bold=True)
        fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
    

    try:
        fundo_original = pygame.image.load("assets/novo_fundo.png").convert()
        img_fundo = pygame.transform.scale(fundo_original, (3000, altura_tela))
    except:
        print("Novo fundo não encontrado, usando o antigo/padrão.")
        tela.fill((0, 0, 200)) 
        img_fundo = pygame.Surface((3000, altura_tela))


    try:
        cano_original = pygame.image.load("assets/cano_zelda.png").convert_alpha()
        img_tubo_baixo = pygame.transform.scale(cano_original, (largura_tubo, altura_tela))
        img_tubo_cima = pygame.transform.flip(img_tubo_baixo, False, True)
        sprites_tubo = {"cima": img_tubo_cima, "baixo": img_tubo_baixo}
    except:
        print("Sprite do cano não encontrado, usando retângulos verdes.")
        img_tubo = None




    largura_botao = 200
    altura_botao = 50
    meio_x = largura_tela // 2 - largura_botao // 2


    botao_reiniciar = pygame.Rect(meio_x, 350, largura_botao, altura_botao)
    botao_voltar_menu = pygame.Rect(meio_x, 430, largura_botao, altura_botao)
    botao_jogar = pygame.Rect(meio_x, 200, largura_botao, altura_botao)
    botao_creditos = pygame.Rect(meio_x, 280, largura_botao, altura_botao)
    botao_sair = pygame.Rect(meio_x, 360, largura_botao, altura_botao)
    botao_voltar = pygame.Rect(meio_x, 450, largura_botao, altura_botao)
    
    overlay = pygame.Surface((largura_tela, altura_tela)) 
    overlay.set_alpha(150) 
    overlay.fill((0, 0, 0)) 
    

    estado_jogo = "MENU"
    
    rodando = True



    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                
                if estado_jogo == "MENU":
                    if botao_jogar.collidepoint(pos_mouse):
                        jogador = logica.criar_jogador(50, altura_tela // 2)
                        fundo_x = 0
                        lista_tubos.clear()
                        pontuacao = 0
                        temporizador_tubos = 0
                        estado_jogo = "JOGANDO"

                    elif botao_creditos.collidepoint(pos_mouse):
                        estado_jogo = "CREDITOS"

                    elif botao_sair.collidepoint(pos_mouse):
                        rodando = False
                
                elif estado_jogo == "CREDITOS":

                    if botao_voltar.collidepoint(pos_mouse):
                        estado_jogo = "MENU"

                if estado_jogo == "GAME_OVER":

                    if botao_reiniciar.collidepoint(pos_mouse):
                        jogador = logica.criar_jogador(50, altura_tela // 2)
                        fundo_x = 0
                        lista_tubos.clear()
                        pontuacao = 0
                        temporizador_tubos = 0
                        estado_jogo = "JOGANDO"
                    
                    elif botao_voltar_menu.collidepoint(pos_mouse):
                        estado_jogo = "MENU"


            if (evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP)) or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                if estado_jogo == "JOGANDO":
                    logica.pular(jogador)

            if estado_jogo == "GAME_OVER" and (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE):  
                jogador = logica.criar_jogador(50, altura_tela // 2)
                fundo_x = 0
                lista_tubos.clear()
                pontuacao = 0
                temporizador_tubos = 0
                estado_jogo = "JOGANDO"


        if estado_jogo == "JOGANDO":
            logica.aplicar_gravidade(jogador)
            fundo_x = logica.mover_fundo(fundo_x, largura_fundo, velocidade_fundo)
            temporizador_tubos += 1

            if temporizador_tubos > 90:
                novo_tubo = logica.criar_tubo(largura_tela, altura_tela)
                lista_tubos.append(novo_tubo)
                temporizador_tubos = 0

            lista_tubos = logica.mover_tubos(lista_tubos, velocidade_tubo)

            nova_pontuacao = logica.atualizar_pontuacao(jogador, lista_tubos, pontuacao)

            if nova_pontuacao > pontuacao:
                pontuacao = nova_pontuacao
                if som_ponto: som_ponto.play()

            bateu_borda = logica.checar_colisao_bordas(jogador, altura_tela)
            bateu_tubo = logica.checar_colisao_tubos(jogador, lista_tubos, altura_tela)


            if bateu_borda or bateu_tubo:
                if som_hit: som_hit.play()
                estado_jogo = "GAME_OVER"


        tela.blit(img_fundo, (fundo_x, 0))
        tela.blit(img_fundo, (fundo_x + largura_fundo, 0))

        if estado_jogo == "JOGANDO" or estado_jogo == "GAME_OVER":
            if sprites_tubo:
                logica.desenhar_tubos(tela, lista_tubos, altura_tela, sprites_tubo )
            else:
                logica.desenhar_tubos_retangulos(tela, lista_tubos, altura_tela, verde)
            
            logica.desenhar_jogador(tela, img_link, jogador)
        

        if estado_jogo != "JOGANDO":
            tela.blit(overlay, (0, 0))


        if estado_jogo == "JOGANDO":
            texto_pontos = fonte_pontuacao.render(str(pontuacao), True, branco)
            tela.blit(texto_pontos, (largura_tela // 2 - 10, 20))
        
        elif estado_jogo == "MENU":
            titulo_sombra = fonte_titulo.render("ZELDA FLAPPY", True, (0, 0, 0))
            titulo = fonte_titulo.render("ZELDA FLAPPY", True, (255, 215, 0))
            
            tela.blit(titulo_sombra, (largura_tela // 2 - titulo.get_width() // 2 + 3, 70 + 3))
            tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 70))


            cor_botao = (70, 130, 180)
            cor_borda = (34, 139, 34)

            botoes_menu = [
                (botao_jogar , "JOGAR"),
                (botao_creditos, "CREDITOS"),
                (botao_sair, "SAIR")
            ]
            

            for retangulo, texto in botoes_menu:
                pygame.draw.rect(tela, cor_borda, retangulo, border_radius=10)
                
                pygame.draw.rect(tela, cor_botao, retangulo.inflate(-6, -6), border_radius=8)
                
                txt_render = fonte_menu.render(texto, True, branco)
                tela.blit(txt_render, (retangulo.centerx - txt_render.get_width() // 2, retangulo.centery - txt_render.get_height() // 2))
            
        elif estado_jogo == "CREDITOS":
            titulo_cred = fonte_pontuacao.render("CREDITOS", True, branco)
            txt_nome = fonte_menu.render("Desenvolvido por: Joao Pedro, Ricardo e Salazar", True, branco)
            txt_inst = fonte_menu.render("Projeto - UFPB", True, branco)

            tela.blit(titulo_cred, (largura_tela // 2 - titulo_cred.get_width() // 2, 80))
            tela.blit(txt_nome, (largura_tela // 2 - txt_nome.get_width() // 2, 200))
            tela.blit(txt_inst, (largura_tela // 2 - txt_inst.get_width() // 2, 250))

            pygame.draw.rect(tela, (180, 50, 50), botao_voltar, border_radius=10)
            txt_voltar = fonte_menu.render("Voltar", True, branco)
            tela.blit(txt_voltar, (botao_voltar.centerx - txt_voltar.get_width() // 2 , botao_voltar.centery - txt_voltar.get_height() // 2))

            
        elif estado_jogo == "GAME_OVER":
            txt_fim_sombra = fonte_titulo.render("GAME OVER", True, (0, 0, 0))
            txt_fim = fonte_titulo.render("GAME OVER", True, (255, 50, 50)) 
            
            tela.blit(txt_fim_sombra, (largura_tela // 2 - txt_fim.get_width() // 2 + 3, 150 + 3))
            tela.blit(txt_fim, (largura_tela // 2 - txt_fim.get_width() // 2, 150))

            txt_pontos = fonte_menu.render(f"PONTOS FINAIS: {pontuacao}", True, branco)
            tela.blit(txt_pontos, (largura_tela // 2 - txt_pontos.get_width() // 2, 260))

            cor_botao = (70, 130, 180)
            cor_borda = branco
            
            for btn, texto in [(botao_reiniciar, "REINICIAR"), (botao_voltar_menu, "MENU")]:
                pygame.draw.rect(tela, cor_borda, btn, border_radius=10)
                pygame.draw.rect(tela, cor_botao, btn.inflate(-6, -6), border_radius=8)
                
                txt_btn = fonte_menu.render(texto, True, branco)
                tela.blit(txt_btn, (btn.centerx - txt_btn.get_width() // 2, btn.centery - txt_btn.get_height() // 2))

            txt_dica = fonte_menu.render("Ou aperte SPACEBAR para tentar de novo", True, (200, 200, 200))
            tela.blit(txt_dica, (largura_tela // 2 - txt_dica.get_width() // 2, 550))
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()