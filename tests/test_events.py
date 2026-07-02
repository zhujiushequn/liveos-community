from pathlib import Path
import tempfile
import unittest

from liveos_community.events import (
    classify_text,
    event_from_text,
    load_events,
    write_events,
)


class ClassifyTextTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertEqual(classify_text("   "), "empty")

    def test_question(self) -> None:
        self.assertEqual(classify_text("这个多少钱"), "question")

    def test_join(self) -> None:
        self.assertEqual(classify_text("小明 来了"), "join")

    def test_gift(self) -> None:
        self.assertEqual(classify_text("送出 小心心"), "gift")

    def test_plain_comment(self) -> None:
        self.assertEqual(classify_text("主播声音真好听"), "comment")

    def test_purchase_intent_beats_question(self) -> None:
        # “几号链接”同时含购买意向词与提问词，购买意向优先。
        self.assertEqual(classify_text("几号链接"), "purchase_intent")


class EventIOTests(unittest.TestCase):
    def test_event_from_text_defaults(self) -> None:
        event = event_from_text("  下单了  ")
        self.assertEqual(event.text, "下单了")
        self.assertEqual(event.kind, "purchase_intent")
        self.assertTrue(event.ts)

    def test_write_and_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "events.jsonl"
            events = [event_from_text("来了"), event_from_text("多少钱")]
            write_events(events, path)
            self.assertEqual(load_events(path), events)

    def test_load_events_fills_missing_kind_and_skips_blank_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(
                '{"ts": "t1", "text": "下单"}\n\n{"text": "你好", "kind": "comment"}\n',
                encoding="utf-8",
            )
            loaded = load_events(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].kind, "purchase_intent")
            self.assertEqual(loaded[1].kind, "comment")


if __name__ == "__main__":
    unittest.main()
