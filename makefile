.PHONY: tests dev

dev:
	python main.py

tests:
	python -m unittest discover -s . -p 'test_*.py' -v
