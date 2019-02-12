PYENVS=2.7.15 3.4.8 3.5.5 3.6.5
REQUIREMENTS_DIR=requirements

.PHONY: clean clean_wheels

build:
	@python setup.py bdist_wheel

clean: clean_build clean_docs clean_requirements clean_wheels

clean_docs:
	cd docs && make clean

clean_build:
	python setup.py clean --all
	rm -rf dist/

clean_requirements:
	rm -rf requirements/*.txt

clean_wheels:
	rm -rf wheelhouse/

.PHONY: docs
docs:
	tox -e docs

serve_docs:
	tox -e docs,serve-docs
