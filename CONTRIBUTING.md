# Contributing

Contributions are welcome when they make the skill more specific, safer, easier to evaluate, or more useful across technical B2B sectors.

## Before Opening a Pull Request

1. Keep `SKILL.md` concise and procedural.
2. Put detailed frameworks and reusable forms in `references/`.
3. Do not add company-specific facts, private data, source presentations, or transcripts.
4. Preserve the evidence ledger and explicit approval gates.
5. Add or update a case in `evals/cases.json` for behavioral changes.
6. Run:

   ```bash
   python tools/validate_skill.py
   ```

## Pull Request Notes

Explain:

- the behavior changed
- why the change generalizes
- the evaluation case used
- any safety or evidence-integrity impact

Do not include real prospect data, private LinkedIn content, credentials, or unpublished company claims in issues, pull requests, or evaluation cases.
