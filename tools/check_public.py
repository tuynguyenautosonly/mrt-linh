#!/usr/bin/env python3
"""check_public.py — finite, offline, stdlib-only consistency check for the mrt-linh public showcase.

Checks ONLY an allow-list of local paths under the given repository root: page metadata (canonical, og:*, twitter:*),
robots.txt + sitemap.xml coherence, local link/asset resolution, social-image dimensions, package.json metadata.
It never opens a network connection (there is no network code in this file), never executes or renders page content
(HTML is tokenized with html.parser only), and refuses any path that escapes the root.

Statuses: PASS (verified), FAIL (verified contradiction), UNKNOWN (file missing/unreadable/unparsable: not verified),
SKIP (external http(s)/mailto/tel references: existence is NOT claimed either way).
Exit: 0 all verified checks PASS (SKIP allowed) · 1 any FAIL · 2 any UNKNOWN or invalid root/arguments.
Usage: python tools/check_public.py [--root PATH] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
from html.parser import HTMLParser

SITE = 'https://tuynguyenautosonly.github.io/mrt-linh/'
SITE_PATH = '/mrt-linh/'                      # path prefix of the two pages on the Pages host
REPO_URLS = ('https://github.com/tuynguyenautosonly/mrt-linh', 'https://github.com/tuynguyenautosonly/mrt-linh.git',
             'git+https://github.com/tuynguyenautosonly/mrt-linh.git', 'github:tuynguyenautosonly/mrt-linh')
MAX_BYTES = 2 * 1024 * 1024
PAGES = {  # path → expected canonical URL
    'docs/index.html': SITE,
    'docs/report.html': SITE + 'report.html',
}
ALLOWED_FILES = ('docs/index.html', 'docs/report.html', 'docs/robots.txt', 'docs/sitemap.xml', 'docs/social.png', 'docs/icon.svg',
                 'package.json', 'README.md', 'README.vi.md', 'CONTRIBUTING.md', 'CAPABILITIES.md', 'ARCHITECTURE.md', 'examples/README.md')
LINK_SOURCES = ('docs/index.html', 'docs/report.html', 'README.md', 'README.vi.md', 'CONTRIBUTING.md', 'CAPABILITIES.md', 'ARCHITECTURE.md', 'examples/README.md')
REQUIRED_META = {'og:title', 'og:description', 'og:image', 'og:url', 'og:type', 'og:locale', 'og:image:alt',
                 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'}
# every required tag must be present AND non-blank; og:type must be the one value these pages claim; og:locale must be ll_CC
OG_TYPE_EXPECTED = 'website'
EXTERNAL_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:')


class Result:
    def __init__(self):
        self.checks = []

    def add(self, cid, status, detail=''):
        self.checks.append({'id': cid, 'status': status, 'detail': detail})

    def summary(self):
        s = [c['status'] for c in self.checks]
        overall = 'FAIL' if 'FAIL' in s else ('UNKNOWN' if 'UNKNOWN' in s else 'PASS')
        return {'status': overall, 'counts': {k: s.count(k) for k in ('PASS', 'FAIL', 'UNKNOWN', 'SKIP')}, 'checks': self.checks,
                'network_used': False, 'note': 'SKIP entries are external references; their availability is not claimed.'}


def safe_path(root, rel):
    """Resolve rel under root; None when it escapes (symlinks resolved)."""
    if rel.startswith(('/', '\\')) or '\x00' in rel:
        return None
    full = os.path.realpath(os.path.join(root, rel))
    if full != root and not full.startswith(root + os.sep):
        return None
    return full


def read_bytes(root, rel, res, cid):
    full = safe_path(root, rel)
    if full is None:
        res.add(cid, 'FAIL', 'path escapes root: %s' % rel)
        return None
    try:
        with open(full, 'rb') as f:
            data = f.read(MAX_BYTES + 1)
    except OSError as e:
        res.add(cid, 'UNKNOWN', '%s unreadable (%s)' % (rel, type(e).__name__))
        return None
    if len(data) > MAX_BYTES:
        res.add(cid, 'UNKNOWN', '%s exceeds %d bytes; not checked' % (rel, MAX_BYTES))
        return None
    return data


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.links, self.hrefs, self.srcs, self.title = {}, {}, [], [], None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('property') or a.get('name')
            if key and 'content' in a:
                self.meta.setdefault(key, a['content'])
        elif tag == 'link':
            if a.get('rel') and a.get('href'):
                self.links.setdefault(a['rel'], a['href'])
        elif tag == 'a' and a.get('href'):
            self.hrefs.append(a['href'])
        elif tag in ('img', 'script') and a.get('src'):
            self.srcs.append(a['src'])
        elif tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or '') + data


def png_size(data):
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', data[16:24])


def check_page(root, rel, canonical, res):
    data = read_bytes(root, rel, res, 'page:%s' % rel)
    if data is None:
        return None
    try:
        p = MetaParser()
        p.feed(data.decode('utf-8'))
    except (UnicodeDecodeError, Exception) as e:  # html.parser is lenient; decode is the realistic failure
        res.add('page:%s' % rel, 'UNKNOWN', 'not parsable (%s)' % type(e).__name__)
        return None
    cid = 'meta:%s' % rel
    import re
    missing = sorted(REQUIRED_META - set(p.meta))
    blank = sorted(k for k in REQUIRED_META if k in p.meta and not p.meta[k].strip())
    problems = []
    if missing:
        problems.append('missing ' + ', '.join(missing))
    if blank:
        problems.append('blank ' + ', '.join(blank))
    if 'og:type' in p.meta and p.meta['og:type'].strip() and p.meta['og:type'].strip() != OG_TYPE_EXPECTED:
        problems.append('og:type %r != %s' % (p.meta['og:type'], OG_TYPE_EXPECTED))
    if 'og:locale' in p.meta and p.meta['og:locale'].strip() and not re.fullmatch(r'[a-z]{2}_[A-Z]{2}', p.meta['og:locale'].strip()):
        problems.append('og:locale %r is not ll_CC' % p.meta['og:locale'])
    if problems:
        res.add(cid + ':required', 'FAIL', '; '.join(problems))
    else:
        res.add(cid + ':required', 'PASS', 'all required og/twitter tags present and non-empty; og:type website; og:locale ll_CC')
    can = p.links.get('canonical')
    if can is None:
        res.add(cid + ':canonical', 'FAIL', 'no <link rel=canonical>')
    elif can != canonical:
        res.add(cid + ':canonical', 'FAIL', 'canonical %s != expected %s' % (can, canonical))
    else:
        res.add(cid + ':canonical', 'PASS', can)
    if p.meta.get('og:url') != canonical:
        res.add(cid + ':og_url', 'FAIL', 'og:url %r != canonical' % p.meta.get('og:url'))
    else:
        res.add(cid + ':og_url', 'PASS', 'og:url equals canonical')
    if p.meta.get('twitter:card') != 'summary_large_image':
        res.add(cid + ':twitter_card', 'FAIL', 'twitter:card %r' % p.meta.get('twitter:card'))
    else:
        res.add(cid + ':twitter_card', 'PASS', 'summary_large_image')
    if not p.title or not p.title.strip():
        res.add(cid + ':title', 'FAIL', 'empty <title>')
    else:
        res.add(cid + ':title', 'PASS', p.title.strip()[:80])
    # social image: must be an absolute URL under the site and exist locally with declared dimensions
    for key in ('og:image', 'twitter:image'):
        url = p.meta.get(key)
        if not url:
            continue
        if not url.startswith(SITE):
            res.add(cid + ':' + key, 'FAIL', '%s not under site origin: %s' % (key, url))
            continue
        local = 'docs/' + url[len(SITE):]
        img = read_bytes(root, local, res, cid + ':' + key)
        if img is None:
            continue
        size = png_size(img)
        if size is None:
            res.add(cid + ':' + key, 'FAIL', '%s is not a PNG' % local)
            continue
        want = (p.meta.get('og:image:width'), p.meta.get('og:image:height'))
        if key == 'og:image' and want != (None, None) and want != (str(size[0]), str(size[1])):
            res.add(cid + ':' + key, 'FAIL', 'declared %sx%s but file is %dx%d' % (want[0], want[1], size[0], size[1]))
        else:
            res.add(cid + ':' + key, 'PASS', '%s %dx%d' % (local, size[0], size[1]))
    return p


def check_links(root, rel, hrefs, res):
    base_dir = os.path.dirname(rel)
    for h in hrefs:
        if h.startswith(EXTERNAL_PREFIXES):
            res.add('link:%s:%s' % (rel, h[:60]), 'SKIP', 'external reference; availability not checked')
            continue
        if h.startswith('#'):
            continue
        target = h.split('#', 1)[0].split('?', 1)[0]
        lid = 'link:%s:%s' % (rel, h[:60])
        is_dir = target in ('', '.', './') or target.endswith('/')
        if target in ('', '.', './'):
            target = '.'
        candidate = os.path.normpath(os.path.join(base_dir, target)) if base_dir else os.path.normpath(target)
        full = safe_path(root, candidate)   # escape is rejected BEFORE any directory/default-document handling
        if full is None:
            res.add(lid, 'FAIL', 'local link escapes root')
            continue
        if is_dir:
            # a directory link must resolve to an existing directory AND a default document, the same way the showcase's
            # own './' resolves to docs/index.html (Pages) and a repo directory link resolves to README.md (GitHub)
            if not os.path.isdir(full):
                res.add(lid, 'FAIL', 'directory missing: %s' % candidate)
                continue
            # the default document itself must stay inside the root (a symlinked index.html/README.md pointing out is an escape)
            def default_doc(name):
                rel_doc = os.path.normpath(os.path.join(candidate, name))
                doc_full = safe_path(root, rel_doc)
                if os.path.lexists(os.path.join(full, name)) and doc_full is None:
                    return 'escape'
                return 'file' if (doc_full is not None and os.path.isfile(doc_full)) else 'absent'
            if rel.startswith('docs/'):
                # Pages host: a directory URL is served only through its index.html
                state = default_doc('index.html')
                if state == 'file':
                    res.add(lid, 'PASS', '%s/index.html' % candidate)
                elif state == 'escape':
                    res.add(lid, 'FAIL', 'default document %s/index.html escapes root' % candidate)
                else:
                    res.add(lid, 'FAIL', 'directory %s has no index.html (Pages would 404)' % candidate)
            else:
                # GitHub-rendered Markdown: an existing directory is a listing; README.md is shown when present
                state = default_doc('README.md')
                if state == 'escape':
                    res.add(lid, 'FAIL', 'default document %s/README.md escapes root' % candidate)
                else:
                    res.add(lid, 'PASS', '%s/ (directory listing%s)' % (candidate, ' + README.md' if state == 'file' else ', no README.md'))
        elif os.path.isfile(full):
            res.add(lid, 'PASS', candidate)
        else:
            res.add(lid, 'FAIL', 'local target missing: %s' % candidate)


def markdown_links(data):
    out, i = [], 0
    text = data.decode('utf-8', 'replace')
    while True:
        i = text.find('](', i)
        if i < 0:
            return out
        j = text.find(')', i)
        if j < 0:
            return out
        out.append(text[i + 2:j].split(' ')[0])
        i = j


def check_robots_sitemap(root, res):
    r = read_bytes(root, 'docs/robots.txt', res, 'robots')
    if r is not None:
        res.add('robots', *robots_verdict(r.decode('utf-8', 'replace')))
    s = read_bytes(root, 'docs/sitemap.xml', res, 'sitemap')
    if s is not None:
        try:
            import xml.etree.ElementTree as ET  # stdlib; parses only, no entity expansion of external resources
            tree = ET.fromstring(s.decode('utf-8'))
            locs = [e.text.strip() for e in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if e.text]
        except Exception as e:
            res.add('sitemap', 'UNKNOWN', 'not parsable (%s)' % type(e).__name__)
            return
        expected = sorted(PAGES.values())
        if sorted(locs) == expected:
            res.add('sitemap', 'PASS', '%d urls match the page allow-list' % len(locs))
        else:
            res.add('sitemap', 'FAIL', 'sitemap urls %s != pages %s' % (sorted(locs), expected))


def robots_verdict(txt):
    """Evaluate the wildcard group (User-agent: *) against the two page paths with the standard longest-match rule.
    Supported: User-agent / Allow / Disallow / Sitemap, comments, blanks. Any other directive, or a pattern using '*' or '$',
    → UNKNOWN (unsupported syntax; not evaluated, never PASS). Other user-agent groups are not evaluated."""
    pages = [SITE_PATH, SITE_PATH + 'report.html']
    groups, cur, sitemap_ok, saw_ua = [], None, False, False
    for raw in txt.splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        if ':' not in line:
            return 'UNKNOWN', 'unsupported robots line: %r' % raw[:40]
        key, _, val = line.partition(':')
        key, val = key.strip().lower(), val.strip()
        if key == 'sitemap':
            sitemap_ok = sitemap_ok or val == SITE + 'sitemap.xml'
        elif key == 'user-agent':
            saw_ua = True
            if cur is None or cur['rules']:
                cur = {'agents': [], 'rules': []}
                groups.append(cur)
            cur['agents'].append(val.lower())
        elif key in ('allow', 'disallow'):
            if cur is None:
                return 'UNKNOWN', 'rule before any User-agent'
            if '*' in val or '$' in val:
                return 'UNKNOWN', 'wildcard/anchor patterns not evaluated: %s' % val[:40]
            cur['rules'].append((key, val))
        else:
            return 'UNKNOWN', 'unsupported directive: %s' % key[:30]
    if not saw_ua:
        return 'FAIL', 'no User-agent group'
    if not sitemap_ok:
        return 'FAIL', 'Sitemap line missing or not %ssitemap.xml' % SITE
    wild = [g for g in groups if '*' in g['agents']]
    if not wild:
        return 'UNKNOWN', 'no wildcard (User-agent: *) group to evaluate'
    if len(wild) > 1:
        return 'UNKNOWN', 'multiple wildcard groups (%d); merge semantics not evaluated' % len(wild)
    rules = wild[0]['rules']
    for path in pages:
        best, allowed = -1, True
        for kind, val in rules:
            if val == '' and kind == 'disallow':
                continue  # empty Disallow = allow all
            if path.startswith(val) and len(val) > best:
                best, allowed = len(val), (kind == 'allow')
            elif path.startswith(val) and len(val) == best and kind == 'allow':
                allowed = True  # tie → allow
        if not allowed:
            return 'FAIL', 'wildcard group disallows %s' % path
    return 'PASS', 'wildcard group allows both pages; Sitemap line present'


def check_package(root, res):
    data = read_bytes(root, 'package.json', res, 'package')
    if data is None:
        return
    try:
        d = json.loads(data.decode('utf-8'))
    except Exception as e:
        res.add('package', 'UNKNOWN', 'not parsable (%s)' % type(e).__name__)
        return
    if not isinstance(d, dict):
        res.add('package', 'FAIL', 'package.json is not an object')
        return
    problems = []
    for k in ('name', 'version', 'description', 'homepage', 'license'):
        v = d.get(k)
        if type(v) is not str or not v.strip():
            problems.append('%s must be a non-empty string' % k)
    import re
    if type(d.get('name')) is str and not re.fullmatch(r'(@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*', d['name']):
        problems.append('name is not a valid package name')
    if type(d.get('version')) is str and not re.fullmatch(r'\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?', d['version']):
        problems.append('version is not x.y.z')
    if d.get('homepage') != SITE:
        problems.append('homepage %r != %s' % (d.get('homepage'), SITE))
    repo = d.get('repository')
    url = repo if type(repo) is str else (repo.get('url') if isinstance(repo, dict) else None)
    if type(url) is not str or url not in REPO_URLS or (isinstance(repo, dict) and repo.get('type') not in (None, 'git')):
        problems.append('repository does not identify %s' % REPO_URLS[0])
    if problems:
        res.add('package', 'FAIL', '; '.join(problems))
    else:
        res.add('package', 'PASS', 'name/version/description/homepage/license typed and non-empty; repository identifies the public repo')


def run(root):
    res = Result()
    root = os.path.realpath(root)
    if not os.path.isdir(root):
        res.add('root', 'UNKNOWN', 'root is not a directory')
        return res.summary()
    for rel in ALLOWED_FILES:
        full = safe_path(root, rel)
        if full is None:
            res.add('exists:%s' % rel, 'FAIL', 'path escapes root')
        elif os.path.isfile(full):
            res.add('exists:%s' % rel, 'PASS', 'present')
        else:
            res.add('exists:%s' % rel, 'UNKNOWN', 'absent')
    for rel, canonical in PAGES.items():
        p = check_page(root, rel, canonical, res)
        if p is not None:
            check_links(root, rel, p.hrefs + p.srcs + [p.links.get('icon', ''), p.links.get('stylesheet', '')], res)
    for rel in LINK_SOURCES:
        if rel.endswith('.md'):
            data = read_bytes(root, rel, res, 'md:%s' % rel)
            if data is not None:
                check_links(root, rel, markdown_links(data), res)
    check_robots_sitemap(root, res)
    check_package(root, res)
    return res.summary()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', default='.', help='repository root (default: current directory)')
    ap.add_argument('--json', action='store_true', help='print the full JSON report')
    a = ap.parse_args(argv)
    out = run(a.root)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print('%s  PASS=%d FAIL=%d UNKNOWN=%d SKIP=%d' % (out['status'], *[out['counts'][k] for k in ('PASS', 'FAIL', 'UNKNOWN', 'SKIP')]))
        for c in out['checks']:
            if c['status'] in ('FAIL', 'UNKNOWN'):
                print('  %-8s %s — %s' % (c['status'], c['id'], c['detail']))
    return {'PASS': 0, 'FAIL': 1, 'UNKNOWN': 2}[out['status']]


if __name__ == '__main__':
    sys.exit(main())
