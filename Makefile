test-dependency:
	pip install flake8

install:
	pip install -e .

test:
	flake8 . --ignore=E121,E123,E126,E226,E24,E704,W503,W504,E501
	python -m unittest
