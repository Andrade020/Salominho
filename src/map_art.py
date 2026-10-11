"""Cenário procedural de Gênesis desenhado com primitivas do Pygame."""
from __future__ import annotations

import pygame

GRASS = (167, 210, 128)
FLOOD = (149, 196, 141)
SAND = (224, 194, 132)
EGYPT = (211, 173, 91)
WATER = (71, 166, 220)
WATER_LIGHT = (156, 224, 245)
TRUNK = (105, 69, 42)
LEAF = (59, 123, 67)
LEAF_LIGHT = (84, 153, 78)


def _screen_y(world_y, viewport, scroll_y):
    return viewport.top + world_y - scroll_y


def _visible(y, viewport, margin=100):
    return viewport.top - margin <= y <= viewport.bottom + margin


def draw_tree(screen, x, y, viewport, scroll_y, scale=1.0):
    sy = _screen_y(y, viewport, scroll_y)
    if not _visible(sy, viewport):
        return
    trunk_w = int(12 * scale)
    trunk_h = int(34 * scale)
    pygame.draw.rect(
        screen,
        TRUNK,
        (x - trunk_w // 2, sy, trunk_w, trunk_h),
        border_radius=3,
    )
    r = int(25 * scale)
    pygame.draw.circle(screen, LEAF, (x, sy - int(12 * scale)), r)
    pygame.draw.circle(
        screen,
        LEAF_LIGHT,
        (x - int(14 * scale), sy - int(18 * scale)),
        int(17 * scale),
    )
    pygame.draw.circle(
        screen,
        LEAF_LIGHT,
        (x + int(15 * scale), sy - int(15 * scale)),
        int(16 * scale),
    )


def draw_tent(screen, x, y, viewport, scroll_y):
    sy = _screen_y(y, viewport, scroll_y)
    if not _visible(sy, viewport):
        return
    pygame.draw.polygon(
        screen,
        (181, 119, 69),
        [(x - 35, sy + 25), (x, sy - 28), (x + 35, sy + 25)],
    )
    pygame.draw.polygon(
        screen,
        (235, 202, 142),
        [(x, sy - 28), (x + 35, sy + 25), (x + 4, sy + 25)],
    )
    pygame.draw.line(screen, (83, 55, 39), (x, sy - 32), (x, sy + 27), 3)


def draw_ark(screen, x, y, viewport, scroll_y):
    sy = _screen_y(y, viewport, scroll_y)
    if not _visible(sy, viewport):
        return
    pygame.draw.ellipse(screen, (105, 70, 38), (x - 55, sy - 8, 110, 35))
    pygame.draw.rect(
        screen, (139, 88, 45), (x - 42, sy - 38, 84, 38), border_radius=5
    )
    pygame.draw.polygon(
        screen,
        (92, 61, 36),
        [(x - 50, sy - 38), (x, sy - 65), (x + 50, sy - 38)],
    )


def draw_tower(screen, x, y, viewport, scroll_y):
    sy = _screen_y(y, viewport, scroll_y)
    if not _visible(sy, viewport):
        return
    for i, (w, h) in enumerate([(70, 22), (58, 22), (46, 22), (34, 22)]):
        yy = sy + 30 - i * 20
        pygame.draw.rect(
            screen, (176, 151, 106), (x - w // 2, yy, w, h), border_radius=3
        )
        pygame.draw.rect(
            screen,
            (112, 95, 71),
            (x - w // 2, yy, w, h),
            2,
            border_radius=3,
        )


def draw_pyramid(screen, x, y, viewport, scroll_y, size=70):
    sy = _screen_y(y, viewport, scroll_y)
    if not _visible(sy, viewport):
        return
    pygame.draw.polygon(
        screen,
        (197, 155, 74),
        [
            (x - size // 2, sy + size // 3),
            (x, sy - size // 2),
            (x + size // 2, sy + size // 3),
        ],
    )
    pygame.draw.line(
        screen,
        (230, 199, 123),
        (x, sy - size // 2),
        (x, sy + size // 3),
        3,
    )


def draw_genesis_background(screen, viewport, scroll_y, virtual_height):
    """Quatro regiões: criação, dilúvio/Babel, patriarcas e Egito."""
    screen.set_clip(viewport)

    zones = [
        (0, 700, GRASS),
        (700, 1250, FLOOD),
        (1250, 2050, SAND),
        (2050, virtual_height + 200, EGYPT),
    ]
    for start, end, color in zones:
        sy = _screen_y(start, viewport, scroll_y)
        ey = _screen_y(end, viewport, scroll_y)
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(viewport.left, sy, viewport.width, ey - sy),
        )

    river = []
    for wy in range(50, virtual_height + 200, 120):
        x = viewport.left + 90 + ((wy // 120) % 4) * 32
        river.append((x, _screen_y(wy, viewport, scroll_y)))
    if len(river) >= 2:
        pygame.draw.lines(screen, WATER, False, river, 26)
        pygame.draw.lines(screen, WATER_LIGHT, False, river, 7)

    trees = [
        (120, 180), (260, 310), (790, 190), (860, 440), (180, 610),
        (760, 820), (160, 1020), (835, 1150), (235, 1370),
        (810, 1550), (135, 1760), (845, 1910),
    ]
    for x, wy in trees:
        draw_tree(screen, viewport.left + x, wy, viewport, scroll_y, 0.9)

    draw_tree(screen, viewport.left + 470, 230, viewport, scroll_y, 1.45)
    draw_ark(screen, viewport.left + 760, 910, viewport, scroll_y)
    draw_tower(screen, viewport.left + 230, 1190, viewport, scroll_y)
    draw_tent(screen, viewport.left + 760, 1450, viewport, scroll_y)
    draw_tent(screen, viewport.left + 300, 1700, viewport, scroll_y)

    draw_pyramid(screen, viewport.left + 760, 2260, viewport, scroll_y, 95)
    draw_pyramid(screen, viewport.left + 650, 2330, viewport, scroll_y, 70)
    draw_pyramid(screen, viewport.left + 850, 2390, viewport, scroll_y, 60)

    screen.set_clip(None)



def draw_pentateuch_background(screen, viewport, scroll_y, config):
    """Fundo funcional do Pentateuco.

    Gênesis preserva o cenário procedural já criado. Os outros quatro livros
    usam uma base simples por enquanto; a decoração será feita depois.
    """
    if config.id == "genesis":
        draw_genesis_background(
            screen,
            viewport,
            scroll_y,
            config.world_height,
        )
        return

    screen.set_clip(viewport)
    pygame.draw.rect(screen, config.background, viewport)

    # Faixas suaves ajudam a enxergar que o mapa continua durante a rolagem,
    # sem comprometer a futura direção de arte.
    stripe_h = 220
    for index, world_y in enumerate(range(0, config.world_height + stripe_h, stripe_h)):
        sy = _screen_y(world_y, viewport, scroll_y)
        if not _visible(sy, viewport, stripe_h):
            continue
        delta = 8 if index % 2 == 0 else -5
        stripe = tuple(
            max(0, min(255, channel + delta))
            for channel in config.background
        )
        pygame.draw.rect(
            screen,
            stripe,
            pygame.Rect(viewport.left, sy, viewport.width, stripe_h),
        )

    # Borda/linha lateral simples para diferenciar cada livro.
    pygame.draw.rect(
        screen,
        config.accent,
        pygame.Rect(viewport.left, viewport.top, 22, viewport.height),
    )
    pygame.draw.rect(
        screen,
        config.accent,
        pygame.Rect(viewport.right - 22, viewport.top, 22, viewport.height),
    )

    screen.set_clip(None)
