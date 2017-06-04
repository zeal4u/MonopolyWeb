## 简单的大富翁游戏网页版

### 目录
* bin/ 后台
    * bin/app.y RESTful接口
    * bin/monopoly.py 游戏逻辑处理模块
    * bin/services.py 服务支持模块
    * bin/stuff.py  数据库支持模块
* static/ 前台

需要设置好数据库支持模块中的连接函数才能运行该项目  
如下所示函数
```python
class DBHelper:
    @staticmethod
    def get_connect(user='zeal4u', passwd='123456', db='monopoly', host='localhost'):
        
```
运行正常的话，系统会自动创建所需要的表
