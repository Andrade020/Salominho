import unittest

from src.pentateuch_maps import (
    PENTATEUCH_CHAPTERS,
    PENTATEUCH_IDS,
    PENTATEUCH_MAPS,
)


class PentateuchMapTests(unittest.TestCase):
    def test_all_five_books_have_maps(self):
        self.assertEqual(
            PENTATEUCH_IDS,
            frozenset({
                "genesis",
                "exodo",
                "levitico",
                "numeros",
                "deuteronomio",
            }),
        )

    def test_chapter_counts(self):
        expected = {
            "genesis": 50,
            "exodo": 40,
            "levitico": 27,
            "numeros": 36,
            "deuteronomio": 34,
        }
        for world_id, chapters in expected.items():
            config = PENTATEUCH_MAPS[world_id]
            self.assertEqual(config.chapters, chapters)
            self.assertEqual(len(config.nodes), chapters)

    def test_total_pentateuch_stages(self):
        self.assertEqual(PENTATEUCH_CHAPTERS, 187)

    def test_each_map_is_scrollable_or_fits_safely(self):
        for config in PENTATEUCH_MAPS.values():
            self.assertGreaterEqual(config.world_height, 680)


if __name__ == "__main__":
    unittest.main()
