"""Structural checks for the generated Experience page (standard library only)."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

from build import page_work, nav
from content import EXPERIENCES

ROOT = Path(__file__).resolve().parents[1]


class Elements(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ExperienceTests(unittest.TestCase):
    def test_generated_page_is_current(self):
        self.assertEqual(page_work(), (ROOT / 'work/index.html').read_text())

    def test_all_six_entries_and_dates(self):
        self.assertEqual(len(EXPERIENCES), 6)
        expected = ['2018–2020', '2020–2022', '2023–2024',
                    '2022–2025', '2023–2024', '2024–2026']
        self.assertEqual([item['years'] for item in EXPERIENCES], expected)
        tags = Elements(page_work()).tags
        spines = [attrs for tag, attrs in tags
                  if tag == 'button' and attrs.get('class') == 'experience-spine']
        self.assertEqual(len(spines), 6)
        self.assertEqual(sum(x['aria-expanded'] == 'true' for x in spines), 1)
        ids = [attrs['id'] for _, attrs in tags if 'id' in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        for spine in spines:
            self.assertIn(spine['aria-controls'], ids)

    def test_local_assets_exist(self):
        for tag, attrs in Elements(page_work()).tags:
            for key in ('src', 'href'):
                path = attrs.get(key, '')
                if path.startswith('/portfolio/'):
                    self.assertTrue((ROOT / path.lstrip('/')).is_file(), path)

    def test_labels_and_legacy_route(self):
        self.assertIn('<title>Experience — Paper Portfolio</title>', page_work())
        self.assertNotIn('Selected work', page_work())
        navigation = nav('work')
        self.assertIn('href="/work/" aria-current="page"', navigation)
        self.assertIn('class="menu-title work">Experience</h1>', navigation)


if __name__ == '__main__':
    unittest.main()
