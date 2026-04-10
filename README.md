
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

<table>
<tr><td>📄</td><td><code>paper_draft.md</code></td><td>Full academic paper (Introduction, Related Work, Method, Experiments, Results, Conclusion)</td></tr>
<tr><td>📐</td><td><code>paper.tex</code></td><td>Conference-ready LaTeX (NeurIPS / ICLR / ICML templates)</td></tr>
<tr><td>📚</td><td><code>references.bib</code></td><td>Real BibTeX references from OpenAlex, Semantic Scholar and arXiv — auto-pruned to match inline citations</td></tr>
<tr><td>🔍</td><td><code>verification_report.json</code></td><td>4-layer citation integrity + relevance verification (arXiv, CrossRef, DataCite, LLM)</td></tr>
<tr><td>🧪</td><td><code>experiment runs/</code></td><td>Generated code + sandbox results + structured JSON metrics</td></tr>
<tr><td>📊</td><td><code>charts/</code></td><td>Auto-generated condition comparison charts with error bars and confidence intervals</td></tr>
<tr><td>📝</td><td><code>reviews.md</code></td><td>Multi-agent peer review with methodology-evidence consistency checks</td></tr>
<tr><td>🧬</td><td><code>evolution/</code></td><td>Self-learning lessons extracted from each run</td></tr>
<tr><td>📦</td><td><code>deliverables/</code></td><td>All final outputs in one folder — compile-ready for Overleaf</td></tr>
</table>
🌍 **Run it anywhere.** AutoResearchClaw isn't locked to a single platform. Use it standalone via CLI, plug it into [OpenClaw](https://github.com/openclaw/openclaw), or wire it up through any ACP-compatible agent — 🤖 Claude Code, 💻 Codex CLI, 🐙 Copilot CLI, ♊ Gemini CLI, 🌙 Kimi CLI, you name it. And because OpenClaw bridges to messaging platforms, you can kick off a full research run from 💬 Discord, ✈️ Telegram, 🐦 Lark (飞书), 💚 WeChat, or wherever your team already hangs out. One topic in, one paper out — no matter where you type it.
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
### 🚀 Use with OpenClaw (Recommended)

