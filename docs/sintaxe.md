# Romântica — Referência de Sintaxe

Romântica (também chamada de *Linguagem Poética* ou *Verso*) é uma linguagem de programação cujos programas se parecem com poesia em português. O compilador transpila para C.

---

## Características gerais

- **Case-insensitive** — `Amor`, `AMOR` e `amor` são equivalentes.
- **Comentários** — linha iniciada com `#` é ignorada até o fim da linha.
- **Terminadores de instrução** — `.` (ponto), `,` (vírgula) ou quebra de linha encerram uma instrução. O ponto é também o fechador de blocos.
- **Palavras de preenchimento** — artigos (`a`, `o`, `um`, `uma`), preposições (`de`, `da`) e a conjunção `que` são ignorados pelo parser na maioria dos contextos, permitindo que frases soem como português natural.

```
# Isto é um comentário
que o amor seja rocha.   # palavras "que", "o" são ignoradas
```

---

## Tipos primitivos

| Keyword(s)                    | Tipo C   | Descrição                          |
|-------------------------------|----------|------------------------------------|
| `rocha`                       | `int`    | Inteiro                            |
| `bruma` · `névoa` · `cinza`   | `float`  | Ponto flutuante                    |
| `traço` · `suspiro`           | `char`   | Caractere                          |
| `verso` · `canção` · `prosa`  | `char*`  | String (ponteiro de char)          |
| `dilema` · `dualidade`        | `bool`   | Booleano                           |

---

## Declaração de variáveis

**Forma básica:**
```
<variável> é <tipo>.
```

**Com artigos (opcionais):**
```
<variável> é <artigo> <tipo>.
que <artigo> <variável> seja <artigo> <tipo>.
```

**Aliases de `é` / `seja`:** `és`, `guarda`, `encerra`, `guarde`, `encerre`

**Exemplos:**
```
amor é rocha.              # int amor;
paz é bruma.               # float paz;
alma é suspiro.            # char alma;
canto é verso.             # char* canto;
duvida é dilema.           # bool duvida;

que o fluxo seja névoa.    # float fluxo;
que a vida seja um verso.  # char* vida;
```

### Declaração com valor inicial

O valor vem após o tipo na mesma linha, antes do terminador.

```
amor é rocha 42.           # int amor = 42;
paz é bruma 3.14.          # float paz = 3.14;
viver é verdadeiro.        # bool viver = true;   (VARIÁVEL=atrib. direta)
```

---

## Expressões poéticas numéricas

Para variáveis `int` e `float`, palavras que não são variáveis declaradas nem literais numéricos são avaliadas pelo **número de letras**: cada palavra vira um dígito.

```
amor é rocha dura demais.
# "dura"=4, "demais"=6  →  int amor = 46;

paz é rocha firme leve.
# "firme"=5, "leve"=4  →  int paz = 54;
```

Para `float`, o token `...` (reticências) separa a parte inteira da decimal:

```
fluxo é bruma breve... leve.
# "breve"=5 (inteiro), "leve"=4 (decimal)  →  float fluxo = 5.4;

poesia é névoa passageira... evanescente e etérea.
# "passageira"=10 (inteiro), "evanescente"=11, "etérea"=6 (decimal)
# →  float poesia = 10.116;
```

---

## Atribuição

Mesma sintaxe da declaração, mas sem tipo — o parser deduz que é uma atribuição.

```
amor é paz.       # amor = paz;
amor é 42.        # amor = 42;
amor é 3.14.      # amor = 3.14;
amor é verdadeiro. # amor = true;
amor é falso.      # amor = false;
```

Expressões poéticas também funcionam na atribuição (para variáveis numéricas):

```
amor é rocha.
amor é dura demais.    # amor = 46;
```

---

## Operadores

### Aritméticos

