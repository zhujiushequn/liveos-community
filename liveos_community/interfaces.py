"""Public interfaces for community integrations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class MonitorRequest:
    """A minimal monitor request for community demos."""

    text: str
    minutes: int = 5
    source_url: str | None = None


@dataclass(frozen=True)
class MonitorResult:
    """Output from a collector or demo run."""

    room_name: str
    events_path: Path
    transcript_path: Path


class Receiver(Protocol):
    """Receives a request from chat, CLI, or a test harness."""

    def receive(self) -> MonitorRequest:
        """Return one request."""


class Collector(Protocol):
    """Collects public events and transcript text."""

    def collect(self, request: MonitorRequest) -> MonitorResult:
        """Collect monitoring evidence."""


class Reporter(Protocol):
    """Turns collected evidence into a local report."""

    def write_report(self, result: MonitorResult, output_dir: Path) -> Path:
        """Write a report and return its path."""

