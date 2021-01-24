# gm_cache 掘金API缓存
## 安装
```python
pip install git+https://github.com/chenjiajia/gm_cache.git --upgrade
```
## 使用

直接在掘金api前面增加gm1day. 前缀，表示缓存1天
```python
from gm_cache import gm1day,gm1hour,gm1week,clean_all_cache

gm1hour.get_instruments(exchanges='SZSE', df=True) #缓存1小时

gm1day.get_instruments(exchanges='SZSE', df=True) #缓存1天

gm1week.get_instruments(exchanges='SZSE', df=True) #缓存1周

clean_all_cache() #删除全部缓存，删除失败，手工删除缓存目录即可
```
