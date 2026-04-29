"""Tests for philiprehberger_diff_strings."""

from __future__ import annotations

import pytest

from philiprehberger_diff_strings import (
    Delete,
    DiffSummary,
    Insert,
    Match,
    Replace,
    assert_strings_equal,
    char_diff,
    diff,
    diff_summary,
    html_diff,
    line_diff,
    markdown_diff,
    patch,
    similarity,
    word_diff,
)


def test_char_diff_identical_returns_one_match() -> None:
    changes = char_diff("hello", "hello")
    assert changes == [Match("hello")]


def test_char_diff_simple_replace() -> None:
    changes = char_diff("cat", "bat")
    types = [type(c) for c in changes]
    assert Replace in types


def test_char_diff_insert() -> None:
    changes = char_diff("cat", "cats")
    assert Insert("s") in changes


def test_char_diff_delete() -> None:
    changes = char_diff("cats", "cat")
    assert Delete("s") in changes


def test_diff_no_color_uses_brackets() -> None:
    out = diff("cat", "bat", color=False)
    assert "[" in out


def test_diff_color_includes_ansi() -> None:
    out = diff("cat", "bat", color=True)
    assert "\033[" in out


def test_word_diff_word_boundaries() -> None:
    out = word_diff("the cat sat", "the dog sat", color=False)
    assert "[-cat|+dog]" in out or ("cat" in out and "dog" in out)


def test_line_diff_unified_format() -> None:
    out = line_diff("a\nb\nc", "a\nB\nc", color=False)
    assert "-b" in out
    assert "+B" in out


def test_diff_summary_counts() -> None:
    s = diff_summary("aaa", "abc")
    assert isinstance(s, DiffSummary)
    assert 0.0 <= s.similarity <= 1.0


def test_similarity_identical_is_one() -> None:
    assert similarity("hello", "hello") == 1.0


def test_similarity_completely_different_is_low() -> None:
    assert similarity("abc", "xyz") < 0.5


def test_html_diff_escapes_specials() -> None:
    out = html_diff("<a>", "<b>")
    assert "&lt;" in out
    assert "<a>" not in out.replace("<ins>", "").replace("</ins>", "").replace(
        "<del>", ""
    ).replace("</del>", "")


def test_patch_round_trip() -> None:
    a = "hello world"
    b = "hello brave new world"
    changes = char_diff(a, b)
    assert patch(a, changes) == b


def test_assert_strings_equal_passes() -> None:
    assert_strings_equal("hello", "hello")


def test_assert_strings_equal_raises_with_diff() -> None:
    with pytest.raises(AssertionError) as exc_info:
        assert_strings_equal("hello", "world")
    assert "Strings differ" in str(exc_info.value)


def test_markdown_diff_uses_strikethrough_for_deletions() -> None:
    out = markdown_diff("cats", "cat")
    assert "~~s~~" in out


def test_markdown_diff_uses_bold_for_insertions() -> None:
    out = markdown_diff("cat", "cats")
    assert "**s**" in out


def test_markdown_diff_keeps_unchanged_text_plain() -> None:
    out = markdown_diff("hello", "hello")
    assert out == "hello"
    assert "**" not in out
    assert "~~" not in out


def test_markdown_diff_replace_uses_both_markers() -> None:
    out = markdown_diff("cat", "bat")
    assert "~~c~~" in out
    assert "**b**" in out
    assert "at" in out


def test_markdown_diff_empty_strings() -> None:
    assert markdown_diff("", "") == ""
