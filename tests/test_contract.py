"""Contract-Tests für Knowledge Platform Struktur."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestKnowledgePlatformContract(unittest.TestCase):
    def test_version_und_manifest(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "1.0.0")
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

    def test_content_linkedin_playbook(self):
        md = ROOT / "content" / "playbooks" / "linkedin-presseschau.md"
        self.assertTrue(md.is_file())
        self.assertIn("Regisseur-Inbox", md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
