PYENVS=2.7.15 3.4.9 3.5.6 3.6.8 3.7.2
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

.PHONY: requirements
requirements:
	@pip install -r $(REQUIREMENTS_DIR)/build.txt

dev_requirements:
	@pip install -r $(REQUIREMENTS_DIR)/build.txt
	@pip install -r $(REQUIREMENTS_DIR)/dev.txt

.PHONY: test
test:
	@make install_envs
	@pyenv local ${PYENVS}
	@tox

install_envs:
	@for v in ${PYENVS} ; do \
		echo "Installing " $$v ; \
		pyenv install -s $$v ; \
	done
