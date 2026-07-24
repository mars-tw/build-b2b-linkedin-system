# Relationship Growth Matrix

## Contents

1. Purpose and non-goals
2. Evidence and privacy rules
3. Candidate-generation lanes
4. Relationship lanes
5. Required row schema
6. Explainable scoring
7. Priority and action gates
8. Approval state machine
9. Portfolio diversity
10. Feedback and measurement
11. Stop conditions
12. Search patterns

## 1. Purpose and Non-Goals

Build an explainable research and prioritization system for finding relevant
people in the same industry, with the same or adjacent skills, or in a useful
buyer, partner, or knowledge role.

Interpret `fast` as reducing research and qualification time. Never interpret it
as increasing unsolicited action volume.

The matrix:

- expands discovery across graph, exact-match, semantic, and evidence lanes
- separates buyers, peers, partners, suppliers, competitors, and internal people
- preserves source, uncertainty, exclusion, and approval state
- recommends the next review step, not permission to contact

The matrix is not:

- LinkedIn's private ranking formula
- an automated contact list
- proof that a profile skill equals verified competence
- proof that a same-industry person has buying intent
- permission to scrape, automate invitations, or evade platform limits

## 2. Evidence and Privacy Rules

Record only minimum, business-relevant public evidence. For each observation,
store a source URL or supplied source, observation date, and confidence.

Use this scale:

- `verified`: directly supported by a current business source
- `supported`: plausible from more than one relevant signal but needs confirmation
- `unknown`: not evidenced; preserve this value rather than guessing
- `excluded`: contradicted, opted out, duplicated, outside scope, or prohibited

Treat a capability as verified only when it is explicitly stated or supported by
current work experience, authored content, projects, certifications, or other
traceable professional evidence. A title, a skill tag, or a Skills Graph
relationship is a discovery signal, not proof of ability.

Never collect, infer, or score sensitive or protected traits, private contact
data, family state, health, political or religious belief, ethnicity, age, sexual
orientation, or other non-business personal information.

Deduplicate by canonical profile URL or another authorized stable identifier.
Honor prior contact, opt-out, do-not-contact, blocked, duplicate, and explicit
disinterest states.

## 3. Candidate-Generation Lanes

Use multiple lanes and record which one produced each candidate:

1. `network`: second- or third-degree relationship, mutual connection, shared
   company, school, group, event, or verified professional interaction
2. `exact`: exact industry, function, title, seniority, account type, or
   explicitly stated skill
3. `semantic`: skill alias, parent, child, sibling, or a natural-language query
   describing the capability or business problem
4. `evidence`: authored technical content, current projects, relevant work,
   standards activity, speaking, or another traceable professional artifact

Generate candidates broadly enough to avoid a single-source echo chamber.
Similarity only retrieves candidates; human review determines relevance and
permitted action.

## 4. Relationship Lanes

Classify every candidate into exactly one primary lane:

- `buyer`: role and account context plausibly align with a defined buying problem
- `peer_expert`: overlapping expertise for learning, credibility, or referral
- `partner_ecosystem`: complementary capability, integrator, association,
  researcher, standards body, event, or technical media
- `supplier`: current or potential upstream provider
- `competitor`: overlapping offer or commercial conflict
- `internal`: current company, colleague, or governed internal relationship
- `unknown`: insufficient evidence to classify
- `exclude`: out of scope, opted out, duplicate, prohibited source, or hard risk

Do not merge these lanes into one opaque growth score. Same-industry or
same-skill similarity must never be treated as buyer intent.

## 5. Required Row Schema

| Field | Required content |
|---|---|
| Candidate ID | Canonical public profile URL or authorized stable ID |
| Name | Public professional name; optional when using anonymized review |
| Source and date | Query or source URL plus observation date |
| Candidate lane | network / exact / semantic / evidence |
| Relationship lane | buyer / peer_expert / partner_ecosystem / supplier / competitor / internal / unknown / exclude |
| Industry evidence | Value, source, and confidence |
| Account evidence | Company type or target-account fit, source, and confidence |
| Role evidence | Function, role, seniority, source, and confidence |
| Skill evidence | Exact, parent/child, sibling, or unknown; include proof |
| Need evidence | Business problem or use-case evidence; never infer intent |
| Relationship context | Degree, mutual context, shared event, or verified interaction |
| Professional evidence | Work, project, content, certification, or unknown |
| Risk and exclusion | Duplicate, opt-out, conflict, prohibited source, or other hard risk |
| Priority | P1 / P2 / HOLD / EXCLUDE |
| Permitted next step | Research, follow, observe, draft, human review, or approved action |
| State | discovered / verified / classified / queued / approved / executed / observed / blocked / cancelled / expired |
| Rationale | Short, source-grounded explanation |

## 6. Explainable Scoring

Use priority bands without a composite score by default. When the user needs
weighted comparison, disclose every weight and keep all underlying fields.

The bundled scorer uses this optional 100-point model:

- target account fit: 16
- role or function fit: 16
- industry fit: 12
- skill fit: 18, using the strongest of exact, parent/child, or sibling evidence
- relationship path and mutual context: 12
- shared professional context: 6
- recent relevant professional activity: 6
- geography fit: 4
- language fit: 4
- evidence confidence: 6

Apply skill similarity as:

`18 × max(exact, 0.75 × parent_or_child, 0.45 × sibling)`

This formula is a transparent local heuristic, not a LinkedIn formula. Never use
the score to infer intent, competence, or permission. A hard exclusion overrides
the score.

