# Checklist de implementação — Romântica

> Legenda: ✅ implementado em todos os estágios relevantes | 🔶 parcialmente implementado | ❌ não implementado

---

## Estágios do compilador

| Estágio               | Status |
|-----------------------|:------:|
| Análise léxica        | ✅ |
| Análise sintática     | 🔶 |
| Análise semântica     | 🔶 |
| Geração de código C   | 🔶 |

---

## Tipos de dados

| Tipo C   | Palavras-chave Romântica     | Léxico | Sintaxe | Semântica | Codegen |
|----------|------------------------------|:------:|:-------:|:---------:|:-------:|
| `int`    | `rocha`                      | ✅ | ✅ | ✅ | ✅ |
| `float`  | `bruma`, `névoa`, `cinza`    | ✅ | ✅ | ✅ | ✅ |
| `char`   | `traço`, `suspiro`           | ✅ | ✅ | ✅ | ✅ |
| `char*`  | `verso`, `canção`, `prosa`   | ✅ | ✅ | ✅ | ✅ |
| `bool`   | `dilema`, `dualidade`        | ✅ | ✅ | ✅ | ✅ |
| `fixed`  | indefinido                   | ❌ | ❌ | ❌ | ❌ |

---

## Declaração e atribuição

| Padrão                                        | Léxico | Sintaxe | Semântica | Codegen |
|-----------------------------------------------|:------:|:-------:|:---------:|:-------:|
| `<var> é <tipo>.`                             | ✅ | ✅ | ✅ | ✅ |
| `Que <var> seja <tipo>.`                      | ✅ | ✅ | ✅ | ✅ |
| `<var> é <tipo> <expr-numérica>.`             | ✅ | ✅ | ✅ | ✅ |
| `<var> é <valor-variável>.`                   | ✅ | ✅ | ✅ | ✅ |
| `<var> é <expr-numérica>.` (atribuição)       | ✅ | ✅ | ✅ | ✅ |
| `<var> é <literal-numérico>.`                 | ✅ | ✅ | ✅ | ✅ |
| `<var> é "<string>".`                         | ❌ | ❌ | ❌ | ❌ |
| Declaração de array com tamanho               | ✅ | ❌ | ❌ | ❌ |
| Declaração de array com valores iniciais      | ✅ | ❌ | ❌ | ❌ |

---

## Literais

| Literal            | Léxico | Sintaxe | Semântica | Codegen |
|--------------------|:------:|:-------:|:---------:|:-------:|
| Inteiro (`42`)     | ✅ | ✅ | ✅ | ✅ |
| Float (`3.14`)     | ✅ | ✅ | ✅ | ✅ |
| Booleano (`verdadeiro`, `falso`) | ✅ | ✅ | ✅ | ✅ |
| String (`"..."`)   | ❌ | ❌ | ❌ | ❌ |
| Char (`'...'`)     | ❌ | ❌ | ❌ | ❌ |
| Apelidos booleanos (`glórias`, `derrotas`…) | ❌ | ❌ | ❌ | ❌ |

---

## Expressões numéricas poéticas

| Funcionalidade                               | Semântica | Codegen |
|----------------------------------------------|:---------:|:-------:|
| Avaliação por contagem de letras (int)       | ✅ | ✅ |
| Avaliação por contagem de letras (float, `...`) | ✅ | ✅ |
| Expressão em declaração                      | ✅ | ✅ |
| Expressão em atribuição                      | ✅ | ✅ |

---

## Operadores

### Comparação

| Operador | Palavras-chave          | Léxico | Codegen (condições) |
|----------|-------------------------|:------:|:-------------------:|
| `==`     | `igual`, `como`         | ✅ | ✅ |
| `!=`     | `diferente`, `distinto` | ✅ | ✅ |
| `>`      | `maior`, `além`         | ✅ | ✅ |
| `<`      | `menor`, `aquém`        | ✅ | ✅ |
| `<=`     | `até`                   | ✅ | ✅ |
| `>=`     | `me`                    | ✅ | ✅ |

### Lógicos

