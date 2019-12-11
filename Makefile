.PHONY: dist

env: cleanall
	virtualenv -p python2 venv

prod: env
	venv/bin/pip install -e .

dev: prod
	venv/bin/pip install ".[dev]"

dist: clean
	rm -rf 'dist'
	venv/bin/python setup.py bdist_wheel

install: dist
	yes | pip uninstall apkworkers
	pip install --user dist/*.whl

monitor:
	venv/bin/flower -A apkworkers

clean_env:
	rm -rf venv

clean_build:
	rm -rf dist/
	rm -rf build/
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.eggs' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

clean_python:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*.pyd' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean: clean_build clean_python;

cleanall: clean clean_env;