| Keyword(s)                                      | Operador C |
|-------------------------------------------------|------------|
| `acrescido de` · `acrescida de` · `acresce`     | `+`        |
| `privado de` · `despido de`                     | `-`        |
| `ecoado por`                                    | `*`        |
| `partilhado por`                                | `/`        |
| `restando de`                                   | `%`        |

```
resultado é amor acrescido de paz.    # resultado = amor + paz;
resto é dez restando de três.         # resto = dez % três;
```

### Comparação

| Keyword(s)                          | Operador C |
|-------------------------------------|------------|
| `igual` · `igual a` · `como` · `for` | `==`       |
| `diferente` · `diferente de`        | `!=`       |
| `distinto` · `distinto de`          | `!=`       |
| `maior` · `maior que`               | `>`        |
| `além de`                           | `>`        |
| `menor` · `menor que`               | `<`        |
| `aquém de`                          | `<`        |
| `até`                               | `<=`       |
| `ao menos` · `me`                   | `>=`       |

### Lógicos

| Keyword | Operador C |
|---------|------------|
| `e`     | `&&`       |
| `ou`    | `\|\|`     |
| `não`   | `!`        |

```
se amor igual paz e vida maior 0 então   # if (amor == paz && vida > 0)
se não amor for forte então              # if (!(amor == forte))
```

---

## Controle de fluxo

### `se` / `então` / `senão`

```
se <condição> então
<instrução>
<instrução>
senão
<instrução>.
```

- O bloco `se` abre após `então` e fecha no `.` da última instrução ou em `.` sozinho numa linha.
- `senão` também aceita `porém` como alias.
- Bloco vazio: `.` sozinho na linha seguinte.

**Exemplos:**
```
se amor igual paz então
grito amor.

se amor maior 10 então
grito grande.
senão
grito pequeno.

se amor igual paz então
.
```

### `enquanto`

```
enquanto <condição>
<instrução>
<instrução>.
```

A condição vai da keyword `enquanto` até o fim da linha. O bloco fecha no `.` da última instrução ou em `.` sozinho.

```
enquanto amor diferente 0
amor é amor privado de 1.

enquanto verdadeiro
grito loop.
```

### Booleanos literais

| Keyword      | Valor C |
|--------------|---------|
| `verdadeiro` | `true`  |
| `falso`      | `false` |

```
enquanto verdadeiro
desista.
```

---

## Desvios de fluxo

| Keyword(s)                           | Comando C  |
|--------------------------------------|------------|
| `desista` · `finde`                  | `break`    |
| `avance` · `prossiga`                | `continue` |
| `retorne` · `volte` · `devolva` · `entregue` | `return`   |

```
enquanto verdadeiro
se amor igual 0 então desista.
avance.
```

```
retorne amor.   # return amor;
volte.          # return;
```

---

## Saída — `print`

```
grito <expressão>.
gritarei <expressão>.
digo que <expressão>.
grito.                   # printf("\n");  — linha vazia
```

A expressão é impressa como texto literal (palavras separadas por espaço) seguida de `\n`.

```
grito amor.              # printf("amor\n");
digo que meu coração.   # printf("meu coração\n");
gritarei.               # printf("\n");
```

---

## Entrada — `scan`

```
escuto <variável>.
escute <variável>.
ouço <variável>.
ouça <variável>.
```

Artigos entre a keyword e a variável são ignorados.

Gera `scanf("%s", &<variável>)`.

```
escuto amor.           # scanf("%s", &amor);
escute o nome.         # scanf("%s", &nome);
ouço a confissão.      # scanf("%s", &confissão);
```

---

## Arrays

### Keywords de tipo (adjetivos)

| Adjetivo(s)                       | Tipo C   |
|-----------------------------------|----------|
| `rochoso` · `rochosa`             | `int`    |
| `enevoado` · `enevoada`           | `float`  |
| `cinzento` · `cinzenta`           | `float`  |
| `traçado` · `traçada`             | `char`   |
| `suspirado` · `suspirada`         | `char`   |
| `versejado` · `versejada`         | `char*`  |
| `prosaico` · `prosaica`           | `char*`  |
| `dúbio` · `dúbia`                 | `bool`   |

