# Contributing to AutoResearchClaw

## Setup

```bash
# 1. Fork and clone
git clone https://github.com/your-fork/AutoResearchClaw.git
cd AutoResearchClaw

# 2. Create a virtual environment and install with dev extras
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Create your local config
cp config.example.yaml config.yaml
# Edit config.yaml — add your API key, choose your model
```

## Running tests

```bash
pytest tests/
```

## Checking your environment

```bash
researchclaw doctor
```

## PR guidelines

- Branch from `main`
- One concern per PR
- Ensure `pytest tests/` passes before opening a PR
- Include tests for any new functionality

## Config files

| File | Purpose |
|------|---------|
| `config.example.yaml` | Tracked template — never add secrets here |
| `config.yaml` | Your local config — gitignored, created by copying the example |

## Questions?

Open an issue or join the [Discord](https://discord.gg/u4ksqW5P).
