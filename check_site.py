#!/usr/bin/env python3
"""Check the actual deployment artifact, including links and language pairs."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent / 'site'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def main():
    errors = []
    pages = {}
    for path in ROOT.rglob('*.html'):
        text = path.read_text()
        pages[path.resolve()] = Page(text)
        if re.search(r'__[A-Z_]+__', text):
            errors.append(f'{path}: unreplaced template token')
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = ((ROOT if url.path.startswith('/') else path.parent) / unquote(url.path).lstrip('/')).resolve()
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append(f'{path}: broken local link {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path}: missing anchor {link}')
    index = json.loads((ROOT / 'search-index.json').read_text())
    expected = {f'{lang}/latest/{slug}.html' for lang in ('zh', 'en') for slug in
                ('index', 'introduction', 'architecture', 'installation', 'quickstart',
                 'experiments', 'configuration', 'publications', 'contributing')}
    if {entry['url'] for entry in index} != expected or len(index) != 18:
        errors.append('Search index must contain exactly 18 bilingual pages')
    for entry in index:
        if not (ROOT / entry['url']).is_file() or not entry.get('text'):
            errors.append(f'Invalid search entry: {entry["url"]}')
    for path in ROOT.rglob('*'):
        if path.name == 'CNAME':
            errors.append(f'Unexpected custom domain file: {path}')
        if path.suffix in ('.html', '.css', '.js', '.json') and 'lzhaoblog.cn' in path.read_text():
            errors.append(f'Expired domain reference: {path}')
    if not (ROOT / '.nojekyll').exists():
        errors.append('Missing .nojekyll')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} HTML pages, 18 full-text search entries, local links, language pairs and domain configuration')


if __name__ == '__main__':
    main()
