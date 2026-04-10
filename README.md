
# 🦞 AI-Paper-Generator
<p align="center">
  <img src="images/framework_v2.png" width="580" alt="AutoResearch">
</p>
**Chat an idea. Get a paper.**

You type a research topic. AI-Paper-Generator finds real papers, runs experiments, analyzes results, and hands you a conference-ready PDF — automatically.

```bash
researchclaw run --topic "Future of AI chips in China" --auto-approve
```

---

## What you get

| File | What it is |
|------|------------|
| `paper_draft.md` | Full paper — Intro, Method, Experiments, Results, Conclusion |
| `paper.tex` | Conference-ready LaTeX (NeurIPS / ICLR / ICML) |
| `references.bib` | Real, verified citations from arXiv, Semantic Scholar, OpenAlex |
| `experiment runs/` | Generated Python code + sandbox results + metrics |
| `charts/` | Auto-generated figures with error bars |
| `reviews.md` | AI peer review with consistency checks |
| `deliverables/` | Everything in one folder, ready for Overleaf |

---

## Get started

**1. Install**
```bash
git clone https://github.com/raja21068/AI-Paper-Generator.git
cd AI-Paper-Generator
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

**2. Set up**
```bash
researchclaw setup    # installs extras, checks Docker/LaTeX
researchclaw init     # choose your LLM provider
```

**3. Add your API key**
```bash
export OPENAI_API_KEY="sk-..."
```

**4. Run**
```bash
# Fully automatic — walk away
researchclaw run --topic "Your research idea" --auto-approve

# Collaborative — you guide the key decisions
researchclaw run --topic "Your research idea" --mode co-pilot
```

Output lands in `artifacts/rc-YYYYMMDD-HHMMSS/deliverables/`.

---

## Two ways to use it

### 🤖 Fully autonomous
Type a topic, walk away. The AI handles everything from literature search to final PDF.

Best for: exploring ideas quickly, generating first drafts.

```bash
researchclaw run --topic "..." --auto-approve
```

### 🧑‍✈️ Co-pilot mode
The AI runs most stages on its own, but pauses at key moments for your input — choosing hypotheses, reviewing experiment design, co-writing the paper.

Best for: research you plan to actually submit.

```bash
researchclaw run --topic "..." --mode co-pilot
```

---

## How much control do you want?

| Mode | Command | Best for |
|------|---------|----------|
| Full auto | `--auto-approve` | Hands-off, quick drafts |
| Gate only | `--mode gate-only` | Approve at 3 key checkpoints |
| Co-pilot | `--mode co-pilot` | Deep collaboration on hypotheses + writing |
| Step-by-step | `--mode step-by-step` | Learning how the pipeline works |
| Custom | `--mode custom` | Define per-stage rules in config |

---

## The pipeline — 23 stages, 8 phases

```
Phase A  Scoping        Stages  1–2   Breaks topic into research questions
Phase B  Literature     Stages  3–6   Finds real papers ⛔ gate
Phase C  Synthesis      Stages  7–8   Clusters findings, generates hypotheses
Phase D  Design         Stages  9–11  Plans + writes experiment code ⛔ gate
Phase E  Execution      Stages 12–13  Runs code, self-heals bugs, iterates
Phase F  Analysis       Stages 14–15  Analyzes results, decides: proceed / refine / pivot
Phase G  Writing        Stages 16–19  Outlines → drafts → reviews → revises
Phase H  Finalize       Stages 20–23  Quality check, LaTeX export, citation verify ⛔ gate
```

> **⛔ Gate stages** pause for your approval. Skip them all with `--auto-approve`.

---

## Key features

- **Real citations only** — searches arXiv, Semantic Scholar, and OpenAlex. Verifies every reference through 4 layers. Hallucinated refs are automatically removed.

- **Self-healing experiments** — if the generated code crashes, the AI reads the error, patches the code, and reruns — up to 10 times.

- **Anti-fabrication guard** — numbers in the paper must come from actual experiment results. Unverified figures are blocked.

- **Contradiction detection** — flags when two sources directly disagree, so you know where the science is unsettled.

- **Claim registry** — tracks every factual claim back to its source and measures hallucination risk before you publish.

- **Self-learning** — lessons from failures are saved as reusable skills. Future runs avoid the same mistakes.

- **Cost guardrails** — set a USD budget. The pipeline pauses when spending approaches the limit.

- **Run anywhere** — CLI, Claude Code, Codex CLI, Gemini CLI, or any ACP-compatible agent. Also works via Discord, Telegram, and Slack.

---

## Supported LLMs and agents

Works with any OpenAI-compatible API. Also supports these CLI agents — no API key needed:

| Agent | Provider |
|-------|----------|
| Claude Code | Anthropic |
| Codex CLI | OpenAI |
| Copilot CLI | GitHub |
| Gemini CLI | Google |
| Kimi CLI | Moonshot |
| OpenCode | SST |

```yaml
# config.arc.yaml — ACP example
llm:
  provider: "acp"
  acp:
    agent: "claude"   # any ACP agent command
```

---

## Minimum config

```yaml
project:
  name: "my-research"

research:
  topic: "Your research topic"

llm:
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]

experiment:
  mode: "sandbox"
  sandbox:
    python_path: ".venv/bin/python"
```

---

## ⚠️ Ethics — please read before submitting anything

AI-Paper-Generator generates **drafts**, not finished papers. Before submitting anywhere:

- Verify all claims, citations, and experiment results yourself
- Disclose AI assistance to the target venue (most conferences require this now)
- Do not use this tool to generate fraudulent submissions or paper mills

You are responsible for the content of any paper you submit.

---



