"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from .demo import run_demo
from .douyin_public_screen import browser_snippet
from .interfaces import MonitorResult
from .report import write_markdown_report


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="liveos-community")
    sub = parser.add_subparsers(dest="cmd", required=True)

    demo = sub.add_parser("demo", help="Run a local sample-data demo")
    demo.add_argument("--minutes", type=int, default=5)
    demo.add_argument("--output-dir", default="outputs")

    report = sub.add_parser("report", help="Generate a report from local evidence files")
    report.add_argument("--room-name", default="community-room")
    report.add_argument("--events", required=True)
    report.add_argument("--transcript", required=True)
    report.add_argument("--output-dir", default="outputs")

    sub.add_parser("print-browser-snippet", help="Print the public-screen browser snippet")

    args = parser.parse_args(argv)
    if args.cmd == "demo":
        path = run_demo(_repo_root(), Path(args.output_dir), minutes=args.minutes)
        print(path)
        return 0
    if args.cmd == "report":
        result = MonitorResult(
            room_name=args.room_name,
            events_path=Path(args.events),
            transcript_path=Path(args.transcript),
        )
        print(write_markdown_report(result, Path(args.output_dir)))
        return 0
    if args.cmd == "print-browser-snippet":
        print(browser_snippet())
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

