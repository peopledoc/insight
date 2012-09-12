# -*- coding: utf-8 -*-
"""API urls"""
from flask import Flask, redirect

from insight.api.sync import view as sync_view
from insight.api.async import view as async_view

try:
    import settings
except ImportError:
    settings = None

HOME_REDIRECT = getattr(settings, 'HOME_REDIRECT', 'http://github.com/novagile/insight/')
DEBUG = getattr(settings, 'DEBUG', True)

app = Flask('insight')
app.debug=DEBUG

@app.route('/')
def home():
    """Redirect home page to API documentation"""
    return redirect(HOME_REDIRECT)

@app.route('/<engine>/')
def sync(engine):
    return sync_view(engine)

@app.route('/async/<engine>/')
def async(engine):
    return async_view(engine)

def main():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