Require at least two sourced fit axes before assigning P1. Record separate
evidence references for industry, account, role, skill, and relationship
context. A high numeric score with fewer than two sourced axes remains `HOLD`.

Recommended universal hard exclusions include:

- `do_not_contact`
- `explicit_disinterest`
- `duplicate`
- `excluded_by_policy` after the exact campaign policy excludes an otherwise
  valid lane such as current company, supplier, or competitor
- `irrelevant_role`
- `unverified_identity`
- `prohibited_source`
- `spam_or_fake_account`

## 7. Priority and Action Gates

- `P1`: goal-relevant lane, at least two verified fit axes, no exclusion, and a
  legitimate relationship path. Send only to human review.
- `P2`: one verified axis plus one supported axis. Research only, or record a
  possible nurture step for later queueing and exact approval.
- `HOLD`: identity, lane, capability, relevance, context, or permission unresolved.
- `EXCLUDE`: opt-out, duplicate, unrelated, prohibited source, sensitive
  inference, explicit disinterest, or hard risk.

For an optional numeric score:

- 80–100: P1 only when evidence and relationship path are verified
- 65–79: P2; research, or propose follow, observe, or natural contribution as a
  possible queued step that still requires exact approval
- below 65: HOLD or EXCLUDE according to the evidence

A high score never changes approval state. When a person is unfamiliar and no
legitimate context exists, a later approved plan may prefer follow, relevant
public participation, a mutual introduction, a group or event, or an authorized
InMail path. Never use a connection invitation as an unsolicited sales pitch.

## 8. Approval State Machine

Use this state machine without skipping stages:

`discovered -> verified -> classified -> queued -> approved -> executed -> observed`

- `discovered`: candidate was found; no action permission exists
- `verified`: identity and minimum professional evidence were checked
- `classified`: relationship lane, priority, risks, and next step were assigned
- `queued`: a proposed action exists but is not authorized
- `approved`: an authorized human approved the exact action manifest
- `executed`: the exact approved action was performed and evidence recorded
- `observed`: outcome and stop state were recorded

Any change to target, sender, payload, count, channel, time window, cap, or stop
condition returns the item to `queued`.

Any stop condition moves the item to `blocked`. Approval-window expiry moves it
to `expired`. Human withdrawal, opt-out, or explicit disinterest moves it to
`cancelled`. Returning any terminal item to `queued` requires fresh verification
and a new exact approval.

Before any `operate` action, require an exact manifest:

- action ID and action type
- exact target identifiers and count
- sender or account
- exact payload
- evidence, candidate lane, and relationship lane
- deduplication, prior-contact, and opt-out results
- time window and maximum count
- approval owner, reference, and current status
- approval expiry
- stop conditions
- blocking or cancellation reason
- rollback or recovery path when one exists

Authorization selects among safe actions. It never waives law, privacy,
anti-spam, opt-out, platform-integrity, or company-policy constraints.

## 9. Portfolio Diversity

Avoid filling the network with one title, company, or popular creator. Use a
portfolio target as a planning hypothesis, then adapt it to the user's goal.

A useful technical-B2B starting hypothesis is:

- 60% core industry: same skill, complementary skill, and defined buyer roles
- 40% adjacent and bridge roles: supply chain, ecosystem, standards, research,
  new applications, new regions, or complementary expertise

This is not a LinkedIn rule or universal benchmark. Preserve diversity across
skill clusters, company size, geography, role, and viewpoint when relevant.

## 10. Feedback and Measurement

Scale research and qualification before scaling any external action. Measure:

- qualified-candidate rate by search lane
- evidence-complete rate
- buyer / peer / partner classification accuracy
- relevant acceptance rate after a sufficient authorized sample
- qualified two-way conversation rate
- useful value exchange or introduction
- relationship activation over the chosen window
- opportunity movement into an authorized handoff
- negative, opt-out, pending, and complaint rates

Treat followers, impressions, connection count, SSI, and comment volume as
diagnostic context, not success metrics.

For small samples, report counts and uncertainty. Do not publish causal claims
from uncontrolled before-and-after observations. Test one variable at a time and
record segment, window, sample size, and competing explanations.

## 11. Stop Conditions

Stop or keep the queue on hold when:

- LinkedIn displays a warning, restriction, verification, challenge, or
  automation concern
- an intended recipient, sender, payload, or approval does not match the manifest
- a duplicate, prior opt-out, do-not-contact state, or explicit disinterest appears
- identity, relationship lane, or relevance cannot be verified
- pending, ignored, negative, or complaint signals materially deteriorate
- the team cannot responsibly respond to accepted relationships
- a live company hold, legal constraint, or project-specific action cap applies
- any crawler, bot, private API, session-cookie reuse, CAPTCHA avoidance, quota
  evasion, bulk action, engagement pod, or artificial coordination is proposed

LinkedIn does not publish a fixed safe invitation number for standard accounts.
Do not invent one. Follow current platform UI and policy, plus any stricter
company or project rule.

## 12. Search Patterns

Build queries from:

`industry terms × role/function × explicit skill/technology × account type × region × relationship context`

Examples:

```text
("optical engineer" OR photonics OR "fiber optic")
AND ("manufacturing" OR "process engineering")
NOT (recruiter OR student)
```

```text
("test engineer" OR "reliability engineer" OR "quality engineer")
AND ("optical communication" OR "optical transceiver")
```

```text
("procurement manager" OR "strategic sourcing" OR "supplier quality")
AND (photonics OR "fiber optic" OR connector)
```

Treat all industry examples as hypotheses until replaced with the user's
verified terminology. Record the exact query and date, change one condition at a
time, and manually inspect relevance before retaining candidates.
