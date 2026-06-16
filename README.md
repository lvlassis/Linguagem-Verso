# Verso

Compilador da linguagem Romântica

Este repositório contém o projeto final da disciplina de Linguagens Formais ministrada pelo professor Maurício em 2026-1.

## Sintaxe

Veja a sintaxe em [[docs/sintaxe.md|Sintaxe]]

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


