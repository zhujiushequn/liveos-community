"""Public-screen event parsing and classification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass(frozen=True)
class PublicScreenEvent:
    ts: str
    text: str
    kind: str


PURCHASE_INTENT_WORDS = ("下单", "拍了", "几号链接", "什么时候发货", "已买", "付款")
QUESTION_WORDS = ("多少钱", "怎么", "哪里", "尺码", "发货", "链接", "有没有")
JOIN_WORDS = ("来了", "加入了直播间", "进入直播间")
GIFT_WORDS = ("送出", "礼物")


def classify_text(text: str) -> str:
    clean = text.strip()
    if not clean:
        return "empty"
    if any(word in clean for word in PURCHASE_INTENT_WORDS):
        return "purchase_intent"
    if any(word in clean for word in QUESTION_WORDS):
        return "question"
    if any(word in clean for word in JOIN_WORDS):
        return "join"
    if any(word in clean for word in GIFT_WORDS):
        return "gift"
    return "comment"


def event_from_text(text: str, ts: str | None = None) -> PublicScreenEvent:
    return PublicScreenEvent(
        ts=ts or datetime.now(timezone.utc).isoformat(),
        text=text.strip(),
        kind=classify_text(text),
    )


def load_events(path: Path) -> list[PublicScreenEvent]:
    events: list[PublicScreenEvent] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            events.append(
                PublicScreenEvent(
                    ts=str(raw.get("ts") or ""),
                    text=str(raw.get("text") or ""),
                    kind=str(raw.get("kind") or classify_text(str(raw.get("text") or ""))),
                )
            )
    return events


def write_events(events: list[PublicScreenEvent], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event.__dict__, ensure_ascii=False) + "\n")
    return path

