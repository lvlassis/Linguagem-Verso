Definição de Token

```
Token:
- type
- value
```

```
Amor é Rocha forte. # int amor;
```

```
Amor {
  type: VARIABLE
  value: amor
}

é {
  type: DECL_ATTR
  value: ""
}

Rocha {
  type: PRIMITIVE_TYPE
  value: "int"
}

forte {
  type: NUMERIC_EXPRESSION
}

. {
  type: DOT
}

# int amor; {
  type: COMMENT
}
```
