.PHONY: test env

test:
	python triparse.py test.txt 2122

env:
	pip install -r pip-requirements.txt
