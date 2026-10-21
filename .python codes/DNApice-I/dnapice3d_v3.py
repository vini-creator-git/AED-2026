import math
import os
import sys
from random import choice, uniform

import pygame

bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
rnab = {"A": "U", "T": "A", "C": "G", "G": "C"}
COR = {"A": (235, 70, 60), "T": (200, 90, 230), "C": (70, 210, 100),
       "G": (60, 200, 235), "U": (200, 90, 230)}
PONTE = {"A": (90, 120, 255), "T": (90, 120, 255), "C": (255, 215, 60), "G": (255, 215, 60)}
FITA_MOLDE, FITA_COD = (120, 150, 255), (255, 170, 90)
WOLBACHIA = "TTTCTTTAAAAGTCGGCAAATATTTGCATTGTGTAATT"   # sequencia predefinida (fita molde)

pygame.init()
W, H = 1200, 720
tela_cheia = False
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("DNApice 3D - Transcrição")
clock = pygame.time.Clock()

# ------------------------------------------------------------------ fontes
AQUI = os.path.dirname(os.path.abspath(__file__))


def _arq(nome):
    p = os.path.join(AQUI, nome)
    return p if os.path.exists(p) else None


FONT_R, FONT_B = _arq("FiraSans-Regular.ttf"), _arq("FiraSans-Bold.ttf")
_fc = {}


def fonte(tam, bold=False):
    k = (tam, bold)
    if k not in _fc:
        arq = FONT_B if bold else FONT_R
        _fc[k] = pygame.font.Font(arq, tam) if arq else pygame.font.SysFont("segoeui,arial,dejavusans", tam, bold=bold)
    return _fc[k]


FONTE_P, FONTE_M, FONTE_G, FONTE_T = fonte(15), fonte(17, True), fonte(28, True), fonte(72, True)
cache = {}

SP, R, TW, FOC = 26, 42, 0.62, 700
CY = 290                        # centro vertical da cena (muda com o layout)
NT_S = 1.3                      # nucleotideos por segundo (velocidade 1x)
T0, T1, T3 = 3.0, 2.0, 4.5      # duracao: iniciacao, bolha, terminacao

ETAPAS = [
    ("1. Iniciação", "O fator sigma guia a RNA polimerase até o promotor, onde ela se liga ao DNA."),
    ("2. Abertura da bolha", "A RNA polimerase separa as duas fitas do DNA e expõe a fita molde."),
    ("3. Alongamento", "A polimerase desliza pela fita molde e encaixa ribonucleotídeos complementares "
                       "(A-U, T-A, C-G, G-C). O sigma se solta e a topoisomerase alivia a tensão à frente."),
    ("4. Terminação", "O fator Rho alcança a polimerase, solta o RNA e o DNA volta a se enrolar."),
    ("Concluído", "RNA pronto! Use Anterior para rever algum passo, ou R para gerar uma nova fita."),
]
PRESETS = [(0.35, 0.25, 650), (0.9, 0.15, 480), (0.4, 0.3, 720), (-0.5, 0.2, 820), (0.2, 0.5, 720)]  # camera por slide

BETA, BETAP, ALFA, OMEGA = (70, 120, 235), (45, 185, 185), (150, 190, 255), (235, 130, 190)
POL = [((-10, -102, 0), 40, BETA), ((30, -92, 12), 34, BETA), ((-45, -85, -10), 32, BETA), ((62, -70, -6), 26, BETA),
       ((-25, -72, 28), 28, BETA), ((5, -112, -25), 28, BETA), ((78, -66, 0), 18, BETA),
       ((-10, 102, 0), 40, BETAP), ((32, 90, -12), 34, BETAP), ((-45, 86, 10), 32, BETAP), ((64, 70, 6), 26, BETAP),
       ((-22, 72, -28), 28, BETAP), ((8, 112, 25), 28, BETAP), ((78, 66, 0), 18, BETAP),
       ((-90, -85, 35), 22, ALFA), ((-90, 85, -35), 22, ALFA), ((-72, 0, 48), 14, OMEGA)]
SIG = [((-35, -62, 22), 17), ((-8, -54, 16), 15), ((18, -46, 10), 15), ((42, -38, 4), 13)]
TOPO = [(190, 110, 240), (150, 90, 220)]


def suave(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp3(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))


def pt(i, s, u):
    th = i * TW + s * math.pi
    r = R * (1 + 0.85 * u)
    return (i * SP, r * math.sin(th), r * math.cos(th))


def fb(u):  # posicao da bolinha da base ao longo do "degrau"
    return 0.40 * (1 - 0.45 * u)


def letra(l, tam, cor=(15, 15, 25)):
    key = (l, tam, cor)
    if key not in cache:
        cache[key] = fonte(tam, True).render(l, True, cor)
    return cache[key]


def texto(t, x, y, fnt=FONTE_P, cor=(235, 235, 245), centro=False, alvo=None):
    alvo = alvo or screen
    img, sh = fnt.render(t, True, cor), fnt.render(t, True, (0, 0, 0))
    if centro:
        x -= img.get_width() / 2
    alvo.blit(sh, (x + 1, y + 1))
    alvo.blit(img, (x, y))


def quebra(t, fnt, larg):
    linhas, linha = [], ""
    for w in t.split():
        if fnt.size(linha + w)[0] > larg and linha:
            linhas.append(linha.strip())
            linha = ""
        linha += w + " "
    if linha:
        linhas.append(linha.strip())
    return linhas


# ------------------------------------------------------------------ esferas sombreadas
esferas = {}


