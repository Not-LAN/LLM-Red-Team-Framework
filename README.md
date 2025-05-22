# 🧠 LLM Red Team Framework

> Adversarial testing suite for Large Language Models, simulating real-world attack chains, evasions, and compliance assessments — with detailed reporting and visualizations.

---

## 🔍 Overview

This project provides a structured framework to red team LLMs using a modular, extensible architecture. It supports both **attack** and **compliance** testing modes, generates Markdown reports, visualizes threat chains, and maps each test to the industry frameworks **MITRE ATLAS** and **OWASP Top 10 for LLMs**.

---

## ✨ Features

- ✅ **Modular Test Engine** — Easily create and run new attack or compliance modules.
- 🔗 **Multiphase Adversary Chains** — Define sequential YAML-based attack plans with dependencies.
- 📊 **Markdown Reporting** — Rich, shareable reports with summaries, prompts, responses, and impact.
- 📈 **Flow Graph Rendering** — Generates SVG/PNG visual diagrams for emulated adversarial chains.
- 🧠 **Tag Glossary** — Built-in descriptions for OWASP and MITRE tags used in assessments.
- 💬 **CLI Interface** — Run modules, categories, or full emulation plans with a single command.

---

## 🧪 Example Emulation Plan

```yaml
name: Safety Barrier Validation
mode: compliance
description: >
  Tests that the LLM rejects known attack patterns such as prompt injection,
  hallucinated data exposure, and evasion through encoding and typos.

steps:
  - step: Direct Prompt Injection
    module: modules.injection.test_direct_injection
    expected_leakage: false
    mitre_tactic: ATLAS-TA0009

  - step: Fake Credential Dump
    module: modules.data_exposure.test_fake_user_dump
    expected_leakage: false
    mitre_tactic: ATLAS-TA0011
```

---

## 🛠️ Supported Models

- 🔹 OpenAI GPT (via API)
- 🔹 Google Gemini (via SDK)
- 🔹 Mistral (custom REST API interface, not available in current project)
- 🔸 Easily extendable via `runners/` (Claude, Cohere, Replicate...)

---

### ✅ Usage Modes

You can run tests in multiple ways:

- **Full Plan Execution**: Run multi-step attack or compliance plans from YAML definitions.
- **Category Execution**: Run all tests in a given category (e.g., `injection`, `evasion`).
- **Individual Module Execution**: Execute a single test module for targeted validation:
  
  ```bash
  python -m interface.cli tests run-module modules.injection.test_direct_injection --model openai

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-red-team.git
cd llm-red-team
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Export your model credentials

```bash
export OPENAI_API_KEY=...
export GEMINI_API_KEY=...
export MODEL_API=...
export MODEL_ID=...
export USER_KEY=...
```

### 3. Run a test plan

```bash
python -m interface.cli run-plan scenarios/safety_barrier_validation.yaml --model gemini
```

### 4. View the report

Reports are saved in the `reports/` directory as Markdown + visual graphs (SVG/PNG).

---

## 📁 Project Structure

```
├── core/                # Engine, config, mappings, reporting logic
├── interface/           # CLI interface
├── modules/             # Test modules grouped by category
├── prompts/             # Reusable prompt snippets
├── runners/             # Model-specific interfaces
├── scenarios/           # YAML-based adversarial plans
├── reports/             # Auto-generated reports
└── requirements.txt
```

---

## 📚 Framework Coverage

| Standard           | Included |
|--------------------|----------|
| OWASP LLM Top 10   | ✅       |
| MITRE ATLAS        | ✅       |
| Custom Tags        | ✅       |

---

## 🧩 Future Roadmap

- [ ] Live Interactive CLI Sessions (`interactive` command)
- [ ] PDF export of reports
- [ ] Regression testing baselines
- [ ] Plugin-based module loading
- [ ] Web dashboard for report browsing

---

## 🤝 Contributing

Pull requests welcome! If you have new modules, integrations, or feedback — open an issue or fork the repo.

---

## ⚖️ License

MIT License © 2025 José Fernando Velázquez Hernández