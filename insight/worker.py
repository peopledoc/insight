# -*- coding: utf-8 -*-
from redis import StrictRedis
import json
import requests

from insight.reader import get_file_for_url
from insight.engines import documents
from insight.writer import get_thumb_from_cache, have_cache_for_kwargs, get_thumb_path_for_kwargs

try:
    import settings
except ImportError:
    pass

REDIS_QUEUE_KEY = getattr(settings, 'REDIS_QUEUE_KEY', 'insight')
REDIS_HOST = getattr(settings, 'REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)
REDIS_DB = getattr(settings, 'REDIS_PORT', 0)

redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def main():
    print "Launch insight worker"    
    while 1:
        msg = redis.blpop(REDIS_QUEUE_KEY)
        params = json.loads(msg[1])
        print u"Consuming task for doc %s" % params['url']

        error = True
        num = 0
        while error and num < 3:
            try:
                file_obj, is_from_cache = get_file_for_url(params['url'])
                error = False
            except:
                sleep(10)
                num += 1
                error = True
        print u"Got %s (%s)" % (params['url'], is_from_cache)
            
        extract_parameters = {'url': params['url'],
                              'max_previews': params['max_previews'],
                              'engine': params.get('engine', 'document')}
        
        for size in params['sizes']:
            extract_parameters['width'] = size[0]
            extract_parameters['height'] = size[1]
            print "Processing", extract_parameters
            num_pages = documents.extract_image(file_obj, **extract_parameters)
            file_obj.seek(0)
            print "Processed", num_pages, "pages"

        if 'callback' in params and params['callback'] is not None:
            try:
                req = requests.post(params['callback'], data={'num_pages': num_pages})
                print req.url, num_pages
            except requests.exceptions.ConnectionError:
                # For localhost error on production server
                pass
