import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.project_profile import validate_profile

ROOT = Path(__file__).resolve().parents[2]


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'decision.md').write_text('Status: ACCEPTED\nApprover: Project owner\nDate: 2026-11-05\n')
        self.profile = json.loads((ROOT / 'project.example.json').read_text())
        self.profile.update(project_name='example', integration_branch='coord/bootstrap',
                            roles={key: 'approved-harness approved-model' for key in self.profile['roles']},
                            tools={'hc': {'version': '1.2.3', 'source': 'https://example.org/official'}},
                            decisions={key: 'decision.md' for key in self.profile['decisions']})
        for check in self.profile['checks']:
            check['command'] = 'native-check --kind ' + check['name']

    def test_valid_profile(self):
        self.assertEqual(validate_profile(self.profile, self.root), [])

    def test_example_is_allowed_only_in_template_mode(self):
        example = json.loads((ROOT / 'project.example.json').read_text())
        self.assertEqual(validate_profile(example, ROOT, example=True), [])
        self.assertTrue(validate_profile(example, ROOT))

    def test_decision_cannot_escape_repository(self):
        self.profile['decisions']['stack'] = '../outside.md'
        self.assertTrue(any('inside the repository' in e for e in validate_profile(self.profile, self.root)))

    def test_symlink_decision_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as other:
            external = Path(other) / 'accepted.md'
            external.write_text('Status: ACCEPTED\nApprover: Owner\nDate: 2026-11-05\n')
            (self.root / 'escape.md').symlink_to(external)
            self.profile['decisions']['stack'] = 'escape.md'
            self.assertTrue(any('inside the repository' in e for e in validate_profile(self.profile, self.root)))

    def test_draft_and_unfilled_approval_block_readiness(self):
        (self.root / 'decision.md').write_text('Status: DRAFT\nApprover: <founder>\nDate: <date>\n')
        errors = validate_profile(self.profile, self.root)
        self.assertTrue(any('ACCEPTED' in e for e in errors))
        self.assertTrue(any('Approver' in e for e in errors))

    def test_empty_approval_and_invalid_date_block_readiness(self):
        (self.root / 'decision.md').write_text('Status: ACCEPTED\nApprover: \nDate: 2026-02-30\n')
        errors = validate_profile(self.profile, self.root)
        self.assertTrue(any('Approver must be recorded' in e for e in errors))
        self.assertTrue(any('valid YYYY-MM-DD' in e for e in errors))
        (self.root / 'decision.md').write_text('Status: ACCEPTED\nApprover: Owner\nDate:\nSupersedes: None\n')
        self.assertTrue(any('Date must be recorded' in e for e in validate_profile(self.profile, self.root)))

    def test_not_applicable_requires_reason_and_no_command(self):
        check = self.profile['checks'][1]
        check.update(status='not_applicable', command='', reason='No database or service boundary in this project')
        self.assertEqual(validate_profile(self.profile, self.root), [])
        check['reason'] = ''
        self.assertTrue(validate_profile(self.profile, self.root))

    def test_missing_duplicate_and_invalid_checks_are_rejected(self):
        for mutation in ('missing', 'duplicate', 'invalid'):
            with self.subTest(mutation=mutation):
                profile = copy.deepcopy(self.profile)
                if mutation == 'missing':
                    profile['checks'].pop()
                elif mutation == 'duplicate':
                    profile['checks'].append(profile['checks'][0])
                else:
                    profile['checks'][0]['status'] = 'skipped'
                self.assertTrue(validate_profile(profile, self.root))

    def test_invalid_shapes_fail_cleanly(self):
        for key in self.profile:
            with self.subTest(key=key):
                profile = copy.deepcopy(self.profile)
                profile[key] = None
                self.assertTrue(validate_profile(profile, self.root))
        self.assertTrue(validate_profile([], self.root))

    def test_credentials_and_tool_arguments_are_rejected(self):
        for source in ('http://example.org/tool', 'https://token@example.org/tool', 'https://example.org?token=secret'):
            with self.subTest(source=source):
                self.profile['tools']['hc']['source'] = source
                self.assertTrue(validate_profile(self.profile, self.root))
        self.profile['tools'] = {'sh -c command': {'version': '1.2.3', 'source': 'https://example.org'}}
        self.assertTrue(validate_profile(self.profile, self.root))

    def test_boolean_capacity_and_invalid_branch_are_rejected(self):
        self.profile['max_workers'] = True
        self.profile['integration_branch'] = 'coord/../main'
        errors = validate_profile(self.profile, self.root)
        self.assertTrue(any('max_workers' in e for e in errors))
        self.assertTrue(any('integration_branch' in e for e in errors))
        self.profile['integration_branch'] = 'coord/milestone.lock/next'
        self.assertTrue(any('integration_branch' in e for e in validate_profile(self.profile, self.root)))
