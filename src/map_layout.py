"""Layout visual dos capítulos nos mapas dos livros."""
from __future__ import annotations


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
