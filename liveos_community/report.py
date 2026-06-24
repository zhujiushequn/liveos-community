"""Simple local Markdown report generation."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

from .events import PublicScreenEvent, load_events
from .interfaces import MonitorResult


def _top_events(events: list[PublicScreenEvent], kind: str, limit: int = 8) -> list[str]:
    return [event.text for event in events if event.kind == kind][:limit]


def write_markdown_report(result: MonitorResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    events = load_events(result.events_path)
    transcript = result.transcript_path.read_text(encoding="utf-8").strip()
    counts = Counter(event.kind for event in events)

    report_path = output_dir / f"liveos_community_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    lines = [
        "# LiveOS Community Report",
        "",
        f"- Room: {result.room_name}",
        f"- Events: {len(events)}",
        f"- Transcript chars: {len(transcript)}",
        "",
        "## Event Summary",
        "",
    ]
    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind}: {count}")

    lines.extend(["", "## Purchase Intent Samples", ""])
    samples = _top_events(events, "purchase_intent")
    lines.extend([f"- {sample}" for sample in samples] or ["- No purchase-intent samples in this demo."])

    lines.extend(["", "## Questions", ""])
    questions = _top_events(events, "question")
    lines.extend([f"- {sample}" for sample in questions] or ["- No question samples in this demo."])

    lines.extend(["", "## Transcript Excerpt", "", transcript[:1200] or "No transcript text."])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This community report is intentionally simple. Commercial scoring, KPI alignment,",
            "Feishu delivery, OpenClaw production routing, and Buyin same-source data are not included.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path

