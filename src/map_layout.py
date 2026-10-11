"""Layout visual dos capítulos nos mapas dos livros."""
from __future__ import annotations

from dataclasses import dataclass


def layout_chapter_nodes(chapters, area, cols=5):
    """Distribui capítulos em uma trilha serpenteada."""
    chapters = list(chapters)
    if not chapters:
        return []

    left, top, width, height = area
    rows = (len(chapters) + cols - 1) // cols

    margin_x = 85
    margin_y = 55
    usable_width = width - 2 * margin_x
    usable_height = height - 2 * margin_y

    step_x = usable_width // max(cols - 1, 1)
    step_y = usable_height // max(rows - 1, 1) if rows > 1 else 0

    nodes = []
    for idx, chapter in enumerate(chapters):
        row = idx // cols
        col = idx % cols
        display_col = col if row % 2 == 0 else (cols - 1 - col)

        x = left + margin_x + display_col * step_x
        y = top + margin_y + row * step_y

        nodes.append({"chapter": chapter, "x": x, "y": y})

    return nodes


def build_path_segments(nodes):
    """Retorna segmentos ligando uma fase à próxima."""
    return [
        ((a["x"], a["y"]), (b["x"], b["y"]))
        for a, b in zip(nodes, nodes[1:])
    ]


@dataclass(frozen=True)
class ChapterNode:
    chapter: int
    x: int
    y: int


def serpentine_nodes(
    total_chapters: int,
    *,
    world_width: int = 920,
    columns: int = 5,
    left_margin: int = 105,
    right_margin: int = 105,
    top_margin: int = 150,
    row_spacing: int = 235,
) -> list[ChapterNode]:
    """Cria uma trilha vertical em zigue-zague."""
    if total_chapters <= 0:
        return []
    if columns < 2:
        raise ValueError("columns deve ser >= 2")

    usable_width = world_width - left_margin - right_margin
    step_x = usable_width / (columns - 1)
    nodes = []

    for index in range(total_chapters):
        row = index // columns
        col = index % columns
        visual_col = col if row % 2 == 0 else columns - 1 - col
        x = round(left_margin + visual_col * step_x)
        y = top_margin + row * row_spacing
        nodes.append(ChapterNode(index + 1, x, y))

    return nodes


def path_segments(nodes: list[ChapterNode]):
    """Pares de pontos que formam a trilha das fases."""
    return [
        ((a.x, a.y), (b.x, b.y))
        for a, b in zip(nodes, nodes[1:])
    ]


def world_height(
    total_chapters: int,
    *,
    columns: int = 5,
    row_spacing: int = 235,
) -> int:
    """Altura virtual necessária para o mapa rolável."""
    if total_chapters <= 0:
        return 680
    rows = (total_chapters + columns - 1) // columns
    return max(680, 220 + rows * row_spacing)
