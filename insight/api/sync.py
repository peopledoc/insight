# -*- coding: utf-8 -*-
"""Sync API view"""
from flask import abort, request, make_response
from insight.api.config import INSIGHT_READER, INSIGHT_ENGINES, INSIGHT_WRITER
from insight.writer import have_cache_for_kwargs, get_thumb_path_for_kwargs


def view(engine):
    """Get job parameters, process it synchroneously and return the requested image."""
    num_pages = None

    # Get Engine
    if engine not in INSIGHT_ENGINES:
        abort(400, '%s engine is not installed on this server' % engine)

    # 1. Get the image or raise 404    
    params = {'url': request.args.get('url', None),
              'width': int(request.args.get('width', 0)),
              'height': int(request.args.get('height', 0)),
              'engine': engine}

    if params['width'] == 0 and params['height'] == 0:
        abort(400, u'You must set either width or height')

    if params['url']:
        if params['url'].startswith('/'):
            params['url'] = '%s%s' % (request.host_url, url[1:])
    else:
        abort(404)

    try:
        params['page'] = int(request.args.get('page', 1))
    except:
        params['page'] = 1

    # Call the reader
    file_obj, is_from_cache = INSIGHT_READER(params['url'])

    if engine == 'document':
        from insight.engines.documents import count_pages
        num_pages = count_pages(file_obj.read())
        if params['page'] > num_pages or params['page'] < 1:
            abort(400, 'page not found')

    # If needed we call the engine
    if not (have_cache_for_kwargs(**params) and is_from_cache):
        num_pages = INSIGHT_ENGINES[engine](file_obj, **params) or None

    # Get the thumb
    thumb = INSIGHT_WRITER(**params)

    # 3. Returns the image
    response = make_response(thumb.read())
    response.content_type = 'image/png'

    if num_pages is not None:        
        response.headers.add('x-document-num_pages', str(num_pages))
    else:
        response.headers.add('x-document-num_pages', 1)

    file_obj.close()
    thumb.close()
    return response
