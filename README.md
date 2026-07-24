# Build B2B LinkedIn System

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An evidence-first Codex skill for building a complete B2B LinkedIn system: company positioning, employee profiles, technical content, ideal customer profiles, prospect research, relationship-first outreach, CTA and CRM handoff, and a 30-day rollout.

This is not a mass-outreach bot. It does not publish, message people, change profiles, or write CRM data without explicit authorization.

## 中文簡介

這是一套以證據為核心的 Codex 技能，用來規劃與稽核 B2B LinkedIn 成長系統，涵蓋公司頁定位、員工個人品牌、技術內容、ICP、潛在客戶研究、關係式開發、CTA／CRM 銜接與 30 天落地計畫。

技能會區分已驗證事實、待確認資料、策略假設與缺失證據；AI 只負責輔助草擬，公開內容與外部動作仍需明確的人工作業與授權。

## What It Produces

- An evidence ledger that separates verified facts, supported material, hypotheses, and missing inputs
- A prioritized audit of the company page, employee profiles, content, targeting, and conversion path
- Positioning, About copy, headline frameworks, banner guidance, and CTA recommendations
- Evidence-backed content pillars and review-ready content briefs
- ICP definitions and business-relevant prospect-research fields
- Relationship-first connection and follow-up drafts with visible placeholders
- CTA-to-owner-to-CRM handoff maps
- A 30-day plan with owners, approval gates, readiness metrics, and outcome metrics

## Install

### Ask Codex to install it

```text
Install the skill from:
https://github.com/mars-tw/build-b2b-linkedin-system/tree/main/skills/build-b2b-linkedin-system
```

### Manual installation

Copy `skills/build-b2b-linkedin-system` into:

- Windows: `%USERPROFILE%\.codex\skills\build-b2b-linkedin-system`
- macOS or Linux: `~/.codex/skills/build-b2b-linkedin-system`

Start a new Codex task after installation so the skill catalog refreshes.

## Use

Invoke the skill explicitly:

```text
Use $build-b2b-linkedin-system to audit our LinkedIn presence and create an evidence-based 30-day improvement plan.
```

Other examples:

```text
Use $build-b2b-linkedin-system to rewrite our company About section without inventing certifications or results.
```

```text
Use $build-b2b-linkedin-system to define an ICP and prepare relationship-first outreach drafts. Do not send anything.
```

```text
Use $build-b2b-linkedin-system to connect our content plan to an RFQ and CRM handoff.
```

## Safety Model

- Never transfer an example into a company claim.
- Never fabricate product specifications, certifications, customers, results, or prospect activity.
- Keep AI-generated material in draft status until a qualified human reviews it.
- Require explicit authorization for every publication, message, profile change, or CRM write.
- Optimize for buyer trust and qualified conversations, not vanity metrics or activity volume.
- Avoid spam, fake personalization, and repeated unwanted follow-ups.

## Repository Layout

```text
.
├── CITATION.cff
├── llms.txt
├── skills/build-b2b-linkedin-system/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── playbook.md
│       ├── quality-rubric.md
│       └── templates.md
├── evals/cases.json
└── tools/validate_skill.py
```

The original presentation and its transcript are not redistributed. The repository contains only the generalized workflow, examples, templates, and quality controls required by the skill.

## Validate

Requires Python 3.10 or newer and no third-party packages.

```bash
python tools/validate_skill.py
```

Run this check before opening a pull request.

The repository does not currently advertise a hosted CI check. This portable local validator is the automated quality gate.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. New behavior should include an evaluation case and must preserve evidence integrity and external-action safety.

## Citation and AI Discovery

- [CITATION.cff](CITATION.cff) provides release and repository metadata for citation tools.
- [llms.txt](llms.txt) provides a concise, machine-readable capability and safety summary.

## License

[MIT](LICENSE)
