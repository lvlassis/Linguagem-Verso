# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Verso** is a compiler/transpiler for **Romântica** ("Linguagem Poética"), a programming language where programs look like Portuguese Romantic-era poetry. The compiler targets C code output. Final project for a Formal Languages (Linguagens Formais) course at UFG.

Full language spec: `docs/Linguagem Poética.md`. Syntax examples: `docs/rascunho_objetivo_2.md`. Implementation checklist: `docs/checklist.md`.

## Commands

```bash
# Compile a .vs source file to C (output goes to bin/<name>.c)
python main.py exemplos/ode_ao_tempo.vs
make dev FILE=exemplos/ode_ao_tempo.vs   # equivalent via makefile

# Run all tests (verbose)
python -m unittest discover
make test

# Run a single test module
python -m unittest verso/token/test_tokenization.py
python -m unittest verso/semantica/test_semantica.py
python -m unittest verso/codigo/test_codigo.py

# Run a single test case
python -m unittest verso.semantica.test_semantica.TestValidacaoTiposNaoNumericos.test_char_atribuicao_com_variavel_incompativel

# Remove compiled .c files from bin/
make clear
```

## Architecture

The compiler is a four-stage pipeline. Each stage lives in its own subpackage under `verso/`:

```
verso/token/      — Lexical analysis
verso/sintaxe/    — Syntax analysis (AST)
verso/semantica/  — Semantic analysis
verso/codigo/     — C code generation
verso/ast.py      — Re-export shim (critical — see below)
```

`main.py` is the compiler entrypoint: reads a `.vs` file, runs the full pipeline, and writes C output to `bin/<name>.c`.

### `verso/ast.py` — the identity shim

**This file is critical for `match/case` to work correctly.** All stages import AST node classes from `verso.ast`, not directly from `verso.sintaxe.constants`. This guarantees a single class identity, so `match node: case IfBody():` works regardless of which module performed the import. Never import node dataclasses from `verso.sintaxe.constants` in semantic or codegen code — always use `verso.ast`.

### Stage 1 — Lexical analysis (`verso/token/`)

`tokenize(program: str) -> list[Token]` in `tokenizer.py`:

1. Builds a master regex from `PALAVRAS_RESERVADAS` keys (which are regex patterns — e.g. `r"digo\s+que"` matches multi-word keywords as a single token).
2. Priority order: `COMMENT`, `RESERVED`, `IDENTIFIER`, `NUMBER`, `ELLIPSE`, `DOT`, `WHITESPACE`, `MISMATCH`, `EOL`.
3. `WHITESPACE` and `COMMENT` tokens are discarded; `MISMATCH` raises `RuntimeError`.
4. Input is lowercased before matching, so tokenization is case-insensitive.

`PALAVRAS_RESERVADAS` in `constants.py` is the single source of truth for keyword → `Token` mapping. Each value is a `Token(type, value?)` where `value` is a `PrimitiveType` enum member for type keywords, `'1'`/`'0'` for boolean literals, or `None` otherwise. To add a keyword, add an entry here; add a new `TokenType` member only if introducing a new syntactic category.

### Stage 2 — Syntax analysis (`verso/sintaxe/`)

`Parser` in `parser.py` consumes a `list[Token]` and produces a `Program` (an AST).

Key parser concepts:
- `SKIP_LIST` = `[ARTICLE, PREPOSITION, CONJUNCTION]` — grammar filler tokens skipped during parsing.
- `EOI_TOKEN_LIST` = `[EOL, DOT, COMMA]` — end-of-instruction sentinels. `.` also closes blocks.
- `TYPE_TOKEN_LIST` = `[PRIMITIVE_TYPE, DATA_STRUCT]` — triggers variable declaration path.
- `_last_eoi: TokenType | None` — instance variable set by statement parsers (`parse_decl_attr`, `parse_print`, `parse_break`, etc.) when they consume their closing token. Block parsers (`parse_while`, `parse_if`) check `_last_eoi == DOT` to detect when an inner statement already consumed the block's closing `.` — this is the key mechanism that prevents `go_to_SNI()` from eating closing dots.

**Block closing rule:** `.` on its own or attached to a statement both close the innermost open block. `go_to_SNI()` consumes all EOI tokens including `.` — **do not call it after `THEN`/`ELSE`/while-condition inside block parsers**, or it will eat the closing dot of an empty block.

**Expression parsing:** Three functions form a two-level precedence hierarchy:
- `parse_expression()` handles comparisons (`EQUAL`, `DIFFERENT`, `GREATER_*`, `LESS_*`) and additive ops (`SUM`, `SUB`), delegating each operand to `parse_term()`.
- `parse_term()` handles multiplicative ops (`MULT`, `DIV`, `REST`), delegating to `parse_factor()`.
- `parse_factor()` returns `Literal(value=['varname', ...])` for consecutive `VARIABLE` tokens (a list of string token values) and `Literal(value='42')` for `NUMBER` (a string).
- `NOT expr` is handled directly in `parse_expression()` and returns `MonadicOperation`.
- `BinaryOperation.operator` is a **Token object** (not a string); access the C operator via `_C_OPERATORS[node.operator.type]`.

