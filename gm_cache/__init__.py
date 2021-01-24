import sys
import os
import gm.api
from diskcache import FanoutCache
from functools import partial
cache = FanoutCache()


@cache.memoize(typed=True, expire=604800, tag='gm1week')
def cache1week(name,**kw):
    result = getattr(gm.api, name)(**kw)
    return result

@cache.memoize(typed=True, expire=86400, tag='gm1day')
def cache1day(name,**kw):
    result = getattr(gm.api, name)(**kw)
    return result

@cache.memoize(typed=True, expire=3600, tag='gm1hour')
def cache1hour(name,**kw):
    result = getattr(gm.api, name)(**kw)
    return result

class GMCache1Week(object):
     def __getattr__(self, name):
         return partial(cache1week,name)
     
class GMCache1Day(object):
     def __getattr__(self, name):
         return partial(cache1day,name)

class GMCache1Hour(object):
     def __getattr__(self, name):
         return partial(cache1hour,name)
gm1week=GMCache1Week()
gm1day=GMCache1Day()
gm1hour=GMCache1Hour()

import shutil
def clean_all_cache():
    try:
        shutil.rmtree(cache.directory)
    except OSError:  # Windows wonkiness
        print("清理失败,请手动清理 {dir}".format(dir=cache.directory))
         


__all__ = ['gm1week','gm1day','gm1hour','clean_all_cache']



