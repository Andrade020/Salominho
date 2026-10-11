"""Catálogo de mundos bíblicos e utilitários de paginação."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class World:
    order: int
    id: str
    name: str
    chapters: int
    asset_dir: str
    status: str = "planned"


def load_old_testament(base: Path) -> list[World]:
    path = base / "data" / "worlds" / "old_testament.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [World(**item) for item in payload["worlds"]]


def chapter_range(world: World) -> range:
    return range(1, world.chapters + 1)


def page_count(total: int, per_page: int) -> int:
    if total <= 0:
        return 1
    return (total + per_page - 1) // per_page


def page_slice(items, page: int, per_page: int):
    max_page = page_count(len(items), per_page)
    page = max(0, min(page, max_page - 1))
    start = page * per_page
    return items[start:start + per_page], page, max_page
