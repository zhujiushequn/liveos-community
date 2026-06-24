"""Demo runner using local sample data."""

from __future__ import annotations

from pathlib import Path

from .interfaces import MonitorResult
from .report import write_markdown_report


def run_demo(root: Path, output_dir: Path, *, minutes: int = 5) -> Path:
    del minutes
    result = MonitorResult(
        room_name="sample-live-room",
        events_path=root / "examples" / "sample_events.jsonl",
        transcript_path=root / "examples" / "sample_transcript.txt",
    )
    return write_markdown_report(result, output_dir)

