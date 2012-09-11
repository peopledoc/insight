VIRTUALENV = virtualenv
PYTHON = env/bin/python

virtualenv:
	$(VIRTUALENV) env

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete

distclean: clean
	rm -fr dist *.egg-info

realclean: distclean

requirements:
	env/bin/pip freeze > etc/versions-kgs.txt

develop: virtualenv
	env/bin/python setup.py develop

rungunicorn:
	env/bin/gunicorn -w3 insight.api:app	

runinsight:
	env/bin/circusd etc/circus_config.ini