### Keywords de estrutura

`compêndio` · `conjunto` · `coro`

### Sintaxe

**Array com valores (modo `com`):**
```
<var> é <artigo> <struct> <tipo_adj> com <v1>, <v2>, ..., <vN>.
```

Os valores são palavras cujo comprimento (em letras) vira o elemento do array. Literais numéricos também são aceitos diretamente.

```
vida é um compêndio rochoso com amor, dor, sofrimento.
# amor=4, dor=3, sofrimento=10  →  int vida[] = {4, 3, 10};

notas é um compêndio rochoso com 4, 3, 10.
# →  int notas[] = {4, 3, 10};
```

**Array com tamanho (modo `de`):**
```
<var> é <artigo> <struct> <tipo_adj> de <tamanho>.
```

O tamanho pode ser uma palavra (comprimento em letras) ou um literal numérico.

```
rascunho é um compêndio traçado de amor.
# amor=4  →  char rascunho[4];

poemas é um compêndio versejado de saudade.
# saudade=7  →  char* poemas[7];

arr é um conjunto rochoso de 5.
# →  int arr[5];
```

**Array vazio (sem `com` nem `de`):**
```
letras é um compêndio traçado.
# →  char letras[];
```

---

## Exemplo completo

```
# Almanaque de Sentimentos

# int almanaque[] = {7, 6, 7, 5}
que o almanaque seja um compêndio rochoso com firmeza, leveza, saudade, ainda.

# float paleta[] = {5, 4}
que a paleta seja um compêndio enevoado com breve, leve.

# char rascunho[4]
que o rascunho seja um compêndio traçado de amor.

# char* cancioneiro[7]
que o cancioneiro seja um compêndio versejado de saudade.

# int soma = firmeza + leveza → variáveis (não avaliadas poeticamente)
que o total seja rocha.
total é almanaque acrescido de paleta.

# loop com desvio
enquanto total maior 0
se total igual 1 então desista.
digo que o total diminui.
total é total privado de 1.

# entrada e saída
que o canto seja verso.
digo que revela teu canto.
escuto o canto.
digo que o canto ecoou.
```

---

## Resumo das palavras reservadas

| Categoria          | Palavras                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------|
| Declaração/Atrib.  | `é` `és` `seja` `guarda` `encerra` `guarde` `encerre`                                     |
| Tipos              | `rocha` `bruma` `névoa` `cinza` `traço` `suspiro` `verso` `canção` `prosa` `dilema` `dualidade` |
| Arrays (struct)    | `compêndio` `conjunto` `coro`                                                              |
| Arrays (tipo adj.) | `rochoso/a` `enevoado/a` `cinzento/a` `traçado/a` `suspirado/a` `versejado/a` `prosaico/a` `dúbio/a` |
| Array valores      | `com`                                                                                      |
| Controle           | `se` `então` `senão` `porém` `enquanto`                                                   |
| Desvios            | `desista` `finde` `avance` `prossiga` `retorne` `volte` `devolva` `entregue`              |
| Booleanos          | `verdadeiro` `falso`                                                                       |
| Comparação         | `igual` `como` `for` `diferente` `distinto` `maior` `menor` `além de` `aquém de` `até` `ao menos` `me` |
| Lógicos            | `e` `ou` `não`                                                                             |
| Aritmética         | `acrescido de` `acrescida de` `acresce` `privado de` `despido de` `ecoado por` `partilhado por` `restando de` |
| Saída              | `grito` `gritarei` `digo que`                                                              |
| Entrada            | `escuto` `escute` `ouço` `ouça`                                                            |
| Preenchimento      | `a` `o` `um` `uma` `de` `da` `que`                                                        |
