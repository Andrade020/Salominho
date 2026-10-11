# 🦁 Salominho

Jogo educativo de estudos bíblicos em **Python + Pygame**, com progressão por livros e capítulos da Bíblia.

## Versão atual

**v0.4.0 — Mapas do Pentateuco**

Esta versão consolida a estrutura de mundos, progresso persistente e os cinco primeiros mapas do Antigo Testamento.

### Estado atual

- **39 mundos** do Antigo Testamento cadastrados;
- **929 capítulos/fases** disponíveis na estrutura;
- progresso local em `save/progress.json`;
- estados de capítulo: **pendente**, **concluído** e **dominado**;
- seleção de mundos paginada;
- mapas roláveis;
- Gênesis 1 com leitura e quiz demonstrativos;
- sistema de áudio/vinheta;
- **Pentateuco funcional com 187 fases**:
  - Gênesis: 50;
  - Êxodo: 40;
  - Levítico: 27;
  - Números: 36;
  - Deuteronômio: 34.

## Direção visual dos mapas

A arquitetura definida para os mapas é:

```text
background pixel-art do livro
          +
trilha e capítulos desenhados pelo Python
          +
estado dinâmico do progresso
```

O **cenário artístico** deve ficar em um `background.png` próprio de cada livro.  
O Python/Pygame desenha por cima:

- caminho entre fases;
- número do capítulo;
- 🔴 capítulo pendente;
- 🔵 capítulo concluído;
- ⭐ capítulo dominado, quando aplicável.

Isso permite manter o mapa visualmente rico sem precisar gerar uma nova imagem sempre que o progresso do jogador mudar.

### Temas do Pentateuco

| Mundo | Tema visual |
|---|---|
| **Gênesis** | Criação e Éden → Queda/Caim/Noé → Babel/Patriarcas → José/Egito |
| **Êxodo** | Egito/opressão → Moisés → Pragas/Páscoa → Mar Vermelho → Deserto/maná → Sinai/Tabernáculo |
| **Levítico** | Tabernáculo, altar, tendas, sacerdócio e utensílios sagrados |
| **Números** | Deserto, grande acampamento, montanhas e peregrinação |
| **Deuteronômio** | Planícies de Moabe, Jordão, Canaã e Monte Nebo |

> Os arquivos `map_generated.png` atuais são **protótipos técnicos**. Eles servem para validar a estrutura, quantidade de fases e geração por código, mas **não representam a arte final** dos mapas.

## Estrutura principal

```text
Salominho/
├── main.py
├── VERSION
│
├── src/
│   ├── audio.py
│   ├── bible.py
│   ├── levels.py
│   ├── map_art.py
│   ├── map_layout.py
│   ├── pentateuch_maps.py
│   ├── progress.py
│   └── worlds.py
│
├── tools/
│   └── generate_pentateuch_maps.py
│
├── data/
│   ├── bible/
│   └── worlds/
│       └── old_testament.json
│
├── assets/
│   ├── audio/
│   ├── mascot/
│   └── worlds/
│       └── old_testament/
│           ├── 01_genesis/
│           ├── 02_exodo/
│           ├── 03_levitico/
│           ├── 04_numeros/
│           └── 05_deuteronomio/
│
├── save/
└── tests/
```

## Executar

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3-pygame python3-requests python3-pil

git clone https://github.com/CarlSouza02/Salominho.git
cd Salominho
python3 main.py
```

Também é possível instalar as dependências listadas no projeto:

```bash
pip install -r requirements.txt
```

## Gerar os mapas técnicos do Pentateuco

```bash
python3 tools/generate_pentateuch_maps.py
```

Saídas:

```text
assets/worlds/old_testament/01_genesis/map_generated.png
assets/worlds/old_testament/02_exodo/map_generated.png
assets/worlds/old_testament/03_levitico/map_generated.png
assets/worlds/old_testament/04_numeros/map_generated.png
assets/worlds/old_testament/05_deuteronomio/map_generated.png
```

Gerar apenas um livro:

```bash
python3 tools/generate_pentateuch_maps.py --only exodo
```

Definir capítulos concluídos:

```bash
python3 tools/generate_pentateuch_maps.py \
  --completed genesis=1-12 \
  --completed exodo=1-4,8
```

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Bíblia

A implementação atual usa uma consulta demonstrativa ao `bible-api.com` e cache local.

O fallback de Gênesis 1:1 utiliza a **Bíblia Livre (2018)**, de Diego Santos, Mario Sérgio e Marco Teles, disponibilizada pelo eBible sob licença **CC BY 4.0 Brasil**.

Para uma versão de produção, o plano é utilizar uma tradução licenciada/aberta armazenada localmente, preferencialmente em SQLite.

## Áudio

A vinheta de abertura é controlada por `src/audio.py`.

- WAV pode ser sintetizado localmente;
- existe MIDI editável no repositório;
- se `assets/audio/salominho_vinheta_v01.ogg` estiver presente, o jogo pode priorizar essa versão.

## Roadmap da v0.4.x

- [x] catálogo dos 39 livros do Antigo Testamento;
- [x] progresso persistente;
- [x] mapas roláveis;
- [x] Pentateuco com 187 fases;
- [x] gerador técnico em Python;
- [ ] substituir os mapas técnicos por **backgrounds pixel-art finais**;
- [ ] integrar os backgrounds finais ao Pygame;
- [ ] manter bolinhas/trilha dinâmicas sobre a arte;
- [ ] preencher leitura, quiz e devocional por capítulo;
- [ ] Bíblia offline;
- [ ] sprites definitivos do Salominho;
- [ ] modo EBD/gincana.

## Histórico resumido

- **v0.1**: menu, Gênesis 1, quiz e XP.
- **v0.2**: vinheta e áudio.
- **v0.3**: 39 mundos, 929 capítulos e progresso persistente.
- **v0.4.0**: mapas do Pentateuco, 187 fases e definição da arquitetura visual final.
