.PHONY: setup dev test build rpm clear

setup:
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt

dev:
	python main.py $(FILE)

test:
	python -m unittest discover -s . -p 'test_*.py' -v

build:
	.venv/bin/pyinstaller --onefile --name verso --distpath dist/ --clean main.py
	@echo "[verso] binário gerado em dist/verso"

rpm:
	@mkdir -p ~/rpmbuild/{SPECS,SOURCES,BUILD,RPMS,SRPMS}
	@VER=$$(grep '^Version:' packaging/rpm/verso.spec | awk '{print $$2}'); \
	 git archive --format=tar.gz --prefix=Linguagem-Verso-$$VER/ HEAD \
	     -o ~/rpmbuild/SOURCES/Linguagem-Verso-$$VER.tar.gz
	cp packaging/rpm/verso.spec ~/rpmbuild/SPECS/verso.spec
	rpmbuild -ba ~/rpmbuild/SPECS/verso.spec
	@echo "[verso] RPM gerado em ~/rpmbuild/RPMS/"

clear:
	rm bin/*.c
