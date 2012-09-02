# -*- coding: utf-8 -*-
from insight.reader import get_file_for_url
from insight.writer import get_thumb_from_cache

INSIGHT_READER = get_file_for_url
INSIGHT_ENGINES = {}

try:
    from insight.engines import images
    INSIGHT_ENGINES.update({
        'scale': images.scale,
        'crop': images.crop,
        'upscale': images.upscale,
        })
except ImportError, e:
    print "insight.engines.images was not imported : %s" % e.message

try:
    from insight.engines import documents
    INSIGHT_ENGINES.update({
        'document': documents.extract_image,
        })
except ImportError, e:
    print "insight.engines.documents was not imported : %s" % e.message

INSIGHT_WRITER = get_thumb_from_cache
