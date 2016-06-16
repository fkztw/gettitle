dependency:
	pip install flake8

travis-dependency: dependency
	sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb

install:
	pip install -e .

test:
	flake8 .
	python -m unittest
