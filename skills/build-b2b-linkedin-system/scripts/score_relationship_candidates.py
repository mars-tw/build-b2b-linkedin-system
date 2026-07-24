#!/usr/bin/env python3
"""Score an authorized CSV of LinkedIn relationship candidates.

This utility performs local, explainable prioritization only. It does not fetch
LinkedIn data, automate a browser, send invitations, or grant contact permission.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from datetime import date
from pathlib import Path


NUMERIC_FIELDS = (
    "industry_fit",
    "account_fit",
    "role_fit",
    "skill_exact",
    "skill_parent_child",
    "skill_sibling",
    "mutual_context",
    "shared_experience",
    "recent_relevant_activity",
    "geography_fit",
    "language_fit",
    "evidence_confidence",
)

REQUIRED_FIELDS = (
    "candidate_id",
    "name",
    "profile_url",
    "source_ref",
    "observation_date",
    "evidence_notes",
    "industry_evidence_ref",
    "account_evidence_ref",
    "role_evidence_ref",
    "skill_evidence_ref",
    "relationship_evidence_ref",
    "relationship_lane",
    "connection_degree",
    *NUMERIC_FIELDS,
    "negative_flags",
)

VALID_LANES = {
    "buyer",
    "peer_expert",
    "partner_ecosystem",
    "supplier",
    "competitor",
    "internal",
    "unknown",
    "exclude",
}

HARD_EXCLUSIONS = {
    "do_not_contact",
    "explicit_disinterest",
    "duplicate",
    "excluded_by_policy",
    "irrelevant_role",
    "unverified_identity",
    "prohibited_source",
    "spam_or_fake_account",
}

AXIS_EVIDENCE_FIELDS = (
    "industry_evidence_ref",
    "account_evidence_ref",
    "role_evidence_ref",
    "skill_evidence_ref",
    "relationship_evidence_ref",
)


def unit_interval(value: str, field: str, row_number: int) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(
            f"row {row_number}: {field} must be a number from 0 to 1"
        ) from exc
    if not 0 <= parsed <= 1:
        raise ValueError(f"row {row_number}: {field} must be between 0 and 1")
    return parsed


def parse_flags(raw: str) -> set[str]:
    return {
        item.strip().lower()
        for item in raw.replace(",", ";").split(";")
        if item.strip()
    }


def validate_evidence_fields(row: dict[str, str], row_number: int) -> None:
    for field in ("source_ref", "observation_date", "evidence_notes"):
        if not row[field].strip():
            raise ValueError(f"row {row_number}: {field} is required")
    try:
        date.fromisoformat(row["observation_date"].strip())
    except ValueError as exc:
        raise ValueError(
            f"row {row_number}: observation_date must use YYYY-MM-DD"
        ) from exc


def relationship_score(degree: str, mutual_context: float) -> float:
    degree_value = {
        "1": 1.0,
        "1st": 1.0,
        "2": 0.8,
        "2nd": 0.8,
        "3": 0.35,
        "3rd": 0.35,
        "unknown": 0.0,
    }.get(degree.strip().lower(), 0.0)
    return 12 * max(degree_value, mutual_context)


def score_row(row: dict[str, str], row_number: int) -> dict[str, object]:
    missing = [field for field in REQUIRED_FIELDS if field not in row]
    if missing:
        raise ValueError(f"row {row_number}: missing fields: {', '.join(missing)}")
    validate_evidence_fields(row, row_number)

    lane = row["relationship_lane"].strip().lower()
    if lane not in VALID_LANES:
        raise ValueError(
            f"row {row_number}: relationship_lane must be one of "
            + ", ".join(sorted(VALID_LANES))
        )

    values = {
        field: unit_interval(row[field], field, row_number)
        for field in NUMERIC_FIELDS
    }
    flags = parse_flags(row["negative_flags"])
    hard_flags = sorted(flags & HARD_EXCLUSIONS)
    sourced_fit_axes = sum(bool(row[field].strip()) for field in AXIS_EVIDENCE_FIELDS)

    skill_component = 18 * max(
        values["skill_exact"],
        0.75 * values["skill_parent_child"],
        0.45 * values["skill_sibling"],
    )
    score = (
        16 * values["account_fit"]
        + 16 * values["role_fit"]
        + 12 * values["industry_fit"]
        + skill_component
        + relationship_score(row["connection_degree"], values["mutual_context"])
        + 6 * values["shared_experience"]
        + 6 * values["recent_relevant_activity"]
        + 4 * values["geography_fit"]
        + 4 * values["language_fit"]
        + 6 * values["evidence_confidence"]
    )
    rounded = round(score, 1)

    reasons: list[str] = []
    if values["skill_exact"] >= 0.8:
        reasons.append("strong exact-skill evidence")
    elif values["skill_parent_child"] >= 0.8:
        reasons.append("strong adjacent parent/child skill")
    if values["industry_fit"] >= 0.8:
        reasons.append("strong industry fit")
    if values["account_fit"] >= 0.8 and values["role_fit"] >= 0.8:
        reasons.append("strong account and role fit")
    if values["mutual_context"] >= 0.7:
        reasons.append("meaningful mutual context")
    if values["evidence_confidence"] < 0.5:
        reasons.append("low evidence confidence")
    reasons.append(f"{sourced_fit_axes} sourced fit axes")

    degree = row["connection_degree"].strip().lower()
    if hard_flags or lane == "exclude":
        priority = "EXCLUDE"
        next_step = "no_action"
        state = (
            "cancelled"
            if flags & {"do_not_contact", "explicit_disinterest"}
            else "blocked"
        )
        reasons.append("hard exclusion: " + ", ".join(hard_flags or ["exclude lane"]))
    elif lane == "unknown" or values["evidence_confidence"] < 0.5:
        priority = "HOLD"
        next_step = "research_only"
        state = "classified"
    elif rounded >= 80 and sourced_fit_axes < 2:
        priority = "HOLD"
        next_step = "source_additional_fit_axes"
        state = "classified"
    elif degree in {"1", "1st"}:
        priority = "P1" if rounded >= 80 else "P2"
        next_step = "existing_connection_nurture"
        state = "classified"
    elif rounded >= 80 and degree in {"2", "2nd"} and values["mutual_context"] >= 0.5:
        priority = "P1"
        next_step = "human_review"
        state = "classified"
    elif rounded >= 65 and sourced_fit_axes >= 1:
        priority = "P2"
        next_step = "follow_observe_or_research"
        state = "classified"
    else:
        priority = "HOLD"
        next_step = "research_only"
        state = "classified"

    return {
        **row,
        "score": rounded,
        "sourced_fit_axes": sourced_fit_axes,
        "priority": priority,
        "recommended_next_step": next_step,
        "state": state,
        "hard_exclusions": ";".join(hard_flags),
        "score_reasons": "; ".join(reasons) or "no dominant signal",
        "permission_note": "priority is not permission; exact human approval is required",
    }


def score_csv(input_path: Path, output_path: Path) -> int:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError("input CSV missing columns: " + ", ".join(missing))
        rows = [score_row(row, index) for index, row in enumerate(reader, start=2)]

    output_fields = list(reader.fieldnames) + [
        "score",
        "sourced_fit_axes",
        "priority",
        "recommended_next_step",
        "state",
        "hard_exclusions",
        "score_reasons",
        "permission_note",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def self_test() -> None:
    records = [
        {
            "candidate_id": "high-fit",
            "name": "High Fit",
            "profile_url": "https://example.test/high",
            "source_ref": "supplied:test-high",
            "observation_date": "2026-07-24",
            "evidence_notes": "Fictional test record with complete evidence fields.",
            "industry_evidence_ref": "supplied:test-high#industry",
            "account_evidence_ref": "supplied:test-high#account",
            "role_evidence_ref": "supplied:test-high#role",
            "skill_evidence_ref": "supplied:test-high#skill",
            "relationship_evidence_ref": "supplied:test-high#relationship",
            "relationship_lane": "peer_expert",
            "connection_degree": "2nd",
            **{field: "0.9" for field in NUMERIC_FIELDS},
            "negative_flags": "",
        },
        {
            "candidate_id": "supplier",
            "name": "Existing Supplier",
            "profile_url": "https://example.test/supplier",
            "source_ref": "supplied:test-supplier",
            "observation_date": "2026-07-24",
            "evidence_notes": "Fictional test record excluded by campaign policy.",
            "industry_evidence_ref": "supplied:test-supplier#industry",
            "account_evidence_ref": "supplied:test-supplier#account",
            "role_evidence_ref": "supplied:test-supplier#role",
            "skill_evidence_ref": "supplied:test-supplier#skill",
            "relationship_evidence_ref": "supplied:test-supplier#relationship",
            "relationship_lane": "supplier",
            "connection_degree": "2nd",
            **{field: "1" for field in NUMERIC_FIELDS},
            "negative_flags": "existing_supplier;excluded_by_policy",
        },
        {
            "candidate_id": "weak",
            "name": "Weak Third Degree",
            "profile_url": "https://example.test/weak",
            "source_ref": "supplied:test-weak",
            "observation_date": "2026-07-24",
            "evidence_notes": "Fictional test record with weak fit evidence.",
            "industry_evidence_ref": "supplied:test-weak#industry",
            "account_evidence_ref": "",
            "role_evidence_ref": "",
            "skill_evidence_ref": "",
            "relationship_evidence_ref": "",
            "relationship_lane": "unknown",
            "connection_degree": "3rd",
            **{field: "0.2" for field in NUMERIC_FIELDS},
            "negative_flags": "",
        },
        {
            "candidate_id": "sparse-high",
            "name": "Sparse High Score",
            "profile_url": "https://example.test/sparse-high",
            "source_ref": "supplied:test-sparse-high",
            "observation_date": "2026-07-24",
            "evidence_notes": "Fictional high scores with only one sourced axis.",
            "industry_evidence_ref": "supplied:test-sparse-high#industry",
            "account_evidence_ref": "",
            "role_evidence_ref": "",
            "skill_evidence_ref": "",
            "relationship_evidence_ref": "",
            "relationship_lane": "buyer",
            "connection_degree": "2nd",
            **{field: "0.95" for field in NUMERIC_FIELDS},
            "negative_flags": "",
        },
    ]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=REQUIRED_FIELDS)
    writer.writeheader()
    writer.writerows(records)
    stream.seek(0)
    reader = csv.DictReader(stream)
    results = [score_row(row, index) for index, row in enumerate(reader, start=2)]

    assert results[0]["priority"] == "P1"
    assert results[0]["recommended_next_step"] == "human_review"
    assert results[0]["state"] == "classified"
    assert results[1]["priority"] == "EXCLUDE"
    assert results[1]["recommended_next_step"] == "no_action"
    assert results[1]["state"] == "blocked"
    assert results[2]["priority"] == "HOLD"
    assert results[2]["recommended_next_step"] == "research_only"
    assert results[2]["state"] == "classified"
    assert results[3]["priority"] == "HOLD"
    assert results[3]["recommended_next_step"] == "source_additional_fit_axes"
    assert results[3]["sourced_fit_axes"] == 1
    print(json.dumps({"self_test": "passed", "cases": 4}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locally score an authorized relationship-candidate CSV."
    )
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if args.input is None or args.output is None:
        parser.error("input and output CSV paths are required unless --self-test is used")

    try:
        count = score_csv(args.input, args.output)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"scored {count} candidates; no external actions were performed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