def esfera_mestre(cor):
    if cor not in esferas:
        S = 128
        sf = pygame.Surface((S, S), pygame.SRCALPHA)
        escuro = tuple(int(v * 0.35) for v in cor)
        claro = tuple(int(v + (255 - v) * 0.55) for v in cor)
        R0, passos = S // 2 - 1, 40
        for i in range(passos):
            t = i / (passos - 1)
            c = tuple(int(escuro[j] + (claro[j] - escuro[j]) * t ** 0.9) for j in range(3))
            pygame.draw.circle(sf, c, (int(S / 2 - 0.22 * R0 * t), int(S / 2 - 0.26 * R0 * t)), max(2, int(R0 * (1 - 0.78 * t))))
        pygame.draw.circle(sf, (240, 245, 255), (int(S * 0.36), int(S * 0.33)), int(S * 0.06))
        pygame.draw.circle(sf, claro, (S // 2, S // 2), R0, 2)
        esferas[cor] = sf
    return esferas[cor]


def esfera(sx, sy, r, cor, alpha):
    r = max(3, min(int(r), 400))
    if alpha <= 3 or sx + r < 0 or sx - r > W or sy + r < 0 or sy - r > H:
        return
    img = pygame.transform.smoothscale(esfera_mestre(cor), (2 * r, 2 * r))
    img.set_alpha(min(255, int(alpha)))
    screen.blit(img, (sx - r, sy - r))


# ------------------------------------------------------------------ fundo (gradiente + nebulosas, sem bolinhas)
def sprite(r, cor, alpha):
    s = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
    passo = max(2, r // 40)
    for rr in range(r, 0, -passo):
        pygame.draw.circle(s, (*cor, int(alpha * (1 - rr / r) ** 2)), (r, r), rr)
    return s


class Fundo:
    def __init__(s):
        s.base = pygame.Surface((W, H))
        topo, meio, fim = (5, 7, 20), (22, 14, 54), (5, 36, 54)
        for y in range(H):
            t = y / max(1, H - 1)
            a, b, u = (topo, meio, t / 0.55) if t < 0.55 else (meio, fim, (t - 0.55) / 0.45)
            s.base.fill(tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3)), (0, y, W, 1))
        s.neb = [(sprite(380, (130, 60, 210), 90), 0.22, 0.35, 0.10), (sprite(340, (30, 180, 200), 75), 0.82, 0.78, 0.16),
                 (sprite(300, (230, 70, 150), 60), 0.7, 0.18, 0.08)]
        s.vig = pygame.Surface((W, H), pygame.SRCALPHA)
        for i in range(min(70, W // 2, H // 2)):
            pygame.draw.rect(s.vig, (0, 0, 0, int(120 * (1 - i / 70) ** 2)), (i, i, W - 2 * i, H - 2 * i), 1)

    def draw(s, yaw, fx, T):
        screen.blit(s.base, (0, 0))
        par = yaw * 200 + fx * 0.25
        for spr, x, y, d in s.neb:
            sw = spr.get_width()
            screen.blit(spr, ((x * W - par * d) % (W + 2 * sw) - sw, y * H - sw / 2 + math.sin(T * 0.2 + x * 9) * 15))
        screen.blit(s.vig, (0, 0))


# ------------------------------------------------------------------ simulacao
class Sim:
    def __init__(s, n, demo=False, seq=None):
        s.n, s.demo, s.seq, s.nome = n, demo, seq, None
        s.d2 = n / NT_S
        s.total = T0 + T1 + s.d2 + T3
        s.b = [0, T0, T0 + T1, T0 + T1 + s.d2, s.total]      # inicio de cada etapa
        s.yaw, s.pitch = 0.35, 0.25
        s.dist_u = s.dist = 1000.0 if demo else 700.0
        s.focus = [n * SP / 2 if demo else 0.0, 0.0, 0.0]
        s.follow, s.auto_rot = not demo, demo
        s.clock, s.i0 = 0.0, 0
        s.rna_on, s.blocos, s.vista, s.slide = True, False, "video", 0
        s.anim, s.aviso, s.slide_t0 = None, None, 0.0
        s.reset()

    def reset(s):
        n = s.n
        s.dna = list(s.seq) if s.seq else [choice("ATCG") for _ in range(n)]      # fita molde
        s.comp = [bases[b] for b in s.dna]                 # fita codificante
        s.rna = [rnab[b] for b in s.dna]
        s.ntp = [(uniform(-80, 80), uniform(110, 170) * choice([-1, 1]), uniform(-90, 90)) for _ in range(n)]
        s.playing, s.speed, s.pan_off, s.polx, s.aviso = True, 1.0, None, 0.0, None
        s.set_time(0)
        if s.vista == "slides":
            s.go_slide(0)

    # ---- linha do tempo
    def set_time(s, t):
        s.tt = t = max(0.0, min(t, s.total))
        s.rho = s.rel = s.bub = s.prog = 0.0
        if t < T0:
            s.stage, s.st = 0, t
        elif t < T0 + T1:
            s.stage, s.st = 1, t - T0
            s.bub = suave(s.st / 2)
        elif t < T0 + T1 + s.d2:
            s.stage, s.st = 2, t - T0 - T1
            s.prog, s.bub = s.st * NT_S, 1.0
        elif t < s.total:
            s.stage, s.st, s.prog = 3, t - T0 - T1 - s.d2, float(s.n)
            s.rho, s.rel = suave(s.st / 2), suave((s.st - 2) / 2.5)
            s.bub = 1 - s.rel
        else:
            s.stage, s.st, s.prog, s.rho, s.rel = 4, 0, float(s.n), 1.0, 1.0

    def avancar(s, d):
        """anda (d>0) ou rebobina (d<0); respeita o fim do slide e as pausas de 10 em 10"""
        if not s.rna_on:
            return
        t0 = s.tt
        t1 = t0 + d
        if d > 0:
            if s.vista == "slides":
                t1 = min(t1, (s.b[s.slide + 1] - 0.001) if s.slide < 4 else s.total)
            if s.blocos:
                ini = T0 + T1
                m = int((t0 - ini) * NT_S / 10 + 1e-6) + 1 if t0 >= ini else 1
                tb = ini + m * 10 / NT_S
                if m * 10 < s.n and t0 + 1e-6 < tb <= t1:
                    t1, s.playing = tb, False
                    s.aviso = (f"Bases {m * 10 - 9}–{m * 10} transcritas · Espaço continua", s.clock + 4)
        s.set_time(t1)

    def go_slide(s, k):
        s.slide = max(0, min(4, k))
        s.set_time(s.b[s.slide] if s.slide < 4 else s.total)
        s.playing, s.slide_t0, s.follow = True, s.clock, True
        y, p, d = PRESETS[s.slide]
        s.cam_to(y, p, d)

    def set_vista(s, v):
        if v != s.vista:
            s.vista = v
            if v == "slides":
                s.go_slide(min(s.stage, 4))

    def toggle_rna(s):
        s.rna_on = not s.rna_on
        s.set_time(0)
        s.playing, s.follow, s.pan_off = True, True, None
        if s.rna_on and s.vista == "slides":
            s.go_slide(0)

    # ---- camera
    def cam_to(s, yaw, pitch, dist, dur=1.4):
        yaw = s.yaw + ((yaw - s.yaw + math.pi) % (2 * math.pi) - math.pi)
        s.anim = [0.0, dur, s.yaw, s.pitch, s.dist_u, yaw, pitch, dist]

    def disp(s):
        if s.prog >= s.n:
            return float(s.n)
        k = int(s.prog)
        return k + suave(s.prog - k)

    def camera(s, dt):
        s.clock += dt
        if s.auto_rot:
            s.yaw += dt * 0.25
        if s.anim:
            a = s.anim
            a[0] += dt
            u = suave(a[0] / a[1])
            s.yaw, s.pitch, s.dist_u = a[2] + (a[5] - a[2]) * u, a[3] + (a[6] - a[3]) * u, a[4] + (a[7] - a[4]) * u
            if a[0] >= a[1]:
                s.anim = None
        fit = 1.0
        if s.follow:
            if s.rna_on:
                tx = 0 if s.stage == 0 else (s.n * SP / 2 if s.stage >= 3 else s.disp() * SP)
                if s.stage >= 3:
                    fit = max(1.0, (s.n * SP + 250) / 1000)
            else:
                tx, fit = s.n * SP / 2, max(1.0, (s.n * SP + 250) / 1000)
            k = min(1, dt * 3)
            s.focus[0] += (tx - s.focus[0]) * k
            s.focus[1] -= s.focus[1] * k
            s.focus[2] -= s.focus[2] * k
        s.dist += (s.dist_u * fit - s.dist) * min(1, dt * 4)

    def proj(s, p):
        x, y, z = p[0] - s.focus[0], p[1] - s.focus[1], p[2] - s.focus[2]
        c, sn = math.cos(s.yaw), math.sin(s.yaw)
        x, z = x * c + z * sn, -x * sn + z * c
        c, sn = math.cos(s.pitch), math.sin(s.pitch)
        y, z = y * c - z * sn, y * sn + z * c
        d = s.dist + z
        if d < 40:
            return (0, 0, z, -1)
        k = FOC / d
        return (W / 2 + x * k, CY + y * k, z, k)

    def u(s, i):
        return (s.bub if s.rna_on else 0.0) * math.exp(-((i * SP - s.polx) / (SP * 3.2)) ** 2)

    def bead(s, j, disp):
        u = s.u(j)
        ph = lerp3(pt(j, 0, u), (j * SP, 0, 0), fb(u) + 0.24)
        t = max(suave((disp - j - 5) / 9), s.rel)
        T = s.clock
        pf = (j * SP, -105 - 12 * math.sin(j * 0.9 + T), 22 * math.cos(j * 0.9 + T * 0.8))
        p = lerp3(ph, pf, t)
        return (p[0], p[1] - 90 * s.rel, p[2]), ph

    def draw(s):
        n, disp = s.n, s.disp()
        s.polx = disp * SP
        items, rot = [], []
        P = []
        for i in range(n):
            u = s.u(i)
            pa, pb, pm = s.proj(pt(i, 0, u)), s.proj(pt(i, 1, u)), s.proj((i * SP, 0, 0))
            if min(pa[3], pb[3], pm[3]) <= 0:
                P.append(None)
                continue
            P.append((pa, pb))
            fr = fb(u)
            ea, eb = mix(pa, pm, fr), mix(pb, pm, fr)
            w = 3 if s.dna[i] in "AT" else 5
            items.append(((pa[2] + ea[2]) / 2, 'l', pa, ea, COR[s.dna[i]], w))
            items.append(((pb[2] + eb[2]) / 2, 'l', pb, eb, COR[s.comp[i]], w))
            items.append((ea[2], 'd', ea, 8, COR[s.dna[i]], s.dna[i]))
            items.append((eb[2], 'd', eb, 8, COR[s.comp[i]], s.comp[i]))
            items.append((pa[2], 'd', pa, 5, FITA_MOLDE, None))
            items.append((pb[2], 'd', pb, 5, FITA_COD, None))
        for i in range(n - 1):
            if P[i] and P[i + 1]:
                for j, cor in ((0, FITA_MOLDE), (1, FITA_COD)):
                    a, b = P[i][j], P[i + 1][j]
                    items.append(((a[2] + b[2]) / 2, 'l', a, b, cor, 4))

        # ---- DNA dividido de 10 em 10: aneis separadores + rotulos dos blocos
        if s.blocos:
            for m in range(0, n + 1, 10):
                x = (m - 0.5) * SP
                ring = [s.proj((x, (R + 24) * math.sin(q * math.pi / 10), (R + 24) * math.cos(q * math.pi / 10))) for q in range(21)]
                if all(p[3] > 0 for p in ring):
                    for q in range(20):
                        items.append(((ring[q][2] + ring[q + 1][2]) / 2, 'l', ring[q], ring[q + 1], (170, 180, 235), 2))
            for blk in range((n + 9) // 10):
                i1, i2 = blk * 10 + 1, min(n, (blk + 1) * 10)
                rot.append((s.proj(((i1 + i2 - 2) / 2 * SP, -(R + 52), 0)), f"{i1}–{i2}", (200, 210, 255)))

        if not s.demo and s.rna_on:
            # RNA
            ncomp = 0 if s.stage < 2 else (int(s.prog) if s.stage == 2 else n)
            rp = {}
            for j in range(ncomp):
                p = s.proj(s.bead(j, disp)[0])
                if p[3] <= 0:
                    continue
                rp[j] = p
                items.append((p[2], 'd', p, 9, COR[s.rna[j]], s.rna[j]))
                if j - 1 in rp:
                    a = rp[j - 1]
                    items.append(((a[2] + p[2]) / 2, 'l', a, p, (225, 200, 255), 3))
            if s.stage == 2 and int(s.prog) < n:
                kk = int(s.prog)
                f = s.prog - kk
                _, ph = s.bead(kk, disp)
                o = s.ntp[kk]
                p = s.proj(lerp3((ph[0] + o[0], ph[1] + o[1], ph[2] + o[2]), ph, suave(f / 0.6)))
                if p[3] > 0:
                    items.append((p[2], 'd', p, 9 * max(0.3, suave(f / 0.15)), COR[s.rna[kk]], s.rna[kk]))

            # proteinas: cada uma e um conjunto de esferas sombreadas
            if s.stage == 0:
                P0 = lerp3((-330, -240, 200), (0, 0, 0), suave(s.st / 3))
            else:
                P0 = lerp3((disp * SP, 0, 0), (disp * SP + 260, 280, 140), s.rel)
            fade = 1 - s.rel

            def prot(pos, r, cor, al):
                p = s.proj(pos)
                if p[3] > 0:
                    items.append((p[2], 'b', p, r, cor, int(al)))
                return p

            def em(base, off):
                return (base[0] + off[0], base[1] + off[1], base[2] + off[2])

            fr = s.prog - int(s.prog)
            pulso = 3 * math.sin(s.clock * 2) + (4 * math.sin(math.pi * fr) if s.stage == 2 else 0)
            for off, r, cor in POL:     # as garras abrem e fecham a cada nucleotideo
                dy = -pulso if off[1] < -60 else (pulso if off[1] > 60 else 0)
                prot(em(P0, (off[0], off[1] + dy, off[2])), r, cor, 215 * fade)
            if fade > 0.3:
                rot.append((s.proj(em(P0, (0, -195, 0))), "RNA polimerase", (150, 200, 255)))
                if s.dist < 650:
                    rot.append((s.proj(em(P0, (-10, -150, 0))), "β", (190, 215, 255)))
                    rot.append((s.proj(em(P0, (-10, 150, 0))), "β′", (150, 240, 235)))
                    rot.append((s.proj(em(P0, (-90, -118, 35))), "α", (200, 220, 255)))
            srel = 0 if s.stage < 2 else (1 if s.stage > 2 else suave((s.prog - 6) / 3))
            if srel < 1:
                so = (-110 * srel, -140 * srel, 70 * srel)
                prev = None
                for off, r in SIG:
                    p = prot(em(P0, (off[0] + so[0], off[1] + so[1], off[2] + so[2])), r, (255, 150, 40),
                             225 * (1 - srel) * fade)
                    if prev is not None and p[3] > 0 and prev[3] > 0 and srel < 0.5:
                        items.append(((p[2] + prev[2]) / 2, 'l', prev, p, (255, 175, 70), 6))
                    prev = p
                if srel < 0.7:
                    rot.append((s.proj(em(P0, (-10 + so[0], -95 + so[1], 15 + so[2]))), "Fator sigma", (255, 190, 110)))
            if s.stage in (2, 3):
                ta = suave(s.prog / 1.5) * fade
                tx = disp * SP + 120
                for k in range(1, 14):      # anel aberto (portao) em volta do DNA
                    th = 2 * math.pi * k / 14
                    rr = 84 + 3 * math.sin(s.clock * 3 + k)
                    r = 16 + (7 if abs(th - math.pi) < 0.8 else 0)
                    prot((tx, rr * math.cos(th), rr * math.sin(th)), r, TOPO[k % 2], 215 * ta)
                if ta > 0.4:
                    rot.append((s.proj((tx, 140, 0)), "Topoisomerase", (215, 160, 255)))
            if s.stage >= 3:
                C = lerp3((disp * SP - 150, -320, 160), (P0[0] - 45, -115, 10), s.rho)
                for k in range(6):          # hexamero em anel, o RNA passa pelo centro
                    th = k * math.pi / 3 + s.clock * 0.5
                    prot((C[0], C[1] + 40 * math.cos(th), C[2] + 40 * math.sin(th)), 20, (70, 220, 170), 225 * fade)
                    th2 = th + math.pi / 6
                    prot((C[0] + 8, C[1] + 64 * math.cos(th2), C[2] + 64 * math.sin(th2)), 11, (150, 250, 215), 225 * fade)
                if fade > 0.3:
                    rot.append((s.proj((C[0], C[1] - 95, C[2])), "Fator Rho", (130, 255, 205)))
            if s.stage < 3:
                rot.append((s.proj((SP, -88, 0)), "Promotor", (255, 255, 160)))

        items.sort(key=lambda it: -it[0])
        for it in items:
            k = it[1]
            if k == 'l':
                a, b = it[2], it[3]
                if (a[0] < -60 and b[0] < -60) or (a[0] > W + 60 and b[0] > W + 60) or \
                        (a[1] < -60 and b[1] < -60) or (a[1] > H + 60 and b[1] > H + 60):
                    continue
                pygame.draw.line(screen, it[4], (a[0], a[1]), (b[0], b[1]), max(1, min(30, int(it[5] * a[3]))))
            elif k == 'd':
                p = it[2]
                if p[0] < -40 or p[0] > W + 40 or p[1] < -40 or p[1] > H + 40:
                    continue
                r = max(2, min(200, int(it[3] * p[3])))
                pygame.draw.circle(screen, it[4], (int(p[0]), int(p[1])), r)
                pygame.draw.circle(screen, (255, 255, 255), (int(p[0]), int(p[1])), r, 1)
                if it[5] and r >= 6:
                    ls = letra(it[5], int(r * 1.5))
                    screen.blit(ls, (p[0] - ls.get_width() / 2, p[1] - ls.get_height() / 2))
            else:
                p = it[2]
                esfera(int(p[0]), int(p[1]), it[3] * p[3], it[4], it[5])
        for p, t, cor in rot:
            if p[3] > 0:
                texto(t, p[0], p[1], cor=cor, centro=True)


# ------------------------------------------------------------------ interface
class Btn:
    def __init__(s, w, h, label=None, icon=None):
        s.r, s.label, s.icon = pygame.Rect(0, 0, w, h), label, icon

    def draw(s, mouse, on=False):
        cor = (80, 110, 200) if s.r.collidepoint(mouse) else ((50, 140, 110) if on else (34, 44, 86))
        pygame.draw.rect(screen, cor, s.r, border_radius=9)
        pygame.draw.rect(screen, (150, 170, 255), s.r, 1, border_radius=9)
        if s.icon:
            icone(s.icon, s.r)
        else:
            t = FONTE_M.render(s.label, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=s.r.center))


def icone(nome, r):
    cx, cy = r.center
    c, a = (255, 255, 255), 9
    if nome == "play":
        pygame.draw.polygon(screen, c, [(cx - 5, cy - a), (cx - 5, cy + a), (cx + a, cy)])
    elif nome == "pause":
        pygame.draw.rect(screen, c, (cx - 7, cy - a, 5, 2 * a))
        pygame.draw.rect(screen, c, (cx + 2, cy - a, 5, 2 * a))
    elif nome == "rew":
        pygame.draw.polygon(screen, c, [(cx - 3, cy - a), (cx - 3, cy + a), (cx - 3 - a, cy)])
        pygame.draw.polygon(screen, c, [(cx + a - 3, cy - a), (cx + a - 3, cy + a), (cx - 3, cy)])
    elif nome == "back":
        pygame.draw.rect(screen, c, (cx - a, cy - a, 3, 2 * a))
        pygame.draw.polygon(screen, c, [(cx + a, cy - a), (cx + a, cy + a), (cx - a + 5, cy)])
    elif nome == "fwd":
        pygame.draw.polygon(screen, c, [(cx - a, cy - a), (cx - a, cy + a), (cx + a - 5, cy)])
        pygame.draw.rect(screen, c, (cx + a - 3, cy - a, 3, 2 * a))


BH = 36
BTN = {"ini": Btn(74, BH, "Início"), "rew": Btn(52, BH, icon="rew"), "back": Btn(52, BH, icon="back"),
       "play": Btn(60, BH, icon="pause"), "fwd": Btn(52, BH, icon="fwd"), "vm": Btn(58, BH, "Vel -"),
       "vp": Btn(58, BH, "Vel +"), "seg": Btn(132, BH, "Seguir"), "menu": Btn(80, BH, "Menu"),
       "prev": Btn(110, BH, "Anterior"), "replay": Btn(100, BH, "Repetir"), "next": Btn(120, BH, "Próximo")}
TB = {"video": Btn(84, BH, "Vídeo"), "slides": Btn(84, BH, "Slides"), "blocos": Btn(108, BH, "10 em 10"),
      "rna": Btn(72, BH, "RNA")}
DOTS = pygame.Rect(0, 0, 44, BH)
DOT_RECTS = []


def ativos_barra(sim):
    if not sim.rna_on:
        chaves = ["seg", "menu"]
    elif sim.vista == "slides":
        chaves = ["prev", "replay", "next", "seg", "menu"]
    else:
        chaves = ["ini", "rew", "back", "play", "fwd", "vm", "vp", "seg", "menu"]
    x, out = 20, []
    for k in chaves:
        BTN[k].r.topleft = (x, H - 48)
        x += BTN[k].r.w + 8
        out.append((k, BTN[k]))
    DOT_RECTS.clear()
    if sim.rna_on and sim.vista == "slides":
        for i in range(5):
            DOT_RECTS.append(pygame.Rect(x + 10 + i * 30, H - 48, 28, BH))
    return out


def ativos_toolbar(sim):
    chaves = ["video", "slides", "blocos", "rna"] if sim.rna_on else ["blocos", "rna"]
    x, out = 20, []
    for k in chaves:
        TB[k].r.topleft = (x, 14)
        x += TB[k].r.w + (14 if k == "slides" else 6)
        out.append((k, TB[k]))
    return out


def painel_rect(sim):
    base = H - (100 if (sim.vista == "video" and sim.rna_on) else 62)
    ph = 106 if sim.rna_on else 74
    return pygame.Rect(10, base - ph, W - 20, ph)


def barra_rect():
    return pygame.Rect(20, H - 72, W - 40, 10)


def painel_fitas(sim, pr):
    n, cw = sim.n, 21
    gap = 14 if sim.blocos else 0
    sf = pygame.Surface(pr.size, pygame.SRCALPHA)
    pygame.draw.rect(sf, (8, 10, 30, 175), sf.get_rect(), border_radius=10)
    pygame.draw.rect(sf, (130, 140, 210, 110), sf.get_rect(), 1, border_radius=10)
    screen.blit(sf, pr.topleft)
    vis = max(4, int((W - 250) / (cw + gap / 10)))
    if sim.pan_off is None:
        i0 = 0 if (sim.stage < 2 or not sim.rna_on) else int(sim.disp()) - vis // 2
    else:
        i0 = sim.pan_off
    i0 = sim.i0 = max(0, min(i0, max(0, n - vis)))
    y1, y2, y3 = pr.y + 6, pr.y + 37, pr.y + 68
    texto("Fita codificante 5'→3'", 22, y1 + 1, cor=FITA_COD)
    texto("Fita molde 3'→5'", 22, y2 + 1, cor=FITA_MOLDE)
    if sim.rna_on:
        texto("RNA 5'→3'", 22, y3 + 1, cor=(225, 200, 255))
    nc = 0 if (sim.stage < 2 or not sim.rna_on) else (int(sim.prog) if sim.stage == 2 else n)

    def xj(j):
        return 215 + (j - i0) * cw + (j // 10 - i0 // 10) * gap

    def cel(ch, x, y):
        ls = letra(ch, 20, COR[ch])
        screen.blit(ls, (x + (cw - ls.get_width()) // 2, y - 2))

    ultimo = i0
    for j in range(i0, min(n, i0 + vis)):
        x = xj(j)
        if x > W - 40:
            break
        ultimo = j
        if sim.blocos and j % 10 == 0 and j > i0:
            pygame.draw.line(screen, (130, 140, 215), (x - gap // 2 - 1, pr.y + 6), (x - gap // 2 - 1, pr.bottom - 8), 1)
        cel(sim.comp[j], x, y1)
        cel(sim.dna[j], x, y2)
        linhas = 2 if sim.dna[j] in "AT" else 3
        for yb, ok in ((y1 + 22, True), (y2 + 22, sim.rna_on and j < nc)):
            if ok:
                for q in range(linhas):
                    yy = yb + 2 + q * 3 + (0 if linhas == 3 else 1)
                    pygame.draw.line(screen, PONTE[sim.dna[j]], (x + 5, yy), (x + cw - 6, yy), 1)
        if sim.rna_on and j < nc:
            cel(sim.rna[j], x, y3)
    if sim.stage == 2 and sim.rna_on and i0 <= int(sim.prog) <= ultimo:
        pygame.draw.rect(screen, (255, 235, 120), (xj(int(sim.prog)) - 1, y1 - 3, cw, (y3 + 26 - y1)), 1, border_radius=4)
    info = f"bases {i0 + 1}–{ultimo + 1} de {n}  ·  scroll aqui rola"
    texto(info, W - 30 - FONTE_P.size(info)[0], pr.bottom - 22, cor=(160, 170, 210))


def popup_info(sim, desenhar):
    larg = 410
    x0, y0 = W - larg - 14, 58
    L = [("DNApice 3D" + (f"  ·  {sim.nome}" if sim.nome else ""), FONTE_M, (255, 255, 255), 6)]
    if sim.rna_on:
        nome, desc = ETAPAS[sim.stage]
        L.append((nome, fonte(21, True), (255, 220, 120), 4))
        L += [(l, FONTE_P, (225, 230, 245), 0) for l in quebra(desc, FONTE_P, larg - 32)]
        if sim.stage >= 2:
            L.append((f"Nucleotídeos transcritos: {min(int(sim.prog), sim.n)}/{sim.n}", FONTE_P, (190, 255, 220), 0))
        L.append((f"Velocidade {sim.speed:.2f}x  ·  Câmera {'seguindo' if sim.follow else 'livre'}  ·  "
                  f"{'pausado' if not sim.playing else 'reproduzindo'}", FONTE_P, (170, 180, 215), 8))
    else:
        L.append((f"Somente DNA: {sim.n} bases. Ative o botão RNA para ver a transcrição.", FONTE_P, (225, 230, 245), 8))
    ajuda = ["Arrastar: girar 360°  ·  Botão direito ou WASD: mover  ·  Q/E: descer/subir  ·  Shift: mais rápido",
             "Scroll: zoom (sobre o painel das fitas: rolar a sequência)",
             "Vídeo: ← → rebobinam/avançam, Espaço pausa.  Slides: ← → passo anterior/próximo",
             "V: vídeo/slides  ·  T: 10 em 10  ·  N: RNA ligado/desligado",
             "F: seguir  ·  O: giro automático  ·  R: reiniciar/nova fita  ·  I: este painel  ·  F11: tela cheia  ·  Esc: menu"]
    for a in ajuda:
        L += [(l, fonte(13), (150, 160, 200), 0) for l in quebra(a, fonte(13), larg - 32)]
    h = 20 + sum(f.get_linesize() + 2 + extra for _, f, _, extra in L)
    rect = pygame.Rect(x0, y0, larg, h)
    if desenhar:
        sf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(sf, (8, 10, 32, 232), sf.get_rect(), border_radius=14)
        pygame.draw.rect(sf, (140, 150, 230, 150), sf.get_rect(), 1, border_radius=14)
        screen.blit(sf, rect.topleft)
        y = y0 + 12
        for t, f, c, extra in L:
            texto(t, x0 + 16, y, f, c)
            y += f.get_linesize() + 2 + extra
    return rect


def cartao_slide(sim):
    k = sim.slide
    nome, desc = ETAPAS[k]
    w = min(450, int(W * 0.4))
    linhas = quebra(desc, FONTE_P, w - 36)
    h = 100 + FONTE_P.get_linesize() * len(linhas) + 40
    u = suave((sim.clock - sim.slide_t0) / 0.6)
    sf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(sf, (8, 10, 32, 225), sf.get_rect(), border_radius=16)
    pygame.draw.rect(sf, (140, 150, 230, 160), sf.get_rect(), 1, border_radius=16)
    texto(f"PASSO {k + 1} DE 5", 18, 14, fonte(13, True), (255, 220, 120), alvo=sf)
    texto(nome, 18, 34, FONTE_G, (255, 255, 255), alvo=sf)
    y = 80
    for l in linhas:
        texto(l, 18, y, FONTE_P, (225, 230, 245), alvo=sf)
        y += FONTE_P.get_linesize()
    if k < 4:
        fr = (sim.tt - sim.b[k]) / (sim.b[k + 1] - sim.b[k])
        pygame.draw.rect(sf, (30, 36, 70), (18, h - 30, w - 36, 6), border_radius=3)
        pygame.draw.rect(sf, (90, 200, 170), (18, h - 30, (w - 36) * min(1, fr), 6), border_radius=3)
        msg, cor = ("animação concluída · → próximo passo", (190, 255, 220)) if fr >= 0.995 else ("animação em andamento…", (160, 170, 210))
        texto(msg, 18, h - 24, fonte(13), cor, alvo=sf)
    sf.set_alpha(int(255 * u))
    screen.blit(sf, (20 - (1 - u) * 70, 62))


def hud(sim, mouse, info_aberta):
    pr = painel_rect(sim)
    painel_fitas(sim, pr)
    if sim.vista == "video" and sim.rna_on:
        BARRA = barra_rect()
        d = sim.b
        for q, nm in enumerate(("Iniciação", "Bolha", "Alongamento", "Terminação")):
            x = BARRA.x + BARRA.w * d[q] / sim.total
            texto(nm, x + 3, BARRA.y - 22, FONTE_P, (255, 220, 120) if sim.stage == q else (150, 160, 200))
            pygame.draw.line(screen, (150, 160, 210), (x, BARRA.y - 3), (x, BARRA.bottom + 3), 1)
        pygame.draw.rect(screen, (30, 36, 70), BARRA, border_radius=5)
        pygame.draw.rect(screen, (90, 200, 170), (BARRA.x, BARRA.y, BARRA.w * sim.tt / sim.total, BARRA.h), border_radius=5)
        pygame.draw.circle(screen, (255, 255, 255), (int(BARRA.x + BARRA.w * sim.tt / sim.total), BARRA.centery), 8)
    if sim.vista == "slides" and sim.rna_on:
        cartao_slide(sim)
    BTN["play"].icon = "pause" if sim.playing else "play"
    BTN["seg"].label = "Seguir: " + ("SIM" if sim.follow else "NÃO")
    for k, b in ativos_barra(sim):
        b.draw(mouse, on=(k == "seg" and sim.follow))
    for i, r in enumerate(DOT_RECTS):
        pygame.draw.circle(screen, (255, 220, 120) if i == sim.slide else (80, 90, 140), r.center, 8 if i == sim.slide else 6)
        if r.collidepoint(mouse):
            pygame.draw.circle(screen, (255, 255, 255), r.center, 9, 1)
    on = {"video": sim.vista == "video", "slides": sim.vista == "slides", "blocos": sim.blocos, "rna": sim.rna_on}
    for k, b in ativos_toolbar(sim):
        b.draw(mouse, on[k])
    # tres pontinhos (informacoes)
    DOTS.topleft = (W - 58, 14)
    cor = (80, 110, 200) if DOTS.collidepoint(mouse) else ((50, 140, 110) if info_aberta else (34, 44, 86))
    pygame.draw.rect(screen, cor, DOTS, border_radius=9)
    pygame.draw.rect(screen, (150, 170, 255), DOTS, 1, border_radius=9)
    for dx in (-10, 0, 10):
        pygame.draw.circle(screen, (255, 255, 255), (DOTS.centerx + dx, DOTS.centery), 3)
    if info_aberta:
        popup_info(sim, True)
    if sim.aviso and sim.clock < sim.aviso[1]:
        w = FONTE_M.size(sim.aviso[0])[0] + 36
        pill = pygame.Rect(W // 2 - w // 2, 66, w, 34)
        pygame.draw.rect(screen, (30, 90, 80), pill, border_radius=17)
        pygame.draw.rect(screen, (150, 255, 220), pill, 1, border_radius=17)
        texto(sim.aviso[0], W // 2, 72, FONTE_M, (255, 255, 255), True)


# ------------------------------------------------------------------ janela
def sincronizar():
    global screen, W, H
    sf = pygame.display.get_surface()
    w, h = sf.get_size()
    if not tela_cheia and (w < 900 or h < 560):
        sf = pygame.display.set_mode((max(w, 900), max(h, 560)), pygame.RESIZABLE)
        w, h = sf.get_size()
    mudou = (w, h) != (W, H)
    screen, W, H = sf, w, h
    return mudou


def alternar_tela_cheia():
    global screen, tela_cheia
    tela_cheia = not tela_cheia
    if tela_cheia:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1200, 720), pygame.RESIZABLE)


def main():
    global CY
    fundo = Fundo()
    demo = Sim(30, demo=True)
    sim, modo, qtxt, origem, stxt = None, "menu", "24", "aleatoria", ""
    info_aberta = False
    mb = {"minus": Btn(50, 50, "-"), "plus": Btn(50, 50, "+"), "ini": Btn(340, 56, "Iniciar simulação"),
          "sair": Btn(340, 44, "Sair"), "tab_a": Btn(175, 42, "Aleatória"), "tab_d": Btn(175, 42, "Sequência própria"),
          "tab_w": Btn(175, 42, "Wolbachia")}
    for v in (12, 24, 48, 96):
        mb[v] = Btn(78, 38, str(v))
    arrasta, rew_hold, scrub = None, False, False

    def pos_menu(oy):
        cx = W // 2
        mb["tab_a"].r.topleft, mb["tab_d"].r.topleft, mb["tab_w"].r.topleft = (cx - 270, oy + 18), (cx - 88, oy + 18), (cx + 94, oy + 18)
        mb["minus"].r.topleft, mb["plus"].r.topleft = (cx - 190, oy + 125), (cx + 140, oy + 125)
        for i, v in enumerate((12, 24, 48, 96)):
            mb[v].r.topleft = (cx - 170 + i * 88, oy + 195)
        mb["ini"].r.topleft, mb["sair"].r.topleft = (cx - 170, oy + 265), (cx - 170, oy + 332)

    def iniciar():
        nonlocal sim, modo
        if origem == "wolbachia":
            sim = Sim(len(WOLBACHIA), seq=WOLBACHIA)
            sim.nome = "Wolbachia"
        elif origem == "digitada":
            if not stxt:
                return
            sim = Sim(len(stxt), seq=stxt)
            sim.nome = "Sequência própria"
        else:
            sim = Sim(max(4, min(int(qtxt or 24), 150)))
        modo = "sim"

    def sair():
        pygame.quit()
        sys.exit()

    def acao_barra(k):
        nonlocal modo, rew_hold
        if k == "ini":
            sim.set_time(0)
            sim.playing = True
        elif k == "rew":
            rew_hold = True
        elif k == "back":
            sim.avancar(-1 / NT_S)
            sim.playing = False
        elif k == "fwd":
            sim.avancar(1 / NT_S)
            sim.playing = False
        elif k == "play":
            if sim.tt >= sim.total:
                sim.set_time(0)
            sim.playing = not sim.playing
        elif k == "vm":
            sim.speed = max(0.25, sim.speed - 0.25)
        elif k == "vp":
            sim.speed = min(4, sim.speed + 0.25)
        elif k == "seg":
            sim.follow, sim.pan_off = not sim.follow, None
        elif k == "menu":
            modo = "menu"
        elif k == "prev":
            sim.go_slide(sim.slide - 1)
        elif k == "next":
            sim.go_slide(sim.slide + 1)
        elif k == "replay":
            sim.go_slide(sim.slide)

    def scrub_to(mx):
        b = barra_rect()
        sim.set_time((mx - b.x) / b.w * sim.total)
        sim.playing = False

    while True:
        dt = min(clock.tick(60) / 1000, 0.05)
        if sincronizar():
            fundo = Fundo()
        mouse = pygame.mouse.get_pos()
        oy = max(150, (H - 440) // 2 + 20)
        pos_menu(oy)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sair()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                alternar_tela_cheia()
                continue
            if modo == "menu":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sair()
                    elif e.key == pygame.K_RETURN:
                        iniciar()
                    elif e.key == pygame.K_TAB:
                        ordem = ["aleatoria", "digitada", "wolbachia"]
                        origem = ordem[(ordem.index(origem) + 1) % 3]
                    elif e.key == pygame.K_BACKSPACE and origem == "aleatoria":
                        qtxt = qtxt[:-1]
                    elif e.key == pygame.K_BACKSPACE and origem == "digitada":
                        stxt = stxt[:-1]
                    elif origem == "digitada" and e.unicode.upper() in ("A", "T", "C", "G") and len(stxt) < 150:
                        stxt += e.unicode.upper()
                    elif e.unicode.isdigit() and len(qtxt) < 3 and origem == "aleatoria":
                        qtxt += e.unicode
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    cur = int(qtxt or 24)
                    if mb["ini"].r.collidepoint(e.pos):
                        iniciar()
                    elif mb["sair"].r.collidepoint(e.pos):
                        sair()
                    elif mb["tab_a"].r.collidepoint(e.pos):
                        origem = "aleatoria"
                    elif mb["tab_d"].r.collidepoint(e.pos):
                        origem = "digitada"
                    elif mb["tab_w"].r.collidepoint(e.pos):
                        origem = "wolbachia"
                    elif origem == "aleatoria" and mb["minus"].r.collidepoint(e.pos):
                        qtxt = str(max(4, cur - 1))
                    elif origem == "aleatoria" and mb["plus"].r.collidepoint(e.pos):
                        qtxt = str(min(150, cur + 1))
                    for v in (12, 24, 48, 96):
                        if origem == "aleatoria" and mb[v].r.collidepoint(e.pos):
                            qtxt = str(v)
                continue
            # ---- modo simulacao ----
            if e.type == pygame.KEYDOWN:
                slides = sim.vista == "slides" and sim.rna_on
                if e.key in (pygame.K_ESCAPE, pygame.K_m):
                    modo = "menu"
                elif e.key == pygame.K_SPACE:
                    if sim.tt >= sim.total and sim.rna_on and not slides:
                        sim.set_time(0)
                    sim.playing = not sim.playing
                elif e.key == pygame.K_r:
                    sim.reset()
                elif e.key == pygame.K_f:
                    sim.follow, sim.pan_off, sim.dist_u = True, None, 700.0
                elif e.key == pygame.K_o:
                    sim.auto_rot = not sim.auto_rot
                elif e.key == pygame.K_v and sim.rna_on:
                    sim.set_vista("slides" if sim.vista == "video" else "video")
                elif e.key == pygame.K_t:
                    sim.blocos = not sim.blocos
                elif e.key == pygame.K_n:
                    sim.toggle_rna()
                elif e.key == pygame.K_i:
                    info_aberta = not info_aberta
                elif slides and e.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN, pygame.K_RETURN):
                    sim.go_slide(sim.slide + 1)
                elif slides and e.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                    sim.go_slide(sim.slide - 1)
                elif e.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    sim.speed = min(4, sim.speed + 0.25)
                elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    sim.speed = max(0.25, sim.speed - 0.25)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                pr = painel_rect(sim)
                if e.button == 1:
                    if DOTS.collidepoint(e.pos):
                        info_aberta = not info_aberta
                        continue
                    if info_aberta and popup_info(sim, False).collidepoint(e.pos):
                        continue
                    tb = next((k for k, b in ativos_toolbar(sim) if b.r.collidepoint(e.pos)), None)
                    if tb:
                        if tb == "video" or tb == "slides":
                            sim.set_vista(tb)
                        elif tb == "blocos":
                            sim.blocos = not sim.blocos
                        else:
                            sim.toggle_rna()
                        continue
                    hit = next((k for k, b in ativos_barra(sim) if b.r.collidepoint(e.pos)), None)
                    if hit:
                        acao_barra(hit)
                        continue
                    di = next((i for i, r in enumerate(DOT_RECTS) if r.collidepoint(e.pos)), None)
                    if di is not None:
                        sim.go_slide(di)
                    elif sim.vista == "video" and sim.rna_on and barra_rect().inflate(0, 22).collidepoint(e.pos):
                        scrub = True
                        scrub_to(e.pos[0])
                    elif e.pos[1] < pr.y:
                        arrasta = "orbita"
                elif e.button in (2, 3) and e.pos[1] < pr.y:
                    arrasta = "pan"
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    rew_hold = scrub = False
                if e.button in (1, 2, 3):
                    arrasta = None
            elif e.type == pygame.MOUSEMOTION:
                if scrub:
                    scrub_to(e.pos[0])
                elif arrasta == "orbita":
                    sim.anim = None
                    sim.yaw += e.rel[0] * 0.008
                    sim.pitch = max(-1.45, min(1.45, sim.pitch + e.rel[1] * 0.008))
                elif arrasta == "pan":
                    sim.anim = None
                    sc, c, sn = sim.dist / 700, math.cos(sim.yaw), math.sin(sim.yaw)
                    sim.focus[0] -= c * e.rel[0] * sc
                    sim.focus[2] -= sn * e.rel[0] * sc
                    sim.focus[1] -= e.rel[1] * sc
                    sim.follow = False
            elif e.type == pygame.MOUSEWHEEL:
                if painel_rect(sim).collidepoint(mouse):
                    sim.pan_off = sim.i0 - e.y * 3
                else:
                    sim.anim = None
                    sim.dist_u = max(160, min(3200, sim.dist_u * 0.9 ** e.y))

        if modo == "menu":
            CY = H // 2 - 20
            demo.camera(dt)
            fundo.draw(demo.yaw, demo.focus[0], demo.clock)
            demo.draw()
            cx = W // 2
            ov = pygame.Surface((560, 420), pygame.SRCALPHA)
            pygame.draw.rect(ov, (8, 10, 32, 228), ov.get_rect(), border_radius=18)
            pygame.draw.rect(ov, (140, 150, 230, 140), ov.get_rect(), 2, border_radius=18)
            screen.blit(ov, (cx - 280, oy))
            a, b = FONTE_T.render("DNA", True, (90, 200, 255)), FONTE_T.render("pice 3D", True, (255, 120, 200))
            x0 = cx - (a.get_width() + b.get_width()) // 2
            screen.blit(a, (x0, oy - 138))
            screen.blit(b, (x0 + a.get_width(), oy - 138))
            texto("Simulador de transcrição: DNA → RNA", cx, oy - 42, FONTE_M, (200, 210, 255), True)
            mb["tab_a"].draw(mouse, on=(origem == "aleatoria"))
            mb["tab_d"].draw(mouse, on=(origem == "digitada"))
            mb["tab_w"].draw(mouse, on=(origem == "wolbachia"))
            if origem == "aleatoria":
                texto("Quantidade de bases nitrogenadas", cx, oy + 80, FONTE_M, (255, 255, 255), True)
                texto("digite o número (4 a 150) ou use os botões", cx, oy + 103, FONTE_P, (160, 170, 210), True)
                box = pygame.Rect(cx - 70, oy + 125, 140, 50)
                pygame.draw.rect(screen, (20, 26, 60), box, border_radius=10)
                pygame.draw.rect(screen, (120, 220, 255), box, 2, border_radius=10)
                cur = FONTE_G.render(qtxt + ("|" if int(demo.clock * 2) % 2 == 0 else ""), True, (255, 255, 255))
                screen.blit(cur, cur.get_rect(center=box.center))
                for k in ("minus", "plus", 12, 24, 48, 96):
                    mb[k].draw(mouse)
            elif origem == "digitada":
                texto("Digite a sequência de bases (somente A, T, C, G)", cx, oy + 80, FONTE_M, (255, 255, 255), True)
                texto("ex.: AATTCCGG  ·  até 150 bases  ·  Backspace apaga", cx, oy + 103, FONTE_P, (160, 170, 210), True)
                box = pygame.Rect(cx - 250, oy + 125, 500, 50)
                pygame.draw.rect(screen, (20, 26, 60), box, border_radius=10)
                pygame.draw.rect(screen, (120, 220, 255), box, 2, border_radius=10)
                vis, xx = stxt[-21:], box.x + 14
                if len(stxt) > 21:
                    texto("…", xx, box.y + 8, FONTE_G)
                    xx += 24
                for ch in vis:
                    screen.blit(letra(ch, 24, COR[ch]), (xx, box.y + 9))
                    xx += 20
                if int(demo.clock * 2) % 2 == 0:
                    pygame.draw.line(screen, (255, 255, 255), (xx + 2, box.y + 10), (xx + 2, box.y + 40), 2)
                texto(f"{len(stxt)} bases", cx, oy + 184, FONTE_P, (190, 255, 220), True)
                if stxt:
                    texto("RNA:", box.x, oy + 210, FONTE_M, (225, 200, 255))
                    xx = box.x + 50 + (24 if len(stxt) > 21 else 0)
                    for ch in vis:
                        screen.blit(letra(rnab[ch], 22, COR[rnab[ch]]), (xx, oy + 206))
                        xx += 20
                else:
                    texto("digite ao menos uma base para iniciar", cx, oy + 240, FONTE_P, (255, 140, 140), True)
            else:
                texto("Wolbachia - sequência predefinida", cx, oy + 80, FONTE_M, (255, 255, 255), True)
                texto(f"{len(WOLBACHIA)} bases (fita molde); o RNA é transcrito a partir dela", cx, oy + 103, FONTE_P, (160, 170, 210), True)
                for r in range(2):
                    for q in range(19):
                        ch = WOLBACHIA[r * 19 + q]
                        screen.blit(letra(ch, 24, COR[ch]), (cx - 266 + q * 28, oy + 135 + r * 34))
            mb["ini"].draw(mouse, on=True)
            mb["sair"].draw(mouse)
            texto("Enter inicia  ·  Tab alterna  ·  F11 tela cheia  ·  Esc sai", cx, oy + 390, FONTE_P, (160, 170, 210), True)
        else:
            keys = pygame.key.get_pressed()
            if sim.rna_on:
                if sim.vista == "video":
                    if rew_hold or keys[pygame.K_LEFT]:
                        sim.avancar(-2 * dt * sim.speed)
                        sim.playing = False
                    elif keys[pygame.K_RIGHT]:
                        sim.avancar(2 * dt * sim.speed)
                        sim.playing = False
                    elif sim.playing:
                        sim.avancar(dt * sim.speed)
                        if sim.tt >= sim.total:
                            sim.playing = False
                elif sim.playing:
                    sim.avancar(dt * sim.speed)
            mv = (keys[pygame.K_w] - keys[pygame.K_s], keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_q] - keys[pygame.K_e])
            if any(mv):
                v = 400 * dt * sim.dist / 700 * (3 if keys[pygame.K_LSHIFT] else 1)
                c, sn = math.cos(sim.yaw), math.sin(sim.yaw)
                sim.focus[0] += (-sn * mv[0] + c * mv[1]) * v
                sim.focus[2] += (c * mv[0] + sn * mv[1]) * v
                sim.focus[1] += mv[2] * v
                sim.follow, sim.anim = False, None
            sim.camera(dt)
            CY = (64 + painel_rect(sim).y) // 2
            fundo.draw(sim.yaw, sim.focus[0], sim.clock)
            sim.draw()
            hud(sim, mouse, info_aberta)
        pygame.display.flip()


if __name__ == "__main__":
    main()