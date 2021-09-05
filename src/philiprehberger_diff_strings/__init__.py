"""Show character-level differences between two strings with colored terminal output."""

from __future__ import annotations

import difflib
import html as _html_mod
from dataclasses import dataclass
from difflib import SequenceMatcher

__all__ = [
    "Change",
    "Match",
    "Insert",
    "Delete",
    "Replace",
    "DiffSummary",
    "diff",
    "char_diff",
    "word_diff",
    "line_diff",
    "diff_summary",
    "html_diff",
    "patch",
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


@dataclass(frozen=True, slots=True)
class DiffSummary:
    """Summary statistics for a diff between two strings."""

    additions: int
    deletions: int
    changes: int
    similarity: float


# ANSI color codes
_ANSI_COLORS: dict[str, str] = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}
_RED = "\033[31m"
_GREEN = "\033[32m"
_STRIKETHROUGH = "\033[9m"
_RESET = "\033[0m"


def _ansi(color: str) -> str:
    """Return the ANSI escape code for a named color."""
    return _ANSI_COLORS.get(color, _ANSI_COLORS["red"])


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


def _format_change(
    change: Change,
    *,
    color: bool,
    insert_color: str = "green",
    delete_color: str = "red",
    replace_color: str = "yellow",
) -> str:
    """Format a single Change as a string, optionally with ANSI colors."""
    if isinstance(change, Match):
        return change.text
    if isinstance(change, Insert):
        text = f"+{change.text}"
        if color:
            return f"{_ansi(insert_color)}{text}{_RESET}"
        return f"[{text}]"
    if isinstance(change, Delete):
        text = f"-{change.text}"
        if color:
            return f"{_ansi(delete_color)}{_STRIKETHROUGH}{text}{_RESET}"
        return f"[{text}]"
    if isinstance(change, Replace):
        old = f"-{change.old}"
        new = f"+{change.new}"
        if color:
            return (
                f"{_ansi(replace_color)}{_STRIKETHROUGH}{old}{_RESET}"
                f"{_ansi(replace_color)}{new}{_RESET}"
            )
        return f"[{old}|{new}]"
    return ""


def diff(
    a: str,
    b: str,
    *,
    color: bool = True,
    insert_color: str = "green",
    delete_color: str = "red",
    replace_color: str = "yellow",
) -> str:
    """Show character-level differences between two strings.

    Args:
        a: The original string.
        b: The modified string.
        color: Whether to use ANSI color codes in the output.
        insert_color: Color name for insertions (default ``"green"``).
        delete_color: Color name for deletions (default ``"red"``).
        replace_color: Color name for replacements (default ``"yellow"``).

    Returns:
        A string showing the differences with inline annotations.
    """
    changes = char_diff(a, b)
    return "".join(
        _format_change(
            c,
            color=color,
            insert_color=insert_color,
            delete_color=delete_color,
            replace_color=replace_color,
        )
        for c in changes
    )


