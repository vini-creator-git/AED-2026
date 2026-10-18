import math
import sys
from random import choice, uniform, random

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
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("DNApice 3D - Transcrição")
clock = pygame.time.Clock()
F = "segoeui,arial,dejavusans"
FONTE_P = pygame.font.SysFont(F, 14)
FONTE_M = pygame.font.SysFont(F, 16, bold=True)
FONTE_G = pygame.font.SysFont(F, 26, bold=True)
FONTE_T = pygame.font.SysFont(F, 66, bold=True)
cache = {}

SP, R, TW, FOC, CY = 26, 42, 0.62, 700, 290
NT_S = 1.3                      # nucleotideos por segundo (velocidade 1x)
T0, T1, T3 = 3.0, 2.0, 4.5      # duracao: iniciacao, bolha, terminacao
PAINEL = pygame.Rect(10, H - 240, W - 20, 106)
BARRA = pygame.Rect(20, H - 112, W - 40, 10)

ETAPAS = [
    ("1. Iniciação", "O fator sigma guia a RNA polimerase até o promotor, onde ela se liga ao DNA."),
    ("2. Abertura da bolha", "A RNA polimerase separa as duas fitas do DNA e expõe a fita molde."),
    ("3. Alongamento", "A polimerase desliza pela fita molde e encaixa ribonucleotídeos complementares "
                       "(A-U, T-A, C-G, G-C). O sigma se solta e a topoisomerase alivia a tensão à frente."),
    ("4. Terminação", "O fator Rho alcança a polimerase, solta o RNA e o DNA volta a se enrolar."),
    ("Concluído", "RNA pronto! Use o rebobinar para rever ou R para gerar uma nova fita."),
]


BETA, BETAP, ALFA, OMEGA = (70, 120, 235), (45, 185, 185), (150, 190, 255), (235, 130, 190)
# RNA polimerase: duas garras (beta / beta') em volta do canal do DNA, alfa e omega atras
POL = [((-10, -102, 0), 40, BETA), ((30, -92, 12), 34, BETA), ((-45, -85, -10), 32, BETA), ((62, -70, -6), 26, BETA),
       ((-25, -72, 28), 28, BETA), ((5, -112, -25), 28, BETA), ((78, -66, 0), 18, BETA),
       ((-10, 102, 0), 40, BETAP), ((32, 90, -12), 34, BETAP), ((-45, 86, 10), 32, BETAP), ((64, 70, 6), 26, BETAP),
       ((-22, 72, -28), 28, BETAP), ((8, 112, 25), 28, BETAP), ((78, 66, 0), 18, BETAP),
       ((-90, -85, 35), 22, ALFA), ((-90, 85, -35), 22, ALFA), ((-72, 0, 48), 14, OMEGA)]
SIG = [((-35, -62, 22), 17), ((-8, -54, 16), 15), ((18, -46, 10), 15), ((42, -38, 4), 13)]   # dominios do sigma
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
        cache[key] = pygame.font.SysFont("consolas,dejavusansmono,monospace", tam, bold=True).render(l, True, cor)
    return cache[key]


def texto(t, x, y, fonte=FONTE_P, cor=(235, 235, 245), centro=False):
    img, sh = fonte.render(t, True, cor), fonte.render(t, True, (0, 0, 0))
    if centro:
        x -= img.get_width() / 2
    screen.blit(sh, (x + 1, y + 1))
    screen.blit(img, (x, y))


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


