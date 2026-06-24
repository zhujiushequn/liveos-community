from pathlib import Path
import tempfile
import unittest

from liveos_community.demo import run_demo
from liveos_community.events import classify_text


class CommunityDemoTests(unittest.TestCase):
    def test_classify_purchase_intent(self) -> None:
        self.assertEqual(classify_text("下单了什么时候发货"), "purchase_intent")

    def test_demo_writes_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            report = run_demo(root, Path(tmp))
            self.assertTrue(report.exists())
            text = report.read_text(encoding="utf-8")
            self.assertIn("LiveOS Community Report", text)
            self.assertIn("purchase_intent", text)


if __name__ == "__main__":
    unittest.main()

