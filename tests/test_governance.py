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
    {
        "task",
        "applied_playbooks",
        "applied_adrs",
        "sources",
        "uncertainties",
        "sql_first",
        "resolution_path",
        "conflicts",
    }
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
CANONICAL_SEQUENCE_IDS = (
    "classify_intent",
    "kp_governance",
    "sql_crm_stammdaten",
    "knowledge_graph",
    "chroma_rag",
    "web_external",
)
SEQUENCE_DOC_PATHS = (
    ROOT / "adr" / "ADR-0011-context-builder-combines-context-layers.md",
    ROOT / "adr" / "ADR-0013-source-resolution-and-sql-first-policy.md",
    ROOT / "docs" / "12_context_assembly_pipeline.md",
    ROOT / "docs" / "13_source_resolution.md",
    ROOT / "contracts" / "source-resolution" / "source_resolution_policy.yaml",
)
EXAMPLE_PAIRS = (
    ("examples/linkedin/linkedin_post.example.json", "linkedin.schema.json"),
    ("examples/retrieval/chroma_index_manifest.example.json", "chroma_index_manifest.schema.json"),
    ("examples/retrieval/chroma_rebuild_report.example.json", "chroma_rebuild_report.schema.json"),
    ("examples/runtime/context_builder_output.example.json", "context_builder_output.schema.json"),
    ("examples/runtime/context_builder_input.example.json", "context_builder_input.schema.json"),
    (
        "examples/source-resolution/context_assembly.example.json",
        "contracts/source-resolution/context_assembly.schema.json",
    ),
    (
        "examples/graph/graph_query.example.json",
        "contracts/graph/graph_query.schema.json",
    ),
    (
        "examples/decision-engine/decision_input.example.json",
        "contracts/decision-engine/decision_input.schema.json",
    ),
    (
        "examples/decision-engine/decision_output.example.json",
        "contracts/decision-engine/decision_output.schema.json",
    ),
    (
        "examples/decision-engine/decision_trace.example.json",
        "contracts/decision-engine/decision_trace.schema.json",
    ),
    (
        "examples/decision-engine/decision_context.example.json",
        "contracts/decision-engine/decision_context.schema.json",
    ),
    (
        "examples/decision-engine/decision_output_clarification.example.json",
        "contracts/decision-engine/decision_output.schema.json",
    ),
    (
        "examples/decision-engine/decision_output_block.example.json",
        "contracts/decision-engine/decision_output.schema.json",
    ),
    (
        "examples/decision-engine/decision_output_approval_gate.example.json",
        "contracts/decision-engine/decision_output.schema.json",
    ),
)
DECISION_OUTPUT_EXAMPLES = (
    "examples/decision-engine/decision_output.example.json",
    "examples/decision-engine/decision_output_clarification.example.json",
    "examples/decision-engine/decision_output_block.example.json",
    "examples/decision-engine/decision_output_approval_gate.example.json",
)
STAGE_EF_DOCS = (
    ROOT / "docs" / "11_roadmap_stufen_a_f.md",
    ROOT / "docs" / "12_architecture_layers.md",
    ROOT / "docs" / "12_context_assembly_pipeline.md",
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


def _contract_validator(schema_path: Path):
    Draft202012Validator = _jsonschema_validator()
    schema = _load_json(schema_path)
    shared = ROOT / "contracts" / "decision-engine" / "decision_shared.schema.json"
    if not shared.is_file():
        return Draft202012Validator(schema)
    try:
        from referencing import Registry, Resource

        shared_doc = _load_json(shared)
        registry = (
            Registry()
            .with_resource(schema_path.name, Resource.from_contents(schema))
            .with_resource("decision_shared.schema.json", Resource.from_contents(shared_doc))
            .with_resource(
                "../decision-engine/decision_shared.schema.json",
                Resource.from_contents(shared_doc),
            )
        )
        return Draft202012Validator(schema, registry=registry)
    except ImportError:
        merged = dict(schema)
        merged.setdefault("$defs", {}).update(shared_doc.get("$defs", {}))
        return Draft202012Validator(merged)


def _reason_codes_from_policy() -> frozenset[str]:
    policy = _load_yaml(ROOT / "contracts" / "decision-engine" / "decision_policy.yaml")
    return frozenset(policy.get("reason_codes", {}).keys())


def _collect_reason_codes(obj) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        if "reason_code" in obj and isinstance(obj["reason_code"], str):
            found.add(obj["reason_code"])
        for value in obj.values():
            found.update(_collect_reason_codes(value))
    elif isinstance(obj, list):
        for item in obj:
            found.update(_collect_reason_codes(item))
    return found


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
        for example_rel, schema_rel in EXAMPLE_PAIRS:
            example = _load_json(ROOT / example_rel)
            if schema_rel.startswith("contracts/"):
                schema_path = ROOT / schema_rel
                validator = _contract_validator(schema_path)
            else:
                schema_path = SCHEMAS / schema_rel
                validator = _jsonschema_validator()(_load_json(schema_path))
            errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))
            self.assertFalse(errors, f"{example_rel}: {[e.message for e in errors]}")

    def test_source_resolution_sequence_konsistent(self):
        for path in SEQUENCE_DOC_PATHS:
            text = path.read_text(encoding="utf-8")
            for step_id in CANONICAL_SEQUENCE_IDS:
                self.assertIn(step_id, text, f"{path.name}: fehlt {step_id}")

    def test_context_builder_input_source_resolution(self):
        schema = _load_json(SCHEMAS / "context_builder_input.schema.json")
        for key in ("sql_first", "required_fields", "resolution_policy_ref", "context_assembly_ref"):
            self.assertIn(key, schema["properties"], key)
        self.assertIn("resolution_policy_ref", schema["required"])

    def test_context_builder_output_adr_0013_felder(self):
        out = _load_json(ROOT / "examples" / "runtime" / "context_builder_output.example.json")
        for key in ("sql_first", "resolution_path", "sql_snippets", "conflicts"):
            self.assertIn(key, out, key)
        Draft202012Validator = _jsonschema_validator()
        schema = _load_json(SCHEMAS / "context_builder_output.schema.json")
        errors = list(Draft202012Validator(schema).iter_errors(out))
        self.assertFalse(errors, [e.message for e in errors])

    def test_context_assembly_source_resolution_nachweis(self):
        data = _load_json(ROOT / "examples" / "source-resolution" / "context_assembly.example.json")
        self.assertEqual(
            data.get("canonical_sequence_ref"),
            "contracts/source-resolution/source_resolution_policy.yaml",
        )
        steps = data["classification"]["steps_completed"]
        self.assertIn("classify_intent", steps)
        self.assertIn("kp_governance", steps)

    def test_chroma_manifest_aktuelle_kp_version(self):
        manifest = _load_json(ROOT / "examples" / "retrieval" / "chroma_index_manifest.example.json")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(manifest.get("knowledge_platform_version"), version)

    def test_decision_engine_contracts_existieren(self):
        de = ROOT / "contracts" / "decision-engine"
        for name in (
            "decision_policy.yaml",
            "decision_shared.schema.json",
            "decision_input.schema.json",
            "decision_output.schema.json",
            "decision_trace.schema.json",
            "decision_context.schema.json",
        ):
            self.assertTrue((de / name).is_file(), name)
        policy = _load_yaml(de / "decision_policy.yaml")
        self.assertEqual(policy.get("status"), "active")
        self.assertIn("no_hardcoded_domain_rules", policy.get("principle", {}))

    def test_decision_engine_keine_antwort_felder(self):
        schema = _load_json(ROOT / "contracts" / "decision-engine" / "decision_output.schema.json")
        not_block = schema.get("not", {})
        for forbidden in ("published_url", "auto_publish", "answer_text"):
            self.assertIn(forbidden, not_block.get("required", []))

    def test_decision_reason_codes_im_policy_katalog(self):
        catalog = _reason_codes_from_policy()
        for rel in DECISION_OUTPUT_EXAMPLES:
            data = _load_json(ROOT / rel)
            used = _collect_reason_codes(data)
            missing = used - catalog
            self.assertFalse(missing, f"{rel}: unbekannte reason_codes {missing}")
        trace = _load_json(ROOT / "examples/decision-engine/decision_trace.example.json")
        trace_codes = _collect_reason_codes(trace)
        ctx = _load_json(ROOT / "examples/decision-engine/decision_context.example.json")
        ctx_codes = _collect_reason_codes(ctx)
        assembly = _load_json(ROOT / "examples/source-resolution/context_assembly.example.json")
        asm_codes = _collect_reason_codes(assembly)
        for label, codes in (
            ("trace", trace_codes),
            ("context", ctx_codes),
            ("assembly", asm_codes),
        ):
            missing = codes - catalog
            self.assertFalse(missing, f"{label}: unbekannte reason_codes {missing}")

    def test_decision_output_und_context_synchron(self):
        out = _load_json(ROOT / "examples/decision-engine/decision_output.example.json")
        ctx = _load_json(ROOT / "examples/decision-engine/decision_context.example.json")
        for key in ("source_requirements", "required_fields"):
            self.assertEqual(out[key], ctx[key], key)
        self.assertEqual(out["readiness"]["next_stage"], ctx["next_stage"])
        self.assertEqual(out["governance"]["approval_required"], ctx["governance"]["approval_required"])

    def test_decision_output_provider_call_verboten(self):
        for rel in DECISION_OUTPUT_EXAMPLES:
            out = _load_json(ROOT / rel)
            self.assertFalse(out["provider_call_allowed"], rel)

    def test_decision_output_sql_required_impliziert_sql_status(self):
        out = _load_json(ROOT / "examples/decision-engine/decision_output.example.json")
        if out["decisions"]["sql_required"]:
            self.assertEqual(out["source_requirements"]["sql_crm_stammdaten"]["status"], "required")

    def test_context_assembly_decision_verknuepfung(self):
        asm = _load_json(ROOT / "examples/source-resolution/context_assembly.example.json")
        self.assertEqual(asm["decision_id"], "dec-presseschau-crm-001")
        self.assertEqual(asm["decision_context_ref"], "dec-presseschau-crm-001")
        self.assertIn("source_requirements_planned", asm)

    def test_playbook_ohne_decision_hints_fallback(self):
        data = _load_yaml(PLAYBOOKS / "brandvoice.yaml")
        self.assertNotIn("decision_hints", data)
        policy = _load_yaml(ROOT / "contracts/decision-engine/decision_policy.yaml")
        self.assertIn("playbook_hints_fallback", policy)

    def test_decision_output_sql_mutex(self):
        out = _load_json(ROOT / "examples" / "decision-engine" / "decision_output.example.json")
        decisions = out["decisions"]
        self.assertNotEqual(decisions["sql_required"], decisions["sql_not_required"])

    def test_playbook_decision_hints_presseschau(self):
        data = _load_yaml(PLAYBOOKS / "presseschau.yaml")
        self.assertIn("decision_hints", data)
        self.assertIn("kundennummer", data["decision_hints"]["sql_first_when_entities"])

    def test_context_builder_input_decision_context_ref(self):
        schema = _load_json(SCHEMAS / "context_builder_input.schema.json")
        self.assertIn("decision_context_ref", schema["properties"])

    def test_manifest_statusmodell(self):
        manifest = _load_yaml(ROOT / "meta" / "manifest.yaml")
        self.assertIn("status_model", manifest)
        kg = manifest["contracts"]["knowledge_graph"]
        self.assertEqual(kg.get("contract_status"), "contract_active")
        self.assertEqual(kg.get("app_status"), "app_planned")
        retrieval = manifest["contracts"]["retrieval"]
        self.assertEqual(retrieval.get("contract_status"), "contract_active")
        self.assertEqual(retrieval.get("app_status"), "app_planned")
        de = manifest["contracts"]["decision_engine"]
        self.assertEqual(de.get("contract_status"), "contract_active")
        self.assertEqual(de.get("app_status"), "app_planned")

    def test_roadmap_stufe_d_spalten(self):
        text = (ROOT / "docs" / "11_roadmap_stufen_a_f.md").read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("| **D** |"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                self.assertEqual(len(cells), 5, f"D-Zeile hat {len(cells)} statt 5 Spalten: {line}")
                break
        else:
            self.fail("Stufe-D-Zeile in Roadmap nicht gefunden")

    def test_merge_policy_nicht_platzhalter(self):
        data = _load_yaml(ROOT / "contracts" / "retrieval" / "merge_policy.yaml")
        self.assertEqual(data.get("status"), "active")
        self.assertIn("token_limits", data)
        self.assertIn("max_rag_snippets", data["token_limits"])

    def test_graph_query_contract_und_beispiele(self):
        query_schema = ROOT / "contracts" / "graph" / "graph_query.schema.json"
        self.assertTrue(query_schema.is_file())
        node = _load_json(ROOT / "examples" / "graph" / "node.example.json")
        edge = _load_json(ROOT / "examples" / "graph" / "edge.example.json")
        node_schema = _load_json(SCHEMAS / "knowledge_graph_node.schema.json")
        edge_schema = _load_json(SCHEMAS / "knowledge_graph_edge.schema.json")
        Draft202012Validator = _jsonschema_validator()
        self.assertFalse(list(Draft202012Validator(node_schema).iter_errors(node)))
        self.assertFalse(list(Draft202012Validator(edge_schema).iter_errors(edge)))

    def test_context_assembly_contract_existiert(self):
        schema = ROOT / "contracts" / "source-resolution" / "context_assembly.schema.json"
        example = ROOT / "examples" / "source-resolution" / "context_assembly.example.json"
        self.assertTrue(schema.is_file())
        self.assertTrue(example.is_file())
        data = _load_json(example)
        self.assertTrue(data.get("ready_for_generation"))
        self.assertIn("context_array", data)
        self.assertFalse(data.get("missing_mandatory_fields"))

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

    def test_source_resolution_policy_existiert(self):
        policy = ROOT / "contracts" / "source-resolution" / "source_resolution_policy.yaml"
        self.assertTrue(policy.is_file())
        text = policy.read_text(encoding="utf-8")
        self.assertIn("sql_first_domains", text)
        self.assertIn("hersteller", text)
        for n in (10, 11, 12, 13):
            path = ROOT / "adr" / f"ADR-{n:04d}-"
            matches = list(ROOT.glob(f"adr/ADR-{n:04d}-*.md"))
            self.assertEqual(len(matches), 1, n)

    def test_field_source_policy_existiert_und_konsistent(self):
        policy = _load_yaml(ROOT / "contracts" / "source-resolution" / "field_source_policy.yaml")
        fields = policy.get("fields") or {}
        self.assertIn("crm_status", fields)
        self.assertIn("presseschau_no_auto_publish", fields)
        self.assertIn("relationship_structure", fields)
        self.assertEqual(fields["crm_status"]["canonical_source"], "sql_crm")
        self.assertIn("chroma_rag", fields["crm_status"]["forbidden_substitute_sources"])
        self.assertEqual(fields["presseschau_no_auto_publish"]["canonical_source"], "knowledge_platform")
        self.assertIn("chroma_rag", fields["presseschau_no_auto_publish"]["forbidden_substitute_sources"])
        self.assertEqual(fields["relationship_structure"]["field_class"], "structural_graph")
        for field_id, spec in fields.items():
            for key in (
                "canonical_source",
                "allowed_supplemental_sources",
                "forbidden_substitute_sources",
                "conflict_rule",
                "provenance_required",
                "minimum_confidence",
                "missing_behavior",
                "uncertain_behavior",
            ):
                self.assertIn(key, spec, field_id)


if __name__ == "__main__":
    unittest.main()
