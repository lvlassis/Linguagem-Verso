from verso.token.constants import TokenType

SKIP_LIST = [
            TokenType.ARTICLE,
            TokenType.PREPOSITION,
            TokenType.CONJUNCTION
        ]

EOI_TOKEN_LIST = [
            TokenType.EOL,
            TokenType.DOT
        ]

DECL_TOKEN_LIST = [
    TokenType.PRIMITIVE_TYPE,
    TokenType.DATA_STRUCT
]