.PHONY: test env

test:
	python triparse.py test.pdf

env:
	pip install -r pip-requirements.txt
