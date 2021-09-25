from functools import partial
from os.path import expanduser

import gm.api
from diskcache import Cache

home = expanduser("~").replace("\\", "/")
cache = Cache(directory=home + "/.gmcache", timeout=60, sqlite_synchronous=0)


class GMCache(object):
    """
    掘金API缓存类,利用元编程缺省方法代理所有掘金API
    """

    @staticmethod
    @cache.memoize(typed=True, expire=604800, tag='1week')
    def cache_api(name, *args, **kwargs):
        """
        gm api 缓存代理
        :param name: 方法名
        :param args: 位置参数
        :param kwargs: 命名参数
        :return:
        """
        result = getattr(gm.api, name)(*args, **kwargs)
        return result

    @staticmethod
    def proxy_api(name, *args, **kwargs):
        result = getattr(gm.api, name)(*args, **kwargs)
        return result

    @staticmethod
    def clear():
        cache.clear()

    def __getattr__(self, name):
        """
        缺省方法
        :param name:方法名
        :return:
        """
        if name in ['history', 'history_n', 'get_history_l2ticks', 'get_history_l2bars',
                    'get_history_l2transactions', 'get_history_l2orders', 'get_history_l2orders_queue',
                    'get_fundamentals', 'get_fundamentals_n', 'get_instruments', 'get_history_instruments',
                    'get_instrumentinfos',
                    'get_constituents', 'get_history_constituents', 'get_continuous_contracts', 'get_industry',
                    'get_dividend', 'get_trading_dates',
                    'get_previous_trading_date', 'get_next_trading_date']:
            return partial(GMCache.cache_api, name)
        else:
            return partial(GMCache.proxy_api, name)


api = GMCache()

__all__ = ['api']
