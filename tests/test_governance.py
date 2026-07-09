"""Governance- und Schema-Validierung für Knowledge Platform."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
PLAYBOOKS = ROOT / "playbooks"

PUBLISH_NEAR = frozenset({"presseschau", "linkedin", "wordpress", "seo", "image"})
ALL_PLAYBOOKS = frozenset(
    {"presseschau", "linkedin", "brandvoice", "sources", "image", "wordpress", "seo"}
)
GOVERNANCE_REQUIRED = frozenset(
    {"owner", "approval_required", "auto_publish", "version", "outputs", "quality_checks"}
)
CHROMA_ALLOWED_SOURCES = frozenset(
    {"playbook", "content", "wiki", "contract", "adr", "approved_inbox_export"}
)
CONTEXT_OUTPUT_REQUIRED = frozenset(
    {"task", "applied_playbooks", "applied_adrs", "sources", "uncertainties"}
)
NEW_SCHEMAS = (
    "playbook.schema.json",
    "runtime_output.schema.json",
    "api_error.schema.json",
    "knowledge_graph_node.schema.json",
    "knowledge_graph_edge.schema.json",
    "context_builder_input.schema.json",
    "context_builder_output.schema.json",
    "chroma_index_manifest.schema.json",
    "chroma_rebuild_report.schema.json",
    "linkedin.schema.json",
)
EXAMPLE_PAIRS = (
    ("examples/linkedin/linkedin_post.example.json", "linkedin.schema.json"),
    ("examples/retrieval/chroma_index_manifest.example.json", "chroma_index_manifest.schema.json"),
    ("examples/runtime/context_builder_output.example.json", "context_builder_output.schema.json"),
)
STAGE_EF_DOCS = (
    ROOT / "docs" / "11_roadmap_stufen_a_f.md",
    ROOT / "docs" / "12_architecture_layers.md",
    ROOT / "cursor" / "CURSOR_TASK_STAGE_E.md",
    ROOT / "cursor" / "CURSOR_TASK_STAGE_F.md",
)
FORBIDDEN_BYPASS_STRINGS = (
    "auto_publish: true",
    "auto-publish: true",
    "ohne regisseur-inbox",
    "umgeht dar",
    "bypass inbox",
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _jsonschema_validator():
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise unittest.SkipTest("jsonschema nicht installiert — pip install jsonschema") from exc
    return Draft202012Validator


class TestGovernance(unittest.TestCase):
    def test_alle_playbooks_haben_governance(self):
        for name in ALL_PLAYBOOKS:
            data = _load_yaml(PLAYBOOKS / f"{name}.yaml")
            self.assertIn("governance", data, name)
            missing = GOVERNANCE_REQUIRED - set(data["governance"])
            self.assertFalse(missing, f"{name}: fehlende governance keys {missing}")

    def test_publish_nahe_playbooks_auto_publish_false(self):
        for name in PUBLISH_NEAR:
            gov = _load_yaml(PLAYBOOKS / f"{name}.yaml")["governance"]
            self.assertFalse(gov["auto_publish"], name)
            self.assertTrue(gov["approval_required"], name)

    def test_playbook_yaml_parsebar(self):
        for path in PLAYBOOKS.glob("*.yaml"):
            data = _load_yaml(path)
            self.assertIsInstance(data, dict, path.name)
            self.assertIn("name", data)

    def test_schemas_draft_2020_12(self):
        for path in SCHEMAS.glob("*.json"):
            schema = _load_json(path)
            self.assertEqual(
                schema.get("$schema"),
                "https://json-schema.org/draft/2020-12/schema",
                path.name,
            )

    def test_neue_contract_schemas_existieren(self):
        for name in NEW_SCHEMAS:
            self.assertTrue((SCHEMAS / name).is_file(), name)

    def test_beispiele_gegen_schemas(self):
        Draft202012Validator = _jsonschema_validator()
        for example_rel, schema_name in EXAMPLE_PAIRS:
            example = _load_json(ROOT / example_rel)
            schema = _load_json(SCHEMAS / schema_name)
            validator = Draft202012Validator(schema)
            errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))
            self.assertFalse(errors, f"{example_rel}: {[e.message for e in errors]}")

    def test_chroma_manifest_nur_kp_quellen(self):
        manifest = _load_json(ROOT / "examples" / "retrieval" / "chroma_index_manifest.example.json")
        self.assertTrue(manifest.get("derived"))
        for item in manifest.get("build_inputs", []):
            self.assertIn(item["source_type"], CHROMA_ALLOWED_SOURCES)

    def test_context_builder_output_pflichtfelder(self):
        out = _load_json(ROOT / "examples" / "runtime" / "context_builder_output.example.json")
        missing = CONTEXT_OUTPUT_REQUIRED - set(out)
        self.assertFalse(missing, missing)
        self.assertTrue(out["applied_playbooks"])
        self.assertTrue(out["sources"])

    def test_stage_e_f_docs_kein_dar_bypass(self):
        for doc in STAGE_EF_DOCS:
            if not doc.is_file():
                self.fail(f"fehlendes Stage-E/F-Dokument: {doc.relative_to(ROOT)}")
            text = doc.read_text(encoding="utf-8")
            self.assertIn("Regisseur-Inbox", text, doc.name)
            self.assertIn("ADR-0004", text, doc.name)
            lower = text.lower()
            for bad in FORBIDDEN_BYPASS_STRINGS:
                self.assertNotIn(bad, lower, f"{doc.name}: {bad}")

    def test_playbooks_gegen_governance_schema(self):
        Draft202012Validator = _jsonschema_validator()
        schema = _load_json(SCHEMAS / "playbook.schema.json")
        validator = Draft202012Validator(schema)
        for name in ALL_PLAYBOOKS:
            data = _load_yaml(PLAYBOOKS / f"{name}.yaml")
            errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
            self.assertFalse(errors, f"{name}: {[e.message for e in errors]}")

    def test_adrs_0010_bis_0012(self):
        for n in (10, 11, 12):
            path = ROOT / "adr" / f"ADR-{n:04d}-"
            matches = list(ROOT.glob(f"adr/ADR-{n:04d}-*.md"))
            self.assertEqual(len(matches), 1, n)


if __name__ == "__main__":
    unittest.main()
