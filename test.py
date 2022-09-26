import textwrap

from markdown_it import MarkdownIt

from mdit_py_emoji import emoji_plugin


def test_emoji_default():

    md = MarkdownIt().use(emoji_plugin)

    assert md.renderInline(":star: mdit-py-emoji! :star:")
    assert (
        md.renderInline("Is shortcut supported too :/? :white_check_mark:")
        == "Is shortcut supported too 😕? ✅"
    )


def test_replace_shortcut():
    md = MarkdownIt().use(
        emoji_plugin,
        shortcuts={
            "arrow_up": [":up_arrow:", ":up_arr:"],
            "arrow_down": [":down_arrow:", ":down_arr:"],
        },
    )  # Some tricks like `false = False`
    assert md.renderInline(":down_arr: Go Down :down_arrow:") == "⬇️ Go Down ⬇️"


def test_ignoring():
    md = MarkdownIt().use(emoji_plugin)
    assert md.renderInline("https://github.com/") == "https://github.com/"
    assert (
        md.renderInline("colon separated values(:starry:milk:)")
        == "colon separated values(:starry:milk:)"
    )
    assert md.render("`:arrow_up:` :arrow_up:") == "<p><code>:arrow_up:</code> ⬆️</p>\n"
    assert (
        md.render(
            textwrap.dedent(
                """\
                <http://www.example.org/foo:joy:bar> :joy:

                [bar](http://www.example.org/foo:joy:)
                """
            )
        )
        == textwrap.dedent(
            """\
            <p><a href="http://www.example.org/foo:joy:bar">http://www.example.org/foo:joy:bar</a> 😂</p>
            <p><a href="http://www.example.org/foo:joy:">bar</a></p>
            """
        )
    )
