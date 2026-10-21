"""Validate an explicit item-analysis context without creating benchmark scores."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from anthropic_api_package_release.item_analysis import prepare
from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.storage import read_json, write_json


class DirectContext(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)
    benchmark: str = Field(min_length=1, max_length=200)
    deployment: str = Field(min_length=1, max_length=12_000)
    task_requirements: str = Field(min_length=1, max_length=12_000)
    answer_requirements: str = Field(min_length=1, max_length=12_000)
    validity_concerns: str = Field(default="", max_length=12_000)

    @field_validator("*", mode="before")
    @classmethod
    def valid_unicode(cls, value):
        if isinstance(value, str):
            try:
                value.encode("utf-8")
            except UnicodeEncodeError:
                # Do not let FastAPI echo an invalid surrogate in its JSON
                # validation response, where UTF-8 encoding would fail again.
                raise HTTPException(422, "Context text must contain valid Unicode.") from None
        return value


class DirectSetup(DirectContext):
    q: str | None = Field(default=None, max_length=200)


def parse_context(value: str) -> DirectContext:
    try:
        return DirectContext.model_validate_json(value)
    except ValidationError:
        raise HTTPException(422, "Provide a benchmark name (up to 200 characters), deployment context, task requirements, and answer requirements (up to 12,000 characters each). Validity concerns are optional. Extra fields are not accepted.") from None


def resolve(context: DirectContext) -> dict:
    """The identifier scopes browser restoration; it is never an access token."""
    raw = context.model_dump()
    identity = hashlib.sha256(json.dumps(raw, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    deployment = (f"Deployment context:\n{raw['deployment']}\n\n"
                  f"Task requirements:\n{raw['task_requirements']}\n\n"
                  f"Answer requirements:\n{raw['answer_requirements']}")
    return {
        "kind": "direct", "id": f"direct-{identity}",
        "benchmark": raw["benchmark"], "benchmark_name": raw["benchmark"],
        "deployment": deployment, "direct_context": deepcopy(raw),
        "analysis_basis": "deployment_requirements", "assessment_status": "not_run",
        "benchmark_identity": {
            "name": raw["benchmark"], "full_name": None, "aliases": [],
            "paper_urls": [], "source_urls": [], "year": None, "languages": [], "version": None,
            "evidence": {"name": "user-declared direct item-analysis context"},
        },
    }


def attach_context(directory: Path, assessment: dict, *, confirmed_source: bool = False) -> None:
    """Use the shared pipeline with frozen requirements and no scored assessment."""
    prepare.attach_direct_context(directory, assessment["direct_context"],
                                  deployment=assessment["deployment"], confirmed_source=confirmed_source)
    evidence = read_json(directory / "evidence.json")
    evidence["assessment"] = {"kind": "direct", "id": assessment["id"]}
    evidence["benchmark_identity"] = deepcopy(assessment["benchmark_identity"])
    write_json(directory / "evidence.json", evidence)
    dataset = read_json(directory / "dataset.json")
    dataset["assessment"] = evidence["assessment"]
    dataset["benchmark_identity_confirmed"] = True
    dataset["source"].pop("path", None)
    dataset["evidence_sha256"] = file_sha256(directory / "evidence.json")
    write_json(directory / "dataset.json", dataset)
    for name in ("provided_spec.json", "classifier_spec.original.json"):
        (directory / name).unlink(missing_ok=True)