def word_diff(
    a: str,
    b: str,
    *,
    color: bool = True,
    insert_color: str = "green",
    delete_color: str = "red",
    replace_color: str = "yellow",
) -> str:
    """Show word-level differences between two strings.

    Splits both strings on whitespace and compares word by word.

    Args:
        a: The original string.
        b: The modified string.
        color: Whether to use ANSI color codes in the output.
        insert_color: Color name for insertions (default ``"green"``).
        delete_color: Color name for deletions (default ``"red"``).
        replace_color: Color name for replacements (default ``"yellow"``).

    Returns:
        A string showing word-level differences with inline annotations.
    """
    words_a = a.split()
    words_b = b.split()
    matcher = SequenceMatcher(None, words_a, words_b)
    parts: list[str] = []

    ins = _ansi(insert_color)
    dl = _ansi(delete_color)
    rp = _ansi(replace_color)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            parts.append(" ".join(words_a[i1:i2]))
        elif tag == "insert":
            text = " ".join(words_b[j1:j2])
            if color:
                parts.append(f"{ins}+{text}{_RESET}")
            else:
                parts.append(f"[+{text}]")
        elif tag == "delete":
            text = " ".join(words_a[i1:i2])
            if color:
                parts.append(f"{dl}{_STRIKETHROUGH}-{text}{_RESET}")
            else:
                parts.append(f"[-{text}]")
        elif tag == "replace":
            old = " ".join(words_a[i1:i2])
            new = " ".join(words_b[j1:j2])
            if color:
                parts.append(
                    f"{rp}{_STRIKETHROUGH}-{old}{_RESET}"
                    f" {rp}+{new}{_RESET}"
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


def line_diff(a: str, b: str, *, color: bool = True, context: int = 3) -> str:
    """Line-level diff in unified diff style.

    Shows additions with ``+``, deletions with ``-``, and context lines
    with a leading space.

    Args:
        a: The original string.
        b: The modified string.
        color: Whether to use ANSI color codes in the output.
        context: Number of surrounding context lines to show.

    Returns:
        A formatted unified-diff string.
    """
    lines_a = a.splitlines(keepends=True)
    lines_b = b.splitlines(keepends=True)
    result = difflib.unified_diff(lines_a, lines_b, n=context, lineterm="")
    parts: list[str] = []
    for line in result:
        # Strip trailing newline for consistent output
        clean = line.rstrip("\n")
        if color:
            if clean.startswith("+++") or clean.startswith("---"):
                parts.append(clean)
            elif clean.startswith("+"):
                parts.append(f"{_GREEN}{clean}{_RESET}")
            elif clean.startswith("-"):
                parts.append(f"{_RED}{clean}{_RESET}")
            elif clean.startswith("@@"):
                parts.append(f"{_ansi('cyan')}{clean}{_RESET}")
            else:
                parts.append(clean)
        else:
            parts.append(clean)
    return "\n".join(parts)


def diff_summary(a: str, b: str) -> DiffSummary:
    """Get a quick overview of differences without full rendering.

    Args:
        a: The original string.
        b: The modified string.

    Returns:
        A ``DiffSummary`` with counts of additions, deletions,
        replacements, and a similarity ratio.
    """
    changes = char_diff(a, b)
    additions = sum(1 for c in changes if isinstance(c, Insert))
    deletions = sum(1 for c in changes if isinstance(c, Delete))
    replacements = sum(1 for c in changes if isinstance(c, Replace))
    ratio = similarity(a, b)
    return DiffSummary(
        additions=additions,
        deletions=deletions,
        changes=replacements,
        similarity=ratio,
    )


def html_diff(a: str, b: str) -> str:
    """Character-level diff as HTML with ``<ins>`` and ``<del>`` tags.

    All text content is HTML-escaped.

    Args:
        a: The original string.
        b: The modified string.

    Returns:
        An HTML string with insertions wrapped in ``<ins>`` and
        deletions wrapped in ``<del>`` tags.
    """
    changes = char_diff(a, b)
    parts: list[str] = []
    for change in changes:
        if isinstance(change, Match):
            parts.append(_html_mod.escape(change.text))
        elif isinstance(change, Insert):
            parts.append(f"<ins>{_html_mod.escape(change.text)}</ins>")
        elif isinstance(change, Delete):
            parts.append(f"<del>{_html_mod.escape(change.text)}</del>")
        elif isinstance(change, Replace):
            parts.append(f"<del>{_html_mod.escape(change.old)}</del>")
            parts.append(f"<ins>{_html_mod.escape(change.new)}</ins>")
    return "".join(parts)


def patch(original: str, changes: list[Change]) -> str:
    """Reconstruct the modified string from a change list.

    Applies the given changes to produce the result string:
    ``Match`` text is kept, ``Insert`` text is added,
    ``Delete`` text is skipped, and ``Replace`` uses the new text.

    Args:
        original: The original string (unused directly, but provided
            for context).
        changes: A list of ``Change`` objects as returned by
            ``char_diff``.

    Returns:
        The reconstructed modified string.
    """
    parts: list[str] = []
    for change in changes:
        if isinstance(change, Match):
            parts.append(change.text)
        elif isinstance(change, Insert):
            parts.append(change.text)
        elif isinstance(change, Delete):
            pass  # skip deleted text
        elif isinstance(change, Replace):
            parts.append(change.new)
    return "".join(parts)


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
