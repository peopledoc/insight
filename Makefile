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

runserver:
	env/bin/gunicorn -w3 insight.api:app	

launch_workers:
	circusd etc/circus_config.ini
