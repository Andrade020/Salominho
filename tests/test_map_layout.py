import unittest

from src.map_layout import build_path_segments, layout_chapter_nodes


class MapLayoutTests(unittest.TestCase):
    def test_serpentine_layout(self):
        nodes = layout_chapter_nodes(range(1, 11), (0, 0, 500, 300), cols=5)
        self.assertEqual(len(nodes), 10)
        self.assertLess(nodes[0]["x"], nodes[4]["x"])
        self.assertGreater(nodes[5]["x"], nodes[9]["x"])

    def test_segments(self):
        nodes = layout_chapter_nodes([1, 2, 3], (0, 0, 300, 200), cols=3)
        self.assertEqual(len(build_path_segments(nodes)), 2)


if __name__ == "__main__":
    unittest.main()
