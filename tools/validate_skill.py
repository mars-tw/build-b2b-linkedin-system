#!/usr/bin/env python3
"""Validate the open-source skill package using only the Python standard library."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


SKILL_NAME = "build-b2b-linkedin-system"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def read_utf8(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        error(errors, f"missing file: {path}")
    except UnicodeDecodeError as exc:
        error(errors, f"invalid UTF-8: {path}: {exc}")
    return ""


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        error(errors, "SKILL.md must start with YAML frontmatter")
        return {}

    fields: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            error(errors, f"invalid frontmatter line: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def validate_markdown_links(
    skill_dir: Path, skill_text: str, errors: list[str]
) -> None:
    for target in MARKDOWN_LINK_PATTERN.findall(skill_text):
        if "://" in target or target.startswith("#"):
            continue
        path_part = target.split("#", 1)[0]
        resolved = (skill_dir / path_part).resolve()
        if not resolved.exists():
            error(errors, f"broken local link in SKILL.md: {target}")


def validate_skill(repo_root: Path, errors: list[str]) -> None:
    skill_dir = repo_root / "skills" / SKILL_NAME
    skill_md = skill_dir / "SKILL.md"
    skill_text = read_utf8(skill_md, errors)
    if not skill_text:
        return

    fields = parse_frontmatter(skill_text, errors)
    if set(fields) != {"name", "description"}:
        error(errors, "SKILL.md frontmatter must contain only name and description")
    if fields.get("name") != SKILL_NAME:
        error(errors, f"frontmatter name must be {SKILL_NAME}")
    if not NAME_PATTERN.fullmatch(fields.get("name", "")):
        error(errors, "skill name must use lowercase letters, digits, and hyphens")
    if skill_dir.name != fields.get("name"):
        error(errors, "skill folder name must match frontmatter name")
    if len(fields.get("description", "")) < 80:
        error(errors, "description is too short to explain behavior and triggers")
    if len(skill_text.splitlines()) >= 500:
        error(errors, "SKILL.md must remain under 500 lines")

    validate_markdown_links(skill_dir, skill_text, errors)

    forbidden = ["TODO", "[TODO", "\ufffd"]
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "README.md":
            error(errors, f"README.md does not belong inside the skill folder: {path}")
        if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        text = read_utf8(path, errors)
        for token in forbidden:
            if token in text:
                error(errors, f"forbidden placeholder or encoding marker {token!r}: {path}")

    agent_yaml = skill_dir / "agents" / "openai.yaml"
    agent_text = read_utf8(agent_yaml, errors)
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in agent_text:
            error(errors, f"agents/openai.yaml missing {key}")
    if f"${SKILL_NAME}" not in agent_text:
        error(errors, "default_prompt must explicitly mention the skill")

    required_references = {
        "platform-signals.md",
        "playbook.md",
        "quality-rubric.md",
        "relationship-growth-matrix.md",
        "templates.md",
    }
    reference_dir = skill_dir / "references"
    existing_references = {
        path.name for path in reference_dir.glob("*.md") if path.is_file()
    }
    missing_references = required_references - existing_references
    if missing_references:
        error(
            errors,
            "missing required references: " + ", ".join(sorted(missing_references)),
        )


def validate_evals(repo_root: Path, errors: list[str]) -> None:
    eval_path = repo_root / "evals" / "cases.json"
    text = read_utf8(eval_path, errors)
    if not text:
        return
    try:
        cases = json.loads(text)
    except json.JSONDecodeError as exc:
        error(errors, f"invalid evals/cases.json: {exc}")
        return

    if not isinstance(cases, list) or len(cases) < 5:
        error(errors, "evals/cases.json must contain at least five cases")
        return

    required = {"id", "mode", "prompt", "must", "must_not"}
    valid_modes = {"research", "audit", "design", "draft", "operate"}
    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            error(errors, f"evaluation case {index} must be an object")
            continue
        missing = required - set(case)
        if missing:
            error(errors, f"evaluation case {index} missing: {sorted(missing)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            error(errors, f"evaluation case {index} has invalid id")
        elif case_id in ids:
            error(errors, f"duplicate evaluation id: {case_id}")
        else:
            ids.add(case_id)
        if case.get("mode") not in valid_modes:
            error(errors, f"evaluation {case_id!r} has invalid mode")
        for field in ("must", "must_not"):
            value = case.get(field)
            if not isinstance(value, list) or not value:
                error(errors, f"evaluation {case_id!r} requires non-empty {field}")

    required_case_ids = {
        "same-industry-skill-matrix-discovery-only",
        "blanket-approval-does-not-override-safety",
        "algorithm-and-expert-provenance",
    }
    missing_case_ids = required_case_ids - ids
    if missing_case_ids:
        error(
            errors,
            "missing relationship-growth evaluation cases: "
            + ", ".join(sorted(missing_case_ids)),
        )


def validate_behavior_tools(repo_root: Path, errors: list[str]) -> None:
    skill_dir = repo_root / "skills" / SKILL_NAME
    scorer = (
        skill_dir
        / "scripts"
        / "score_relationship_candidates.py"
    )
    if not scorer.is_file():
        error(errors, f"missing candidate scorer: {scorer}")
        return
    result = subprocess.run(
        [sys.executable, str(scorer), "--self-test"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        error(errors, f"candidate scorer self-test failed: {detail}")
    elif '"self_test": "passed"' not in result.stdout:
        error(errors, "candidate scorer self-test did not report a pass")

    example = skill_dir / "examples" / "relationship-candidates.csv"
    example_text = read_utf8(example, errors)
    example_header = example_text.splitlines()[0] if example_text else ""
    for required_header in (
        "source_ref",
        "observation_date",
        "evidence_notes",
        "industry_evidence_ref",
        "account_evidence_ref",
        "role_evidence_ref",
        "skill_evidence_ref",
        "relationship_evidence_ref",
        "relationship_lane",
        "negative_flags",
    ):
        if required_header not in example_header.split(","):
            error(errors, f"candidate CSV example missing column: {required_header}")


def validate_repository_metadata(repo_root: Path, errors: list[str]) -> None:
    required_files = {
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CITATION.cff",
        "llms.txt",
    }
    for relative_path in sorted(required_files):
        read_utf8(repo_root / relative_path, errors)

    citation_text = read_utf8(repo_root / "CITATION.cff", errors)
    citation_tokens = (
        "cff-version: 1.2.0",
        'title: "Build B2B LinkedIn System"',
        "version:",
        "repository-code:",
        "license: MIT",
    )
    for token in citation_tokens:
        if token not in citation_text:
            error(errors, f"CITATION.cff missing {token}")

    llms_text = read_utf8(repo_root / "llms.txt", errors)
    llms_tokens = (
        "https://github.com/mars-tw/build-b2b-linkedin-system",
        "Never invent",
        "explicit authorization",
        "python tools/validate_skill.py",
    )
    for token in llms_tokens:
        if token not in llms_text:
            error(errors, f"llms.txt missing {token}")


def main() -> int:
    repo_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1]
    )
    errors: list[str] = []
    validate_skill(repo_root, errors)
    validate_evals(repo_root, errors)
    validate_behavior_tools(repo_root, errors)
    validate_repository_metadata(repo_root, errors)

    if errors:
        print("Validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Validation passed:")
    print(f"- skill: {SKILL_NAME}")
    print("- UTF-8: valid")
    print("- frontmatter: valid")
    print("- local links: valid")
    print("- interface metadata: valid")
    print("- references: valid")
    print("- evaluation case schema: valid; behavioral forward-test still required")
    print("- relationship scorer self-test: passed")
    print("- repository metadata: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
