# philiprehberger-diff-strings

[![Tests](https://github.com/philiprehberger/py-diff-strings/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-diff-strings/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-diff-strings.svg)](https://pypi.org/project/philiprehberger-diff-strings/)
[![License](https://img.shields.io/github/license/philiprehberger/py-diff-strings)](LICENSE)

Show character-level differences between two strings with colored terminal output.

## Installation

```bash
pip install philiprehberger-diff-strings
```

## Usage

```python
from philiprehberger_diff_strings import diff

print(diff("hello world", "hello there"))
```

### Character-level diff

```python
from philiprehberger_diff_strings import diff

# Colored output (default)
print(diff("the cat sat", "the bat sat"))

# Plain text output
print(diff("the cat sat", "the bat sat", color=False))
```

### Programmatic diff

```python
from philiprehberger_diff_strings import char_diff

changes = char_diff("abc", "adc")
# [Match(text='a'), Replace(old='b', new='d'), Match(text='c')]
```

### Word-level diff

```python
from philiprehberger_diff_strings import word_diff

print(word_diff("the quick brown fox", "the slow brown dog", color=False))
```

### Line-level diff

```python
from philiprehberger_diff_strings import line_diff

a = "line one\nline two\nline three"
b = "line one\nline 2\nline three"
print(line_diff(a, b, color=False))
# Shows unified-diff style output with +/- markers

# Control context lines shown around changes
print(line_diff(a, b, context=1))
```

### Diff summary

```python
from philiprehberger_diff_strings import diff_summary

summary = diff_summary("hello world", "hello there")
print(summary.additions)   # number of insertions
print(summary.deletions)   # number of deletions
print(summary.changes)     # number of replacements
print(summary.similarity)  # similarity ratio (0.0 to 1.0)
```

### HTML diff

```python
from philiprehberger_diff_strings import html_diff

result = html_diff("the cat", "the bat")
# 'the <del>c</del><ins>b</ins>at'
```

### Custom colors

```python
from philiprehberger_diff_strings import diff, word_diff

# Use custom ANSI colors (red, green, yellow, blue, magenta, cyan)
print(diff("abc", "adc", insert_color="cyan", delete_color="magenta", replace_color="blue"))
print(word_diff("old text", "new text", insert_color="blue", replace_color="cyan"))
```

### Patch (reconstruct from changes)

```python
from philiprehberger_diff_strings import char_diff, patch

changes = char_diff("hello world", "hello there")
result = patch("hello world", changes)
assert result == "hello there"
```

### Similarity ratio

```python
from philiprehberger_diff_strings import similarity

score = similarity("hello", "hallo")  # 0.8
```

### Test assertions

```python
from philiprehberger_diff_strings import assert_strings_equal

assert_strings_equal("expected output", "expected output")  # passes
assert_strings_equal("expected", "actual")  # raises AssertionError with diff
```

## API

| Function | Description |
|----------|-------------|
| `diff(a, b, *, color=True, insert_color="green", delete_color="red", replace_color="yellow")` | Character-level diff as a string |
| `char_diff(a, b)` | Programmatic diff returning a list of Change objects |
| `word_diff(a, b, *, color=True, insert_color="green", delete_color="red", replace_color="yellow")` | Word-level diff as a string |
| `line_diff(a, b, *, color=True, context=3)` | Unified-style line-level diff |
| `diff_summary(a, b)` | Summary with addition/deletion/change counts and similarity |
| `html_diff(a, b)` | Character-level diff as HTML with `<ins>`/`<del>` tags |
| `patch(original, changes)` | Reconstruct the modified string from a change list |
| `similarity(a, b)` | Similarity ratio between 0.0 and 1.0 |
| `assert_strings_equal(expected, actual, *, msg="")` | Assert equal or raise with diff |

### Change types

| Type | Fields | Description |
|------|--------|-------------|
| `Match(text)` | `text: str` | Unchanged text |
| `Insert(text)` | `text: str` | Text added in the second string |
| `Delete(text)` | `text: str` | Text removed from the first string |
| `Replace(old, new)` | `old: str`, `new: str` | Text that changed between strings |

### DiffSummary

| Field | Type | Description |
|-------|------|-------------|
| `additions` | `int` | Number of insertion operations |
| `deletions` | `int` | Number of deletion operations |
| `changes` | `int` | Number of replacement operations |
| `similarity` | `float` | Similarity ratio between 0.0 and 1.0 |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
