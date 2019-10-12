# philiprehberger-diff-strings

[![Tests](https://github.com/philiprehberger/py-diff-strings/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-diff-strings/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-diff-strings.svg)](https://pypi.org/project/philiprehberger-diff-strings/)
[![License](https://img.shields.io/github/license/philiprehberger/py-diff-strings)](LICENSE)

Show character-level differences between two strings with colored terminal output.

## Install

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
| `diff(a, b, *, color=True)` | Character-level diff as a string |
| `char_diff(a, b)` | Programmatic diff returning a list of Change objects |
| `word_diff(a, b, *, color=True)` | Word-level diff as a string |
| `similarity(a, b)` | Similarity ratio between 0.0 and 1.0 |
| `assert_strings_equal(expected, actual, *, msg="")` | Assert equal or raise with diff |

### Change types

| Type | Fields | Description |
|------|--------|-------------|
| `Match(text)` | `text: str` | Unchanged text |
| `Insert(text)` | `text: str` | Text added in the second string |
| `Delete(text)` | `text: str` | Text removed from the first string |
| `Replace(old, new)` | `old: str`, `new: str` | Text that changed between strings |

## License

MIT
