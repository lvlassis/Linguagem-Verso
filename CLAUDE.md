# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Verso** is a compiler/transpiler for **Romântica** ("Linguagem Poética"), a programming language where programs look like Portuguese Romantic-era poetry. The compiler targets C code output. Final project for a Formal Languages (Linguagens Formais) course at UFG.

Full language spec: `docs/Linguagem Poética.md`. Syntax examples: `docs/rascunho_objetivo_2.md`.

## Running

```bash
python main.py
```

`main.py` is currently a scratch test file that calls `tokenize()` on a hardcoded string and prints the result.

## Architecture

All compiler logic lives in `verso/tokens.py`. The only implemented stage is lexical analysis (`tokenize()`).

### Tokenization pipeline

`tokenize(program: str) -> list[Token]` uses a single-pass regex tokenizer:

1. A master regex matches token kinds in priority order: `COMMENT`, `IDENTIFIER`, `NUMBER`, `ELLIPSE`, `DOT`, `WHITESPACE`, `MISMATCH`, `EOL`.
2. `WHITESPACE` and `COMMENT` tokens are discarded.
3. `IDENTIFIER` tokens are looked up in `verso/palavras_reservadas.json`; if found, the JSON value becomes the token kind; otherwise the word is classified as `VARIABLE`.
4. The result is a flat `list[Token]`.

### Reserved words

`verso/palavras_reservadas.json` is the single source of truth for keyword-to-`TokenType` mapping. To add a new keyword, add it here — no code changes needed unless the `TokenType` member itself is new.

> **Known bugs in `palavras_reservadas.json`:** Several entries use `PRIMITIVA_TYPE` (not `PRIMITIVE_TYPE`) and `DIFERENT` (not `DIFFERENT`), and the `"me "` key has a trailing space. These will cause `KeyError` at runtime for those tokens.

## Token types

**`TokenType`** — add new members here when introducing new syntax:

| Member | Meaning |
|---|---|
| `VARIABLE` | Identifier not found in reserved words |
| `DOT` | `.` — statement/block terminator |
| `ELLIPSE` | `...` — used in float value phrases |
| `NUMBER` | Integer or float literal (`\d+(\.\d+)?`) |
| `DECL_ATTR` | `é`, `és`, `seja` — assignment/declaration keyword |
| `PRIMITIVE_TYPE` | Type keyword (`rocha`, `bruma`) |
| `DATA_STRUCT` | Array/collection keyword (`coro`, `compêndio`) |
| `IF` / `ELSE` / `WHILE` / `FOR` | Control flow |
| `EQUAL` / `DIFFERENT` / `GREATER_THAN` / `LESS_THAN` / `GREATER_OR_EQUAL` / `LESS_OR_EQUAL` | Comparison operators |
| `AND` / `OR` / `NOT` | Logical operators |
| `BOOLEAN_TRUE` / `BOOLEAN_FALSE` | Boolean literals |
| `ARTICLE` | `a`, `o`, `um`, `uma` — grammar filler |
| `PREPOSITION` | `de`, `da` — grammar filler |
| `CONJUNCTION` | `que` — grammar filler |
| `EOL` | End of line sentinel |

> **Note:** `STRUCT` and `DATA_STRUCT` are both defined in the enum with the same value `'DATA_STRUCT'` — this is a duplicate.

## Language Semantics

**Types** (keyword → C type):
- `Rocha` → `int`
- `Bruma`, `Névoa`, `Cinza` → `float`
- `Traço`, `Suspiro` → `char`
- `Verso`, `Canção`, `Prosa` → `char[]`
- `Dilema`, `Dualidade` → `bool`

**Declaration patterns:**
- `<var> é <type>.` → `type var;`
- `Que <var> seja <type>.` → `type var;`
- `Que <var> seja <type> <adjective>.` → `type var = value;`

**Assignment aliases for `é`:** `és`, `guarda`, `encerra`, `seja`, `guarde`, `encerre`

**Control flow:** `se … então` → `if` | `porém, se|caso` → `else if` | `senão` → `else` | `enquanto` → `while` | `para` → `for` | `.` → `}`

**Output:** `gritarei` / `digo que` → `print`

**Arrays:** `Coro`, `Compêndio` — element type indicated by adjective (e.g. `rochoso` for int)
