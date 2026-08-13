from harness.markdown_render import render_markdown


def test_render_markdown_formats_common_syntax():
    html = render_markdown("**bold** and *italic*\n\n- one\n- two")
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<li>one</li>" in html
