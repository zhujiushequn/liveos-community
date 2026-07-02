import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest

from liveos_community.cli import main
from liveos_community.douyin_public_screen import browser_snippet


class CliTests(unittest.TestCase):
    def test_demo_command_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(["demo", "--output-dir", tmp])
            self.assertEqual(code, 0)
            printed = Path(buf.getvalue().strip())
            self.assertTrue(printed.exists())

    def test_report_command_uses_given_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.jsonl"
            transcript = Path(tmp) / "transcript.txt"
            events.write_text('{"ts": "t", "text": "下单"}\n', encoding="utf-8")
            transcript.write_text("大家好", encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main(
                    [
                        "report",
                        "--room-name",
                        "room-a",
                        "--events",
                        str(events),
                        "--transcript",
                        str(transcript),
                        "--output-dir",
                        tmp,
                    ]
                )
            self.assertEqual(code, 0)
            report_text = Path(buf.getvalue().strip()).read_text(encoding="utf-8")
            self.assertIn("room-a", report_text)
            self.assertIn("purchase_intent", report_text)

    def test_print_browser_snippet(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["print-browser-snippet"])
        self.assertEqual(code, 0)
        self.assertIn("webcast-chatroom", buf.getvalue())
        self.assertEqual(buf.getvalue().strip(), browser_snippet())


if __name__ == "__main__":
    unittest.main()
