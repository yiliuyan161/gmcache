# gm_cache 掘金API缓存
## 安装
```python
pip install gmcache
```
## 使用

from gm.api import *  改成 from gmcache import *
所有数据查询API加了一层代理,数据API默认优先走缓存(保存7天),其他API还是走掘金API

```python
from gmcache import *  # 回测环境使用缓存API,实时环境使用掘金原始API
# from gm.api import *  

set_token("XXXXXX")

df = get_instruments(exchanges='SZSE,SHSE',sec_types=1, df=True)

# 清理所有缓存
clear_cache()
```
