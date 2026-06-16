# Verso

Compilador da linguagem Romântica

Este repositório contém o projeto final da disciplina de Linguagens Formais ministrada pelo professor Maurício em 2026-1.

## Sintaxe

Veja a sintaxe em [Sintaxe](docs/sintaxe.md)

## Compilando um exemplo

Dado o arquivo `exemplos/ode_ao_tempo.vs`:

```
# Ode ao Tempo

que o ano seja rocha sol ardente.

que o fluxo seja bruma breve... leve.

chama é dilema.
chama é verdadeiro.

se ano maior que 3 então
digo que o tempo acelera.
senão digo que o tempo repousa.

enquanto chama
se ano igual 5 então desista.
digo que o coração pulsa.
chama é falso.
```

Execute o compilador:

```bash
python main.py exemplos/ode_ao_tempo.vs
# ou: make dev FILE=exemplos/ode_ao_tempo.vs
```

O código C é gerado no diretório atual (`ode_ao_tempo.c`):

```c
#include <stdio.h>
#include <stdbool.h>

int main() {
    int ano = 37;
    float fluxo = 5.4;
    bool chama;
    chama = 1;
    if (ano > 3) {
        printf("o tempo acelera\n");
    } else {
        printf("o tempo repousa\n");
    }
    while (chama) {
        if (ano == 5) {
            break;
        }
    }
    printf("o coração pulsa\n");
    chama = 0;
    return 0;
}
```

Compile e execute com GCC:

```bash
gcc ode_ao_tempo.c -o ode_ao_tempo
./ode_ao_tempo
```

Para inspecionar o C gerado sem criar arquivo, use `--preview`:

```bash
python main.py --preview exemplos/ode_ao_tempo.vs
```

## Installing from source

### Arch Linux

Requer `base-devel` e `git`.

```bash
cd packaging/arch
makepkg -si
```

O pacote instala o binário `verso` em `/usr/bin/verso`.

### RPM (Fedora / RHEL)

Requer `rpm-build` e `python3-pyinstaller`.

```bash
sudo dnf install rpm-build python3-pyinstaller
make rpm
```

O `.rpm` gerado fica em `~/rpmbuild/RPMS/`. Para instalar:

```bash
sudo dnf install ~/rpmbuild/RPMS/$(uname -m)/verso-*.rpm
```

## Autores

Projeto realizado pelos alunos:

- Jonathas dos Santos
- Lucas Vinícius de Lima Assis

do curso de Engenharia de Computação da UFG.


