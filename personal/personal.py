"""
TUTORIAL DE PYGAME: DO 2D AO 3D
================================

Este arquivo pode ser lido como uma apostila e executado como exemplos:

    pip install pygame
    python personal.py --demo 2d
    python personal.py --demo 3d

Pygame e uma biblioteca 2D. O exemplo "3D" abaixo ensina a tecnica de
projecao em perspectiva: pontos (x, y, z) sao convertidos para coordenadas
da tela. Para jogos 3D completos, considere um motor como Ursina, Panda3D
ou Godot; a matematica apresentada aqui continua sendo util.

1. MODELO MENTAL
----------------
Todo jogo costuma repetir este ciclo:

    eventos -> entrada -> atualizacao -> desenho -> limite de FPS

Eventos sao mensagens do sistema (fechar janela, teclado, mouse). A
atualizacao altera o estado do jogo. O desenho apenas mostra esse estado.
Separar essas responsabilidades deixa o projeto mais facil de testar.

2. INSTALACAO E JANELA MINIMA
------------------------------
    import pygame
    pygame.init()
    tela = pygame.display.set_mode((800, 450))
    relogio = pygame.time.Clock()
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
        tela.fill((20, 25, 40))
        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()

As coordenadas comecam no canto superior esquerdo: x cresce para a direita
e y cresce para baixo. "tick(60)" limita a atualizacao a 60 FPS.

3. FORMAS, TEXTO E IMAGENS
---------------------------
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    pygame.draw.circle(tela, cor, (x, y), raio)
    pygame.draw.line(tela, cor, inicio, fim, espessura)
    pygame.draw.polygon(tela, cor, [(x1, y1), (x2, y2), (x3, y3)])

Texto:
    fonte = pygame.font.Font(None, 32)
    imagem = fonte.render("Pontuacao: 10", True, (255, 255, 255))
    tela.blit(imagem, (20, 20))

Imagem:
    personagem = pygame.image.load("assets/player.png").convert_alpha()
    personagem = pygame.transform.scale(personagem, (48, 48))
    tela.blit(personagem, (x, y))

Use caminhos relativos ao projeto, crie a pasta "assets" e mantenha os
arquivos em formato PNG para preservar transparencia.

4. ENTRADA E MOVIMENTO
----------------------
pygame.key.get_pressed() informa o estado atual das teclas:

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade * dt

dt (delta time) e o tempo em segundos desde o ultimo quadro. Multiplicar
velocidade por dt faz o jogo ter movimento semelhante em computadores
rapidos e lentos. O exemplo abaixo usa exatamente essa ideia.

5. COLISOES
-----------
Retangulos:
    jogador = pygame.Rect(x, y, 32, 32)
    parede = pygame.Rect(300, 200, 120, 30)
    if jogador.colliderect(parede):
        print("colidiu")

Para circulos, compare a distancia entre os centros:
    distancia = pygame.Vector2(a).distance_to(b)
    if distancia < raio_a + raio_b:
        ...

6. ESTRUTURA DE UM PROJETO MAIOR
--------------------------------
Uma organizacao simples:

    meu_jogo/
      main.py
      settings.py
      player.py
      level.py
      assets/
        player.png

Quando a lista de objetos crescer, crie classes ou use pygame.sprite.Sprite
e pygame.sprite.Group. Nao coloque toda a logica em um unico while.

7. CAMERA 2D E ANIMACAO
-----------------------
Uma camera desloca o mundo antes de desenhar:

    tela.blit(imagem, (mundo_x - camera_x, mundo_y - camera_y))

Para animar, guarde uma lista de quadros e altere o indice com um
temporizador. A camera deve acompanhar o jogador, mas pode ser limitada ao
tamanho do mapa para nao mostrar areas fora da fase.

8. AUDIO E ESTADOS
------------------
    pygame.mixer.music.load("assets/musica.ogg")
    pygame.mixer.music.play(-1)
    pulo = pygame.mixer.Sound("assets/pulo.wav")
    pulo.play()

Estados comuns sao MENU, JOGANDO e PAUSADO. Um estado evita que o menu
continue movimentando inimigos e torna as transicoes explicitas.

9. COMO A PROJECAO 3D FUNCIONA
-------------------------------
Um ponto 3D (x, y, z) pode ser projetado na tela por:

    tela_x = centro_x + x * foco / z
    tela_y = centro_y - y * foco / z

Quanto maior z, mais distante e menor fica o objeto. Nunca projete z <= 0:
o ponto esta atras da camera ou causara divisao por zero. O demo abaixo
desenha um cubo girando, com arestas ordenadas pela profundidade.

10. IDEIAS DE EXERCICIOS
------------------------
1. Adicione inimigos que perseguem o jogador.
2. Coloque uma imagem e uma animacao de caminhada.
3. Crie paredes e resolva a colisao separadamente em x e y.
4. Adicione vidas, pontuacao e uma tela de fim.
5. No demo 3D, preencha as faces do cubo e use back-face culling.
6. Troque o cubo por uma piramide e implemente uma camera orbital.
"""

