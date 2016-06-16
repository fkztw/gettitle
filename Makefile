dependency:
	pip install flake8

travis-dependency: dependency
	sudo apt-get -q update
	sudo apt-get install --no-install-recommends -y -q \
		qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
	sudo apt-get clean

install:
	pip install -e .

test:
	flake8 .
	python -m unittest
