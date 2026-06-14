from dataclasses import dataclass

from .constants import TokenType


@dataclass
class Token:
    type: TokenType
    value: str | None = None
