# LiveOS Community

LiveOS Community is a sanitized, open-core demo of the LiveOS live-commerce
monitoring idea.

It shows the public parts of the architecture:

- collect public-screen events from a live room or sample file
- classify comment, join, purchase-intent, and system messages
- generate a simple local Markdown report
- expose interfaces for receivers, collectors, and reporters

It intentionally does **not** include:

- Feishu app auto-creation or permission automation
- OpenClaw production `anchor` routing
- DeepSeek keys, prompts, or commercial report logic
- Juliang Baiying / Buyin login automation
- same-source KPI dashboard capture
- customer logs, browser cookies, app secrets, or generated customer reports

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m liveos_community.cli demo --minutes 5
```

The demo writes a Markdown report under `outputs/`.

## CLI

```bash
liveos-community demo
liveos-community report --events examples/sample_events.jsonl --transcript examples/sample_transcript.txt
liveos-community print-browser-snippet
```

`print-browser-snippet` prints a JavaScript `MutationObserver` snippet that can
be pasted into a browser console for research on a public live room.

## Commercial Boundary

Community edition is for education and integration prototyping. The commercial
edition adds private-chat Feishu delivery, OpenClaw production agents, Buyin
same-source KPI monitoring, account initialization, remote diagnostics, PDF
delivery, ledgers, and proprietary scoring/report logic.

Read [docs/open-core-boundary.md](docs/open-core-boundary.md) before forking.