import argparse
import math
from dataclasses import dataclass

import pygame


LARGURA, ALTURA = 900, 560
FUNDO = (18, 22, 35)
BRANCO = (240, 240, 245)


def iniciar(titulo):
    """Cria a janela e retorna tela e relogio."""
    pygame.init()
    pygame.display.set_caption(titulo)
    return pygame.display.set_mode((LARGURA, ALTURA)), pygame.time.Clock()


@dataclass
class Jogador:
    """Exemplo de objeto 2D com estado e comportamento."""

    posicao: pygame.Vector2
    velocidade: float = 260
    tamanho: int = 34

    @property
    def rect(self):
        return pygame.Rect(
            round(self.posicao.x),
            round(self.posicao.y),
            self.tamanho,
            self.tamanho,
        )

    def atualizar(self, dt):
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(
            teclas[pygame.K_d] - teclas[pygame.K_a],
            teclas[pygame.K_s] - teclas[pygame.K_w],
        )
        if direcao.length_squared():
            direcao = direcao.normalize()
        self.posicao += direcao * self.velocidade * dt
        self.posicao.x = max(0, min(LARGURA - self.tamanho, self.posicao.x))
        self.posicao.y = max(0, min(ALTURA - self.tamanho, self.posicao.y))

    def desenhar(self, tela):
        pygame.draw.rect(tela, (80, 190, 255), self.rect, border_radius=8)
        pygame.draw.circle(tela, BRANCO, self.rect.center, 5)


def demo_2d():
    """Jogo 2D pequeno: mova-se com WASD e colete o alvo amarelo."""
    tela, relogio = iniciar("Pygame - exemplo 2D")
    jogador = Jogador(pygame.Vector2(100, 240))
    alvo = pygame.Vector2(700, 300)
    pontos = 0
    fonte = pygame.font.Font(None, 32)
    executando = True

    while executando:
        dt = relogio.tick(60) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                executando = False

        jogador.atualizar(dt)
        if jogador.rect.collidepoint(alvo):
            pontos += 1
            alvo.update(
                80 + (pontos * 137) % (LARGURA - 160),
                100 + (pontos * 83) % (ALTURA - 160),
            )

        tela.fill(FUNDO)
        pygame.draw.circle(tela, (255, 210, 65), alvo, 18)
        jogador.desenhar(tela)
        texto = fonte.render(
            f"WASD: mover | pontos: {pontos} | ESC: sair", True, BRANCO
        )
        tela.blit(texto, (20, 20))
        pygame.display.flip()

    pygame.quit()


def projetar(ponto, angulo, foco=430):
    """Gira um ponto no eixo Y e aplica perspectiva."""
    x, y, z = ponto
    cosseno, seno = math.cos(angulo), math.sin(angulo)
    x_rotacionado = x * cosseno - z * seno
    z_rotacionado = x * seno + z * cosseno + 4.5
    if z_rotacionado <= 0.1:
        return None
    return (
        LARGURA / 2 + x_rotacionado * foco / z_rotacionado,
        ALTURA / 2 - y * foco / z_rotacionado,
        z_rotacionado,
    )


def demo_3d():
    """Desenha um cubo 3D por projecao em perspectiva."""
    tela, relogio = iniciar("Pygame - 3D por projecao")
    vertices = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
    ]
    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    angulo = 0.0
    fonte = pygame.font.Font(None, 30)
    executando = True

    while executando:
        dt = relogio.tick(60) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                executando = False

        angulo += dt
        pontos = [projetar(v, angulo) for v in vertices]
        tela.fill((10, 12, 24))
        linhas = []
        for inicio, fim in arestas:
            a, b = pontos[inicio], pontos[fim]
            if a is not None and b is not None:
                linhas.append((a[2] + b[2], a, b))
        for _, a, b in sorted(linhas, reverse=True):
            pygame.draw.line(
                tela, (95, 210, 255), (a[0], a[1]), (b[0], b[1]), 4
            )
        tela.blit(
            fonte.render("Cubo 3D: perspectiva | ESC: sair", True, BRANCO),
            (20, 20),
        )
        pygame.display.flip()

    pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Exemplos do tutorial de Pygame")
    parser.add_argument(
        "--demo",
        choices=("2d", "3d"),
        default="3d",
        help="exemplo para executar (padrao: 2d)",
    )
    args = parser.parse_args()
    (demo_2d if args.demo == "2d" else demo_3d)()


if __name__ == "__main__":
    main()