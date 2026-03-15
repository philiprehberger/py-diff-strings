"""Show character-level differences between two strings with colored terminal output."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

__all__ = [
    "Change",
    "Match",
    "Insert",
    "Delete",
    "Replace",
    "diff",
    "char_diff",
    "word_diff",
    "similarity",
    "assert_strings_equal",
]


@dataclass(frozen=True, slots=True)
class Change:
    """Base class for diff changes."""


@dataclass(frozen=True, slots=True)
class Match(Change):
    """Unchanged text."""

    text: str


@dataclass(frozen=True, slots=True)
class Insert(Change):
    """Text present only in the second string."""

    text: str


@dataclass(frozen=True, slots=True)
class Delete(Change):
    """Text present only in the first string."""

    text: str


@dataclass(frozen=True, slots=True)
class Replace(Change):
    """Text that differs between the two strings."""

    old: str
    new: str


# ANSI color codes
_RED = "\033[31m"
_GREEN = "\033[32m"
_STRIKETHROUGH = "\033[9m"
_RESET = "\033[0m"


def char_diff(a: str, b: str) -> list[Change]:
    """Return a list of Change objects representing character-level differences.

    Args:
        a: The original string.
        b: The modified string.

    Returns:
        A list of Match, Insert, Delete, and Replace objects.
    """
    matcher = SequenceMatcher(None, a, b)
    changes: list[Change] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            changes.append(Match(a[i1:i2]))
        elif tag == "insert":
            changes.append(Insert(b[j1:j2]))
        elif tag == "delete":
            changes.append(Delete(a[i1:i2]))
        elif tag == "replace":
            changes.append(Replace(a[i1:i2], b[j1:j2]))

    return changes


def _format_change(change: Change, *, color: bool) -> str:
    """Format a single Change as a string, optionally with ANSI colors."""
    if isinstance(change, Match):
        return change.text
    if isinstance(change, Insert):
        text = f"+{change.text}"
        return f"{_GREEN}{text}{_RESET}" if color else f"[{text}]"
    if isinstance(change, Delete):
        text = f"-{change.text}"
        return f"{_RED}{_STRIKETHROUGH}{text}{_RESET}" if color else f"[{text}]"
    if isinstance(change, Replace):
        old = f"-{change.old}"
        new = f"+{change.new}"
        if color:
            return f"{_RED}{_STRIKETHROUGH}{old}{_RESET}{_GREEN}{new}{_RESET}"
        return f"[{old}|{new}]"
    return ""


def diff(a: str, b: str, *, color: bool = True) -> str:
    """Show character-level differences between two strings.

    Args:
        a: The original string.
        b: The modified string.
        color: Whether to use ANSI color codes in the output.

    Returns:
        A string showing the differences with inline annotations.
    """
    changes = char_diff(a, b)
    return "".join(_format_change(c, color=color) for c in changes)


def word_diff(a: str, b: str, *, color: bool = True) -> str:
    """Show word-level differences between two strings.

    Splits both strings on whitespace and compares word by word.

    Args:
        a: The original string.
        b: The modified string.
        color: Whether to use ANSI color codes in the output.

    Returns:
        A string showing word-level differences with inline annotations.
    """
    words_a = a.split()
    words_b = b.split()
    matcher = SequenceMatcher(None, words_a, words_b)
    parts: list[str] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            parts.append(" ".join(words_a[i1:i2]))
        elif tag == "insert":
            text = " ".join(words_b[j1:j2])
            if color:
                parts.append(f"{_GREEN}+{text}{_RESET}")
            else:
                parts.append(f"[+{text}]")
        elif tag == "delete":
            text = " ".join(words_a[i1:i2])
            if color:
                parts.append(f"{_RED}{_STRIKETHROUGH}-{text}{_RESET}")
            else:
                parts.append(f"[-{text}]")
        elif tag == "replace":
            old = " ".join(words_a[i1:i2])
            new = " ".join(words_b[j1:j2])
            if color:
                parts.append(
                    f"{_RED}{_STRIKETHROUGH}-{old}{_RESET}"
                    f" {_GREEN}+{new}{_RESET}"
                )
            else:
                parts.append(f"[-{old}|+{new}]")

    return " ".join(parts)


def similarity(a: str, b: str) -> float:
    """Return a similarity ratio between two strings.

    Uses ``difflib.SequenceMatcher`` to compute a value between 0.0
    (completely different) and 1.0 (identical).

    Args:
        a: The first string.
        b: The second string.

    Returns:
        A float between 0.0 and 1.0.
    """
    return SequenceMatcher(None, a, b).ratio()


def assert_strings_equal(expected: str, actual: str, *, msg: str = "") -> None:
    """Assert that two strings are equal, raising with a diff on failure.

    Args:
        expected: The expected string value.
        actual: The actual string value.
        msg: Optional message prefix for the assertion error.

    Raises:
        AssertionError: If the strings differ, includes an inline diff.
    """
    if expected == actual:
        return

    detail = diff(expected, actual, color=False)
    parts = [msg, f"Strings differ:\n{detail}"] if msg else [f"Strings differ:\n{detail}"]
    raise AssertionError(" ".join(parts))
