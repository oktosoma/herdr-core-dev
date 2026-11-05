import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import doctor


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'decision.md').write_text('Status: ACCEPTED\nApprover: Owner\nDate: 2026-11-05\n')
        self.profile = json.loads((ROOT / 'project.example.json').read_text())
        self.profile.update(project_name='example', integration_branch='coord/bootstrap',
                            roles={key: 'approved harness model' for key in self.profile['roles']},
                            decisions={key: 'decision.md' for key in self.profile['decisions']},
                            tools={'hc': {'version': '1.2.3', 'source': 'https://example.org/official'}})
        for check in self.profile['checks']:
            check['command'] = 'must-never-be-executed-by-doctor'
        self.config = self.root / 'project.json'

    def run_doctor(self, versions):
        self.config.write_text(json.dumps(self.profile))
        with patch.object(doctor, 'ROOT', self.root), patch.object(sys, 'argv', ['doctor', '--profile', 'project', '--config', str(self.config)]), patch.object(doctor, 'version_output', side_effect=lambda name: versions.get(name)) as version, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = doctor.main()
        return result, [call.args[0] for call in version.call_args_list]

    def test_project_preflight_checks_only_declared_tools_not_application_commands(self):
        result, checked = self.run_doctor({'git': 'git version 2.47.0', 'hc': 'hc 1.2.3'})
        self.assertEqual(result, 0)
        self.assertEqual(checked, ['git', 'hc'])

    def test_wrong_missing_and_partial_versions_fail(self):
        for actual in (None, 'hc 11.2.30', 'hc 1.2.3-beta', 'hc 1.2.4'):
            with self.subTest(actual=actual):
                result, _ = self.run_doctor({'git': 'git version 2.47.0', 'hc': actual})
                self.assertEqual(result, 1)

    def test_unresolved_profile_does_not_probe_project_tools(self):
        self.profile['project_name'] = '<unresolved>'
        result, checked = self.run_doctor({'git': 'git version 2.47.0', 'hc': 'hc 1.2.3'})
        self.assertEqual(result, 1)
        self.assertEqual(checked, ['git'])
