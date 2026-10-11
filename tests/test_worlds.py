import unittest
from pathlib import Path

from src.worlds import load_old_testament, page_count, page_slice

BASE = Path(__file__).resolve().parents[1]


class WorldsTests(unittest.TestCase):
    def test_catalog_has_39_books_and_929_chapters(self):
        worlds = load_old_testament(BASE)
        self.assertEqual(len(worlds), 39)
        self.assertEqual(sum(world.chapters for world in worlds), 929)
        self.assertEqual(worlds[0].name, "Gênesis")
        self.assertEqual(worlds[-1].name, "Malaquias")

    def test_pagination(self):
        self.assertEqual(page_count(39, 12), 4)
        items, page, pages = page_slice(list(range(39)), 99, 12)
        self.assertEqual(page, 3)
        self.assertEqual(pages, 4)
        self.assertEqual(len(items), 3)


if __name__ == "__main__":
    unittest.main()
