# Platform Signals and Expert Synthesis

## Contents

1. Claim discipline
2. Public architecture pattern
3. Official evidence register
4. Practitioner evidence register
5. Disputed tactics and rulings
6. Multi-expert debate protocol
7. Experiment protocol
8. Required non-claims

## 1. Claim Discipline

Do not claim to have reverse-engineered LinkedIn's exact algorithm. Public
information supports an architecture pattern and classes of signals, not
complete production code, fixed weights, guaranteed outcomes, or a permanent
safe activity quota.

Label every algorithm or growth claim:

| Tier | Source class | Allowed treatment |
|---|---|---|
| 1 | Current official LinkedIn Help, Engineering, legal, or policy source | Platform fact within the named product, date, and scope |
| 2 | Reproducible local observation with segment, sample, window, and method | Local observation, not platform fact |
| 3 | Named practitioner analysis or published case | Expert hypothesis with attribution and limitations |
| 4 | Reasoned idea without direct evidence | Hypothesis for testing only |

Record contradictory evidence and a recheck date for time-sensitive claims.
Never move a tier 2–4 claim into tier 1 because several people repeat it.

Keep product boundaries explicit:

- Feed ranking evidence does not prove People Search or PYMK ranking behavior.
- Recruiter or Sales Navigator research does not prove consumer People Search behavior.
- Historical architecture does not prove the current production implementation.
- A Skills Graph relationship does not prove a member's real capability.

## 2. Public Architecture Pattern

The public pattern can be abstracted as:

1. candidate generation from graph relationships, similarity, and heuristics
2. lightweight calibration or first-stage ranking
3. deeper multi-objective ranking
4. fairness, diversity, integrity, and concentration-aware re-ranking
5. online learning or evaluation from real member behavior

Use this as inspiration for an external, human-auditable discovery funnel:

`multi-lane discovery -> evidence verification -> relationship classification -> local prioritization -> diversity review -> human approval`

Do not use it to automate platform activity or claim access to internal signals.

## 3. Official Evidence Register

The following sources were checked on 2026-07-24. Recheck live platform
instructions and policy before exact operational guidance.

### People You May Know

