#!/usr/bin/env python3
"""Build a self-contained bilingual documentation website for GitHub Pages."""
from __future__ import annotations
import html
import json
from pathlib import Path
from html.parser import HTMLParser

try:
    import mistune
except ImportError as exc:
    raise SystemExit('Install website dependencies: python -m pip install -r requirements-docs.txt') from exc

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'site'
PAGES = [
    ('basics', 'index', '首页', 'Home'),
    ('basics', 'introduction', '项目简介', 'Introduction'),
    ('basics', 'architecture', '系统架构', 'Architecture'),
    ('start', 'installation', '安装与环境', 'Installation'),
    ('start', 'quickstart', '快速开始', 'Quick Start'),
    ('research', 'experiments', '攻防实验', 'Experiments'),
    ('research', 'configuration', '配置说明', 'Configuration'),
    ('more', 'publications', '论文与引用', 'Publications'),
    ('more', 'contributing', '贡献与反馈', 'Contributing'),
]
GROUPS = {
    'zh': {'basics': '项目概览', 'start': '使用指南', 'research': '实验与配置', 'more': '社区与研究'},
    'en': {'basics': 'Overview', 'start': 'Get Started', 'research': 'Experiments & Configuration', 'more': 'Research & Community'},
}
MESSAGES = {
 'zh': {'tagline':'面向供水系统的高保真信息物理安全联合仿真平台','home':'返回首页','lang':'English','repo':'源代码','lab':'CPS² Lab','search':'搜索文档…','noresult':'没有找到匹配页面','copy':'复制链接','footer':'研究软件文档 · 初版草稿 · 功能以公开源码为准','preview':'文档初版','sidebar':'文档导航','menu':'菜单'},
 'en': {'tagline':'High-fidelity co-simulation for water cyber-physical system security','home':'Home','lang':'中文','repo':'Source Code','lab':'CPS² Lab','search':'Search documentation…','noresult':'No matching pages','copy':'Copy link','footer':'Research software documentation · Working draft · Source code is authoritative','preview':'Documentation draft','sidebar':'Documentation','menu':'Menu'},
}

md = mistune.create_markdown(escape=False, plugins=['table','strikethrough'])

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(markup):
    parser = PlainText()
    parser.feed(markup)
    return ' '.join(' '.join(parser.parts).split())


def nav_html(lang: str, active: str) -> str:
    out = []
    for group in ('basics','start','research','more'):
        out.append(f'<div class="nav-heading">{html.escape(GROUPS[lang][group])}</div>')
        for g, slug, zh_name, en_name in PAGES:
            if g != group:
                continue
            name = zh_name if lang == 'zh' else en_name
            current = ' aria-current="page" class="nav-link active"' if slug == active else ' class="nav-link"'
            out.append(f'<a{current} href="{slug}.html">{html.escape(name)}</a>')
    return '\n'.join(out)



def build_one(lang: str, slug: str, label: str):
    content = (ROOT / 'content' / lang / f'{slug}.md').read_text(encoding='utf-8')
    body = md(content)
    strings = MESSAGES[lang]
    other = 'en' if lang == 'zh' else 'zh'
    page_title = f'{label} · Hydro-CPS-Sim'
    tmpl = (ROOT / 'template.html').read_text(encoding='utf-8')
    replacements = {
        '__LANG__': lang,
        '__TITLE__': html.escape(page_title),
        '__DESCRIPTION__': html.escape(strings['tagline'], quote=True),
        '__NAV__': nav_html(lang, slug),
        '__CONTENT__': body,
        '__LANG_LABEL__': strings['lang'],
        '__LANG_URL__': f'../../{other}/latest/{slug}.html',
        '__SITE_HOME__': 'index.html',
        '__TAGLINE__': strings['tagline'],
        '__SEARCH__': strings['search'],
        '__NORESULT__': strings['noresult'],
        '__REPO_LABEL__': strings['repo'],
        '__FOOTER__': strings['footer'],
        '__BADGE__': strings['preview'],
        '__MENU__': strings['menu'],
        '__SLUG__': slug,
    }
    for key, value in replacements.items():
        tmpl = tmpl.replace(key, value)
    page = OUTPUT / lang / 'latest' / f'{slug}.html'
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(tmpl, encoding='utf-8')
    return {'lang':lang, 'slug':slug, 'title':label, 'description':plain_text(body)[:145], 'text':plain_text(body), 'url':f'{lang}/latest/{slug}.html'}


def main():
    (OUTPUT / 'assets').mkdir(parents=True, exist_ok=True)
    for src in (ROOT / 'assets').iterdir():
        if src.is_file():
            (OUTPUT / 'assets' / src.name).write_bytes(src.read_bytes())
    pages = []
    for lang in ('zh','en'):
        for _, slug, label_zh, label_en in PAGES:
            pages.append(build_one(lang, slug, label_zh if lang == 'zh' else label_en))
    (OUTPUT / 'search-index.json').write_text(json.dumps(pages, ensure_ascii=False), encoding='utf-8')
    (OUTPUT / 'index.html').write_text('''<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=zh/latest/index.html"><title>Hydro-CPS-Sim Docs</title><link rel="canonical" href="zh/latest/index.html"></head><body><p><a href="zh/latest/index.html">中文文档</a> · <a href="en/latest/index.html">English docs</a></p></body></html>''', encoding='utf-8')
    (OUTPUT / '.nojekyll').touch()
    print(f'Built {len(pages)} pages in {OUTPUT}')

if __name__ == '__main__':
    main()
