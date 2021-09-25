import shutil
from functools import partial

import gm.api
import gm.api
from diskcache import Cache

cache = Cache()


@cache.memoize(typed=True, expire=604800, tag='1week')
def cache_api(name, *args, **kw):
    result = getattr(gm.api, name)(*args, **kw)
    return result


class GMCache(object):

    def __getattr__(self, name):
        return partial(cache_api, name)


api = GMCache()


def clean_all_cache():
    try:
        shutil.rmtree(cache.directory)
    except OSError:
        print("清理失败,请手动清理 {dir}".format(dir=cache.directory))


__all__ = ['api', 'clean_all_cache']