[Building a Large-Scale Recommendation System: People You May Know](https://www.linkedin.com/blog/engineering/recommendations/building-a-large-scale-recommendation-system-people-you-may-know)
(2024-02-06) describes a multi-stage funnel: L0 candidate generation, L1
calibration, L2 deep ranking for member actions such as invitation and
acceptance, followed by fairness and diversity re-ranking.

[Candidate Generation in a Large Scale Graph Recommendation System: PYMK](https://www.linkedin.com/blog/engineering/recommendations/candidate-generation-in-a-large-scale-graph-recommendation-system-people-you-may-know)
(2024-06-18) describes three candidate families:

- graph relationships, including 2/3-hop paths, common connections, and
  Personalized PageRank
- member similarity using profile, education, employment, skills, Two-Tower
  embeddings, and approximate-nearest-neighbor retrieval
- heuristic sources such as recent feed, search, or notification interaction

The article also reports that graph-neural-network embeddings had not replaced
explicit 2/3-hop and graph-walk sources at that time. Do not turn this historical
finding into a permanent current-production claim.

[People You May Know overview](https://www.linkedin.com/help/linkedin/answer/a544682/people-you-may-know-feature-overview?lang=en)
states that recommendations can reflect common connections, similar profile
information and experience, the same company or industry, and the same school.
It also states that LinkedIn does not scan message contents for this feature.

### People Search

[Reimagining LinkedIn's search tech stack](https://www.linkedin.com/blog/engineering/search/reimagining-linkedins-search-stack)
(2026-01-21) describes intent understanding, embedding-based retrieval, and
cross-encoder small-language-model ranking for AI-powered People Search. It
describes profile-aware query understanding and multi-objective behavior
signals, but many training details are illustrated through Job Search. Do not
assume every internal module is identical across products.

[LinkedIn Search relevance for people search](https://www.linkedin.com/help/linkedin/answer/a524188/linkedin-search-relevance-people-search?lang=en)
states that People Search is personalized and can use the query, the searcher's
profile and activity, connections and network, similar searches, and search
history. It warns that keyword stuffing may trigger spam detection rather than
improve visibility. Exact weights are proprietary.

### Skills

[Building and maintaining LinkedIn's Skills Graph taxonomy](https://www.linkedin.com/blog/engineering/data/building-maintaining-the-skills-taxonomy-that-powers-linkedins-skills-graph)
(2023-03-21) describes canonical skills, aliases, parent/child/sibling
relationships, polyhierarchy, embeddings, machine learning, and human
taxonomists. The article's size figures are a 2023 snapshot, not current counts.

[Completing a member knowledge graph with graph neural networks](https://www.linkedin.com/blog/engineering/knowledge/completing-a-member-knowledge-graph-with-graph-neural-networks)
(2021-12-01) describes inferring possibly missing skills from professional
entities. Inferred or adjacent skills remain discovery hypotheses until verified
from the person's current professional evidence.

### Feed

[Engineering the next generation of LinkedIn's Feed](https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed)
(2026-03-12) describes profile, industry, experience, skills, geography, and a
long interaction sequence in retrieval and ranking. It concerns Feed content,
not a direct PYMK or People Search formula.

### Safety and Limits

[Prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions?lang=en)
prohibits unauthorized crawlers, bots, extensions, scraping, automated contacts
or messages, automated reactions or comments, fake engagement, and bypassing
usage limits.

[Invitation restrictions](https://www.linkedin.com/help/linkedin/answer/a551012/invitation-limitations?lang=en)
states that sending many invitations quickly, accumulating ignored or pending
invitations, spam reports, or suspected automation can cause restrictions. It
does not publish one fixed safe weekly invitation number for standard accounts.

[Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies)
prohibit irrelevant or repetitive promotion, invitation-based promotion to
strangers, and coordinated artificial engagement such as engagement pods.

## 4. Practitioner Evidence Register

Practitioner sources are tier 3. Attribute them and retain their uncertainty.
They do not become platform facts. The following register was observed on
2026-07-24.

| Practitioner and publication | Claim used for synthesis | Method or limitation | Permitted use |
|---|---|---|---|
| [Richard van der Blom, 2025-04-28](https://www.linkedin.com/posts/richardvanderblom_chapter-1-algorithm-insights-report-2025-activity-7322514599126130688-Q895) | Large observational reports propose content-quality and interaction patterns. | Self-published commercial research; complete sampling and causal method are not platform-verified. | Content-experiment hypothesis only. |
| [John Espirian, 2024-02-28](https://www.linkedin.com/posts/johnespirian_linkedinlearnerlounge-linkedintips-activity-7168538836778602496-RVKx) and [network-pruning experiment, 2024-08-28](https://espirian.co.uk/linkedin-disconnection-experiment/) | Selective, contextual invitations and clear positioning support network quality. | Personal practice and uncontrolled before/after observation. | Use the quality principle; do not claim pruning causes reach. |
| [Brynne Tillman, 2014](https://business.linkedin.com/content/dam/business/sales-solutions/global/en_US/c/pdfs/linkedin-17-tips-start-the-social-selling-transformation-en-us.pdf) | Buyer-centered profiles and warm introductions reduce cold-start friction. | Old LinkedIn/Demand Gen material; interface details and figures may be obsolete. | Relationship-first design principle after current UI recheck. |
| [Mandy McEwen, 2025-08-05](https://www.linkedin.com/posts/mandymcewen_one-sales-team-got-3-new-clients-in-a-month-activity-7358549880568455169-m5N-) | Recognition through profile, content, and engagement can warm outreach. | Client outcome is author-reported and not independently verified. | Sequencing hypothesis; reject speed and pipeline-multiple guarantees. |
| [Daniel Disney interview, 2023](https://www.linkedin.com/business/sales/blog/real-sales/how-daniel-disney-sells-know-that-people-need-what-you-sell) and [volume claim, 2026-05-16](https://www.linkedin.com/posts/danieldisney_a-c-level-exec-at-microsoft-once-replied-activity-7461430279665156096-zg9V) | Relevance, value, and personalization matter; the later post also proposes a daily connection volume. | Practitioner guidance; no universal safe volume is established. | Use relevance and value; reject the volume as a platform benchmark. |
| [Justin Welsh, 2023-01-02](https://www.linkedin.com/posts/justinwelsh_when-i-see-people-starting-on-social-media-activity-6993255856372883456-e-_w) and [2024-06-17](https://www.linkedin.com/posts/justinwelsh_if-i-were-starting-on-linkedin-today-and-activity-7184388307609387008-I9wl) | Consistency, niche expertise, helpful information, and relevant participation support audience building. | Individual operating model, not a controlled platform study. | Positioning and content hypotheses; reject visibility-seeking comments without relevance. |
| [Jasmin Alić, 2025-03-31](https://www.linkedin.com/posts/alicjasmin_the-first-quarter-of-2025-is-already-over-activity-7312420764442406912-RFZP) and [2025-09-04](https://www.linkedin.com/posts/alicjasmin_i-received-214954-comments-this-year-but-activity-7368953235195297796-zAWw) | Community and continued conversation matter; one post also uses high-volume comment and message tactics. | Personal operating data; causality and transferability are unverified. | Use community follow-through; reject fixed interaction or DM quotas. |
| [Lea Turner, 2026-02-19](https://www.linkedin.com/posts/lea-turner_the-world-is-a-lonelier-place-than-ever-activity-7430161057769295872-nvPf) | Contribution and connection are more useful community lenses than raw count. | Qualitative practitioner framework. | Community-design lens only. |

When citing a practitioner in a deliverable, use the exact publication, include
the publication and observation dates, state the limitation, and recheck the
source if the claim affects a current operational decision.

## 5. Disputed Tactics and Rulings

| Dispute | Growth argument | Counterargument | Ruling |
|---|---|---|---|
| Fast expansion vs selective network | More relevant invitations may increase discovery | Volume increases rejection, restriction, and low-quality network risk | Scale discovery; gate all external action by evidence and approval |
| Exact skill vs adjacent skill | Exact match improves immediate relevance | Adjacent skills and bridge nodes reduce echo chambers | Use exact match for core recall and adjacent skills for a controlled bridge portfolio |
| Early comments vs useful comments | Early placement can gain visibility | Timing-first behavior becomes noise or manipulation | Relevance and contribution are mandatory; timing is at most a test variable |
| Same-industry peers vs buyers | Peers are easy to identify | Peers may be competitors and have no buying intent | Separate relationship lanes and never infer buyer status |
| Repeated follow-up vs respect | More touches may improve replies | Silence, opt-out, and annoyance damage trust | At most one permission-based follow-up unless the recipient actively re-engages |
| Profile optimization vs keyword stuffing | Clear terminology aids semantic retrieval | Repetition can trigger spam detection and weaken trust | Use truthful, buyer-readable evidence; never stuff keywords |
| Core density vs network diversity | Dense specialization builds authority | Excess homogeneity limits non-redundant information | Start with a transparent core/bridge portfolio and validate outcomes |

## 6. Multi-Expert Debate Protocol

Use this protocol when the user asks for many experts, deep debate, or
distillation.

Assign independent review lenses:

1. recommendation-system and graph retrieval
2. search relevance and semantic retrieval
3. skills taxonomy and capability evidence
4. technical B2B growth
5. community and trust
6. sales operations and relationship handoff
7. privacy, anti-abuse, and platform policy
8. measurement, experimentation, and statistics
9. industry subject-matter expertise
10. independent red-team audit

Require each contributor to submit:

- claim
- evidence tier and exact source
- product scope and date
- assumptions
- strongest counterargument
- risk if wrong
- reversible test or stop condition

Keep builders and auditors separate. A contributor must not approve its own
synthesis. Use no more than two rework rounds before escalating unresolved
claims to a human decision owner. Resolve conflict by source quality, scope,
recency, and risk—not majority vote.

Label provenance accurately:

- `connected human participant`: a real person directly participated and their
  output was recorded
- `published expert source`: the system synthesized a named person's public work
- `AI reviewer role`: an AI evaluated the evidence from a declared lens

Never claim that named LinkedIn experts joined a debate when only their published
work was synthesized. Never invent quotes, endorsement, consensus, or attendance.

## 7. Experiment Protocol

For a local growth experiment:

1. state the hypothesis and evidence tier
2. define one independent variable
3. define the eligible segment and exclusions before observing outcomes
4. record sample size, date window, source, and approval state
5. choose a quality outcome such as qualified conversation or useful exchange
6. set stop conditions before execution
7. report counts, rates, uncertainty, and alternative explanations
8. retain contradictory results

Potential low-risk tests include:

- warm introduction versus verified shared-event context
- exact-skill versus parent/child-skill candidate quality
- core-industry versus bridge-role conversation quality
- query-source precision across Boolean, natural language, connections-of, and PYMK
- profile evidence completeness before and after an authorized profile revision

Do not test:

- bulk invitation speed
- automated comments or messages
- engagement pods or reciprocal interaction agreements
- identical templates at scale
- account rotation or limit evasion
- sensitive-trait targeting

## 8. Required Non-Claims

- Do not claim the exact private LinkedIn algorithm or its weights.
- Do not claim a guaranteed reach, ranking, recommendation, acceptance, lead, or
  revenue outcome.
- Do not combine historical PYMK, current Feed, People Search, Recruiter, and
  Sales Navigator research into one current universal algorithm.
- Do not claim that Feed behavior directly increases PYMK or People Search rank.
- Do not claim that same industry, same skill, or mutual connections guarantee a
  recommendation or a legitimate invitation.
- Do not claim inferred skills prove real competence.
- Do not claim a fixed public safe invitation limit where LinkedIn publishes none.
- Do not claim a practitioner benchmark is a platform rule.
- Do not claim human expert participation without recorded participation.
- Do not recommend scraping, bots, private APIs, browser automation, session
  cookie reuse, fake personalization, bulk messaging, engagement pods, or
  platform-limit evasion.
