from pathlib import Path
import tempfile
import unittest

from liveos_community.interfaces import MonitorResult
from liveos_community.report import _unique_report_path, write_markdown_report


class ReportPathTests(unittest.TestCase):
    def test_unique_path_suffixes_on_collision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            first = _unique_report_path(out, "20260101_000000")
            first.write_text("x", encoding="utf-8")
            second = _unique_report_path(out, "20260101_000000")
            self.assertNotEqual(first, second)
            second.write_text("y", encoding="utf-8")
            third = _unique_report_path(out, "20260101_000000")
            self.assertNotIn(third, {first, second})


class ReportContentTests(unittest.TestCase):
    def _result(self, root: Path) -> MonitorResult:
        events = root / "events.jsonl"
        transcript = root / "transcript.txt"
        events.write_text('{"ts": "t", "text": "主播好"}\n', encoding="utf-8")
        transcript.write_text("", encoding="utf-8")
        return MonitorResult(room_name="r", events_path=events, transcript_path=transcript)

    def test_two_runs_in_same_second_do_not_overwrite(self) -> None:
        # 同一秒内连续生成两份报告，文件名不能撞车互相覆盖。
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self._result(root)
            out = root / "out"
            paths = {write_markdown_report(result, out) for _ in range(2)}
            self.assertEqual(len(paths), 2)
            for path in paths:
                self.assertTrue(path.exists())

    def test_report_falls_back_when_no_samples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self._result(root)
            text = write_markdown_report(result, root / "out").read_text(encoding="utf-8")
            self.assertIn("No purchase-intent samples", text)
            self.assertIn("No question samples", text)
            self.assertIn("No transcript text.", text)


if __name__ == "__main__":
    unittest.main()