# ------------------------------------------------------------------ fundo
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
            t = y / (H - 1)
            a, b, u = (topo, meio, t / 0.55) if t < 0.55 else (meio, fim, (t - 0.55) / 0.45)
            s.base.fill(tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3)), (0, y, W, 1))
        s.neb = [(sprite(380, (130, 60, 210), 90), 0.22, 0.35, 0.10), (sprite(340, (30, 180, 200), 75), 0.82, 0.78, 0.16),
                 (sprite(300, (230, 70, 150), 60), 0.7, 0.18, 0.08)]
        cores = [(150, 110, 255), (80, 220, 230), (255, 130, 190)]
        s.spr = [[sprite(r, c, 150) for r in (8, 14, 22)] for c in cores]
        s.part = [(random(), random(), 0.2 + 0.8 * random(), int(random() * 3)) for _ in range(60)]
        s.stars = [(random(), random(), random()) for _ in range(130)]
        s.vig = pygame.Surface((W, H), pygame.SRCALPHA)
        for i in range(70):
            pygame.draw.rect(s.vig, (0, 0, 0, int(120 * (1 - i / 70) ** 2)), (i, i, W - 2 * i, H - 2 * i), 1)

    def draw(s, yaw, fx, T):
        screen.blit(s.base, (0, 0))
        par = yaw * 200 + fx * 0.25
        for spr, x, y, d in s.neb:
            screen.blit(spr, ((x * W - par * d) % (W + 400) - 400 + 200 - spr.get_width() / 2 + 200 * 0,
                              y * H - spr.get_height() / 2 + math.sin(T * 0.2 + x * 9) * 15))
        for x, y, b in s.stars:
            v = int(90 + 120 * (0.5 + 0.5 * math.sin(T * (0.8 + b * 2) + b * 40)))
            pygame.draw.circle(screen, (v, v, min(255, v + 30)), (int((x * W - par * 0.05 * (1 + b)) % W), int(y * H)), 1)
        for x, y, d, k in s.part:
            spr = s.spr[k][0 if d < 0.45 else (1 if d < 0.8 else 2)]
            px = (x * (W + 300) - par * d) % (W + 300) - 150
            py = (y * (H + 200) - T * (5 + 14 * d)) % (H + 200) - 100
            screen.blit(spr, (px - spr.get_width() / 2, py - spr.get_height() / 2))
        screen.blit(s.vig, (0, 0))


# ------------------------------------------------------------------ simulacao
class Sim:
    def __init__(s, n, demo=False, seq=None):
        s.n, s.demo, s.seq = n, demo, seq
        s.d2 = n / NT_S
        s.total = T0 + T1 + s.d2 + T3
        s.yaw, s.pitch = 0.35, 0.25
        s.dist_u = s.dist = 1000.0 if demo else 700.0
        s.focus = [n * SP / 2 if demo else 0.0, 0.0, 0.0]
        s.follow, s.auto_rot = not demo, demo
        s.clock, s.i0 = 0.0, 0
        s.reset()

    def reset(s):
        n = s.n
        s.dna = list(s.seq) if s.seq else [choice("ATCG") for _ in range(n)]        # fita molde
        s.comp = [bases[b] for b in s.dna]                 # fita codificante
        s.rna = [rnab[b] for b in s.dna]
        s.ntp = [(uniform(-80, 80), uniform(110, 170) * choice([-1, 1]), uniform(-90, 90)) for _ in range(n)]
        s.playing, s.speed, s.pan_off, s.polx = True, 1.0, None, 0.0
        s.set_time(0)

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

    def disp(s):
        if s.prog >= s.n:
            return float(s.n)
        k = int(s.prog)
        return k + suave(s.prog - k)

    def camera(s, dt):
        s.clock += dt
        if s.auto_rot:
            s.yaw += dt * 0.25
        fit = 1.0
        if s.follow:
            tx = 0 if s.stage == 0 else (s.n * SP / 2 if s.stage >= 3 else s.disp() * SP)
            k = min(1, dt * 3)
            s.focus[0] += (tx - s.focus[0]) * k
            s.focus[1] -= s.focus[1] * k
            s.focus[2] -= s.focus[2] * k
            if s.stage >= 3:
                fit = max(1.0, (s.n * SP + 250) / 1000)
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
        return s.bub * math.exp(-((i * SP - s.polx) / (SP * 3.2)) ** 2)

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

        if not s.demo:
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
    def __init__(s, rect, label=None, icon=None):
        s.r, s.label, s.icon = pygame.Rect(rect), label, icon

    def draw(s, mouse, on=False):
        cor = (80, 110, 200) if s.r.collidepoint(mouse) else ((50, 140, 110) if on else (34, 44, 86))
        pygame.draw.rect(screen, cor, s.r, border_radius=8)
        pygame.draw.rect(screen, (150, 170, 255), s.r, 1, border_radius=8)
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


