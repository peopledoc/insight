# -*- coding: utf-8 -*-
"""Read and URL and get the file from cache if possible or update the file."""
import hashlib
import settings
import os
import pickle
try:
    from collections import OrderedDict
except ImportError:
    # Python 2.6 fallback
    from ordereddict import OrderedDict

THUMB_CACHE_DIR = getattr(settings, 'THUMB_CACHE_DIR', '/tmp')

def get_thumb_path_for_kwargs(**kwargs):
    """Return the cache file path for url"""
    keys = kwargs.keys()
    keys.sort()
    params = OrderedDict()
    for key in keys:
        params[key] = kwargs[key]
    dumps = pickle.dumps(params)
    hash_id = hashlib.sha256(pickle.dumps(params)).hexdigest()
    return os.path.join(THUMB_CACHE_DIR, hash_id)

def get_thumb_from_cache(**kwargs):
    """Return the thumb file object related to the URL"""
    return open(get_thumb_path_for_kwargs(**kwargs), 'r')

def have_cache_for_kwargs(**kwargs):
    """Return if the cache exists for this url"""
    return os.path.exists(get_thumb_path_for_kwargs(**kwargs))

def get_last_modified(**kwargs):
    """Return the timestamp of the cache file"""
    if have_cache_for_kwargs(**kwargs):
        cache_file_path = get_thumb_path_for_kwargs(**kwargs)
        return os.path.getmtime(cache_file_path)
    return None
