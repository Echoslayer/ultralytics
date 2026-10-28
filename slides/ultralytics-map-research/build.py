"""Build the deck's evidence index; run from the repository root with Python 3.8+."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

BASE = Path('slides/ultralytics-map/resources/ultralytics-map')


def git(*args):
    return subprocess.check_output(['git', *args])


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


snapshot = load(BASE / 'codecov-snapshot.json')
sha = snapshot['commit']
head = git('rev-parse', 'HEAD').decode().strip()
reports = {f['name']: f for f in snapshot['files']}
audits = {}
crosscheck_path = BASE / 'coverage-crosscheck.json'
crosschecks = load(crosscheck_path)['findings'] if crosscheck_path.exists() else []
for path in sorted(BASE.glob('audit-*.json')):
    for row in load(path):
        assert row['path'] not in audits, row['path']
        audits[row['path']] = row

files = []
tracked = git('ls-files', 'ultralytics').decode().splitlines()
for path in sorted(p for p in tracked if p.endswith('.py')):
    raw = Path(path).read_bytes()
    code = raw.decode('utf-8-sig')
    tree = ast.parse(code)
    symbols = []

    def visit(node, prefix=''):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                symbols.append({'name': name, 'line': child.lineno, 'start': min([child.lineno] + [d.lineno for d in child.decorator_list]), 'end': child.end_lineno,
                                'kind': 'class' if isinstance(child, ast.ClassDef) else 'function'})
                visit(child, name + '.')
            else:
                visit(child, prefix)

    visit(tree)
    report = reports.get(path)
    row = {'path': path, 'module': path.split('/')[1], 'symbolsIndex': symbols,
           'contentHash': hashlib.sha256(raw).hexdigest(), 'review': audits.get(path),
           'crosscheck': [x for x in crosschecks if x['path'] == path]}
    if report:
        old = git('show', sha + ':' + path).replace(b'\r\n', b'\n')
        row['sameSource'] = raw.replace(b'\r\n', b'\n') == old
        totals = report['totals']
        lines = report['line_coverage']
        assert len(lines) == totals['lines'], path
        assert sum(v == 0 for _, v in lines) == totals['hits'], path
        assert sum(v == 1 for _, v in lines) == totals['misses'], path
        row['coverage'] = {k: totals[k] for k in ('lines', 'hits', 'misses', 'partials')}
        row['coverage']['percent'] = totals['coverage']
        missing = [line for line, value in lines if value == 1]
        row['coverage']['missingLines'] = missing
        for finding in row['crosscheck']:
            assert row['sameSource'] and set(finding['missingLines']).issubset(missing), finding
        gaps = {}
        if row['sameSource']:
            for line in missing:
                candidates = [s for s in symbols if s['start'] <= line <= s['end']]
                # The smallest enclosing declaration prevents nested methods being counted twice.
                symbol = min(candidates, key=lambda s: s['end'] - s['line']) if candidates else None
                name = symbol['name'] if symbol else '<module>'
                gap = gaps.setdefault(name, {'name': name, 'line': symbol['line'] if symbol else 1, 'lines': []})
                gap['lines'].append(line)
        row['gaps'] = sorted(gaps.values(), key=lambda g: (-len(g['lines']), g['line']))
        source_lines = code.splitlines()
        for gap in row['gaps']:
            gap['examples'] = [{'line': line, 'code': source_lines[line - 1].strip()} for line in gap['lines'][:3]]
    else:
        row['coverage'] = None
        row['sameSource'] = None
        row['gaps'] = []
    if row['review']:
        review = row['review']
        for key in ('changeDifficulty', 'testDifficulty'):
            assert review[key] in ('容易', '中等', '困難'), (path, key)
        assert review['testIdeas'] and review['rationale'] and review['symbols'], path
        for test in review['existingTests']:
            parts = test.split('::')
            assert Path(parts[0]).is_file(), (path, test)
            if len(parts) > 1:
                test_tree = ast.parse(Path(parts[0]).read_text(encoding='utf-8-sig'))
                names = {n.name for n in ast.walk(test_tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
                assert all(part.split('[')[0] in names for part in parts[1:]), (path, test)
        review['starts'] = []
        for name in review['symbols']:
            matches = [s for s in symbols if s['name'] == name or s['name'].endswith('.' + name)]
            assert matches or name in code, (path, name)
            if matches:
                review['starts'].append(matches[0])
    files.append(row)

assert set(audits).issubset({f['path'] for f in files})
assert set(reports).issubset({f['path'] for f in files})
assert len(reports) == snapshot['totals']['files']
assert sum(f['totals']['lines'] for f in reports.values()) == snapshot['totals']['lines']
assert sum(f['totals']['hits'] for f in reports.values()) == snapshot['totals']['hits']
data = {'head': head, 'coverageCommit': sha, 'observedAt': snapshot['observedAt'],
        'source': snapshot['source'], 'totals': snapshot['totals'], 'files': files}
(BASE / 'test-map-data.js').write_text('window.testAtlas = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print(json.dumps({'files': len(files), 'reviewed': len(audits), 'coverage': len(reports),
                  'matchingSource': sum(f['sameSource'] is True for f in files)}, ensure_ascii=False))
