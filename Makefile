VIRTUALENV = virtualenv
PYTHON = env/bin/python

virtualenv:
	if [ ! -f $(PYTHON) ]; then \
            if [[ "`$(VIRTUALENV) --version`" < "`echo '1.8'`" ]]; then \
                $(VIRTUALENV) --no-site-packages --distribute env; \
            else \
                $(VIRTUALENV) env; \
            fi \
        fi

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete

distclean: clean
	rm -fr dist *.egg-info

realclean: distclean

requirements:
	env/bin/pip freeze > etc/versions-kgs.txt

develop: virtualenv update
	env/bin/python setup.py develop

update:
	env/bin/pip install -r etc/requirements.txt
