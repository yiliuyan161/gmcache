# gm_cache 掘金API缓存
## 安装
```python
pip install gmcache
```
## 使用

直接在掘金api前面增加gm1day. 前缀，表示缓存1天

```python
from gmcache import api  # 回测环境使用缓存API,实时环境使用掘金原始API
#import gm.api as api  
api.set_token("XXXXXX")


df = api.get_instruments(exchanges='SZSE,SHSE',sec_types=1, df=True)

# 清理缓存
api.clear()
```
