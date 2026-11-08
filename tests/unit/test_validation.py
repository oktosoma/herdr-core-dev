import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import validate


class TemplateValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['docs', 'templates', 'apps']:
            shutil.copytree(ROOT / name, self.root / name)
        for name in ['README.md', 'AGENTS.md', 'HERDR.md', 'template.json', 'project.example.json', '.env.example']:
            shutil.copy2(ROOT / name, self.root / name)
        subprocess.run(['git', 'init', '--quiet', str(self.root)], check=True, capture_output=True)

    def test_current_template_validates(self):
        self.assertEqual(validate(self.root), [])

    def test_stale_readme_version_fails(self):
        model = json.loads((self.root / 'template.json').read_text())['model_version']
        path = self.root / 'README.md'
        path.write_text(path.read_text().replace(f'v{model}', 'v0.0'))
        self.assertIn('README version is stale', validate(self.root))

    def test_missing_local_link_fails(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\n[Missing](missing.md)\n')
        self.assertTrue(any('Missing or escaping local link' in e for e in validate(self.root)))

    def test_missing_fragment_and_duplicate_id_fail(self):
        path = self.root / 'docs/guide/index.html'
        path.write_text(path.read_text() + '<a href="#absent">missing</a><div id="main"></div>')
        errors = validate(self.root)
        self.assertIn('Guide contains duplicate IDs', errors)
        self.assertIn('Missing guide fragment: absent', errors)

    def test_external_asset_and_populated_env_example_fail(self):
        path = self.root / 'docs/guide/index.html'
        path.write_text(path.read_text() + '<script src="https://example.org/code.js"></script>')
        (self.root / '.env.example').write_text('API_KEY=example-value\n')
        errors = validate(self.root)
        self.assertIn('Offline guide contains an external asset', errors)
        self.assertIn('.env.example must contain variable names with empty values only', errors)

    def test_broken_launch_example_fails(self):
        (self.root / 'templates/codex.md').write_text('command: codex &&\n')
        self.assertIn('codex rendered launch command does not parse', validate(self.root))
