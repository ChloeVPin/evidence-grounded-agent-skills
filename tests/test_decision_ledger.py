import unittest
import json
from pathlib import Path
import subprocess
import shutil
import tempfile

from scripts.decision_ledger import (
    PARAPHRASE_MIN_SHARED_TERMS, candidate_metrics, evaluate_labeled_queries,
    audit_context_names, audit_migrations, find_matching_entries,
    find_paraphrase_candidates, validate_contexts, validate_context_artifacts,
    check_generation_revision, check_source_inventory_digest, validate_entry,
    check_captured_generation_revision, migrate_contexts,
    source_file_inventory_digest, source_inventory_digest,
    audit_policy_assertion_chain, audit_policy_assertion_references,
    discover_current_assertion,
    compare_policy_audit, validate_generation_evidence,
    validate_migration,
    validate_policy_audit, validate_policy_audit_bundle,
    validate_policy_assertion_content, validate_current_assertion_bundle,
    validate_source_file_manifest,
)
from scripts.contradiction_policy import Claim, resolve_claims


class DecisionLedgerTest(unittest.TestCase):
    def test_contextual_entry_is_valid(self):
        result = validate_entry({
            "entry_id": "c-1", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a", "b"], "outcome": "contextual",
            "evidence": ["different contexts"], "decision": "retain both",
        })
        self.assertTrue(result.valid)

    def test_unresolved_entry_requires_next_action(self):
        entry = {
            "entry_id": "c-2", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a", "b"], "outcome": "unresolved",
            "evidence": ["equal strength"], "decision": "defer",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry["next_action"] = "run discriminating experiment"
        self.assertTrue(validate_entry(entry).valid)

    def test_failure_requires_mechanism_correction_and_guard(self):
        entry = {
            "entry_id": "f-1", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["skill claim"], "outcome": "failure",
            "evidence": ["reproduction"], "decision": "deprecate",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry.update(mechanism="stale assumption", corrective_action="revise skill", regression_trigger="add test")
        self.assertTrue(validate_entry(entry).valid)

    def test_empty_evidence_is_rejected(self):
        result = validate_entry({
            "entry_id": "c-3", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a"], "outcome": "supported_refuted",
            "evidence": [], "decision": "accept a",
        })
        self.assertFalse(result.valid)

    def test_missing_cycle_or_artifact_link_is_rejected(self):
        result = validate_entry({
            "entry_id": "c-4", "claims": ["a"], "outcome": "contextual",
            "evidence": ["context"], "decision": "retain",
        })
        self.assertFalse(result.valid)

    def test_archived_contextual_entry_is_valid_and_matches_policy(self):
        path = Path("ledger/decisions/0052-contextual-contradiction.json")
        entry = json.loads(path.read_text())
        result = resolve_claims(
            Claim("a", "low latency", 1), Claim("b", "high throughput", 1),
            discriminating_evidence=False,
        )
        self.assertEqual(result.outcome, "contextual")
        self.assertTrue(validate_entry(entry).valid)
        self.assertEqual(entry["cycle_id"], "0052")

    def test_archived_failure_entry_preserves_correction_and_regression_guard(self):
        path = Path("ledger/decisions/0053-boundary-mutant-failure.json")
        entry = json.loads(path.read_text())
        assessment = validate_entry(entry)
        self.assertTrue(assessment.valid)
        self.assertEqual(entry["outcome"], "failure")
        self.assertIn("zero-value", entry["corrective_action"])
        self.assertIn("survives", entry["regression_trigger"])

    def test_prior_failure_is_found_before_rediscovery(self):
        paths = sorted(Path("ledger/decisions").glob("*-failure.json"))
        entries = [json.loads(path.read_text()) for path in paths]
        entry = next(item for item in entries if item["entry_id"] == "0053-boundary-mutant-failure")
        matches = find_matching_entries(
            entries, "mutation survival is evidence of an incomplete test oracle",
        )
        self.assertEqual([item["entry_id"] for item in matches], [entry["entry_id"]])
        tool_matches = find_matching_entries(
            entries, "wildcard authority can bypass least-privilege boundaries",
        )
        self.assertEqual([item["entry_id"] for item in tool_matches], ["0055-wildcard-authority-failure"])
        self.assertEqual(find_matching_entries(entries, "new failure"), [])

    def test_paraphrase_lookup_returns_candidates_without_merging(self):
        entries = [
            {"entry_id": "boundary", "claims": ["happy-path-only tests can miss a boundary regression"]},
            {"entry_id": "tool", "claims": ["wildcard authority can bypass least-privilege boundaries"]},
        ]
        candidates = find_paraphrase_candidates(
            entries, "missing boundary coverage can let a regression survive",
        )
        self.assertEqual([entry["entry_id"] for entry in candidates], ["boundary"])
        self.assertEqual(
            find_paraphrase_candidates(entries, "database schema migration"), [],
        )

    def test_candidate_metrics_expose_precision_and_recall(self):
        metrics = candidate_metrics({"boundary", "tool"}, {"boundary", "noise"})
        self.assertEqual(metrics["true_positive"], 1)
        self.assertEqual(metrics["false_positive"], 1)
        self.assertEqual(metrics["false_negative"], 1)
        self.assertEqual(metrics["precision"], 0.5)
        self.assertEqual(metrics["recall"], 0.5)

    def test_expanded_labeled_set_measures_current_lookup(self):
        entries = [
            json.loads(path.read_text())
            for path in sorted(Path("ledger/decisions").glob("*-failure.json"))
        ]
        labels = json.loads(Path("ledger/evaluations/0057-paraphrase-labels.json").read_text())
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(len(labels), 9)
        self.assertEqual(metrics["true_positive"], 7)
        self.assertEqual(metrics["false_positive"], 0)
        self.assertEqual(metrics["false_negative"], 0)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)

    def test_adversarial_alias_query_is_only_a_review_candidate(self):
        entries = [{
            "entry_id": "tool",
            "claims": ["wildcard authority can bypass least-privilege boundaries"],
        }]
        candidates = find_paraphrase_candidates(entries, "unrestricted authority decisions")
        self.assertEqual([entry["entry_id"] for entry in candidates], ["tool"])

    def test_context_filter_removes_cross_domain_alias_candidate(self):
        entries = [{
            "entry_id": "tool", "contexts": ["tool-authorization"],
            "claims": ["wildcard authority can bypass least-privilege boundaries"],
        }]
        self.assertEqual(
            find_paraphrase_candidates(
                entries, "unrestricted authority decisions", context="differential-review",
            ), [],
        )

    def test_threshold_is_explicit_and_conservative(self):
        self.assertEqual(PARAPHRASE_MIN_SHARED_TERMS, 2)
        entries = [{"entry_id": "one", "claims": ["boundary regression"]}]
        self.assertEqual(
            [entry["entry_id"] for entry in find_paraphrase_candidates(entries, "boundary regression")],
            ["one"],
        )

    def test_labeled_metrics_do_not_hide_cross_query_false_positive(self):
        entries = [{"entry_id": "one", "claims": ["boundary regression"]}]
        labels = [
            {"query": "boundary regression", "expected_ids": ["one"]},
            {"query": "boundary regression again", "expected_ids": []},
        ]
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(metrics["true_positive"], 1)
        self.assertEqual(metrics["false_positive"], 1)
        self.assertEqual(metrics["false_negative"], 0)
        self.assertEqual(metrics["precision"], 0.5)

    def test_explicit_aliases_recall_authorization_variant(self):
        entries = [{
            "entry_id": "tool",
            "claims": ["wildcard authority can bypass least-privilege boundaries"],
        }]
        candidates = find_paraphrase_candidates(
            entries, "unrestricted authorization can escape declared scope",
        )
        self.assertEqual([entry["entry_id"] for entry in candidates], ["tool"])

    def test_context_filter_recall_exposes_cross_domain_loss(self):
        entries = [
            {"entry_id": "boundary", "contexts": ["test-effectiveness"],
             "claims": ["happy-path-only tests can miss a boundary regression"]},
            {"entry_id": "tool", "contexts": ["tool-authorization"],
             "claims": ["wildcard authority can bypass least-privilege boundaries"]},
            {"entry_id": "dependency", "contexts": ["dependency-security"],
             "claims": ["unverified dependency evidence can conceal supply-chain risk"]},
            {"entry_id": "differential", "contexts": ["differential-review"],
             "claims": ["happy-path equivalence can hide boundary divergence"]},
        ]
        labels = [
            {"query": "boundary regression incomplete tests", "expected_ids": ["boundary"],
             "context": "test-effectiveness"},
            {"query": "wildcard authority bypass", "expected_ids": ["tool"],
             "context": "tool-authorization"},
            {"query": "dependency provenance supply chain risk", "expected_ids": ["dependency"],
             "context": "dependency-security"},
            {"query": "happy path equivalence boundary divergence",
             "expected_ids": ["boundary", "differential"], "context": "differential-review"},
        ]
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(metrics["true_positive"], 4)
        self.assertEqual(metrics["false_positive"], 0)
        self.assertEqual(metrics["false_negative"], 1)
        self.assertAlmostEqual(metrics["recall"], 4 / 5)

    def test_multiple_contexts_restore_explicit_cross_domain_recall(self):
        entries = [
            {"entry_id": "boundary", "contexts": ["test-effectiveness"],
             "claims": ["happy-path-only tests can miss a boundary regression"]},
            {"entry_id": "differential", "contexts": ["differential-review"],
             "claims": ["happy-path equivalence can hide boundary divergence"]},
        ]
        labels = [{
            "query": "happy path equivalence boundary divergence",
            "expected_ids": ["boundary", "differential"],
            "contexts": ["test-effectiveness", "differential-review"],
        }]
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(metrics["true_positive"], 2)
        self.assertEqual(metrics["false_negative"], 0)
        self.assertEqual(metrics["recall"], 1.0)

    def test_malformed_context_declarations_are_rejected(self):
        self.assertFalse(validate_contexts([]).valid)
        self.assertFalse(validate_contexts(["tool", "tool"]).valid)
        self.assertFalse(validate_contexts(["*"]).valid)
        self.assertFalse(validate_contexts(["tool", 3]).valid)
        self.assertTrue(validate_contexts(["tool", "security"]).valid)

    def test_evaluation_fails_closed_on_malformed_contexts(self):
        with self.assertRaisesRegex(ValueError, "wildcard"):
            evaluate_labeled_queries(
                [], [{"query": "anything", "expected_ids": [], "contexts": ["*"]}],
            )

    def test_contexts_are_bound_to_artifact_paths(self):
        valid = {
            "contexts": ["tool-authorization"],
            "artifacts": ["scripts/tool_policy.py"],
        }
        invalid = {
            "contexts": ["tool-authorization"],
            "artifacts": ["scripts/dependency_review.py"],
        }
        unknown = {"contexts": ["unknown"], "artifacts": ["scripts/tool.py"]}
        self.assertTrue(validate_context_artifacts(valid).valid)
        self.assertFalse(validate_context_artifacts(invalid).valid)
        self.assertFalse(validate_context_artifacts(unknown).valid)

    def test_archived_failure_contexts_bind_to_artifacts(self):
        for path in Path("ledger/decisions").glob("*-failure.json"):
            self.assertTrue(validate_entry(json.loads(path.read_text())).valid)

    def test_legacy_context_audit_accepts_archived_names(self):
        entries = [
            json.loads(path.read_text())
            for path in Path("ledger/decisions").glob("*-failure.json")
        ]
        self.assertTrue(audit_context_names(entries).valid)
        self.assertFalse(audit_context_names([
            {"contexts": ["retired-domain"], "artifacts": ["scripts/x.py"]},
        ]).valid)

    def test_context_rename_preserves_binding_and_rejects_collision(self):
        migration = migrate_contexts(
            ["differential-review"], {"differential-review": "behavioral-differential"},
        )
        self.assertTrue(migration.valid)
        self.assertEqual(migration.contexts, ("behavioral-differential",))
        self.assertTrue(validate_context_artifacts({
            "contexts": list(migration.contexts),
            "artifacts": ["scripts/differential_review.py"],
        }).valid)
        collision = migrate_contexts(
            ["differential-review", "behavioral-differential"],
            {"differential-review": "behavioral-differential"},
        )
        self.assertFalse(collision.valid)

    def test_durable_context_migration_matches_historical_entry(self):
        source = json.loads(Path(
            "ledger/decisions/0061-differential-boundary-failure.json",
        ).read_text())
        migration = json.loads(Path(
            "ledger/migrations/0072-differential-context-rename.json",
        ).read_text())
        result = migrate_contexts(
            migration["source_contexts"], {"differential-review": "behavioral-differential"},
        )
        self.assertTrue(result.valid)
        self.assertEqual(migration["source_entry_id"], source["entry_id"])
        self.assertEqual(list(result.contexts), migration["target_contexts"])
        migrated = dict(source, contexts=list(result.contexts))
        self.assertTrue(validate_entry(migrated).valid)

    def test_migration_record_audit_requires_complete_reversible_shape(self):
        migration = json.loads(Path(
            "ledger/migrations/0072-differential-context-rename.json",
        ).read_text())
        self.assertTrue(validate_migration(migration).valid)
        malformed = dict(migration, reversible="yes")
        self.assertFalse(validate_migration(malformed).valid)
        mismatched = dict(migration, artifacts=["scripts/tool_policy.py"])
        self.assertFalse(validate_migration(mismatched).valid)

    def test_migration_inventory_audit_rejects_duplicate_ids(self):
        migration = json.loads(Path(
            "ledger/migrations/0072-differential-context-rename.json",
        ).read_text())
        self.assertTrue(audit_migrations([migration]).valid)
        self.assertFalse(audit_migrations([migration, dict(migration)]).valid)
        self.assertTrue(audit_migrations(
            [migration], {"0061-differential-boundary-failure"},
        ).valid)
        self.assertFalse(audit_migrations([migration], {"missing-entry"}).valid)

    def test_source_inventory_digest_is_stable_and_bound(self):
        source_ids = {"0053-boundary-mutant-failure", "0061-differential-boundary-failure",
                      "0055-wildcard-authority-failure", "0059-unverified-dependency-failure"}
        migration = json.loads(Path(
            "ledger/migrations/0072-differential-context-rename.json",
        ).read_text())
        self.assertEqual(
            migration["source_inventory_sha256"], source_inventory_digest(source_ids),
        )
        self.assertNotEqual(source_inventory_digest(source_ids), source_inventory_digest({"other"}))

    def test_source_inventory_drift_is_detected(self):
        source_ids = {"0053-boundary-mutant-failure", "0055-wildcard-authority-failure",
                      "0059-unverified-dependency-failure", "0061-differential-boundary-failure"}
        migration = json.loads(Path(
            "ledger/migrations/0072-differential-context-rename.json",
        ).read_text())
        self.assertTrue(check_source_inventory_digest(
            migration["source_inventory_sha256"], source_ids,
        ).valid)
        self.assertFalse(check_source_inventory_digest(
            migration["source_inventory_sha256"], source_ids | {"0077-new-entry"},
        ).valid)

    def test_source_file_inventory_manifest_is_bound(self):
        manifest = json.loads(Path(
            "ledger/inventories/0078-source-entry-files.json",
        ).read_text())
        self.assertTrue(validate_source_file_manifest(manifest).valid)
        self.assertEqual(
            manifest["mapping_sha256"], source_file_inventory_digest({
                key: value["path"] for key, value in manifest["entries"].items()
            }),
        )
        changed = json.loads(json.dumps(manifest))
        changed["entries"]["0053-boundary-mutant-failure"]["sha256"] = "0" * 64
        self.assertFalse(validate_source_file_manifest(changed).valid)
        missing_provenance = json.loads(json.dumps(manifest))
        del missing_provenance["generated_by"]
        self.assertFalse(validate_source_file_manifest(missing_provenance).valid)

    def test_generation_revision_must_remain_in_history(self):
        manifest = json.loads(Path(
            "ledger/inventories/0078-source-entry-files.json",
        ).read_text())
        revision = manifest["generated_by"]["revision"]
        self.assertTrue(check_generation_revision(revision, {revision, "current"}).valid)
        self.assertFalse(check_generation_revision(revision, {"current"}).valid)

    def test_generation_revision_binds_to_captured_success(self):
        from scripts.capture_evidence import capture
        root = Path(__file__).resolve().parents[1]
        evidence = capture("python3 -c 'print(\"manifest\")'", root)
        self.assertTrue(check_captured_generation_revision(evidence.revision, evidence).valid)
        self.assertFalse(check_captured_generation_revision("0" * 40, evidence).valid)

    def test_persisted_generation_capture_is_consistent(self):
        record = json.loads(Path(
            "ledger/evidence/0083-generation-capture.json",
        ).read_text())
        self.assertTrue(check_captured_generation_revision(
            record["revision"], record,
        ).valid)
        self.assertEqual(record["exit_status"], 0)
        self.assertEqual(len(record["output_sha256"]), 64)

    def test_generation_evidence_policy_rejects_command_drift(self):
        record = json.loads(Path(
            "ledger/evidence/0083-generation-capture.json",
        ).read_text())
        self.assertTrue(validate_generation_evidence(
            record, "python3 -m unittest discover -s tests", {record["revision"]},
        ).valid)
        altered = dict(record, command="python3 -m unittest discover")
        self.assertFalse(validate_generation_evidence(
            altered, "python3 -m unittest discover -s tests", {record["revision"]},
        ).valid)

    def test_persisted_policy_audit_has_structured_evidence(self):
        audit = json.loads(Path(
            "ledger/evidence/0085-generation-policy-audit.json",
        ).read_text())
        self.assertTrue(validate_policy_audit(audit).valid)
        self.assertFalse(validate_policy_audit(dict(audit, evidence_refs=[])).valid)

    def test_persisted_policy_audit_matches_fresh_rerun(self):
        audit = json.loads(Path(
            "ledger/evidence/0085-generation-policy-audit.json",
        ).read_text())
        evidence = json.loads(Path(
            "ledger/evidence/0086-generation-rerun.json",
        ).read_text())
        self.assertTrue(compare_policy_audit(audit, evidence).valid)
        self.assertFalse(compare_policy_audit(
            dict(audit, result="failed"), evidence,
        ).valid)

    def test_current_versioned_policy_assertion_is_valid(self):
        audit = json.loads(Path(
            "ledger/evidence/0087-generation-policy-audit.json",
        ).read_text())
        evidence = json.loads(Path(
            "ledger/evidence/0087-generation-rerun.json",
        ).read_text())
        self.assertTrue(compare_policy_audit(audit, evidence).valid)

    def test_policy_assertion_chain_has_one_current_head(self):
        assertions = [
            json.loads(Path("ledger/evidence/0085-generation-policy-audit.json").read_text()),
            json.loads(Path("ledger/evidence/0087-generation-policy-audit.json").read_text()),
            json.loads(Path("ledger/evidence/0093-generation-policy-audit.json").read_text()),
        ]
        self.assertTrue(audit_policy_assertion_chain(assertions).valid)
        second_current = dict(assertions[2], audit_id="other-current")
        self.assertFalse(audit_policy_assertion_chain([assertions[2], second_current]).valid)

    def test_policy_assertion_references_are_present(self):
        assertions = [
            json.loads(Path("ledger/evidence/0085-generation-policy-audit.json").read_text()),
            json.loads(Path("ledger/evidence/0087-generation-policy-audit.json").read_text()),
        ]
        available = {
            "ledger/evidence/0083-generation-capture.json",
            "ledger/evidence/0087-generation-rerun.json",
            "scripts/decision_ledger.py",
            "tests/test_decision_ledger.py",
        }
        self.assertTrue(audit_policy_assertion_references(assertions, available).valid)
        self.assertFalse(audit_policy_assertion_references(assertions, set()).valid)

    def test_combined_policy_audit_bundle_requires_all_gates(self):
        audit = json.loads(Path(
            "ledger/evidence/0093-generation-policy-audit.json",
        ).read_text())
        evidence = json.loads(Path(
            "ledger/evidence/0093-generation-rerun.json",
        ).read_text())
        paths = set(audit["evidence_refs"])
        self.assertTrue(validate_policy_audit_bundle(audit, evidence, paths).valid)
        self.assertFalse(validate_policy_audit_bundle(audit, evidence, set()).valid)

    def test_policy_assertion_references_match_content_digests(self):
        audit = json.loads(Path(
            "ledger/evidence/0087-generation-policy-audit.json",
        ).read_text())
        digests = json.loads(Path(
            "ledger/evidence/0087-policy-content-digests.json",
        ).read_text())
        self.assertTrue(validate_policy_assertion_content(audit, digests).valid)
        altered = dict(digests)
        altered["ledger/evidence/0087-generation-rerun.json"] = "0" * 64
        self.assertFalse(validate_policy_assertion_content(audit, altered).valid)

    def test_current_assertion_bundle_joins_all_evidence_layers(self):
        bundle = json.loads(Path(
            "ledger/evidence/0087-current-assertion-bundle.json",
        ).read_text())
        paths = {
            "ledger/evidence/0087-generation-policy-audit.json",
            "ledger/evidence/0087-generation-rerun.json",
            "ledger/evidence/0087-policy-content-digests.json",
        }
        self.assertTrue(validate_current_assertion_bundle(bundle, paths).valid)
        self.assertFalse(validate_current_assertion_bundle(bundle, paths - {
            bundle["content_digest_ref"],
        }).valid)

    def test_current_revision_bundle_is_complete(self):
        audit = json.loads(Path("ledger/evidence/0093-generation-policy-audit.json").read_text())
        evidence = json.loads(Path("ledger/evidence/0093-generation-rerun.json").read_text())
        bundle = json.loads(Path("ledger/evidence/0093-current-assertion-bundle.json").read_text())
        paths = set(audit["evidence_refs"]) | {bundle["assertion_ref"], bundle["content_digest_ref"]}
        self.assertTrue(validate_current_assertion_bundle(bundle, paths).valid)
        self.assertTrue(compare_policy_audit(audit, evidence).valid)

    def test_expanded_assertion_chain_and_current_content_both_pass(self):
        assertions = [
            json.loads(Path(f"ledger/evidence/{name}").read_text())
            for name in (
                "0085-generation-policy-audit.json",
                "0087-generation-policy-audit.json",
                "0093-generation-policy-audit.json",
            )
        ]
        self.assertTrue(audit_policy_assertion_chain(assertions).valid)
        current = assertions[-1]
        digests = json.loads(Path(
            "ledger/evidence/0093-policy-content-digests.json",
        ).read_text())
        self.assertTrue(validate_policy_assertion_content(current, digests).valid)

    def test_current_assertion_is_discovered_from_repository_records(self):
        assertions = [
            json.loads(path.read_text())
            for path in sorted(Path("ledger/evidence").glob("*-generation-policy-audit.json"))
        ]
        head = discover_current_assertion(assertions)
        self.assertTrue(head.valid)
        self.assertEqual(head.assertion["audit_id"], "0093-generation-policy-audit")

    def test_discovered_head_bundle_and_content_pass(self):
        assertions = [
            json.loads(path.read_text())
            for path in sorted(Path("ledger/evidence").glob("*-generation-policy-audit.json"))
        ]
        head = discover_current_assertion(assertions)
        bundle = json.loads(Path(
            "ledger/evidence/0093-current-assertion-bundle.json",
        ).read_text())
        paths = set(head.assertion["evidence_refs"]) | {
            bundle["assertion_ref"], bundle["content_digest_ref"],
        }
        self.assertTrue(validate_current_assertion_bundle(bundle, paths).valid)
        digests = json.loads(Path(
            "ledger/evidence/0093-policy-content-digests.json",
        ).read_text())
        self.assertTrue(validate_policy_assertion_content(head.assertion, digests).valid)

    def test_executable_current_head_audit_passes(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["python3", "scripts/audit_current_assertion.py"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertEqual(output["audit_id"], "0093-generation-policy-audit")
        self.assertEqual(output["result"], "passed")

    def test_executable_current_head_audit_fails_without_evidence_root(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["python3", "scripts/audit_current_assertion.py", "--root", "/tmp"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["result"], "failed")

    def test_executable_current_head_audit_rejects_tampered_bundle(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            (temp_root / "ledger").mkdir()
            shutil.copytree(root / "ledger" / "evidence", temp_root / "ledger" / "evidence")
            bundle_path = temp_root / "ledger/evidence/0093-current-assertion-bundle.json"
            bundle = json.loads(bundle_path.read_text())
            bundle["assertion_ref"] = "ledger/evidence/missing.json"
            bundle_path.write_text(json.dumps(bundle))
            result = subprocess.run(
                ["python3", "scripts/audit_current_assertion.py", "--root", str(temp_root)],
                cwd=root, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["result"], "failed")

    def test_executable_current_head_audit_reports_malformed_json(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            (temp_root / "ledger").mkdir()
            shutil.copytree(root / "ledger" / "evidence", temp_root / "ledger" / "evidence")
            (temp_root / "ledger/evidence/0093-generation-policy-audit.json").write_text("{")
            result = subprocess.run(
                ["python3", "scripts/audit_current_assertion.py", "--root", str(temp_root)],
                cwd=root, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            output = json.loads(result.stdout)
            self.assertEqual(output["result"], "failed")
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