def quebra(t, larg, x, y):
    linha = ""
    for w in t.split():
        if FONTE_P.size(linha + w)[0] > larg:
            texto(linha, x, y)
            linha, y = "", y + 18
        linha += w + " "
    texto(linha, x, y)


def painel_fitas(sim):
    n, cw = sim.n, 21
    vis = (W - 250) // cw
    s = pygame.Surface(PAINEL.size, pygame.SRCALPHA)
    pygame.draw.rect(s, (8, 10, 30, 175), s.get_rect(), border_radius=10)
    pygame.draw.rect(s, (130, 140, 210, 110), s.get_rect(), 1, border_radius=10)
    screen.blit(s, PAINEL.topleft)
    if sim.pan_off is None:
        i0 = 0 if sim.stage < 2 else int(sim.disp()) - vis // 2
    else:
        i0 = sim.pan_off
    i0 = sim.i0 = max(0, min(i0, max(0, n - vis)))
    y1, y2, y3 = H - 234, H - 203, H - 172
    texto("Fita codificante 5'→3'", 22, y1 + 2, cor=FITA_COD)
    texto("Fita molde 3'→5'", 22, y2 + 2, cor=FITA_MOLDE)
    texto("RNA 5'→3'", 22, y3 + 2, cor=(225, 200, 255))
    nc = 0 if sim.stage < 2 else (int(sim.prog) if sim.stage == 2 else n)
    for j in range(i0, min(n, i0 + vis)):
        x = 215 + (j - i0) * cw
        screen.blit(letra(sim.comp[j], 20, COR[sim.comp[j]]), (x, y1))
        screen.blit(letra(sim.dna[j], 20, COR[sim.dna[j]]), (x, y2))
        linhas = 2 if sim.dna[j] in "AT" else 3
        for yb, ok in ((y1 + 22, True), (y2 + 22, j < nc)):
            if ok:
                for q in range(linhas):
                    yy = yb + 2 + q * 3 + (0 if linhas == 3 else 1)
                    pygame.draw.line(screen, PONTE[sim.dna[j]], (x + 2, yy), (x + 11, yy), 1)
        if j < nc:
            screen.blit(letra(sim.rna[j], 20, COR[sim.rna[j]]), (x, y3))
    if sim.stage == 2 and i0 <= int(sim.prog) < i0 + vis:
        pygame.draw.rect(screen, (255, 235, 120), (215 + (int(sim.prog) - i0) * cw - 3, y1 - 3, cw, 94), 1, border_radius=4)
    texto(f"bases {i0 + 1}–{min(n, i0 + vis)} de {n}  (scroll aqui para navegar)", W - 330, H - 154, cor=(160, 170, 210))


