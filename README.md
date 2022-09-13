# gm_cache 掘金API缓存
## 安装
```python
pip install gmcache
```
## 使用

from gm.api import *  改成 from gmcache import *
所有数据查询API加了一层代理,数据API默认优先走缓存(保存7天),其他API还是走掘金API

```python
from gmcache import *  # 回测环境使用缓存API,实时运行的时候再改回去
# from gm.api import *  

set_token("XXXXXX")  # 第一次设置会保存到.gmcache/config.json 下次import 会自动加载token执行set_token 

df = get_instruments(exchanges='SZSE,SHSE',sec_types=1, df=True) # 缓存读取大约花费1-3ms

# 清理所有缓存
clear_cache()
```

## 原理说明
数据查询API会根据方法名和参数值生成key,检查缓存里是否已经有数据,没有就会走掘金API,返回值会加入到缓存,下次调用如果参数没变,就会直接走本地缓存
多次回测的情况，取数据API参数如果没变化，能极大加快回测速度