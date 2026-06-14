# Checklist de implementação — Romântica

> Estágio atual: apenas **análise léxica** (tokenização). Parser e geração de código C ainda não existem.
> "Implementado" aqui significa: o tokenizador reconhece a palavra e emite o `TokenType` correto.
> Palavras-chave definidas em `verso/token/constants.py`.

---

## Estágios do compilador

- [x] Análise léxica (tokenização)
- [ ] Análise sintática (parser)
- [ ] Análise semântica
- [ ] Geração de código C

---

## Tipos de dados

| Tipo C   | Palavras-chave Romântica          | Tokenizado |
|----------|-----------------------------------|:---:|
| `int`    | `rocha`                           | ✅ |
| `float`  | `bruma`, `cinza`                  | ✅ |
| `float`  | `névoa`                           | ✅ |
| `char`   | `traço`, `suspiro`                | ✅ |
| `char[]` | `verso`, `canção`, `prosa`        | ✅ |
| `bool`   | `dilema`, `dualidade`             | ✅ |
| `fixed`  | indefinido                        | ❌ (indefinido na spec) |

---

## Estruturas de dados

- [x] Array — `coro`, `compêndio`
- [ ] Matrizes / Multidimensionais
- [ ] Structs
- [ ] Dicionários / Hash-tables / Maps

---

## Declaração e atribuição

### Palavras-chave de atribuição (`DECLARATION`)

| Palavra     | Tokenizado |
|-------------|:---:|
| `é`, `és`   | ✅ |
| `seja`      | ✅ |
| `guarda`, `encerra`  | ✅ |
| `guarde`, `encerre`  | ✅ |

### Padrões sintáticos (requerem parser)

- [ ] `<var> é <tipo>.` → `tipo var;`
- [ ] `Que <var> seja <tipo>.` → `tipo var;`
- [ ] `Que <var> seja <tipo> <adjunto>.` → `tipo var = valor;`
- [ ] Declaração de array com tamanho
- [ ] Declaração de array com valores iniciais

---

## Literais

- [x] Inteiro — ex: `42`
- [x] Float — ex: `3.14`
- [x] Booleano — `verdadeiro`, `falso`
- [ ] String literal — `"..."` (aspas causam erro léxico)
- [ ] Char literal — `'...'` (aspas causam erro léxico)
- [ ] Apelidos booleanos — ex: `glórias`, `vitórias` (true); `derrotas`, `tristezas` (false)

---

## Operadores aritméticos

> Nenhum operador aritmético está definido na spec ainda (marcados como `???` no rascunho).

- [ ] Soma
- [ ] Subtração
- [ ] Multiplicação
- [ ] Divisão
- [ ] Resto

---

## Operadores de comparação

| Operador       | Palavras-chave              | Tokenizado |
|----------------|-----------------------------|:---:|
| `==`           | `igual`, `como`             | ✅ |
| `!=`           | `diferente`, `distinto`     | ✅ |
| `>`            | `maior`, `além`             | ✅ |
| `<`            | `menor`, `aquém`            | ✅ |
| `<=`           | `até`                       | ✅ |
| `>=`           | `me`                        | ✅ |

---

## Operadores lógicos

| Operador | Palavra-chave | Tokenizado |
|----------|---------------|:---:|
| `&&`     | `e`           | ✅ |
| `\|\|`   | `ou`          | ✅ |
| `!`      | `não`         | ✅ |

---

## Fluxo de controle

| Estrutura  | Romântica                      | Tokenizado |
|------------|--------------------------------|:---:|
| `if`       | `se`                           | ✅ |
| `else`     | `senão`                        | ✅ |
| `else if`  | `porém, se` / `porém, caso`   | ❌ (multi-palavra, não suportado) |
| `while`    | `enquanto`                     | ✅ |
| `for`      | `sendo`                        | ✅ |
| (bloco `if`/`while`) | `então`            | ✅ |
| `}`        | `.` (ponto final)              | ✅ |

---

## Desvios de fluxo

| Instrução  | Palavras-chave                           | Tokenizado |
|------------|------------------------------------------|:---:|
| `return`   | `retorne`, `volte`, `devolva`, `entregue`| ✅ |
| `break`    | `desista`, `finde`                       | ✅ |
| `continue` | `avance`, `prossiga`                     | ✅ |

---

## Saída

| Instrução | Romântica              | Tokenizado |
|-----------|------------------------|:---:|
| `print`   | `gritarei`             | ❌ |
| `print`   | `digo que`             | ❌ (multi-palavra) |

---

## Funções

- [ ] Definição de função
- [ ] Chamada de função
- [ ] Parâmetros e retorno

---

## Outros

- [x] Comentários — `#`
- [x] Reticências — `...` (`ELLIPSE`)
- [ ] Pronomes — `Este`, `Ela`, etc. como alias de variável (na spec como "provavelmente não vai dar tempo")
