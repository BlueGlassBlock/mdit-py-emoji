from typing import Dict, List, Pattern

from markdown_it.common.utils import arrayReplaceAt as array_replace_at
from markdown_it.common.utils import isPunctChar as is_punctuation
from markdown_it.common.utils import isWhiteSpace as is_whitespace
from markdown_it.rules_core.state_core import StateCore
from markdown_it.token import Token


def is_letter(ch: str) -> bool:
    return not (is_punctuation(ch) or is_whitespace(ord(ch)))


class EmojiRuleFunctor:
    def __init__(
        self,
        defs: Dict[str, str],
        shortcuts: Dict[str, str],
        pattern: Pattern[str],
    ) -> None:
        self.defs = defs
        self.shortcuts = shortcuts
        self.pattern = pattern

    def replace(self, content: str) -> List[Token]:
        tokens: List[Token] = []
        last_pos: int = 0

        for match in self.pattern.finditer(content):
            st, ed = match.span()
            string = content[st:ed]
            emoji_name = self.shortcuts.get(string, string[1:-1])
            if st > 0 and is_letter(content[st - 1]):
                continue
            if ed < len(content) and is_letter(content[ed]):
                continue
            if st > last_pos:
                tokens.append(Token("text", "", 0, content=content[last_pos:st]))
            tokens.append(
                Token(
                    "emoji",
                    "",
                    0,
                    markup=emoji_name,
                    content=self.defs[emoji_name],
                )
            )
            last_pos = ed
        if last_pos < len(content):
            tokens.append(Token("text", "", 0, content=content[last_pos:]))
        return tokens

    def __call__(self, state: StateCore):
        autolink_lv = 0
        for tok in state.tokens:
            if tok.type != "inline":
                continue
            tokens = tok.children or []
            # We scan from the end, to keep position when new tags added.
            # Use reversed logic in links start/end match
            for i in reversed(range(len(tokens))):
                token = tokens[i]
                if token.type in ("link_open", "link_close") and token.info == "auto":
                    autolink_lv -= token.nesting
                if (
                    token.type == "text"
                    and autolink_lv == 0
                    and self.pattern.search(token.content) is not None
                ):
                    # replace current node
                    tok.children = tokens = array_replace_at(
                        tokens, i, self.replace(token.content)
                    )
