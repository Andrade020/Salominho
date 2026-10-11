# Mundo 01 — Gênesis

Primeiro mundo visual do Salominho.

## Sprites iniciais

O arquivo `sprites/genesis_spritesheet.png` é um spritesheet horizontal com **6 sprites de 64×64 px** e fundo transparente.

| Frame | Tema | Capítulo de referência |
|---:|---|---:|
| 0 | Criação / Sol | 1 |
| 1 | Jardim do Éden | 3 |
| 2 | Arca de Noé | 6 |
| 3 | Torre de Babel | 11 |
| 4 | Tenda de Abraão | 12 |
| 5 | Túnica de José | 37 |

O `main.py` já recorta esses frames e exibe os ícones acima das bolinhas correspondentes no mapa de Gênesis.

## Próximos assets

```text
01_genesis/
├── background.png
├── thumbnail.png
├── tileset.png
├── sprites/
│   └── genesis_spritesheet.png
└── props/
```

Os sprites atuais são placeholders em pixel art produzidos especificamente para o protótipo. O próximo passo é criar o `background.png` do mundo e depois substituir/expandir os sprites conforme a direção de arte definitiva.


## Visualização do mapa

O mapa de Gênesis é desenhado dinamicamente pelo Pygame em `src/map_art.py`.

Para conseguir **ver o mapa diretamente pelo GitHub**, sem executar o jogo, foi adicionada a prévia:

- [`map_preview.svg`](./map_preview.svg)

Ela mostra os **50 capítulos como 50 fases**, o caminho serpenteado e as regiões principais do mundo.
