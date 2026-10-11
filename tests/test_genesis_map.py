import unittest

from src.map_layout import path_segments, serpentine_nodes, world_height


class GenesisMapTests(unittest.TestCase):
    def test_genesis_has_50_nodes(self):
        nodes = serpentine_nodes(50)
        self.assertEqual(len(nodes), 50)
        self.assertEqual(nodes[0].chapter, 1)
        self.assertEqual(nodes[-1].chapter, 50)

    def test_rows_are_serpentine(self):
        nodes = serpentine_nodes(10, world_width=920, columns=5)
        self.assertLess(nodes[0].x, nodes[4].x)
        self.assertGreater(nodes[5].x, nodes[9].x)

    def test_path_has_49_segments(self):
        nodes = serpentine_nodes(50)
        self.assertEqual(len(path_segments(nodes)), 49)

    def test_world_is_scrollable(self):
        self.assertGreater(world_height(50), 680)


if __name__ == "__main__":
    unittest.main()
