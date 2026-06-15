.PHONY: tests dev

dev:
	python main.py $(FILE)

test:
	python -m unittest discover -s . -p 'test_*.py' -v

clear:
	rm bin/*.c