If you already use [OpenClaw](https://github.com/openclaw/openclaw) as your AI assistant:

```
1️⃣  Share the GitHub repo URL with OpenClaw
2️⃣  OpenClaw auto-reads RESEARCHCLAW_AGENTS.md → understands the pipeline
3️⃣  Say: "Research [your topic]"
4️⃣  Done — OpenClaw clones, installs, configures, runs, and returns results
```

**That's it.** OpenClaw handles `git clone`, `pip install`, config setup, and pipeline execution automatically. You just chat.

<details>
<summary>💡 What happens under the hood</summary>

1. OpenClaw reads `RESEARCHCLAW_AGENTS.md` → learns the research orchestrator role
2. OpenClaw reads `README.md` → understands installation and pipeline structure
3. OpenClaw copies `config.researchclaw.example.yaml` → `config.yaml`
4. Asks for your LLM API key (or uses your environment variable)
5. Runs `pip install -e .` + `researchclaw run --topic "..." --auto-approve`
6. Returns the paper, LaTeX, experiments, and citations

</details>

### 🔌 OpenClaw Bridge (Advanced)

For deeper integration, AutoResearchClaw includes a **bridge adapter system** with 6 optional capabilities:

```yaml
# config.arc.yaml
openclaw_bridge:
  use_cron: true              # ⏰ Scheduled research runs
  use_message: true           # 💬 Progress notifications (Discord/Slack/Telegram)
  use_memory: true            # 🧠 Cross-session knowledge persistence
  use_sessions_spawn: true    # 🔀 Spawn parallel sub-sessions for concurrent stages
  use_web_fetch: true         # 🌐 Live web search during literature review
  use_browser: false          # 🖥️ Browser-based paper collection
```

Each flag activates a typed adapter protocol. When OpenClaw provides these capabilities, the adapters consume them without code changes. See [`docs/integration-guide.md`](docs/integration-guide.md) for full details.

### ACP (Agent Client Protocol)

AutoResearchClaw can use **any ACP-compatible coding agent** as its LLM backend — no API keys required. The agent communicates via [acpx](https://github.com/openclaw/acpx), maintaining a single persistent session across all 23 pipeline stages.

| Agent | Command | Notes |
|-------|---------|-------|
| Claude Code | `claude` | Anthropic |
| Codex CLI | `codex` | OpenAI |
| Copilot CLI | `gh` | GitHub |
| Gemini CLI | `gemini` | Google |
| OpenCode | `opencode` | SST |
| Kimi CLI | `kimi` | Moonshot |

```yaml
# config.yaml — ACP example
llm:
  provider: "acp"
  acp:
    agent: "claude"   # Any ACP-compatible agent CLI command
    cwd: "."          # Working directory for the agent
  # No base_url or api_key needed — the agent handles its own auth.
```

```bash
# Just run — the agent uses its own credentials
researchclaw run --config config.yaml --topic "Your research idea" --auto-approve
```

### 🛠️ Other Ways to Run

| Method | How |
|--------|-----|
| **Standalone CLI** | `researchclaw run --topic "..." --auto-approve` (autonomous) or `--mode co-pilot` (collaborative) |
| **Python API** | `from researchclaw.pipeline import Runner; Runner(config).run()` |
| **Claude Code** | Reads `RESEARCHCLAW_CLAUDE.md` — just say *"Run research on [topic]"* |
| **Copilot CLI** | `researchclaw run --topic "..."` with `llm.acp.agent: "gh"` |
| **OpenCode** | Reads `.claude/skills/` — same natural language interface |
| **Any AI CLI** | Provide `RESEARCHCLAW_AGENTS.md` as context → agent auto-bootstraps |

---

## 🔬 Pipeline: 23 Stages, 8 Phases

```
Phase A: Research Scoping          Phase E: Experiment Execution
  1. TOPIC_INIT                      12. EXPERIMENT_RUN
  2. PROBLEM_DECOMPOSE               13. ITERATIVE_REFINE  ← self-healing

Phase B: Literature Discovery      Phase F: Analysis & Decision
  3. SEARCH_STRATEGY                 14. RESULT_ANALYSIS    ← multi-agent
  4. LITERATURE_COLLECT  ← real API  15. RESEARCH_DECISION  ← PIVOT/REFINE
  5. LITERATURE_SCREEN   [gate]
  6. KNOWLEDGE_EXTRACT               Phase G: Paper Writing
                                     16. PAPER_OUTLINE
Phase C: Knowledge Synthesis         17. PAPER_DRAFT
  7. SYNTHESIS                       18. PEER_REVIEW        ← evidence check
  8. HYPOTHESIS_GEN    ← debate      19. PAPER_REVISION

Phase D: Experiment Design         Phase H: Finalization
  9. EXPERIMENT_DESIGN   [gate]      20. QUALITY_GATE      [gate]
 10. CODE_GENERATION                 21. KNOWLEDGE_ARCHIVE
 11. RESOURCE_PLANNING               22. EXPORT_PUBLISH     ← LaTeX
                                     23. CITATION_VERIFY    ← relevance check
```

> **Gate stages** (5, 9, 20) pause for human approval or auto-approve with `--auto-approve`. On rejection, the pipeline rolls back.

> **Co-Pilot mode** (`--mode co-pilot`): Deep human-AI collaboration at Stages 7-8 (Idea Workshop), Stage 9 (Baseline Navigator), and Stages 16-17 (Paper Co-Writer). Other stages auto-execute with SmartPause monitoring.

> **Decision loops**: Stage 15 can trigger REFINE (→ Stage 13) or PIVOT (→ Stage 8), with automatic artifact versioning.




You: researchclaw run --topic "Quantum noise as neural network regularization" --mode co-pilot

Pipeline runs Stages 1-7 automatically...

  ┌─────────────────────────────────────────────────────────────┐
  │  HITL | Stage 08: HYPOTHESIS_GEN                            │
  │  Post-stage review                                          │
  │                                                             │
  │  Hypotheses mentioned: 3                                    │
  │  Novelty score: 0.72 (moderate)                             │
  │                                                             │
  │  [a] Approve  [r] Reject  [e] Edit  [c] Collaborate         │
  │  [i] Inject guidance  [v] View output  [q] Abort            │
  └─────────────────────────────────────────────────────────────┘

You: c  (start collaborative chat)
You: Hypothesis 3 is interesting but needs Dropout/Label Smoothing as baselines
AI:  Updated — added Dropout, Label Smoothing, MixUp, CutMix as baselines...
You: approve

Pipeline continues with your refined hypothesis...
```
`bash
# Start with HITL mode
researchclaw run --topic "..." --mode co-pilot

# Attach to a paused pipeline (from another terminal)
researchclaw attach artifacts/rc-2026-xxx

# Check pipeline and HITL status
researchclaw status artifacts/rc-2026-xxx

# Approve/reject from another terminal or script
researchclaw approve artifacts/rc-2026-xxx --message "LGTM"
researchclaw reject artifacts/rc-2026-xxx --reason "Missing key baseline"

# Inject guidance for a stage (even before it runs)
researchclaw guide artifacts/rc-2026-xxx --stage 9 --message "Use ResNet-50 as primary baseline"
```


### CLI Commands

```bash
# Start with HITL mode
researchclaw run --topic "..." --mode co-pilot

# Attach to a paused pipeline (from another terminal)
researchclaw attach artifacts/rc-2026-xxx

# Check pipeline and HITL status
researchclaw status artifacts/rc-2026-xxx

# Approve/reject from another terminal or script
researchclaw approve artifacts/rc-2026-xxx --message "LGTM"
researchclaw reject artifacts/rc-2026-xxx --reason "Missing key baseline"

# Inject guidance for a stage (even before it runs)
researchclaw guide artifacts/rc-2026-xxx --stage 9 --message "Use ResNet-50 as primary baseline"
```

### Key Capabilities

| Feature | Description |
|---------|------------|
| **Idea Workshop** | Brainstorm, evaluate, and refine hypotheses collaboratively (Stage 7-8) |
| **Baseline Navigator** | AI suggests baselines + human adds/removes + reproducibility checklist (Stage 9) |
| **Paper Co-Writer** | Section-by-section drafting with human editing and AI polishing (Stage 16-19) |
| **SmartPause** | Confidence-driven dynamic pausing — auto-detects when human input would help |
| **Claim Verification** | Inline fact-checking against collected literature — flags ungrounded claims |
| **Cost Guardrails** | Budget monitoring with 50%/80%/100% threshold alerts |
| **Intervention Learning** | ALHF — learns from your review patterns to optimize future pause decisions |
| **Branch Exploration** | Fork pipeline to explore multiple hypotheses, compare, merge the best |
| **Escalation Policy** | Tiered notification (terminal → Slack → email → auto-halt) when unattended |
| **3 Adapters** | CLI (terminal), WebSocket (web dashboard), MCP (external agents) |

### Configuration

```yaml
# config.arc.yaml
hitl:
  enabled: true
  mode: co-pilot                     # full-auto | gate-only | checkpoint | co-pilot | custom
  cost_budget_usd: 50.0              # Pause when cost exceeds budget (0 = no limit)

  notifications:
    on_pause: true
    on_quality_drop: true
    channels: ["terminal"]            # terminal | slack | webhook

  timeouts:
    default_human_timeout_sec: 86400  # 24h default wait
    auto_proceed_on_timeout: false

  collaboration:
    max_chat_turns: 50
    save_chat_history: true

  # Per-stage custom policies (optional, for 'custom' mode)
  stage_policies:
    8: { require_approval: true, enable_collaboration: true }
    9: { require_approval: true, allow_edit_output: true }
```

### Backward Compatibility

- **Default: OFF.** Without `hitl.enabled: true` or `--mode`, the pipeline behaves exactly as before.
- **`--auto-approve` still works.** It overrides HITL mode.
- **All 2,699 existing tests pass** with HITL code present.

---

## 🧠 MetaClaw Integration

**AutoResearchClaw + [MetaClaw](https://github.com/aiming-lab/MetaClaw) = A pipeline that learns from every run.**

MetaClaw adds **cross-run knowledge transfer** to AutoResearchClaw. When enabled, the pipeline automatically captures lessons from failures and warnings, converts them into reusable skills, and injects those skills into all 23 pipeline stages on subsequent runs — so the same mistakes are never repeated.

### How It Works

```
Run N executes → failures/warnings captured as Lessons
                      ↓
          MetaClaw Lesson → Skill conversion
                      ↓
          arc-* Skill files stored in ~/.metaclaw/skills/
                      ↓
Run N+1 → build_overlay() injects skills into every LLM prompt
                      ↓
          LLM avoids known pitfalls → higher quality, fewer retries
```

### Quick Setup

```bash
# 1. Install MetaClaw (if not already)
pip install metaclaw

# 2. Enable in your config
```

```yaml
# config.arc.yaml
metaclaw_bridge:
  enabled: true
  proxy_url: "http://localhost:30000"        # MetaClaw proxy (optional)
  skills_dir: "~/.metaclaw/skills"          # Where skills are stored
  fallback_url: "https://api.openai.com/v1" # Direct LLM fallback
  fallback_api_key: ""                      # API key for fallback URL
  lesson_to_skill:
    enabled: true
    min_severity: "warning"                 # Convert warnings + errors
    max_skills_per_run: 3
```

```bash
# 3. Run as usual — MetaClaw works transparently
researchclaw run --config config.arc.yaml --topic "Your idea" --auto-approve
```

After each run, check `~/.metaclaw/skills/arc-*/SKILL.md` to see the skills your pipeline has learned.

### Experiment Results

In controlled A/B experiments (same topic, same LLM, same configuration):

| Metric | Baseline | With MetaClaw | Improvement |
|--------|----------|---------------|-------------|
| Stage retry rate | 10.5% | 7.9% | **-24.8%** |
| Refine cycle count | 2.0 | 1.2 | **-40.0%** |
| Pipeline stage completion | 18/19 | 19/19 | **+5.3%** |
| Overall robustness score (composite) | 0.714 | 0.845 | **+18.3%** |

> Composite robustness score is a weighted average of stage completion rate (40%), retry reduction (30%), and refine cycle efficiency (30%).

### Backward Compatibility

- **Default: OFF.** If `metaclaw_bridge` is absent or `enabled: false`, the pipeline behaves exactly as before.
- **No new dependencies.** MetaClaw is optional — the core pipeline works without it.
- **All 2,699 existing tests pass** with the integration code present.

---

## 🧩 Skills Library

AutoResearchClaw now supports loading **open-source and custom skills** to further enhance your research experience. We also ship with **19 pre-loaded built-in skills** (scientific writing, literature search, chemistry, biology, and more) as ready-to-use references, offering a high degree of flexibility out of the box. Disable any skill by adding `enabled: false` to its frontmatter.

**Sample built-in skills:**

| Category | Skill | Description |
|----------|-------|-------------|
| **Writing** | `scientific-writing` | IMRAD structure, citation formatting, reporting guidelines |
| **Domain** | `chemistry-rdkit` | Molecular analysis, SMILES, fingerprints, drug discovery |
| **Experiment** | `literature-search` | Systematic review, PRISMA methodology |

> See all 19 skills with `researchclaw skills list`.

### Load Your Own Skills

```bash
# Option 1: Install a skill (persists across projects)
researchclaw skills install /path/to/my-skill/

# Option 2: Drop a SKILL.md into the project
mkdir -p .claude/skills/my-custom-skill
# Then create a SKILL.md with YAML frontmatter (name, description, trigger-keywords, applicable-stages)

# Option 3: Configure shared skill directories in config.arc.yaml
# skills:
#   custom_dirs:
#     - /path/to/team-shared-skills
```

### Using Skills

Skills are loaded and injected into LLM prompts automatically — no manual activation needed. Use the CLI to inspect:

```bash
researchclaw skills list               # Show all loaded skills with sources
researchclaw skills validate ./my-skill # Check SKILL.md format
```

Browse community skills: [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) (150+ scientific skills across multiple disciplines).

---

## ⚙️ Configuration Reference

<details>
<summary>Click to expand full configuration reference</summary>

```yaml
# === Project ===
project:
  name: "my-research"              # Project identifier
  mode: "docs-first"               # docs-first | semi-auto | full-auto

# === Research ===
research:
  topic: "..."                     # Research topic (required)
  domains: ["ml", "nlp"]           # Research domains for literature search
  daily_paper_count: 8             # Target papers per search query
  quality_threshold: 4.0           # Minimum quality score for papers

# === Runtime ===
runtime:
  timezone: "America/New_York"     # For timestamps
  max_parallel_tasks: 3            # Concurrent experiment limit
  approval_timeout_hours: 12       # Gate stage timeout
  retry_limit: 2                   # Retry count on stage failure

# === LLM ===
llm:
  provider: "openai-compatible"    # openai | openrouter | deepseek | minimax | acp | openai-compatible
  base_url: "https://..."          # API endpoint (required for openai-compatible)
  api_key_env: "OPENAI_API_KEY"    # Env var for API key (required for openai-compatible)
  api_key: ""                      # Or hardcode key here
  primary_model: "gpt-4o"          # Primary model
  fallback_models: ["gpt-4o-mini"] # Fallback chain
  s2_api_key: ""                   # Semantic Scholar API key (optional, higher rate limits)
  acp:                             # Only used when provider: "acp"
    agent: "claude"                # ACP agent CLI command (claude, codex, gemini, etc.)
    cwd: "."                       # Working directory for the agent

# === Experiment ===
experiment:
  mode: "sandbox"                  # simulated | sandbox | docker | ssh_remote
  time_budget_sec: 300             # Max execution time per run (default: 300s)
  max_iterations: 10               # Max optimization iterations
  metric_key: "val_loss"           # Primary metric name
  metric_direction: "minimize"     # minimize | maximize
  sandbox:
    python_path: ".venv/bin/python"
    gpu_required: false
    allowed_imports: [math, random, json, csv, numpy, torch, sklearn]
    max_memory_mb: 4096
  docker:
    image: "researchclaw/experiment:latest"
    network_policy: "setup_only"   # none | setup_only | pip_only | full
    gpu_enabled: true
    memory_limit_mb: 8192
    auto_install_deps: true        # Auto-detect imports → requirements.txt
  ssh_remote:
    host: ""                       # GPU server hostname
    gpu_ids: []                    # Available GPU IDs
    remote_workdir: "/tmp/researchclaw_experiments"
  opencode:                          # OpenCode Beast Mode (auto-installed via `researchclaw setup`)
    enabled: true                    # Master switch (default: true)
    auto: true                       # Auto-trigger without confirmation (default: true)
    complexity_threshold: 0.2        # 0.0-1.0 — higher = only trigger on complex experiments
    model: ""                        # Override model (empty = use llm.primary_model)
    timeout_sec: 600                 # Max seconds for OpenCode generation
    max_retries: 1                   # Retry count on failure
    workspace_cleanup: true          # Remove temp workspace after collection
  code_agent:                        # CodeAgent v2 — multi-phase code generation
    enabled: true                    # Use CodeAgent instead of legacy single-prompt codegen
    architecture_planning: true      # Generate deep implementation blueprint before coding
    sequential_generation: true      # Generate files one-by-one following dependency DAG
    hard_validation: true            # AST-based validation gates (blocks identical ablations, hardcoded metrics)
    hard_validation_max_repairs: 2   # Max repair attempts when validation fails
    exec_fix_max_iterations: 3       # Execution-in-the-loop fix attempts
    exec_fix_timeout_sec: 60         # Timeout per exec-fix attempt
  benchmark_agent:                   # BenchmarkAgent — automated dataset & baseline selection
    enabled: true                    # Enable 4-agent benchmark pipeline (Surveyor→Selector→Acquirer→Validator)
    enable_hf_search: true           # Search HuggingFace Datasets
    enable_web_search: true          # Search Google Scholar for benchmarks
    tier_limit: 2                    # Dataset tier filtering (1=small/cached, 2=medium, 3=large)
    min_benchmarks: 1                # Minimum datasets required
    min_baselines: 2                 # Minimum baseline methods required
  figure_agent:                      # FigureAgent — academic figure generation
    enabled: true                    # Enable 5-agent figure pipeline (Planner→CodeGen→Renderer→Critic→Integrator)
    min_figures: 3                   # Minimum figures to generate
    max_figures: 8                   # Maximum figures
    max_iterations: 3                # Critic-driven refinement iterations
    dpi: 300                         # Output resolution
    strict_mode: false               # Fail pipeline if figure generation fails
  repair:                            # Anti-fabrication experiment repair
    enabled: true                    # Auto-diagnose and repair failed experiments
    max_cycles: 3                    # Repair retry loops
    min_completion_rate: 0.5         # >=50% conditions must complete to proceed
    min_conditions: 2                # At least 2 conditions for valid experiment
    use_opencode: true               # Route repairs through OpenCode Beast Mode

# === Web Search (Optional) ===
web_search:
  enabled: true                      # Enable web-augmented literature search
  tavily_api_key_env: "TAVILY_API_KEY"  # Tavily API key env var (optional)
  enable_scholar: true               # Google Scholar search
  enable_pdf_extraction: true        # Extract text from PDFs
  max_web_results: 10                # Max web results per query

# === Export ===
export:
  target_conference: "neurips_2025"  # neurips_2025 | iclr_2026 | icml_2026
  authors: "Anonymous"
  bib_file: "references"

# === Prompts ===
prompts:
  custom_file: ""                  # Path to custom prompts YAML (empty = defaults)

# === HITL Co-Pilot (NEW in v0.4.0) ===
hitl:
  enabled: false                     # Set to true to enable HITL
  mode: co-pilot                     # full-auto | gate-only | checkpoint | step-by-step | co-pilot | custom
  cost_budget_usd: 0.0              # Cost limit in USD (0 = no limit)
  notifications:
    on_pause: true                   # Notify when pipeline pauses
    on_quality_drop: true            # Notify on quality issues
    channels: ["terminal"]           # terminal | slack | webhook
  timeouts:
    default_human_timeout_sec: 86400 # Wait up to 24h for human input
    auto_proceed_on_timeout: false   # If true, auto-approve on timeout
  collaboration:
    max_chat_turns: 50               # Max turns per collaboration session
    save_chat_history: true          # Persist chat logs
  stage_policies: {}                 # Per-stage overrides (for 'custom' mode)

# === Security ===
security:
  hitl_required_stages: [5, 9, 20] # Stages requiring human approval
  allow_publish_without_approval: false
  redact_sensitive_logs: true

# === Knowledge Base ===
knowledge_base:
  backend: "markdown"              # markdown | obsidian
  root: "docs/kb"

# === Notifications ===
notifications:
  channel: "console"               # console | discord | slack
  target: ""

# === MetaClaw Bridge (Optional) ===
metaclaw_bridge:
  enabled: false                   # Set to true to enable cross-run learning
  proxy_url: "http://localhost:30000"  # MetaClaw proxy URL
  skills_dir: "~/.metaclaw/skills" # Where arc-* skills are stored
  fallback_url: ""                 # Direct LLM fallback when proxy is down
  fallback_api_key: ""             # API key for fallback endpoint
  lesson_to_skill:
    enabled: true                  # Auto-convert lessons to skills
    min_severity: "warning"        # Minimum severity to convert
    max_skills_per_run: 3          # Max new skills per pipeline run
  prm:                             # Process Reward Model quality gate (optional)
    enabled: false                 # Use LLM-as-judge to score stage outputs
    model: "gpt-5.4"              # PRM judge model
    votes: 3                       # Majority vote count
    gate_stages: [5, 9, 15, 20]   # Stages to apply PRM gates

# === OpenClaw Bridge ===
openclaw_bridge:
  use_cron: false                  # Scheduled research runs
  use_message: false               # Progress notifications
  use_memory: false                # Cross-session knowledge persistence
  use_sessions_spawn: false        # Spawn parallel sub-sessions
  use_web_fetch: false             # Live web search
  use_browser: false               # Browser-based paper collection
```

</details>

---

## 🙏 Acknowledgments

Inspired by:

- 🔬 [AI Scientist](https://github.com/SakanaAI/AI-Scientist) (Sakana AI) — Automated research pioneer
- 🧠 [AutoResearch](https://github.com/karpathy/autoresearch) (Andrej Karpathy) — End-to-end research automation
- 🌐 [FARS](https://analemma.ai/blog/introducing-fars/) (Analemma) — Fully Automated Research System

---

## ⚠️ Ethics and Responsible Use

 AI-Paper-Generator is a research assistance tool, not a replacement for human researchers. We ask all users to observe the following principles:

**Academic integrity.** Papers generated by  AI-Paper-Generator should be treated as drafts that require thorough human review, verification, and revision before any submission. Authors listed on a paper bear full responsibility for its content, claims, and correctness. Using AI-generated text without adequate human oversight or disclosure may violate academic integrity policies at your institution or target venue.

**Transparency and disclosure.** We strongly encourage users to disclose the use of AutoResearchClaw (or any AI assistance) in their manuscripts, in accordance with the policies of the target venue (e.g., NeurIPS, ICML, ICLR, and most major venues now require disclosure of AI writing assistance). The Human-in-the-Loop Co-Pilot exists precisely to keep humans in meaningful control of research decisions.

**Citation and attribution.**  AI-Paper-Generator verifies citations through a 4-layer pipeline, but no automated system is perfect. Users must manually verify that all references are real, relevant, and correctly cited before submission. Fabricated or misattributed citations undermine scientific trust.

**Potential for misuse.** Like any powerful tool,  AI-Paper-Generator can be misused to produce low-quality or misleading research at scale. We do not condone using this system to generate paper mills, fraudulent submissions, or content designed to game peer review. We reserve the right to update the license or terms of use if systematic misuse is identified.

**Dual use.** Autonomous research systems raise broader questions about the future of scientific labor, authorship norms, and review processes. We welcome community discussion on these topics and are committed to developing this technology responsibly.

By using  AI-Paper-Generator, you agree to use it in a manner consistent with these principles and with the ethical guidelines of your institution and research community.
