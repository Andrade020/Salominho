"""Salominho: protótipo desktop em Pygame.

Fluxo atual:
Início -> seleção de mundo -> capítulos -> detalhe -> leitura/quiz.
"""
from __future__ import annotations

import math
from pathlib import Path

import pygame

from src.audio import play_intro
from src.bible import get_creation_passage
from src.levels import QUESTIONS
from src.progress import Progress
from src.worlds import load_old_testament, page_slice

BASE = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 1024, 680, 60

INK = (50, 43, 42)
DARK = (48, 70, 66)
CREAM = (250, 244, 231)
PAPER = (255, 251, 242)
GOLD = (244, 188, 73)
GREEN = (79, 128, 93)
BLUE = (74, 142, 210)
MUTED = (120, 112, 100)
LOCKED = (174, 170, 158)

GENESIS_LANDMARKS = {1: 0, 3: 1, 6: 2, 11: 3, 12: 4, 37: 5}


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words, result, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if line and font.size(trial)[0] > max_width:
            result.append(line)
            line = word
        else:
            line = trial
    if line:
        result.append(line)
    return result


class Game:
    WORLDS_PER_PAGE = 12
    CHAPTERS_PER_PAGE = 20

    def __init__(self, passage: dict):
        pygame.init()
        pygame.display.set_caption("Salominho | Jornada Bíblica")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("dejavusans", 23)
        self.small = pygame.font.SysFont("dejavusans", 17)
        self.tiny = pygame.font.SysFont("dejavusans", 14)
        self.large = pygame.font.SysFont("dejavusans", 42, bold=True)
        self.bold = pygame.font.SysFont("dejavusans", 24, bold=True)

        self.passage = passage
        self.worlds = load_old_testament(BASE)
        self.current_world = self.worlds[0]
        self.current_chapter = 1
        self.world_page = 0
        self.chapter_page = 0

        self.progress = Progress(BASE / "save" / "progress.json")
        self.page = "home"
        self.question_index = 0
        self.correct_count = 0
        self.answered = False
        self.selected = None
        self.buttons = []
        self.message = ""

        self.audio_on = play_intro(pygame, BASE)
        art = BASE / "assets" / "mascot" / "idle_01.png"
        if not art.exists():
            art = BASE / "assets" / "mascot" / "concept.png"
        try:
            self.mascot = pygame.image.load(str(art)).convert_alpha()
            self.mascot = pygame.transform.scale(self.mascot, (210, 210))
        except (pygame.error, FileNotFoundError):
            self.mascot = None

        # Primeiros sprites reais do Mundo Gênesis.
        self.genesis_sprites = []
        sheet_path = (
            BASE / "assets" / "worlds" / "old_testament" / "01_genesis"
            / "sprites" / "genesis_spritesheet.png"
        )
        if sheet_path.is_file():
            try:
                sheet = pygame.image.load(str(sheet_path)).convert_alpha()
                for index in range(6):
                    frame = sheet.subsurface(
                        pygame.Rect(index * 64, 0, 64, 64)
                    ).copy()
                    self.genesis_sprites.append(
                        pygame.transform.scale(frame, (40, 40))
                    )
            except pygame.error as exc:
                print(f"Não foi possível carregar os sprites de Gênesis: {exc}")

    @property
    def xp(self) -> int:
        return self.progress.xp

    def text(self, msg, x, y, color=INK, font=None):
        surf = (font or self.font).render(str(msg), True, color)
        self.screen.blit(surf, (x, y))

    def centered_text(self, msg, rect, color=INK, font=None):
        surf = (font or self.font).render(str(msg), True, color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def panel(self, rect, color=PAPER, radius=20):
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)
        pygame.draw.rect(self.screen, (226, 211, 183), rect, 2, border_radius=radius)

    def button(self, title, rect, action, bg=GOLD, font=None):
        active = rect.collidepoint(pygame.mouse.get_pos())
        draw_bg = tuple(min(255, c + 9) for c in bg) if active else bg
        pygame.draw.rect(self.screen, draw_bg, rect, border_radius=13)
        pygame.draw.rect(self.screen, INK, rect, 2, border_radius=13)
        self.centered_text(title, rect, INK, font or self.bold)
        self.buttons.append((rect, action))

    def mascot_at(self, x, y, size=210):
        if self.mascot is not None:
            mascot = self.mascot
            if mascot.get_width() != size:
                mascot = pygame.transform.scale(self.mascot, (size, size))
            bob = int(4 * math.sin(pygame.time.get_ticks() / 480))
            self.screen.blit(mascot, (x, y + bob))
        else:
            pygame.draw.circle(self.screen, GOLD, (x + size // 2, y + size // 2), size // 2)
            self.text("Leão", x + size // 3, y + size // 2)

    def heading(self, title, subtitle=None):
        self.text(title, 48, 29, INK, self.large)
        self.text(f"XP: {self.xp}", WIDTH - 155, 39, DARK, self.bold)
        if subtitle:
            self.text(subtitle, 50, 82, MUTED, self.small)
        self.text("M: som " + ("ON" if self.audio_on else "OFF"), WIDTH - 173, 86, MUTED, self.small)

    def go(self, page):
        self.page = page
        self.message = ""

    # ------------------------------------------------------------------
    # TELAS
    # ------------------------------------------------------------------

    def home(self):
        self.heading("Salominho", "Jornada Bíblica")
        self.panel(pygame.Rect(48, 132, 928, 468))
        self.mascot_at(100, 235)

        self.text("Sua jornada pela Bíblia começa aqui.", 397, 222, DARK, self.bold)
        self.text("39 mundos do Antigo Testamento já cadastrados.", 397, 271)
        self.text("Cada livro é um mundo e cada capítulo é uma fase.", 397, 309, MUTED, self.small)

        self.button(
            "CONTINUAR EM GÊNESIS",
            pygame.Rect(414, 365, 440, 62),
            self.open_genesis,
            GREEN,
        )
        self.button(
            "SELECIONAR MUNDO",
            pygame.Rect(414, 452, 440, 62),
            lambda: self.go("world_select"),
            GOLD,
        )

        self.text(
            "Protótipo v0.3 • progresso salvo localmente",
            55, 626, MUTED, self.small
        )

    def world_select(self):
        visible, page, pages = page_slice(
            self.worlds, self.world_page, self.WORLDS_PER_PAGE
        )
        self.world_page = page
        self.heading(
            "Antigo Testamento",
            f"Escolha um mundo • página {page + 1}/{pages}"
        )

        cols = 4
        start_x, start_y = 55, 142
        card_w, card_h = 217, 118
        gap_x, gap_y = 21, 22

        for i, world in enumerate(visible):
            row, col = divmod(i, cols)
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)
            rect = pygame.Rect(x, y, card_w, card_h)

            is_genesis = world.id == "genesis"
            color = (228, 239, 219) if is_genesis else PAPER
            self.panel(rect, color, 14)
            self.text(f"{world.order:02d}", x + 13, y + 10, MUTED, self.tiny)
            self.text(world.name, x + 13, y + 33, DARK, self.bold)
            self.text(f"{world.chapters} capítulos", x + 13, y + 70, MUTED, self.small)
            self.text("EM PRODUÇÃO" if is_genesis else "PLANEJADO",
                      x + 13, y + 94,
                      GREEN if is_genesis else MUTED, self.tiny)
            self.buttons.append((rect, lambda w=world: self.open_world(w)))

        if page > 0:
            self.button("◀", pygame.Rect(55, 602, 75, 48), self.prev_world_page, PAPER)
        if page < pages - 1:
            self.button("▶", pygame.Rect(894, 602, 75, 48), self.next_world_page, PAPER)

        self.button("INÍCIO", pygame.Rect(419, 602, 185, 48), lambda: self.go("home"), PAPER)

    def world_map(self):
        world = self.current_world
        chapters = list(range(1, world.chapters + 1))
        visible, page, pages = page_slice(
            chapters, self.chapter_page, self.CHAPTERS_PER_PAGE
        )
        self.chapter_page = page
        read_count, mastered_count = self.progress.count_world(world.id, world.chapters)

        self.heading(
            f"Mundo {world.order}: {world.name}",
            f"{world.chapters} capítulos • lidos {read_count} • dominados {mastered_count}"
        )

        # Fundo procedural temporário, será substituído por background.png do livro.
        pygame.draw.rect(self.screen, (221, 233, 196), pygame.Rect(42, 118, 940, 470), border_radius=24)
        pygame.draw.rect(self.screen, (198, 178, 127), pygame.Rect(90, 305, 840, 76), border_radius=38)

        cols = 5
        start_x, start_y = 128, 177
        gap_x, gap_y = 181, 96

        for i, chapter in enumerate(visible):
            row, col = divmod(i, cols)
            x = start_x + col * gap_x
            y = start_y + row * gap_y
            state = self.progress.chapter(world.id, chapter)

            if state["mastered"]:
                fill = GOLD
            elif state["read"]:
                fill = BLUE
            else:
                fill = LOCKED

            pygame.draw.circle(self.screen, fill, (x, y), 30)
            pygame.draw.circle(self.screen, DARK, (x, y), 30, 3)
            label = self.small.render(str(chapter), True, INK)
            self.screen.blit(label, label.get_rect(center=(x, y)))

            # Marcos visuais de algumas histórias principais de Gênesis.
            if (
                world.id == "genesis"
                and chapter in GENESIS_LANDMARKS
                and self.genesis_sprites
            ):
                sprite_index = GENESIS_LANDMARKS[chapter]
                if sprite_index < len(self.genesis_sprites):
                    self.screen.blit(
                        self.genesis_sprites[sprite_index],
                        (x - 20, y - 72),
                    )

            hit = pygame.Rect(x - 31, y - 31, 62, 62)
            self.buttons.append((hit, lambda c=chapter: self.open_chapter(c)))

        self.text(
            f"Capítulos {visible[0] if visible else 0}–{visible[-1] if visible else 0}",
            445, 551, DARK, self.small
        )

        if page > 0:
            self.button("◀", pygame.Rect(52, 608, 75, 45), self.prev_chapter_page, PAPER)
        if page < pages - 1:
            self.button("▶", pygame.Rect(897, 608, 75, 45), self.next_chapter_page, PAPER)

        self.button("MUNDOS", pygame.Rect(414, 608, 196, 45), lambda: self.go("world_select"), PAPER)

        self.text("cinza = não lido", 145, 613, MUTED, self.tiny)
        self.text("azul = lido", 655, 613, BLUE, self.tiny)
        self.text("dourado = dominado", 745, 613, GOLD, self.tiny)

    def chapter_detail(self):
        world = self.current_world
        chapter = self.current_chapter
        state = self.progress.chapter(world.id, chapter)

        self.heading(f"{world.name} {chapter}", "Detalhes da fase")
        self.panel(pygame.Rect(70, 145, 884, 420))

        self.text(f"Mundo: {world.name}", 118, 191, DARK, self.bold)
        self.text(f"Capítulo: {chapter}/{world.chapters}", 118, 231)

        status = "Dominado" if state["mastered"] else "Lido" if state["read"] else "Não iniciado"
        self.text(f"Status: {status}", 118, 278, DARK)

        if world.id == "genesis" and chapter == 1:
            self.text("Protótipo jogável: A Criação", 118, 326, GREEN, self.bold)
            self.button("LER", pygame.Rect(118, 398, 220, 62), lambda: self.go("read"), GREEN)
            self.button("QUIZ", pygame.Rect(382, 398, 220, 62), self.begin_quiz, GOLD)
            self.button("DEVOCIONAL", pygame.Rect(646, 398, 220, 62), self.devotional, BLUE)
        else:
            self.text("Conteúdo desta fase será adicionado durante a produção do mundo.", 118, 342, MUTED, self.small)
            self.button("VOLTAR AO MAPA", pygame.Rect(340, 423, 345, 62), lambda: self.go("map"), PAPER)

        if self.message:
            self.text(self.message, 118, 510, GREEN, self.small)

    def reading(self):
        self.heading("Gênesis 1", "Leitura demonstrativa")
        self.panel(pygame.Rect(53, 118, 910, 474))
        self.text(self.passage["reference"], 78, 139, DARK, self.bold)

        y = 198
        for verse in self.passage["verses"][:5]:
            line = f'{verse["number"]}. {verse["text"]}'
            for subline in wrap_text(line, self.font, 815):
                if y > 440:
                    break
                self.text(subline, 79, y)
                y += 34
            y += 9
            if y > 440:
                break

        self.text(self.passage["translation"], 78, 500, MUTED, self.small)
        self.text("Protótipo: a versão final exibirá o capítulo completo.", 78, 530, MUTED, self.tiny)

        self.button("CONCLUIR LEITURA", pygame.Rect(535, 610, 405, 48), self.finish_reading, GREEN)
        self.button("MAPA", pygame.Rect(53, 610, 174, 48), lambda: self.go("map"), PAPER)

    def quiz(self):
        q = QUESTIONS[self.question_index]
        self.heading(f"Quiz {self.question_index + 1}/{len(QUESTIONS)}", "Gênesis 1")
        self.panel(pygame.Rect(52, 125, 918, 478))
        self.text(q["prompt"], 76, 162, DARK, self.bold)

        for idx, option in enumerate(q["choices"]):
            rect = pygame.Rect(89, 228 + idx * 78, 830, 59)
            color = (235, 225, 203)
            if self.answered and idx == q["correct"]:
                color = (160, 222, 163)
            elif self.answered and idx == self.selected:
                color = (245, 163, 160)
            self.button(
                f"{chr(65 + idx)}) {option}",
                rect,
                lambda idx=idx: self.answer(idx),
                color,
            )

        if self.answered:
            self.text(q["explanation"], 75, 563, DARK, self.small)
            self.button("PRÓXIMA", pygame.Rect(694, 617, 230, 45), self.next_question)

    def result(self):
        mastered = self.correct_count == len(QUESTIONS)
        self.heading("Fase concluída!", "Gênesis 1")
        self.panel(pygame.Rect(53, 139, 918, 446))
        self.mascot_at(116, 242, 190)

        self.text(f"Acertos: {self.correct_count}/{len(QUESTIONS)}", 421, 242, DARK, self.bold)
        self.text(f"XP total: {self.xp}", 421, 292, DARK, self.bold)
        self.text(
            "Capítulo DOMINADO ★" if mastered else "Tente novamente para dominar o capítulo.",
            421, 349,
            GREEN if mastered else MUTED,
            self.bold if mastered else self.small,
        )
        self.button("VOLTAR AO MAPA", pygame.Rect(421, 421, 390, 61), lambda: self.go("map"))

    def devotional_screen(self):
        self.heading("Devocional", "Gênesis 1")
        self.panel(pygame.Rect(72, 145, 880, 423))
        self.text("Criados com propósito", 118, 192, DARK, self.bold)
        lines = [
            "A criação nos lembra que a vida não é um acidente.",
            "O texto começa apresentando Deus como Criador e origem de tudo.",
            "Observe hoje algo da criação e agradeça conscientemente por isso.",
        ]
        y = 252
        for line in lines:
            for wrapped in wrap_text(line, self.font, 760):
                self.text(wrapped, 118, y)
                y += 38
            y += 8
        self.text("Devocional demonstrativo original do Salominho.", 118, 485, MUTED, self.small)
        self.button("VOLTAR", pygame.Rect(392, 599, 240, 50), lambda: self.go("chapter"), PAPER)

    # ------------------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------------------

    def open_genesis(self):
        self.open_world(self.worlds[0])

    def open_world(self, world):
        self.current_world = world
        self.chapter_page = 0
        self.go("map")

    def open_chapter(self, chapter):
        self.current_chapter = chapter
        self.go("chapter")

    def prev_world_page(self):
        self.world_page = max(0, self.world_page - 1)

    def next_world_page(self):
        self.world_page += 1

    def prev_chapter_page(self):
        self.chapter_page = max(0, self.chapter_page - 1)

    def next_chapter_page(self):
        self.chapter_page += 1

    def finish_reading(self):
        first = self.progress.mark_read("genesis", 1, 20)
        self.message = "+20 XP • capítulo marcado como lido" if first else "Capítulo já estava marcado como lido"
        self.current_world = self.worlds[0]
        self.current_chapter = 1
        self.go("chapter")
        self.message = "+20 XP • capítulo marcado como lido" if first else "Capítulo já estava marcado como lido"

    def devotional(self):
        self.go("devotional")

    def begin_quiz(self):
        self.current_world = self.worlds[0]
        self.current_chapter = 1
        self.question_index = 0
        self.correct_count = 0
        self.selected = None
        self.answered = False
        self.go("quiz")

    def answer(self, index):
        if self.answered:
            return
        self.selected = index
        self.answered = True
        if index == QUESTIONS[self.question_index]["correct"]:
            self.correct_count += 1

    def next_question(self):
        if not self.answered:
            return
        self.question_index += 1
        self.selected = None
        self.answered = False

        if self.question_index >= len(QUESTIONS):
            self.progress.record_quiz(
                "genesis",
                1,
                self.correct_count,
                len(QUESTIONS),
                xp_per_correct=10,
                mastery_bonus=20,
            )
            self.go("result")

    # ------------------------------------------------------------------
    # LOOP
    # ------------------------------------------------------------------

    def run(self):
        screens = {
            "home": self.home,
            "world_select": self.world_select,
            "map": self.world_map,
            "chapter": self.chapter_detail,
            "read": self.reading,
            "quiz": self.quiz,
            "result": self.result,
            "devotional": self.devotional_screen,
        }

        while True:
            self.clock.tick(FPS)
            self.buttons = []
            self.screen.fill(CREAM)
            screens[self.page]()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    if pygame.mixer.get_init():
                        self.audio_on = not self.audio_on
                        if self.audio_on:
                            play_intro(pygame, BASE)
                        else:
                            pygame.mixer.music.stop()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.page == "home":
                        pygame.quit()
                        return
                    self.go("home")

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, action in reversed(self.buttons):
                        if rect.collidepoint(event.pos):
                            action()
                            break

            pygame.display.flip()


if __name__ == "__main__":
    passage = get_creation_passage()
    print("Fonte bíblica:", passage["translation"])
    if passage["offline"]:
        print("Sem rede: usando cache ou amostra de Gênesis 1:1.")
    Game(passage).run()
