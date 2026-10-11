import unittest

from tools.generate_pentateuch_maps import SPECS, parse_completed


class PentateuchGeneratorTests(unittest.TestCase):
    def test_chapter_counts(self):
        self.assertEqual(
            {spec.key: spec.chapters for spec in SPECS},
            {
                "genesis": 50,
                "exodo": 40,
                "levitico": 27,
                "numeros": 36,
                "deuteronomio": 34,
            },
        )

    def test_total_is_187(self):
        self.assertEqual(sum(spec.chapters for spec in SPECS), 187)

    def test_completed_parser(self):
        parsed = parse_completed(["genesis=1-3,8", "exodo=1,4"])
        self.assertEqual(parsed["genesis"], {1, 2, 3, 8})
        self.assertEqual(parsed["exodo"], {1, 4})


if __name__ == "__main__":
    unittest.main()
