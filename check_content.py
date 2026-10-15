"""Check lesson counts, local links, starters, and embedded Python syntax."""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    entries = json.loads((ROOT / 'course.json').read_text())
    assert len(entries) == 26
    assert len(list((ROOT / 'lessons').glob('*.md'))) == 26
    assert len(list((ROOT / 'exercises').glob('*.py'))) == 26
    for entry in entries:
        assert (ROOT / entry['file']).is_file()
        ast.parse((ROOT / entry['exercise']).read_text())
        text = (ROOT / entry['file']).read_text()
        for required in ('## The idea', '## Walk through an example', '## Your exercise', '### Why it works', '### Time and space', '## Retrieval check', '## Completion checkpoint'):
            assert required in text, (entry['file'], required)
        for code in re.findall(r'```python\n(.*?)```', text, re.S):
            ast.parse(code)
            # Definitions must execute with their documented imports.
            exec(compile(code, entry['file'], 'exec'), {})
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        for destination in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if destination.startswith(('https://', 'http://', '#')):
                continue
            local = destination.split('#')[0]
            assert (path.parent / local).exists(), (str(path.relative_to(ROOT)), destination)
    print('26 lessons, 26 starters, embedded code, and local Markdown links checked.')


if __name__ == '__main__':
    main()
