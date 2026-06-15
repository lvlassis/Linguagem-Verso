.PHONY: setup dev test build clear

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

clear:
	rm bin/*.c
