# -*- coding: utf-8 -*-
"""Async API view"""
from flask import abort, request
from redis import StrictRedis
import json

from insight.api.config import INSIGHT_ENGINES

try:
    import settings
except ImportError:
    settings = None

REDIS_QUEUE_KEY = getattr(settings, 'REDIS_QUEUE_KEY', 'insight')
REDIS_HOST = getattr(settings, 'REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)
REDIS_DB = getattr(settings, 'REDIS_PORT', 0)

redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def view(engine):
    """Get job parameters and add it to a redis queue"""
    params = {'url': request.args.get('url', None),
              'engine': engine,
              'callback': request.args.get('callback', None)}

    # Get URL
    if params['url']:
        if params['url'].startswith('/'):
            params['url'] = '%s%s' % (request.host_url, url[1:])
    else:
        abort(404)

    # Get Engine
    if engine not in INSIGHT_ENGINES:
        abort(400, '%s engine is not installed on this server' % engine)

    # Process sizes
    widths = [int(x) for x in request.args.getlist('width')]
    heights = [int(y) for y in  request.args.getlist('height')]

    nb_width = len(widths)
    nb_height = len(heights)

    if nb_width == 0 and nb_height == 0:
        abort(400, u'You must set either width or height')

    if nb_width == 0:
        widths = heights
        nb_width = nb_height
    
    if nb_height == 0:
        heights = widths
        nb_height = nb_width

    if nb_width == nb_height:
        sizes = zip(widths, heights)
    elif nb_width == 1:
        if nb_height > 1:
            sizes = zip(widths*nb_height, heights)
        else:
            sizes = zip(widths, heights)
    elif nb_height == 1:
        if nb_width > 1:
            sizes = zip(widths, heights*nb_width)
        else:
            sizes = zip(widths, heights)
    else:
        abort(400, u'Number of widths and heights should be the same')

    # Max number of pages to compile
    try:
        params['max_previews'] = int(request.args.get('pages', 20))
    except:
        params['max_previews'] = 20

    params['sizes'] = sizes
    
    message = json.dumps(params)
    redis.rpush(REDIS_QUEUE_KEY, message)

    return "Job added to queue"
