# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Verso** is a compiler/transpiler for **Romântica** ("Linguagem Poética"), a programming language where programs look like Portuguese Romantic-era poetry. The compiler targets C code output. Final project for a Formal Languages (Linguagens Formais) course at UFG.

Full language spec: `docs/Linguagem Poética.md`. Syntax examples: `docs/rascunho_objetivo_2.md`. Implementation checklist: `docs/checklist.md`.

## Commands

```bash
# Run the scratch pipeline (tokenize → parse → semantic → codegen)
python main.py

# Run lexer tests
python -m unittest verso/token/test_tokenization.py

# Run all tests
python -m unittest discover
```

## Architecture

The compiler is a four-stage pipeline. Each stage lives in its own subpackage under `verso/`:

```
verso/token/      — Lexical analysis
verso/sintaxe/    — Syntax analysis (AST)
verso/semantica/  — Semantic analysis (stub)
verso/codigo/     — C code generation (stub)
```

`main.py` is a scratch driver that wires all stages together for manual testing.

### Stage 1 — Lexical analysis (`verso/token/`)

`tokenize(program: str) -> list[Token]` in `tokenizer.py`:

1. Builds a master regex from `PALAVRAS_RESERVADAS` keys (which are regex patterns, not plain strings — e.g. `r"digo\s+que"` matches multi-word keywords as a single token).
2. Priority order: `COMMENT`, `RESERVED`, `IDENTIFIER`, `NUMBER`, `ELLIPSE`, `DOT`, `WHITESPACE`, `MISMATCH`, `EOL`.
3. `WHITESPACE` and `COMMENT` tokens are discarded; `MISMATCH` raises `RuntimeError`.
4. Input is lowercased before matching, so tokenization is case-insensitive.

`PALAVRAS_RESERVADAS` in `constants.py` is the single source of truth for keyword → `Token` mapping. Each value is a `Token(type, value?)` where `value` is a `PrimitiveType` enum member for type keywords, or `None` otherwise. To add a keyword, add an entry here; add a new `TokenType` member only if introducing a new syntactic category.

### Stage 2 — Syntax analysis (`verso/sintaxe/`)

`Parser` in `parser.py` consumes a `list[Token]` and produces `list[Statement]` (an AST).

Key parser concepts:
- `SKIP_LIST` = `[ARTICLE, PREPOSITION, CONJUNCTION]` — grammar filler tokens skipped during parsing.
- `EOI_TOKEN_LIST` = `[EOL, DOT]` — end-of-instruction sentinels (`.` closes blocks too).
- `DECL_TOKEN_LIST` = `[PRIMITIVE_TYPE, DATA_STRUCT]` — triggers variable declaration path.

Currently handles: variable declarations (`var é tipo`) and assignments (`var é valor`). `IF`/`WHILE`/`FOR` branches are stubs.

AST node dataclasses live in `constants.py`: `VariableDeclaration`, `Attribution`, `Literal`, `Variable` (all extend `Statement` or `Expression`).

### Stages 3 & 4 — Semantic analysis and code generation

Both are stubs. `SemanticAnalyzer.analyse()` returns `(tree, None)` unchanged. `GeradorCodigo.gerar_codigo()` returns an empty string.

## Token types

`TokenType` members:

| Member | Meaning |
|---|---|
| `VARIABLE` | Identifier not in reserved words |
| `DOT` | `.` — statement/block terminator (also closes `if`/`while` blocks) |
| `ELLIPSE` | `...` — used in float value phrases |
| `NUMBER` | Integer or float literal |
| `DECL_ATTR` | `é`, `és`, `seja`, `guarda/e`, `encerra/e` — assignment/declaration |
| `PRIMITIVE_TYPE` | Type keyword; `Token.value` holds the `PrimitiveType` enum member |
| `DATA_STRUCT` | Array keyword (`coro`, `compêndio`) |
| `IF` / `THEN` / `ELSE` / `WHILE` / `FOR` | Control flow |
| `EQUAL` / `DIFFERENT` / `GREATER_THAN` / `LESS_THAN` / `GREATER_OR_EQUAL` / `LESS_OR_EQUAL` | Comparison operators |
| `AND` / `OR` / `NOT` | Logical operators |
| `BOOLEAN_TRUE` / `BOOLEAN_FALSE` | Boolean literals |
| `ARTICLE` | `a`, `o`, `um`, `uma` — grammar filler |
| `PREPOSITION` | `de`, `da` — grammar filler |
| `CONJUNCTION` | `que` — grammar filler |
| `CONTINUE` / `BREAK` / `RETURN` | Jump statements |
| `PRINT` | `grito`, `gritarei`, `digo que` |
| `EOL` | End of line sentinel |

## Language Semantics

**Types** (keyword → C type):
- `rocha` → `int`
- `bruma`, `névoa`, `cinza` → `float`
- `traço`, `suspiro` → `char`
- `verso`, `canção`, `prosa` → `char[]`
- `dilema`, `dualidade` → `bool`

**Declaration patterns:**
- `<var> é <tipo>.` → `tipo var;`
- `Que <var> seja <tipo>.` → `tipo var;`
- `Que <var> seja <tipo> <adjunto>.` → `tipo var = valor;`

**Control flow:** `se … então` → `if` | `senão` / `porém` → `else` | `enquanto` → `while` | `sendo` → `for` | `.` → `}`

**Output:** `grito` / `gritarei` / `digo que` → `print`
