# Repository structure

```
AutoResearchClaw/
│
├── README.md                  ← Start here
├── config.example.yaml        ← Copy this → config.yaml and fill in your API key
├── prompts.default.yaml       ← Default LLM prompts (rarely need to edit)
│
├── AGENTS.md                  ← How AI agents (OpenClaw, Claude Code) bootstrap the pipeline
├── CLAUDE.md                  ← Claude Code specific instructions
│
├── researchclaw/              ← Source code — you don't need to touch this to use the tool
│   ├── pipeline/              ← The 23-stage research pipeline
│   ├── agents/                ← Benchmark, code search, and figure sub-agents
│   ├── experiment/            ← Sandbox, Docker, SSH execution backends
│   ├── literature/            ← arXiv, Semantic Scholar, OpenAlex clients
│   ├── llm/                   ← LLM client with model fallback chain
│   ├── memory/                ← Short-term, long-term, and vector memory
│   ├── hitl/                  ← Human-in-the-loop co-pilot system
│   └── skills/                ← Built-in research skills library
│
├── docs/                      ← User guides and paper showcase
│   ├── co-pilot.md            ← Co-pilot mode, intervention modes, CLI commands
│   ├── integration.md         ← OpenClaw, ACP agents, messaging platforms
│   ├── tester-guide.md        ← How to test the pipeline and give feedback
│   ├── languages/             ← Translated READMEs (CN, JA, KO, FR, DE, ES, PT, RU, AR)
│   └── showcase/              ← 8 generated papers (PDFs on GitHub Releases)
│
├── images/                    ← Logo and framework diagram
└── tests/                     ← Test suite (2,699 tests)
```

## Where to go depending on what you need

| I want to… | Go to… |
|-----------|--------|
| Run the pipeline | `README.md` → Quick start |
| Configure the LLM or experiment mode | `config.example.yaml` |
| Use co-pilot / human-in-the-loop mode | `docs/co-pilot.md` |
| Connect to OpenClaw, Claude Code, Discord | `docs/integration.md` |
| Add a custom research skill | `researchclaw/skills/` |
| Understand how the 23 stages work | `researchclaw/pipeline/` |
| Run the tests | `pytest tests/` |
