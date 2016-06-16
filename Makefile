test-dependency:
	pip install flake8

install:
	pip install -e .

test:
	flake8 .
	python -m unittest
