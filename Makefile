# Makefile for pydstat
#
# Source:: https://github.com/ampledata/pydstat
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: Apache License 2.0
#


init:
	pip install -r requirements.txt --use-mirrors

lint:
	pylint -f parseable -i y -r y pydstat/*.py tests/*.py *.py | \
		tee pylint.log

cli_lint:
	pylint -f colorized -i y -r n pydstat/*.py tests/*.py *.py

flake8:
	flake8 --exit-zero  --max-complexity 12 pydstat/*.py tests/*.py *.py | \
		awk -F\: '{printf "%s:%s: [E]%s\n", $$1, $$2, $$3}' | tee flake8.log

cli_flake8:
	flake8 --max-complexity 12 pydstat/*.py tests/*.py *.py

pep8: flake8

clonedigger:
	clonedigger --cpd-output .

install:
	pip install .

uninstall:
	pip uninstall pydstat

develop:
	python setup.py develop

publish:
	python setup.py register sdist upload

nosetests:
	python setup.py nosetests

test: init lint flake8 clonedigger nosetests

clean:
	rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg nosetests.xml \
		pylint.log *.egg output.xml flake8.log */*.pyc */*.pyo
