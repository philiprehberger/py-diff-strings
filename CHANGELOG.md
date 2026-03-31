# Changelog

## 0.2.3 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template
## 0.2.2

- Trim keywords to match pyproject template guide

## 0.2.1- Add pytest and mypy tool configuration to pyproject.toml

## 0.2.0 (2026-03-16)

- Add `line_diff()` for unified-style line-level diffs with configurable context
- Add `diff_summary()` returning a `DiffSummary` with counts and similarity
- Add `html_diff()` for HTML-formatted diffs with `<ins>`/`<del>` tags
- Add `patch()` to reconstruct strings from a change list
- Add configurable color support to `diff()` and `word_diff()`

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- Character-level diff with ANSI colored output
- Word-level diff for comparing text by words
- Programmatic `char_diff` returning typed Change dataclasses
- Similarity ratio via `difflib.SequenceMatcher`
- `assert_strings_equal` helper for test assertions
