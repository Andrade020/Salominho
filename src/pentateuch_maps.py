"""Configurações dos mapas funcionais do Pentateuco."""
from __future__ import annotations

from dataclasses import dataclass

from src.map_layout import serpentine_nodes, world_height


@dataclass(frozen=True)
class BookMapConfig:
    id: str
    order: int
    name: str
    chapters: int
    background: tuple[int, int, int]
    accent: tuple[int, int, int]
    landmarks: dict[int, str]
    columns: int = 5
    row_spacing: int = 220

    @property
    def nodes(self):
        return serpentine_nodes(
            self.chapters,
            world_width=920,
            columns=self.columns,
            row_spacing=self.row_spacing,
        )

    @property
    def world_height(self) -> int:
        return world_height(
            self.chapters,
            columns=self.columns,
            row_spacing=self.row_spacing,
        )


PENTATEUCH_MAPS = {
    "genesis": BookMapConfig(
        id="genesis",
        order=1,
        name="Gênesis",
        chapters=50,
        background=(167, 210, 128),
        accent=(84, 153, 78),
        landmarks={
            1: "Criação",
            2: "Éden",
            3: "Queda",
            6: "Noé",
            11: "Babel",
            12: "Abraão",
            22: "Isaque",
            28: "Jacó",
            37: "José",
            50: "Fim",
        },
    ),
    "exodo": BookMapConfig(
        id="exodo",
        order=2,
        name="Êxodo",
        chapters=40,
        background=(224, 194, 132),
        accent=(193, 143, 72),
        landmarks={
            1: "Egito",
            3: "Sarça",
            12: "Páscoa",
            14: "Mar Vermelho",
            20: "Sinai",
            25: "Tabernáculo",
            32: "Bezerro",
            40: "Glória",
        },
    ),
    "levitico": BookMapConfig(
        id="levitico",
        order=3,
        name="Levítico",
        chapters=27,
        background=(224, 211, 181),
        accent=(150, 111, 95),
        landmarks={
            1: "Ofertas",
            8: "Sacerdócio",
            16: "Expiação",
            19: "Santidade",
            23: "Festas",
            25: "Jubileu",
            27: "Votos",
        },
    ),
    "numeros": BookMapConfig(
        id="numeros",
        order=4,
        name="Números",
        chapters=36,
        background=(211, 184, 123),
        accent=(151, 125, 74),
        landmarks={
            1: "Censo",
            6: "Nazireu",
            10: "Partida",
            13: "Espias",
            14: "Deserto",
            20: "Meribá",
            21: "Serpente",
            22: "Balaão",
            27: "Josué",
            36: "Heranças",
        },
    ),
    "deuteronomio": BookMapConfig(
        id="deuteronomio",
        order=5,
        name="Deuteronômio",
        chapters=34,
        background=(176, 193, 135),
        accent=(104, 124, 75),
        landmarks={
            1: "Revisão",
            5: "Mandamentos",
            6: "Shemá",
            8: "Memória",
            18: "Profeta",
            27: "Aliança",
            30: "Escolha",
            31: "Josué",
            34: "Moisés",
        },
    ),
}

PENTATEUCH_IDS = frozenset(PENTATEUCH_MAPS)
PENTATEUCH_CHAPTERS = sum(config.chapters for config in PENTATEUCH_MAPS.values())
