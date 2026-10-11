# 🦁 Salominho | SalmoNela

Protótipo de jogo de estudos bíblicos em **Python + Pygame**.

## Versão 0.1

- Menu com o Salmão (imagem conceitual temporária).
- Mapa de Gênesis com dez fases esboçadas e uma acessível.
- Leitura de Gênesis 1:1–5 via `bible-api.com`, com cache local e fallback de 1 versículo.
- Quiz demonstrativo com 3 perguntas, explicações, resultados e XP.
- Projeto preparado para sprites transparentes e textos offline no futuro.

## Vinheta de abertura (v0.2)

Tema instrumental de aproximadamente **11,8 segundos**, em **Sol maior** a **112 BPM**. O jogo toca a vinheta na abertura; pressione **M** para silenciar ou tocar novamente.

`src/audio.py` sintetiza uma versão WAV automaticamente no primeiro acesso, sem numpy nem ffmpeg. Para usar o arranjo estéreo original, copie `salominho_vinheta_v01.ogg` do [pacote de áudio da vinheta](https://github.com/CarlSouza02/Salominho/tree/main/assets/audio) para `assets/audio/`; se existir, o jogo dá preferência ao OGG. O MIDI editável está no repositório.

## Executar no Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3-pygame python3-requests
git clone https://github.com/CarlSouza02/Salominho.git
cd Salominho
python3 main.py
```

No VS Code, selecione o interpretador `/usr/bin/python3` se o Pygame não for encontrado.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Estrutura

```text
main.py                    telas e loop Pygame
src/bible.py               cliente bíblico, cache e fallback
src/levels.py              fases planejadas e quiz demonstrativo
src/audio.py               reprodução e síntese offline da vinheta
assets/audio/              MIDI e instruções para OGG estéreo
assets/mascot/concept.png  miniatura conceitual (não é sprite transparente)
docs/ASSETS.md             especificações dos sprites e tiles
data/bible/README.md       plano de importação bíblica e créditos
tests/test_core.py         testes das funções de conteúdo
```

## Textos e licenças

A amostra offline de Gênesis 1:1 é da **Bíblia Livre (2018)** de Diego Santos, Mario Sérgio e Marco Teles, disponível em https://ebible.org/porbr2018/, sob licença **CC BY 4.0 Brasil**. O texto completo não está incluído.

O serviço `bible-api.com` é externo. Para o lançamento, a proposta é importar uma tradução aberta para SQLite.

## Roadmap

- [x] Menu em Pygame e mapa provisório
- [x] Uma fase com quiz e XP
- [x] Consulta bíblica demonstrativa com cache
- [ ] Criar sprites PNG transparentes e animações
- [ ] Desenhar tiles e mapa pixel art
- [ ] Integrar Bíblia offline em SQLite
- [ ] Desenvolver fases seguintes e salvar progresso
- [ ] Amigos, duelos e ranking


## Protótipo v0.3 — mundos e progresso

A base do jogo agora usa o catálogo real do Antigo Testamento:

- **39 mundos** cadastrados em `data/worlds/old_testament.json`;
- **929 capítulos/fases** navegáveis;
- seleção de mundos paginada;
- mapa de capítulos gerado dinamicamente para qualquer livro;
- progresso local persistente em `save/progress.json`;
- estados de capítulo: **não lido**, **lido** e **dominado**;
- Gênesis 1 continua como a primeira fase jogável do protótipo;
- devocional demonstrativo integrado.

O cenário atual do mapa é procedural e temporário. Cada livro receberá seu próprio `background.png` em `assets/worlds/old_testament/<livro>/`.


## Mapa rolável de Gênesis

O Mundo 1 agora possui um mapa vertical desenhado em Python/Pygame:

- 50 capítulos = 50 bolinhas/fases;
- trilha serpenteada conectando os capítulos;
- rolagem com roda do mouse, ↑/↓, W/S, PageUp/PageDown, Home e End;
- quatro regiões visuais: Criação/Éden, Noé/Babel, Patriarcas e José/Egito;
- marcos procedurais como árvore, arca, Torre de Babel, tendas e pirâmides;
- o progresso persistente continua definindo bolinhas não lidas, lidas e dominadas.

O mapa de outros livros continua usando o layout genérico enquanto os cenários específicos são produzidos.


## Pentateuco funcional

Os cinco primeiros mundos agora possuem mapa próprio no motor rolável:

- Gênesis: 50 fases;
- Êxodo: 40 fases;
- Levítico: 27 fases;
- Números: 36 fases;
- Deuteronômio: 34 fases.

Total: **187 capítulos/fases**.

Nesta etapa o foco é estrutural: bolinhas, trilha, clique, rolagem e progresso. A decoração específica de cada mapa será feita em seguida. Cada uma das cinco pastas também possui um `map_preview.svg` para visualização direta no GitHub.
