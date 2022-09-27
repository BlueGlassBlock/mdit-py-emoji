import re
from typing import TYPE_CHECKING, Dict, List, Pattern, Union

from markdown_it import MarkdownIt
from markdown_it.token import Token

from mdit_py_emoji.rule import EmojiRuleFunctor

if TYPE_CHECKING:  # pragma: no cover
    from typing import TypedDict

    class _Opts(TypedDict):
        defs: Dict[str, str]
        shortcuts: Dict[str, str]
        pattern: Pattern[str]


def _normalize_opts(
    defs: Union[Dict[str, str], None] = None,
    shortcuts: Union[Dict[str, List[str]], None] = None,
) -> "_Opts":
    if defs is None:
        from . import data

        defs = data.mapping
    if shortcuts is None:
        from . import data

        shortcuts = data.shortcuts
    shortcut_map: Dict[str, str] = {}
    for target, aliases in shortcuts.items():
        for alias in aliases:
            shortcut_map[alias] = target
    replacing: List[str] = [f":{name}:" for name in defs] + list(shortcut_map)
    pattern = re.compile(
        "|".join(re.escape(i) for i in replacing) if replacing else "^$"
    )
    return {"defs": defs, "shortcuts": shortcut_map, "pattern": pattern}


def emoji_plugin(
    md: MarkdownIt,
    defs: Union[Dict[str, str], None] = None,
    shortcuts: Union[Dict[str, List[str]], None] = None,
):
    def render(r, tokens: List[Token], idx: int, *_):
        return tokens[idx].content

    md.add_render_rule("emoji", render)
    md.core.ruler.after(
        "linkify", "emoji", EmojiRuleFunctor(**_normalize_opts(defs, shortcuts))
    )
