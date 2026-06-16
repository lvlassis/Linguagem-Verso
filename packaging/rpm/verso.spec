Name:           verso
Version:        0.1.0
Release:        1%{?dist}
Summary:        Compilador da linguagem Romântica para C

# TODO: adicionar arquivo LICENSE ao repositório e atualizar este campo
License:        Proprietary
URL:            https://github.com/lvlassis/Linguagem-Verso
Source0:        %{url}/archive/v%{version}.tar.gz#/Linguagem-Verso-%{version}.tar.gz

BuildRequires:  python3
BuildRequires:  python3-pyinstaller
Recommends:     gcc

%description
verso é o compilador da linguagem Romântica (também chamada Linguagem Poética),
onde programas se parecem com poesia romântica em português.
O compilador transpila código .vs para C.

%prep
%autosetup -n Linguagem-Verso-%{version}

%build
pyinstaller --onefile --name verso --distpath dist/ --clean main.py

%install
install -Dpm 755 dist/verso %{buildroot}%{_bindir}/verso
install -Dpm 644 docs/sintaxe.md \
    %{buildroot}%{_docdir}/%{name}/sintaxe.md

%files
%{_bindir}/verso
%doc %{_docdir}/%{name}/

%changelog
* Mon Jun 16 2026 Vinicius Lassis <lvlassis.2@gmail.com> - 0.1.0-1
- Empacotamento inicial
