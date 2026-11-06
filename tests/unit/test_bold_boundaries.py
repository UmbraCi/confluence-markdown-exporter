"""Regression coverage for strong emphasis next to punctuation and CJK text."""

# ruff: noqa: RUF001 -- Unicode punctuation is the regression input.

from types import SimpleNamespace

import pytest

from confluence_markdown_exporter.confluence import Page


@pytest.mark.parametrize("tag", ["strong", "b"])
@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("<{tag}>阶段：</{tag}>继续", "<strong>阶段：</strong>继续"),
        ("前文<{tag}>（阶段）</{tag}>后文", "前文<strong>（阶段）</strong>后文"),
        ("<{tag}>Stage:</{tag}>next", "<strong>Stage:</strong>next"),
        ("前文<{tag}>★阶段</{tag}>继续", "前文<strong>★阶段</strong>继续"),
        ("<{tag}>阶段</{tag}>继续", "**阶段**继续"),
        ("<{tag}>Bold</{tag}> text", "**Bold** text"),
        ("<{tag}>&nbsp;text&nbsp;</{tag}>", "**text**"),
        ("<{tag}></{tag}>", ""),
        ("<code><{tag}>阶段：</{tag}></code>", "`阶段：`"),
    ],
)
def test_bold_boundaries(tag: str, source: str, expected: str) -> None:
    """Preserve bold without inserting whitespace into the source text."""
    converter = Page.Converter(SimpleNamespace(html="", title="Example", id="example"))
    assert converter.convert(source.format(tag=tag)).strip() == expected
