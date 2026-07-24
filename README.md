# Build B2B LinkedIn System

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](CITATION.cff)

An evidence-first Codex skill for B2B LinkedIn positioning, content, ideal
customer profiles, relationship discovery, buyer/peer/partner matrices,
approval-gated outreach, CTA and CRM handoff, and a 30-day rollout.

It converts LinkedIn's publicly described multi-stage recommendation pattern
into a transparent local research workflow. It does not claim access to
LinkedIn's private algorithm, and it is not a mass-outreach bot.

## 中文說明

這是一套以證據為核心的 B2B LinkedIn 工作技能，涵蓋公司定位、員工專業品牌、技術內容、
ICP、同產業／同技能人選發現、買家／同業／夥伴分流、人工核准的關係建立、CTA 與 CRM
交接，以及 30 天導入計畫。

「快速」是加速搜尋、驗證、分類與排序，不是增加陌生邀請量。系統不會宣稱破解 LinkedIn
私有演算法，也不會在未經精確核准時發布、傳訊、送出邀請、修改個人檔案或寫入 CRM。

## What It Produces

- An evidence ledger separating facts, supported material, hypotheses, and missing inputs
- A prioritized audit of company page, employee profiles, content, targeting, and conversion
- Positioning, About copy, profile frameworks, banner guidance, and CTA recommendations
- Evidence-backed content pillars and review-ready content briefs
- ICP definitions and business-relevant prospect-research fields
- An explainable same-industry and same-skill relationship matrix
- Separate buyer, peer, partner, supplier, competitor, internal, unknown, and exclude lanes
- A platform-signal and expert-claim ledger with provenance and product scope
- Queue-only external-action manifests with approval and stop conditions
- CTA-to-owner-to-CRM handoff maps
- A 30-day plan with owners, approval gates, and quality metrics

## Algorithm Evidence Boundary

The skill uses public LinkedIn Engineering, Help, legal, and policy sources to
model a high-level pattern:

```text
multi-lane candidate generation
-> evidence verification
-> relationship classification
-> explainable local prioritization
-> diversity review
-> exact human approval
```

It keeps People You May Know, People Search, Feed, Recruiter, and Sales Navigator
evidence separate. Practitioner studies are labeled as hypotheses rather than
platform facts.

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

```text
Use $build-b2b-linkedin-system to build an evidence-based buyer/peer/partner
relationship matrix for our industry. Research and queue only; do not send
invitations or messages.
```

```text
Use $build-b2b-linkedin-system to separate official LinkedIn algorithm evidence,
published expert analysis, and testable hypotheses, then run an independent
multi-lens debate.
```

```text
Use $build-b2b-linkedin-system to audit our LinkedIn presence and create a
review-only 30-day improvement plan.
```

## Optional Candidate Scorer

The bundled standard-library script scores an authorized CSV locally. It never
fetches LinkedIn data and never grants contact permission.

```bash
python skills/build-b2b-linkedin-system/scripts/score_relationship_candidates.py \
  candidates.csv scored-candidates.csv
```

Start from
`skills/build-b2b-linkedin-system/examples/relationship-candidates.csv`; replace
the fictional rows with authorized evidence. Every numeric fit field uses
`0..1`.

Run its built-in test:

```bash
python skills/build-b2b-linkedin-system/scripts/score_relationship_candidates.py --self-test
```

## Safety Model

- Never fabricate product claims, prospect activity, skills, buying intent, or human participation.
- Never merge same-skill peers, buyers, suppliers, and competitors into one opaque score.
- Never use sensitive personal traits or private data for targeting.
- Never use scraping, bots, undocumented APIs, session-cookie reuse, bulk actions, fake engagement, or limit evasion.
- Keep discovery, verification, classification, queue, approval, execution, and observation separate.
- Require an exact human approval manifest for any external action.
- Honor opt-outs, prior contact, do-not-contact states, live holds, and platform warnings.
- Optimize for qualified conversations and value exchange, not connection count or vanity metrics.

## Repository Layout

```text
.
├── CITATION.cff
├── llms.txt
├── skills/build-b2b-linkedin-system/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── examples/relationship-candidates.csv
│   ├── scripts/score_relationship_candidates.py
│   └── references/
│       ├── platform-signals.md
│       ├── playbook.md
│       ├── quality-rubric.md
│       ├── relationship-growth-matrix.md
│       └── templates.md
├── evals/cases.json
└── tools/validate_skill.py
```

The original presentation and transcript are not redistributed. The repository
contains the generalized workflow, examples, templates, evidence controls, and
local scoring utility required by the skill.

## Validate

Requires Python 3.10 or newer and no third-party packages.

```bash
python tools/validate_skill.py
```

The validator checks structure, metadata, evaluation-case schema, and the local
scorer self-test. Behavioral forward-testing remains a separate quality gate.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. New behavior
should include an evaluation case and preserve evidence integrity, targeting
safety, provenance, and external-action approval.

## Citation and AI Discovery

- [CITATION.cff](CITATION.cff) provides release and repository metadata.
- [llms.txt](llms.txt) provides a machine-readable capability and safety summary.

## License

[MIT](LICENSE)