AST node dataclasses live in `verso/sintaxe/constants.py` and are re-exported via `verso/ast.py`:
- `Program(instructions: list[Statement])`
- `VariableDeclaration(name, varType: PrimitiveType, value: Expression)` — for `int`/`float` types, semantic analysis replaces `value` in-place with `[evaluated_number]`
- `Attribution(name, value: Expression)` — same in-place replacement for poetic numeric expressions
- `IfBody(condition: Expression, positive_instructions, negative_instructions)`
- `WhileLoop(condition: list[Token], body: list[Statement])` — condition is raw token list
- `BinaryOperation(firstOperand, operator: Token, SecondOperand)` — `operator` is a Token at runtime despite the `str` type annotation
- `MonadicOperation(operand, operator: str | None)` — `None` for NOT
- `Literal(value: str | list)` — list for variables, str for numbers
- `Variable(name: str)` — defined but not currently emitted by the parser; `parse_factor()` produces `Literal(value=[names...])` for variable references instead
- `PrintStatement(args: list)`, `BreakStatement()`, `ContinueStatement()`, `ReturnStatement(value: list)`

### Stage 3 — Semantic analysis (`verso/semantica/`)

`SemanticAnalyzer.analyse(tree) -> (Program, list[SemanticError] | None)`:
- Visitor pattern with `match/case` in `_visit(node)`
- Scope stack `_scopes: list[dict[str, PrimitiveType]]` — `_push_scope`/`_pop_scope` for `if`/`while` bodies
- `_validar_valor(varname, declared_type, value)` — shared helper that checks undeclared words and type compatibility for all types
- For `int`/`float` declarations and attributions: evaluates poetic expressions via `_avaliar_expressao_int`/`_avaliar_expressao_float` (counts letters per word → digits; `...` separates integer/decimal parts for float)
- Returns `(tree, None)` on success; `(tree, [SemanticError(...)])` on failure. Errors are accumulated, not thrown.

### Stage 4 — Code generation (`verso/codigo/`)

`GeradorCodigo.gerar(program) -> str`:
- Visitor pattern with `match/case` in `_visitar(node)` 
- `_gerar_expressao(node: Expression)` — recursively generates C from `BinaryOperation`/`MonadicOperation`/`Literal`; uses `_C_OPERATORS` dict (combines `_C_COMPARISONS` and `_C_ARITHMETIC`) keyed on `node.operator.type`
- `_gerar_condicao(tokens: list[Token])` — legacy flat-token condition generator used by `WhileLoop` (while loop condition is stored as raw tokens, not an Expression tree)
- `_C_BOOLEANS` maps `BOOLEAN_TRUE → 'true'`, `BOOLEAN_FALSE → 'false'` for conditions; boolean token *values* are `'1'`/`'0'` for use in assignments

## Token types

| Member | Meaning |
|---|---|
| `VARIABLE` | Identifier not in reserved words |
| `DOT` | `.` — statement/block terminator |
| `COMMA` | `,` — EOI variant |
| `ELLIPSE` | `...` — separates integer/decimal parts in float poetic expressions |
| `NUMBER` | Integer or float literal |
| `DECL_ATTR` | `é`, `és`, `seja`, `guarda/e`, `encerra/e` — assignment/declaration |
| `PRIMITIVE_TYPE` | Type keyword; `Token.value` holds `PrimitiveType` enum member |
| `DATA_STRUCT` | Array keyword (`coro`, `compêndio`) |
| `IF` / `THEN` / `ELSE` / `WHILE` / `FOR` | Control flow |
| `EQUAL` / `DIFFERENT` / `GREATER_THAN` / `LESS_THAN` / `GREATER_OR_EQUAL` / `LESS_OR_EQUAL` | Comparison operators |
| `AND` / `OR` / `NOT` | Logical operators |
| `SUM` / `SUB` / `MULT` / `DIV` / `REST` | Arithmetic operators (`acrescido de`, `privado/despido de`, `ecoado por`, `partilhado por`, `restando de`) — all are multi-word regex patterns |
| `BOOLEAN_TRUE` / `BOOLEAN_FALSE` | Boolean literals; `Token.value` is `'1'` / `'0'` |
| `ARTICLE` | `a`, `o`, `um`, `uma` — grammar filler |
| `PREPOSITION` | `de`, `da` — grammar filler |
| `CONJUNCTION` | `que` — grammar filler |
| `CONTINUE` / `BREAK` / `RETURN` | Jump statements |
| `PRINT` | `grito`, `gritarei`, `digo que` |
| `EOL` | End of line sentinel |

## Language semantics

**Types** (keyword → C type):
- `rocha` → `int`
- `bruma`, `névoa`, `cinza` → `float`
- `traço`, `suspiro` → `char`
- `verso`, `canção`, `prosa` → `char*`
- `dilema`, `dualidade` → `bool`

**Poetic numeric expressions** — words in an int/float declaration or assignment that are neither declared variables nor numeric literals are evaluated by letter count: each word's length becomes a digit. E.g. `"dura"(4) "demais"(6)` → `46`. For float, `...` (ELLIPSE token) separates integer digits from decimal digits.

**Control flow:**
- `se … então` → `if` | `senão`/`porém` → `else` | `enquanto` → `while` | `.` → closes block
- Arithmetic operators are parsed via `parse_expression()` everywhere — in `se...então` conditions, declarations, and attributions. For `int`/`float` variables, semantic analysis intercepts the `Literal` node and evaluates poetic letter-count expressions; for other types it passes through.
- `WhileLoop.condition` stores raw tokens; `IfBody.condition` stores an `Expression` tree from `parse_expression()`.