def hud(sim, btns, mouse):
    nome, desc = ETAPAS[sim.stage]
    texto("DNApice 3D" + ("  ·  Wolbachia" if sim.seq else ""), 20, 12, FONTE_G, (255, 255, 255))
    texto(nome, 20, 46, FONTE_G, (255, 220, 120))
    quebra(desc, 520, 20, 80)
    if sim.stage >= 2:
        texto(f"Nucleotídeos transcritos: {min(int(sim.prog), sim.n)}/{sim.n}", 20, 134, cor=(190, 255, 220))
    texto(f"Velocidade {sim.speed:.2f}x   |   Câmera: {'seguindo' if sim.follow else 'livre'}   |   "
          f"{'pausado' if not sim.playing else 'reproduzindo'}", W - 470, 14)
    painel_fitas(sim)
    d = [0, T0, T0 + T1, T0 + T1 + sim.d2, sim.total]
    for q, nm in enumerate(("Iniciação", "Bolha", "Alongamento", "Terminação")):
        x = BARRA.x + BARRA.w * d[q] / sim.total
        texto(nm, x + 3, H - 130, FONTE_P, (255, 220, 120) if sim.stage == q else (150, 160, 200))
        pygame.draw.line(screen, (150, 160, 210), (x, BARRA.y - 3), (x, BARRA.bottom + 3), 1)
    pygame.draw.rect(screen, (30, 36, 70), BARRA, border_radius=5)
    pygame.draw.rect(screen, (90, 200, 170), (BARRA.x, BARRA.y, BARRA.w * sim.tt / sim.total, BARRA.h), border_radius=5)
    pygame.draw.circle(screen, (255, 255, 255), (int(BARRA.x + BARRA.w * sim.tt / sim.total), BARRA.centery), 8)
    btns["play"].icon = "pause" if sim.playing else "play"
    btns["seg"].label = "Seguir: " + ("SIM" if sim.follow else "NÃO")
    for k, b in btns.items():
        b.draw(mouse, on=(k == "seg" and sim.follow))
    texto("Arrastar: girar 360°  |  Botão direito ou WASD: mover  |  Q/E: descer/subir  |  Scroll: zoom  |  Shift: mais rápido",
          20, H - 50, cor=(160, 170, 210))
    texto("←/→ (segure): rebobinar/avançar  |  Espaço: pausa  |  F: seguir  |  O: girar sozinho  |  R: nova fita/reiniciar  |  Esc: menu",
          20, H - 32, cor=(160, 170, 210))


