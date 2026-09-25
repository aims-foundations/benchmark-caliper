import json
import sys

from bayesian_auditing.__main__ import main


def arguments(corpus, tmp_path):
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps(corpus[0]))
    deployment = tmp_path / "deployment.txt"
    deployment.write_text("A text mathematics tutor")
    return ["bayesian_auditing", "run", "--inventory", str(inventory),
            "--deployment", str(deployment), "--output-dir", str(tmp_path / "output")]


def test_cli_preview_and_resume_without_api_key(corpus, tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    args = arguments(corpus, tmp_path) + ["--dry-run", "--limit-per-table", "1"]
    monkeypatch.setattr(sys, "argv", args)
    assert main() == 0
    config = json.loads((tmp_path / "output/run.json").read_text())
    assert config["model"] == "gpt-6-luna"
    assert config["reasoning_effort"] == "high"
    assert config["max_output_tokens"] == 25_000
    before = (tmp_path / "output/assessments.jsonl").read_bytes()
    monkeypatch.setattr(sys, "argv", args + ["--resume"])
    assert main() == 0
    assert (tmp_path / "output/assessments.jsonl").read_bytes() == before


def test_cli_requires_key_before_creating_live_run(corpus, tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", arguments(corpus, tmp_path))
    assert main() == 1
    assert "Set OPENAI_API_KEY" in capsys.readouterr().err
    assert not (tmp_path / "output").exists()
