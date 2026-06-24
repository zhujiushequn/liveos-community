# Architecture

```text
receiver -> collector -> normalizer -> reporter
```

- `Receiver`: accepts a message from a user or test harness.
- `Collector`: returns public-screen events and transcript text.
- `Normalizer`: converts raw lines into typed events.
- `Reporter`: writes a local report.

The community edition keeps these units local and credential-free. Production
integrations should implement the interfaces in `liveos_community/interfaces.py`
without committing credentials or customer state.

