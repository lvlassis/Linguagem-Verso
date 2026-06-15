.PHONY: tests dev

dev:
	python main.py

test:
	python -m unittest discover -s . -p 'test_*.py' -v
