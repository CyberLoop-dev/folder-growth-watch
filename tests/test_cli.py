import tempfile
import unittest
from pathlib import Path
from folder_growth_watch.cli import save_snapshot, load_history, compare

class GrowthWatchTests(unittest.TestCase):
    def test_reports_new_and_changed_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "watched"
            root.mkdir()
            store = Path(temp) / "history.json"
            (root / "a.txt").write_text("one", encoding="utf-8")
            save_snapshot(root, store)
            (root / "a.txt").write_text("one plus", encoding="utf-8")
            (root / "b.txt").write_text("new", encoding="utf-8")
            save_snapshot(root, store)
            report = compare(load_history(store))
            self.assertTrue(report["ready"])
            self.assertEqual(report["new"], ["b.txt"])
            self.assertEqual(report["delta"], 8)

    def test_needs_two_snapshots(self):
        self.assertFalse(compare({"snapshots": []})["ready"])

if __name__ == "__main__":
    unittest.main()
