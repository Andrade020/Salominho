import json
import tempfile
import unittest
from pathlib import Path

from src.progress import Progress


class ProgressTests(unittest.TestCase):
    def test_read_reward_only_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            progress = Progress(path)
            self.assertTrue(progress.mark_read("genesis", 1, 20))
            self.assertFalse(progress.mark_read("genesis", 1, 20))
            self.assertEqual(progress.xp, 20)

    def test_quiz_best_score_and_mastery(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            progress = Progress(path)
            progress.record_quiz("genesis", 1, 2, 3)
            self.assertEqual(progress.xp, 20)
            result = progress.record_quiz("genesis", 1, 3, 3)
            self.assertTrue(result["mastered"])
            self.assertEqual(progress.xp, 50)

            reloaded = Progress(path)
            self.assertEqual(reloaded.chapter("genesis", 1)["best_score"], 3)
            self.assertTrue(reloaded.chapter("genesis", 1)["mastered"])


if __name__ == "__main__":
    unittest.main()
