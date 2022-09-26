<div align=center>

# mdit-py-emoji
> Emoji plugin for markdown-it-py. Ported from https://github.com/markdown-it/markdown-it-emoji
</div>

## Usage

Use it just like other plugins!

```python
from markdown_it import MarkdownIt
from mdit_py_emoji import emoji_plugin

md = MarkdownIt().use(emoji_plugin)

print(md.renderInline(":star: mdit-py-emoji! :star:"))
# ⭐ mdit-py-emoji! ⭐
print(md.renderInline("Is shortcut supported too :/? :white_check_mark:"))
# Is shortcut supported too 😕? ✅
```

## Customization

Pass `defs` and `shortcuts` and that's it!

```python
from markdown_it import MarkdownIt
from mdit_py_emoji import emoji_plugin

md = MarkdownIt().use(
    emoji_plugin,
    shortcuts={
        "arrow_up": [":up_arrow:", ":up_arr:"],
        "arrow_down": [":down_arrow:", ":down_arr:"],
    },
)  # Some tricks like `false = False`
print(md.renderInline(":down_arr: Go Down :down_arrow:"))
# ⬇️ Go Down ⬇️
```

Wondering about the defaults? Check [data.py](./mdit_py_emoji/data.py) !

Note: twemoji shortcuts are enabled by default. pass `shortcuts={}`  to disable it.

## License

This project is licensed under [MIT License](./LICENSE).