| Operador | Palavra-chave | Léxico | Codegen (condições) |
|----------|---------------|:------:|:-------------------:|
| `&&`     | `e`           | ✅ | ✅ |
| `\|\|`   | `ou`          | ✅ | ✅ |
| `!`      | `não`         | ✅ | ✅ |

### Aritméticos

| Operador | Palavra-chave | Léxico | Sintaxe | Semântica | Codegen |
|----------|---------------|:------:|:-------:|:---------:|:-------:|
| `+`      | `acresce`     | ✅ | 🔶 | ❌ | ✅ |
| `-`      | `deduz`       | ✅ | 🔶 | ❌ | ✅ |
| `*`      | `amplia`      | ✅ | 🔶 | ❌ | ✅ |
| `/`      | `reparte`     | ✅ | 🔶 | ❌ | ✅ |
| `%`      | `resta`       | ✅ | 🔶 | ❌ | ✅ |

> Sintaxe 🔶: operadores aritméticos são parseados como `BinaryOperation` dentro de expressões de condição (`se … então`). Não são reconhecidos em declarações nem atribuições.

---

## Fluxo de controle

| Estrutura     | Romântica                   | Léxico | Sintaxe | Semântica | Codegen |
|---------------|-----------------------------|:------:|:-------:|:---------:|:-------:|
| `if`          | `se … então`                | ✅ | ✅ | 🔶 | ✅ |
| `else`        | `senão`, `porém`            | ✅ | ✅ | 🔶 | ✅ |
| `else if`     | `porém, se` / `porém, caso` | ❌ | ❌ | ❌ | ❌ |
| `while`       | `enquanto`                  | ✅ | ✅ | ✅ | ✅ |
| `for`         | `sendo`                     | ✅ | ❌ | ❌ | ❌ |
| fechamento    | `.` (ponto final)           | ✅ | ✅ | — | — |

> `if`/`else` marcados como 🔶 em Semântica: corpo é visitado com escopo próprio, mas a condição não é verificada semanticamente (variáveis/tipos na condição não são validados).

> `for` não tem sintaxe definida na spec além da keyword `sendo`.

---

## Desvios de fluxo

| Instrução  | Palavras-chave                              | Léxico | Sintaxe | Semântica | Codegen |
|------------|---------------------------------------------|:------:|:-------:|:---------:|:-------:|
| `return`   | `retorne`, `volte`, `devolva`, `entregue`   | ✅ | ✅ | ✅ | ✅ |
| `break`    | `desista`, `finde`                          | ✅ | ✅ | ✅ | ✅ |
| `continue` | `avance`, `prossiga`                        | ✅ | ✅ | ✅ | ✅ |

---

## Saída

| Instrução | Romântica                        | Léxico | Sintaxe | Semântica | Codegen |
|-----------|----------------------------------|:------:|:-------:|:---------:|:-------:|
| `printf`  | `grito`, `gritarei`, `digo que`  | ✅ | ✅ | ✅ | ✅ |

---

## Funções

| Funcionalidade          | Status |
|-------------------------|:------:|
| Definição de função     | ❌ |
| Chamada de função       | ❌ |
| Parâmetros e retorno    | ❌ |

---

## Análise semântica — verificações

| Verificação                                     | Status |
|-------------------------------------------------|:------:|
| Tabela de símbolos (declaração)                 | ✅ |
| Re-declaração de variável                       | ✅ |
| Uso de variável não declarada (atribuição)      | ✅ |
| Compatibilidade de tipos (atribuição)           | ✅ |
| Escopo de bloco (`while`)                       | ✅ |
| Escopo de bloco (`if`/`else`)                   | ✅ |
| Verificação de variáveis/tipos na condição      | ❌ |
| Escopo de bloco (`for`)                         | ❌ |
| Inferência de tipo de expressões                | ❌ |

---

## Outros

| Funcionalidade                     | Status |
|------------------------------------|:------:|
| Comentários (`#`)                  | ✅ |
| Reticências (`...`) — float        | ✅ |
| Pronomes (`Este`, `Ela`…)          | ❌ (fora do escopo) |
