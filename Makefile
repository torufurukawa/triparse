.PHONY: test env

test:
	python triparse.py test.txt

env:
	pip install -r pip-requirements.txt
