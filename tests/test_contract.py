"""Contract-Tests für Knowledge Platform Struktur."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestKnowledgePlatformContract(unittest.TestCase):
    def test_version_und_manifest(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "1.2.0")
        manifest = (ROOT / "meta" / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("digiwiz-knowledge-platform", manifest)

    def test_pflicht_playbooks(self):
        for name in ("presseschau", "linkedin", "brandvoice", "sources", "image", "wordpress", "seo"):
            self.assertTrue((ROOT / "playbooks" / f"{name}.yaml").is_file(), name)

    def test_schema_v3(self):
        schema = json.loads((ROOT / "schemas" / "agent-lieferung.v3.json").read_text(encoding="utf-8"))
        self.assertEqual(schema.get("version"), 3)
        self.assertEqual(schema.get("schema_id"), "digiwiz.agent_lieferung")

    def test_runtime_routing(self):
        routing = json.loads((ROOT / "runtime" / "routing.json").read_text(encoding="utf-8"))
        tasks = {r["task"] for r in routing.get("routing", [])}
        self.assertIn("presseschau", tasks)
        self.assertIn("linkedin_post", tasks)

    def test_beispiel_gueltig_v3(self):
        beispiel = json.loads(
            (ROOT / "examples" / "presseschau" / "gueltig_v3.json").read_text(encoding="utf-8")
        )
        self.assertEqual(beispiel.get("version"), 3)
        self.assertTrue(beispiel.get("vorschlaege"))

    def test_manifest_contracts(self):
        manifest = (ROOT / "meta" / "manifest.yaml").read_text(encoding="utf-8")
        for key in ("playbooks", "json_schemas", "runtime", "adrs", "knowledge_graph", "retrieval", "source_resolution"):
            self.assertIn(key, manifest)

    def test_contract_index_existiert(self):
        self.assertTrue((ROOT / "contracts" / "README.md").is_file())
        self.assertTrue((ROOT / "docs" / "10_contracts.md").is_file())

    def test_roadmap_existiert(self):
        roadmap = ROOT / "docs" / "11_roadmap_stufen_a_f.md"
        self.assertTrue(roadmap.is_file())
        text = roadmap.read_text(encoding="utf-8")
        for stufe in ("Stufe A", "Stufe B", "Stufe C", "Stufe D", "Stufe E", "Stufe F"):
            self.assertIn(stufe, text)

    def test_content_linkedin_playbook(self):
        md = ROOT / "content" / "playbooks" / "linkedin-presseschau.md"
        self.assertTrue(md.is_file())
        self.assertIn("Regisseur-Inbox", md.read_text(encoding="utf-8"))

    def test_adr_0008_knowledge_graph(self):
        adr = ROOT / "adr" / "ADR-0008-knowledge-graph-as-platform-extension.md"
        self.assertTrue(adr.is_file())
        text = adr.read_text(encoding="utf-8")
        self.assertIn("keine neue Runtime", text)
        self.assertIn("Knowledge Platform", text)

    def test_adr_0009_graph_chroma_rag(self):
        adr = ROOT / "adr" / "ADR-0009-knowledge-graph-and-chroma-rag.md"
        self.assertTrue(adr.is_file())
        text = adr.read_text(encoding="utf-8")
        self.assertIn("abgeleiteter", text.lower())
        self.assertIn("Context Builder", text)
        self.assertTrue((ROOT / "contracts" / "retrieval" / "README.md").is_file())
        self.assertTrue((ROOT / "adr" / "README.md").is_file())

    def test_manifest_retrieval_contract(self):
        manifest = (ROOT / "meta" / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("retrieval:", manifest)


if __name__ == "__main__":
    unittest.main()