def main():
    fundo = Fundo()
    demo = Sim(30, demo=True)
    sim, modo, qtxt, fonte = None, "menu", "24", "aleatoria"
    x = 20
    btns = {}
    for k, w, lab, ic in (("ini", 70, "Início", None), ("rew", 52, None, "rew"), ("back", 52, None, "back"),
                          ("play", 60, None, "pause"), ("fwd", 52, None, "fwd"), ("vm", 56, "Vel -", None),
                          ("vp", 56, "Vel +", None), ("seg", 130, "Seguir", None), ("menu", 80, "Menu", None)):
        btns[k] = Btn((x, H - 92, w, 34), lab, ic)
        x += w + 8
    mb = {"minus": Btn((W // 2 - 190, 285, 50, 50), "-"), "plus": Btn((W // 2 + 140, 285, 50, 50), "+"),
          "ini": Btn((W // 2 - 170, 425, 340, 56), "Iniciar simulação"), "sair": Btn((W // 2 - 170, 492, 340, 44), "Sair"),
          "tab_a": Btn((W // 2 - 250, 178, 245, 42), "Ver geração aleatória"),
          "tab_w": Btn((W // 2 + 5, 178, 245, 42), "Ver Wolbachia")}
    for i, v in enumerate((12, 24, 48, 96)):
        mb[v] = Btn((W // 2 - 170 + i * 88, 355, 78, 38), str(v))
    arrasta, rew_hold, scrub = None, False, False

    def iniciar():
        nonlocal sim, modo
        if fonte == "wolbachia":
            sim = Sim(len(WOLBACHIA), seq=WOLBACHIA)
        else:
            sim = Sim(max(4, min(int(qtxt or 24), 150)))
        modo = "sim"

    def scrub_to(mx):
        sim.set_time((mx - BARRA.x) / BARRA.w * sim.total)
        sim.playing = False

    while True:
        dt = min(clock.tick(60) / 1000, 0.05)
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if modo == "menu":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif e.key == pygame.K_RETURN:
                        iniciar()
                    elif e.key == pygame.K_TAB:
                        fonte = "wolbachia" if fonte == "aleatoria" else "aleatoria"
                    elif e.key == pygame.K_BACKSPACE and fonte == "aleatoria":
                        qtxt = qtxt[:-1]
                    elif e.unicode.isdigit() and len(qtxt) < 3 and fonte == "aleatoria":
                        qtxt += e.unicode
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    cur = int(qtxt or 24)
                    if mb["ini"].r.collidepoint(e.pos):
                        iniciar()
                    elif mb["sair"].r.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()
                    elif mb["tab_a"].r.collidepoint(e.pos):
                        fonte = "aleatoria"
                    elif mb["tab_w"].r.collidepoint(e.pos):
                        fonte = "wolbachia"
                    elif fonte == "aleatoria" and mb["minus"].r.collidepoint(e.pos):
                        qtxt = str(max(4, cur - 1))
                    elif fonte == "aleatoria" and mb["plus"].r.collidepoint(e.pos):
                        qtxt = str(min(150, cur + 1))
                    for v in (12, 24, 48, 96):
                        if fonte == "aleatoria" and mb[v].r.collidepoint(e.pos):
                            qtxt = str(v)
                continue
            # ---- modo simulacao ----
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_m):
                    modo = "menu"
                elif e.key == pygame.K_SPACE:
                    if sim.tt >= sim.total:
                        sim.set_time(0)
                    sim.playing = not sim.playing
                elif e.key == pygame.K_r:
                    sim.reset()
                elif e.key == pygame.K_f:
                    sim.follow, sim.pan_off, sim.dist_u = True, None, 700.0
                elif e.key == pygame.K_o:
                    sim.auto_rot = not sim.auto_rot
                elif e.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    sim.speed = min(4, sim.speed + 0.25)
                elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    sim.speed = max(0.25, sim.speed - 0.25)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    hit = next((k for k, b in btns.items() if b.r.collidepoint(e.pos)), None)
                    if hit == "ini":
                        sim.set_time(0)
                        sim.playing = True
                    elif hit == "rew":
                        rew_hold = True
                    elif hit == "back":
                        sim.set_time(sim.tt - 1 / NT_S)
                        sim.playing = False
                    elif hit == "fwd":
                        sim.set_time(sim.tt + 1 / NT_S)
                        sim.playing = False
                    elif hit == "play":
                        if sim.tt >= sim.total:
                            sim.set_time(0)
                        sim.playing = not sim.playing
                    elif hit == "vm":
                        sim.speed = max(0.25, sim.speed - 0.25)
                    elif hit == "vp":
                        sim.speed = min(4, sim.speed + 0.25)
                    elif hit == "seg":
                        sim.follow = not sim.follow
                        sim.pan_off = None
                    elif hit == "menu":
                        modo = "menu"
                    elif BARRA.inflate(0, 22).collidepoint(e.pos):
                        scrub = True
                        scrub_to(e.pos[0])
                    elif e.pos[1] < PAINEL.y:
                        arrasta = "orbita"
                elif e.button in (2, 3) and e.pos[1] < PAINEL.y:
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
                    sim.yaw += e.rel[0] * 0.008
                    sim.pitch = max(-1.45, min(1.45, sim.pitch + e.rel[1] * 0.008))
                elif arrasta == "pan":
                    sc, c, sn = sim.dist / 700, math.cos(sim.yaw), math.sin(sim.yaw)
                    sim.focus[0] -= c * e.rel[0] * sc
                    sim.focus[2] -= sn * e.rel[0] * sc
                    sim.focus[1] -= e.rel[1] * sc
                    sim.follow = False
            elif e.type == pygame.MOUSEWHEEL:
                if PAINEL.collidepoint(mouse):
                    sim.pan_off = sim.i0 - e.y * 3
                else:
                    sim.dist_u = max(160, min(3200, sim.dist_u * 0.9 ** e.y))

        if modo == "menu":
            demo.camera(dt)
            fundo.draw(demo.yaw, demo.focus[0], demo.clock)
            demo.draw()
            ov = pygame.Surface((560, 420), pygame.SRCALPHA)
            pygame.draw.rect(ov, (8, 10, 32, 228), ov.get_rect(), border_radius=18)
            pygame.draw.rect(ov, (140, 150, 230, 140), ov.get_rect(), 2, border_radius=18)
            screen.blit(ov, (W // 2 - 280, 160))
            a, b = FONTE_T.render("DNA", True, (90, 200, 255)), FONTE_T.render("pice 3D", True, (255, 120, 200))
            x0 = W // 2 - (a.get_width() + b.get_width()) // 2
            screen.blit(a, (x0, 28))
            screen.blit(b, (x0 + a.get_width(), 28))
            texto("Simulador de transcrição: DNA → RNA", W // 2, 112, FONTE_M, (200, 210, 255), True)
            mb["tab_a"].draw(mouse, on=(fonte == "aleatoria"))
            mb["tab_w"].draw(mouse, on=(fonte == "wolbachia"))
            if fonte == "aleatoria":
                texto("Quantidade de bases nitrogenadas", W // 2, 240, FONTE_M, (255, 255, 255), True)
                texto("digite o número (4 a 150) ou use os botões", W // 2, 262, FONTE_P, (160, 170, 210), True)
                box = pygame.Rect(W // 2 - 70, 285, 140, 50)
                pygame.draw.rect(screen, (20, 26, 60), box, border_radius=10)
                pygame.draw.rect(screen, (120, 220, 255), box, 2, border_radius=10)
                cur = FONTE_G.render(qtxt + ("|" if int(demo.clock * 2) % 2 == 0 else ""), True, (255, 255, 255))
                screen.blit(cur, cur.get_rect(center=box.center))
                for k in ("minus", "plus", 12, 24, 48, 96):
                    mb[k].draw(mouse)
            else:
                texto("Wolbachia - sequência predefinida", W // 2, 240, FONTE_M, (255, 255, 255), True)
                texto(f"{len(WOLBACHIA)} bases (fita molde); o RNA é transcrito a partir dela", W // 2, 262, FONTE_P, (160, 170, 210), True)
                for r in range(2):
                    for q in range(19):
                        ch = WOLBACHIA[r * 19 + q]
                        screen.blit(letra(ch, 24, COR[ch]), (W // 2 - 266 + q * 28, 295 + r * 34))
            mb["ini"].draw(mouse, on=True)
            mb["sair"].draw(mouse)
            texto("Enter inicia  |  Tab alterna o modo  |  Esc sai", W // 2, 550, FONTE_P, (160, 170, 210), True)
        else:
            keys = pygame.key.get_pressed()
            if rew_hold or keys[pygame.K_LEFT]:
                sim.set_time(sim.tt - 2 * dt * sim.speed)
                sim.playing = False
            elif keys[pygame.K_RIGHT]:
                sim.set_time(sim.tt + 2 * dt * sim.speed)
                sim.playing = False
            elif sim.playing:
                sim.set_time(sim.tt + dt * sim.speed)
                if sim.tt >= sim.total:
                    sim.playing = False
            mv = (keys[pygame.K_w] - keys[pygame.K_s], keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_q] - keys[pygame.K_e])
            if any(mv):
                v = 400 * dt * sim.dist / 700 * (3 if keys[pygame.K_LSHIFT] else 1)
                c, sn = math.cos(sim.yaw), math.sin(sim.yaw)
                sim.focus[0] += (-sn * mv[0] + c * mv[1]) * v
                sim.focus[2] += (c * mv[0] + sn * mv[1]) * v
                sim.focus[1] += mv[2] * v
                sim.follow = False
            sim.camera(dt)
            fundo.draw(sim.yaw, sim.focus[0], sim.clock)
            sim.draw()
            hud(sim, btns, mouse)
        pygame.display.flip()


if __name__ == "__main__":
    main()
