"""Startup isolation and bounded task-context regressions."""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/building-tnr-content/scripts'))
import session_open
import session_close
import validate


class StartupTests(unittest.TestCase):
    def test_session_open_never_writes_digest_or_runs_guards_by_default(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'state').mkdir()
            path = root / 'state/digest.json'
            path.write_text(json.dumps({'state_line': 'test', 'token_ledger': ['keep'], 'verified_at_close': ['keep']}))
            before = path.read_bytes()
            with patch.object(session_open, 'ROOT', root), patch.object(session_open, 'run_guards') as guards, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(session_open.main([]), 0)
                self.assertEqual(session_open.main(['--read', 'state/digest.json']), 0)
                guards.assert_not_called()
                def mutate_summary(_, d):
                    d['verified_at_close'] = ['in memory']; return []
                guards.side_effect = mutate_summary
                self.assertEqual(session_open.main(['--guards']), 0)
            self.assertEqual(path.read_bytes(), before)

    def test_parity_null_reports_error_instead_of_crash(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'bundle.json'; p.write_text('{"checks":null}')
            report = validate.Report()
            validate.parity(str(p), report)
            with contextlib.redirect_stdout(io.StringIO()): self.assertNotEqual(report.dump(False), 0)

    def test_forge_parity_not_applicable_and_legacy_errors_expose_stderr(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); inbox = root / 'harvests/inbox'; inbox.mkdir(parents=True)
            bundle = inbox / 'tnr_results_1.json'; bundle.write_text('{"cfg":"forge","checks":null}')
            ok = subprocess.CompletedProcess([], 0, 'passed\n', '')
            with patch.object(session_close.subprocess, 'run', return_value=ok) as run:
                d = {}; self.assertEqual(session_close.run_guards(str(root), d), [])
                self.assertEqual(run.call_count, 3)
                self.assertTrue(any('NOT APPLICABLE' in s for s in d['verified_at_close']))
            bundle.write_text('{"cfg":"generated","checks":null}')
            bad = subprocess.CompletedProcess([], 1, '', 'actionable stderr\n')
            with patch.object(session_close.subprocess, 'run', side_effect=[ok,ok,ok,bad]):
                d = {}; self.assertTrue(session_close.run_guards(str(root), d))
                self.assertIn('actionable stderr', d['verified_at_close'][-1])

    def test_context_plus_entry_point_under_budget(self):
        p = subprocess.run([sys.executable, 'scripts/tnr.py', 'context', 'missions.check'], cwd=ROOT, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        # Conservative byte budget: 8KB approximates 2,000 tokens at four bytes/token.
        self.assertLessEqual(len(p.stdout) + (ROOT / 'CHATGPT.md').stat().st_size, 8000)

    def test_queries_leave_tracked_inputs_unchanged(self):
        paths = [ROOT / p for p in ['state/digest.json','state/active-context.md','state/status.json','answers/records.json']]
        before = {p: p.read_bytes() for p in paths}
        for args in [['session'], ['missions','check','--rank','A']]:
            p = subprocess.run([sys.executable, 'scripts/tnr.py', *args], cwd=ROOT, capture_output=True, text=True)
            # A later capture can legitimately introduce findings; that remains a read-only query.
            self.assertIn(p.returncode, [0, 1], p.stderr + p.stdout)
            self.assertFalse(p.stderr, p.stderr)
        self.assertEqual(before, {p: p.read_bytes() for p in paths})


class GateTests(unittest.TestCase):
    def test_missing_routed_reference_fails(self):
        from scripts import check_repo
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for rel in ['state/staged_workflows/release_pin.yml', '.github/workflows/release_pin.yml']:
                p = root / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('same')
            data = root / 'skills/building-tnr-content/data'; data.mkdir(parents=True)
            for name in ['32b_DATA_pool.json','45c_DATA_constructors.json','45g_DATA_checks.json']:
                (root / name).write_text('{}'); (data / name).write_text('{}')
            (root / 'README.md').write_text('Read `docs/missing.md`')
            with patch.object(check_repo, 'ENTRY_POINTS', ['README.md']), patch.object(check_repo, 'CONTEXTS', {}):
                self.assertIn('README.md: missing routed file docs/missing.md', check_repo.check_routes(root))

    def test_changed_generated_view_fails_parity(self):
        from scripts import check_repo
        import shutil
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for rel in ['.github/scripts/build_answers.py','skills/building-tnr-content/scripts/record_index.py']:
                p = root / rel; p.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, p)
            (root / 'harvests/inbox').mkdir(parents=True)
            p = subprocess.run([sys.executable, str(root / '.github/scripts/build_answers.py'), '--repo', str(root)], capture_output=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(check_repo.check_answers(root), [])
            (root / 'answers/missions_A.md').write_text('Invented all-clear')
            self.assertIn('stale generated answers/missions_A.md', check_repo.check_answers(root))


if __name__ == '__main__': unittest.main()
