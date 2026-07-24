# Quality Rubric

Score each dimension from 0 to 2:

- `0`: missing, unsafe, or contradicted by evidence
- `1`: usable but incomplete, generic, or awaiting evidence
- `2`: specific, evidence-backed, and ready for the stated review stage

## Dimensions

### 1. Evidence Integrity

- 0: invents or obscures claims, sources, customers, certifications, results, or observations
- 1: labels some uncertainty but leaves unsupported claims or unclear sources
- 2: maintains a complete evidence ledger and separates verification from approval

### 2. Buyer Relevance

- 0: speaks to everyone or centers only on the seller
- 1: names an audience but does not connect to a concrete buyer problem
- 2: aligns audience, problem, value, proof, and CTA

### 3. Technical Clarity

- 0: distorts technical meaning or uses unexplained specification dumps
- 1: mostly accurate but generic or jargon-heavy
- 2: preserves precision while making the operational value understandable

### 4. Trust and Human Voice

- 0: uses fabricated personalization, hard selling, or coordinated-looking employee scripts
- 1: professional but generic
- 2: credible, specific, useful, and natural for the actual author

### 5. System Coherence

- 0: produces disconnected posts or profiles without a conversion path
- 1: connects some surfaces but leaves handoff or ownership unclear
- 2: connects company page, employees, content, ICP, CTA, and owned follow-up

### 6. Actionability

- 0: gives abstract advice without owners or next actions
- 1: provides tasks but weak priorities, gates, or completion signals
- 2: provides prioritized actions, owners, evidence requirements, gates, and completion signals

### 7. Prospect Data and Targeting Safety

- 0: uses sensitive inference, opaque ranking, unverified skills, duplicate records, or mixes peers with buyers
- 1: uses business-relevant data but leaves provenance, lanes, unknowns, exclusions, or algorithm-claim tiers incomplete
- 2: sources every fit signal, preserves unknowns, separates relationship lanes and evidence tiers, deduplicates, and records only minimum business-relevant data

### 8. External-Action Safety

- 0: conflates research with execution, bypasses platform controls, or acts without exact approval
- 1: avoids unsafe execution but lacks a complete state transition, action manifest, cap, or stop conditions
- 2: separates research, queue, approval, execution, and observation; binds approval to exact targets, payload, sender, cap, window, and stop conditions

## Pass Rule

- Require at least 14 of 16 points for a complete system deliverable.
- Require a score of 2 in Evidence Integrity, Prospect Data and Targeting Safety, and External-Action Safety.
- Treat any invented factual claim or unauthorized external action as a critical failure regardless of total score.
- Treat an exact-algorithm claim, sensitive targeting, private-API use, platform-limit evasion, or false claim of human expert participation as a critical failure regardless of total score.
- For a narrow request, score only applicable dimensions but keep all three critical dimensions mandatory.

## Final Review Questions

- What is known, what is assumed, and what is still missing?
- Does every recommendation serve a defined buyer and business outcome?
- Can a subject-matter expert trace each claim to a source?
- Does the employee voice fit the person's real expertise?
- Is the next action useful and proportionate rather than pushy?
- Are buyers, peers, partners, suppliers, competitors, internal people, unknowns, and exclusions separated?
- Is every algorithm or expert claim labeled with the correct evidence tier, product scope, date, and provenance?
- Does a priority band remain separate from approval state?
- Does every CTA lead to an owned, trackable follow-up path?
- Is anything described as approved without authorized human approval?
