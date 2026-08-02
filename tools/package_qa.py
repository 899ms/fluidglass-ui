"""Package QA for the Fluid Glass UI.

Validates that the skill package is complete and that its canonical visual
core has not drifted. Four groups of checks are performed:

1. ``missing``          - every required file is present.
2. ``forbidden_hits``   - no internal / downstream-specific tokens leaked into
                          the package (blacklist is configurable, see below).
3. ``canonical_checks`` - the shader, CSS and reference config still expose the
                          canonical material features (FBM, domain warp,
                          reveal, plumes, card geometry, chart default off...).
4. ``hash_checks``      - sha256 and byte size of the canonical core files
                          match ``CANONICAL_CORE_HASHES.json``.

The report is printed to stdout and written to ``PACKAGE_QA.json`` at the
repository root. Exit code is 0 when ``passed`` is true, 1 otherwise.

Usage:
    python tools/package_qa.py                  # run all checks
    python tools/package_qa.py --update-hashes  # regenerate the hash manifest
    python tools/package_qa.py --help

The forbidden-token blacklist can be overridden with an optional, untracked
``tools/qa-forbidden.json`` file::

    {
      "tokens":   ["SomeInternalName"],
      "patterns": ["regex-with-\\\\d-escapes"]
    }
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HASH_MANIFEST = 'CANONICAL_CORE_HASHES.json'
REPORT_FILE = 'PACKAGE_QA.json'
FORBIDDEN_CONFIG = 'tools/qa-forbidden.json'

REQUIRED = [
    'README.md',
    'SKILL.md',
    'MASTER_PROMPT.md',
    'QUICK_START_PROMPT.md',
    'DESIGN_SYSTEM.md',
    'COMPONENT_API.md',
    'CONFIG_SCHEMA.json',
    'REFERENCE_CONFIG.json',
    'ACCEPTANCE_CHECKLIST.md',
    'CHANGELOG.md',
    'CANONICAL_CORE_HASHES.json',
    'LICENSE',
    'manifest.json',
    'references/canonical-demo.html',
    'references/canonical-demo-single-file.html',
    'references/canonical-vertex-shader.glsl',
    'references/canonical-fragment-shader.glsl',
    'references/fluid-glass-material.css',
    'references/fluid-glass-engine.js',
    'references/canonical-reference.png',
    'references/visual-regression-spec.md',
]

# Files whose bytes define the shared visual identity of every downstream
# project. Any change here must be mirrored into the hash manifest.
CANONICAL_CORE_FILES = [
    'references/canonical-vertex-shader.glsl',
    'references/canonical-fragment-shader.glsl',
    'references/fluid-glass-material.css',
    'references/fluid-glass-engine.js',
    'references/canonical-demo-single-file.html',
    'references/canonical-reference.png',
]

# Manifest entries kept for backwards compatibility with older packages.
# They are tolerated (skipped) instead of reported as a failure.
OBSOLETE_CORE_FILES = {
    'references/reference-config.json',
}

# Generic leakage detection only: hardcoded downstream business keys such as
# data-fluid-card="<business-name>" instead of the neutral card-<n> form.
# Project-specific tokens belong in the untracked tools/qa-forbidden.json.
DEFAULT_FORBIDDEN_PATTERNS = [
    r'data-fluid-card\s*=\s*"(?!card-\d)[^"]*"',
    r"data-fluid-card\s*=\s*'(?!card-\d)[^']*'",
]
DEFAULT_FORBIDDEN_TOKENS = []

# Never scanned for forbidden tokens: binary assets, generated output and the
# QA tooling itself (which necessarily contains the patterns).
SCAN_EXCLUDED_NAMES = {
    REPORT_FILE,
    'canonical-reference.png',
    'package_qa.py',
    'qa-forbidden.json',
}
SCAN_EXCLUDED_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def sha256_of(path):
    """Return (sha256_hexdigest, byte_size) for the given file."""
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def read_text(relative_path):
    """Read a UTF-8 text file, returning '' when it is absent."""
    path = ROOT / relative_path
    if not path.is_file():
        return ''
    return path.read_text(encoding='utf-8')


def read_json(relative_path):
    """Read a JSON file, returning {} when it is absent or malformed."""
    text = read_text(relative_path)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def load_forbidden():
    """Load the forbidden blacklist, falling back to the generic defaults."""
    config = read_json(FORBIDDEN_CONFIG)
    tokens = config.get('tokens', DEFAULT_FORBIDDEN_TOKENS)
    patterns = config.get('patterns', DEFAULT_FORBIDDEN_PATTERNS)
    return list(tokens), list(patterns)


def check_missing():
    """Return the list of required files that do not exist."""
    return [item for item in REQUIRED if not (ROOT / item).exists()]


def scan_forbidden(tokens, patterns):
    """Scan every text file for forbidden tokens and regex patterns."""
    compiled = [re.compile(pattern) for pattern in patterns]
    hits = {}
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if path.name in SCAN_EXCLUDED_NAMES:
            continue
        relative = path.relative_to(ROOT)
        if SCAN_EXCLUDED_DIRS.intersection(relative.parts):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        found = [token for token in tokens if token in text]
        for regex in compiled:
            found.extend(match.group(0) for match in regex.finditer(text))
        if found:
            hits[relative.as_posix()] = sorted(set(found))
    return hits


def check_canonical():
    """Verify that the canonical material features are still present."""
    shader = read_text('references/canonical-fragment-shader.glsl')
    css = read_text('references/fluid-glass-material.css')
    config = read_json('REFERENCE_CONFIG.json')
    cards = config.get('cards', [])
    compact = shader.replace(' ', '')
    return {
        'has_fbm': 'float fbm' in shader,
        'has_domain_warp': 'vec2q=p+' in compact,
        'has_reveal': 'floatreveal=' in compact,
        'has_plumes': 'plume1' in shader and 'plume2' in shader,
        'has_surface_uniform': 'u_surfaceOpacity' in shader,
        'has_mouse_uniforms': all(
            name in shader
            for name in ('u_mouse', 'u_mouseVelocity', 'u_mouseMix')
        ),
        'canonical_height': '--fg-card-height: 144px' in css,
        'canonical_radius': '--fg-card-radius: 30px' in css,
        'chart_default_off': all(
            not card.get('chart', {}).get('enabled', False) for card in cards
        ),
        'generic_keys': all(
            card.get('key', '').startswith('card-') for card in cards
        ),
        'surface_default': all(
            abs(float(card.get('surface', 0)) - 0.08) < 1e-9 for card in cards
        ),
    }


def check_hashes():
    """Compare the canonical core files against the sha256 manifest."""
    manifest_path = ROOT / HASH_MANIFEST
    if not manifest_path.is_file():
        return {HASH_MANIFEST: {'ok': False, 'reason': 'manifest not found'}}

    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        return {
            HASH_MANIFEST: {'ok': False, 'reason': f'invalid JSON: {error}'}
        }

    results = {}
    for relative, expected in manifest.items():
        path = ROOT / relative
        if not path.is_file():
            if relative in OBSOLETE_CORE_FILES:
                results[relative] = {
                    'ok': True,
                    'skipped': 'obsolete manifest entry, file removed',
                }
            else:
                results[relative] = {'ok': False, 'reason': 'file not found'}
            continue

        actual_sha, actual_bytes = sha256_of(path)
        expected_sha = expected.get('sha256')
        expected_bytes = expected.get('bytes')
        if actual_sha == expected_sha and actual_bytes == expected_bytes:
            results[relative] = {'ok': True}
        else:
            results[relative] = {
                'ok': False,
                'reason': 'sha256 or byte size mismatch',
                'expected_sha256': expected_sha,
                'actual_sha256': actual_sha,
                'expected_bytes': expected_bytes,
                'actual_bytes': actual_bytes,
            }

    for relative in CANONICAL_CORE_FILES:
        if relative not in results:
            results[relative] = {'ok': False, 'reason': 'missing from manifest'}

    return results


def update_hashes():
    """Recompute the manifest for the canonical core files and save it."""
    manifest = {}
    missing = []
    for relative in CANONICAL_CORE_FILES:
        path = ROOT / relative
        if not path.is_file():
            missing.append(relative)
            continue
        digest, size = sha256_of(path)
        manifest[relative] = {'sha256': digest, 'bytes': size}

    payload = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    (ROOT / HASH_MANIFEST).write_text(payload, encoding='utf-8')

    print(f'Updated {HASH_MANIFEST} ({len(manifest)} entries):')
    for relative, entry in manifest.items():
        print(f"  {relative}\n    sha256={entry['sha256']} bytes={entry['bytes']}")
    if missing:
        print('Warning: skipped files that do not exist:')
        for relative in missing:
            print(f'  {relative}')


def run_checks():
    """Run every QA check and return the report dictionary."""
    tokens, patterns = load_forbidden()
    missing = check_missing()
    hits = scan_forbidden(tokens, patterns)
    canonical_checks = check_canonical()
    hash_checks = check_hashes()

    passed = (
        not missing
        and not hits
        and all(canonical_checks.values())
        and all(entry['ok'] for entry in hash_checks.values())
    )
    return {
        'passed': passed,
        'missing': missing,
        'forbidden_hits': hits,
        'canonical_checks': canonical_checks,
        'hash_checks': hash_checks,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='package_qa.py',
        description=(
            'Check the Fluid Glass UI package: required files, '
            'forbidden tokens, canonical material features and sha256 '
            'integrity of the canonical core files.'
        ),
    )
    parser.add_argument(
        '--update-hashes',
        action='store_true',
        help=(
            'recompute sha256 and byte size of the canonical core files, '
            f'overwrite {HASH_MANIFEST} and exit'
        ),
    )
    args = parser.parse_args(argv)

    if args.update_hashes:
        update_hashes()
        return 0

    result = run_checks()
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    (ROOT / REPORT_FILE).write_text(payload, encoding='utf-8')
    print(payload)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
