"""Socket-free evidence selection regressions, including the real A-rank corpus."""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/building-tnr-content/scripts'))
import record_index as records
import harvest


def capture(record_id='q1', name='Mission', at='2026-10-06T12:00:00Z'):
    return {'proc': 'quests.get', 'input': {'id': record_id}, 'persist': 'full',
            'ok': True, 'error': None, 'persistOk': True, 'persistError': None,
            'snapshotKey': 'job::before::0', 'at': at,
            'data': {'id': record_id, 'name': name, 'hidden': False,
                     'questType': 'mission', 'questRank': 'A',
                     'content': {'objectives': [{'id': 'win', 'task': 'win_quest'}]}}}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'harvests/inbox').mkdir(parents=True)
        p = self.root / records.PRODUCER
        p.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / records.PRODUCER, p)

    def write(self, name, captures, **overrides):
        bundle = {'cfg': 'forge', 'state': 'DONE', 'outcome': 'success', 'captures': captures}
        bundle.update(overrides)
        path = self.root / 'harvests/inbox' / name
        path.write_text(json.dumps(bundle))
        return path

    def test_latest_timestamp_wins_over_filename(self):
        self.write('z.json', [capture(name='Old', at='2026-10-05T12:00:00Z')])
        self.write('a.json', [capture(name='New')])
        r = records.derive(self.root)
        self.assertEqual(r['records'][0]['name'], 'New')
        self.assertFalse(r['coverage']['complete_population'])
        self.assertEqual(r['records'][0]['evidence']['pointer'], '/captures/0/data')

    def test_newer_bad_full_read_does_not_fall_back(self):
        self.write('old.json', [capture(at='2026-10-05T12:00:00Z')])
        for field, value in [('ok', False), ('persistOk', False), ('at', None),
                             ('snapshotKey', ''), ('error', 'failed')]:
            with self.subTest(field=field):
                c = capture(); c[field] = value
                self.write('new.json', [c])
                r = records.derive(self.root)
                self.assertEqual(r['records'], [])
                self.assertEqual(r['unresolved'][0]['id'], 'q1')

    def test_invalid_bundle_outcome_is_unresolved(self):
        for override in [{'state': 'RUNNING'}, {'outcome': 'unverified'}]:
            self.write('bundle.json', [capture()], **override)
            self.assertEqual(records.derive(self.root)['records'], [])

    def test_identity_mismatch_is_unresolved(self):
        c = capture(); c['data']['id'] = 'other'
        self.write('bundle.json', [c])
        self.assertIn('input/record identity mismatch', records.derive(self.root)['unresolved'][0]['reasons'])

    def test_same_time_conflicting_records_are_not_tiebroken_by_path(self):
        self.write('a.json', [capture(name='One')]); self.write('b.json', [capture(name='Two')])
        r = records.derive(self.root)
        self.assertEqual(r['records'], [])
        self.assertIn('conflicting records at the same timestamp', r['unresolved'][0]['reasons'])

    def test_equivalent_timezone_and_duplicate_record(self):
        self.write('a.json', [capture()])
        self.write('b.json', [capture(at='2026-10-06T14:00:00+02:00')])
        r = records.derive(self.root)
        self.assertEqual(len(r['records']), 1)
        self.assertEqual(r['unresolved'], [])

    def test_summary_and_legacy_are_excluded_not_absence(self):
        c = capture(); c.pop('persist'); c.pop('at')
        self.write('summary.json', [c]); self.write('legacy.json', [capture()], cfg='generated')
        self.write('valid.json', [capture()])
        r = records.derive(self.root)
        self.assertEqual(len(r['records']), 1)
        self.assertEqual(r['coverage']['excluded'], {'legacy_adapter_required': 1, 'summary_not_record_evidence': 1})

    def test_invalid_json_fails_explicitly(self):
        (self.root / 'harvests/inbox/bad.json').write_text('{bad')
        with self.assertRaises(ValueError): records.derive(self.root)

    def test_cache_invalidates_on_change_addition_and_deletion_without_writes(self):
        p = self.write('one.json', [capture()])
        cached = records.derive(self.root)
        output = self.root / records.OUTPUT; output.parent.mkdir(); output.write_text(records.encoded(cached))
        original = output.read_bytes()
        self.write('one.json', [capture(name='Changed')])
        self.assertEqual(records.load_current(self.root)['records'][0]['name'], 'Changed')
        self.write('two.json', [capture('q2')])
        self.assertEqual(len(records.load_current(self.root)['records']), 2)
        p.unlink()
        self.assertEqual(len(records.load_current(self.root)['records']), 1)
        self.assertEqual(output.read_bytes(), original)

    def test_producer_hash_invalidates_cache(self):
        self.write('one.json', [capture()]); r = records.derive(self.root)
        output = self.root / records.OUTPUT; output.parent.mkdir(); output.write_text(records.encoded(r))
        p = self.root / records.PRODUCER; p.write_text(p.read_text() + '\n# changed\n')
        self.assertNotEqual(records.load_current(self.root)['inputs'], r['inputs'])

    def test_targeted_lookup_reports_missing_id(self):
        self.write('one.json', [capture()]); r = records.mission_report(records.derive(self.root), 'A', ['missing'])
        self.assertEqual(r['records'], [])
        self.assertEqual(r['requested_ids_not_resolved'], ['missing'])

    def test_known_structural_findings(self):
        c = capture(); c['data']['content']['objectives'] = [
            {'id': 'a', 'task': 'dialog', 'nextObjectiveId': [{'nextObjectiveId': 'missing'}]},
            {'id': 'a', 'task': 'win_quest'}]
        self.write('one.json', [c]); m = records.derive(self.root)['records'][0]['mission']
        self.assertIn('duplicate objective IDs', m['findings'])
        self.assertIn('missing edge targets: missing', m['findings'])

    def test_terminal_empty_edge_and_visible_records_are_valid(self):
        c = capture(); c['data']['content']['objectives'][0]['nextObjectiveId'] = ''
        self.write('one.json', [c]); r = records.derive(self.root)['records'][0]
        self.assertEqual(r['mission']['findings'], [])
        self.assertFalse(r['hidden'])

    def test_answer_generation_refreshes_seed_names_and_hidden(self):
        seed = self.root / 'harvests/seed'; seed.mkdir()
        (seed / '47_INDEX_quest.json').write_text(json.dumps({'cols': ['id','n','hidden'], 'rows': [['q1','New Quest - q1',None]]}))
        self.write('one.json', [capture(name='Correct Name'), capture('q2', 'New Record')])
        result = subprocess.run([sys.executable, str(ROOT / '.github/scripts/build_answers.py'), '--repo', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads((self.root / 'answers/names_quest.json').read_text())
        self.assertEqual(out['rows'], [['q1', 'Correct Name', False]])
        hot = json.loads((self.root / 'answers/hot.json').read_text())
        self.assertEqual(hot['entities']['quest']['rows'], [['q2', 'New Record', False]])

    def test_harvest_refuses_ambiguous_selection_and_supports_id_and_all(self):
        p = self.write('one.json', [capture(), capture('q2')])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(harvest.cmd_get(str(p), 'quests.get'), 1)
            self.assertEqual(harvest.cmd_get(str(p), 'quests.get', record_id='q2'), 0)
            out = self.root / 'selected.json'
            self.assertEqual(harvest.cmd_get(str(p), 'quests.get', str(out), all_matches=True), 0)
        self.assertEqual([r['id'] for r in json.loads(out.read_text())], ['q1', 'q2'])


class RepositoryCorpusTests(unittest.TestCase):
    def test_forsworn_latest_records_and_reproducibility(self):
        # Pin the regression corpus, not the moving repository's latest observations.
        # Future captures may legitimately change rank, visibility or objective count.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'harvests/inbox').mkdir(parents=True)
            (root / records.PRODUCER).parent.mkdir(parents=True)
            shutil.copyfile(ROOT / records.PRODUCER, root / records.PRODUCER)
            fixture = 'harvests/inbox/tnr_results_1791294237928.json'
            shutil.copyfile(ROOT / fixture, root / fixture)
            index = records.derive(root)
            self.assertEqual(records.encoded(index), records.encoded(records.derive(root)))
        by_name = {r['name']: r for r in records.mission_report(index, 'A')['records']}
        for name in ['Three Rounds', 'The Long Winter', 'Old Ghost', 'The Tenth Name']:
            r = by_name[name]
            self.assertEqual(r['mission']['objective_count'], 5)
            self.assertEqual(r['mission']['findings'], [])
            self.assertEqual(r['evidence']['bundle'], 'harvests/inbox/tnr_results_1791294237928.json')


if __name__ == '__main__': unittest.main()
