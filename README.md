#  mongodb-cluster-migration

mongodb-cluster-migration项目用于在不同MongoDB Cluster（或者MongoDB实例）之间进行无缝的数据库迁移，零停机。


### 实现原理与基本框架

基于Python Flask Web框架，并使用Flask-RESTful模块实现类RESTful接口。
使用的模块为：pymongo 和 flask-restful。

实现的基本思路：
1. RESTful接口接收迁移时用到路径db和参数source、target（source表示迁移的MongoDB源副本集群、target表示迁移的MongoDB目标副本集群、db表示要迁移的数据库名）；
2. 启动迁移线程，获取最新的db的oplog信息；
3. 使用mongodump和mongostore工具进行数据库的导入导出；
4. 实时进行oplog的同步回放；
5. 提供状态查询接口。


### 运行环境
Python 3.5 +  
MongoDB 3.0 +


### 项目启动方法
1. 根据实际情况，添加配置文件中的MongoDB和log信息；
2. 进入项目目录mongodb-cluster-migration；
3. 执行 bash ./bin/startup.sh start，会自动进行Python3 venv创建和依赖安装；
提前安装好Python 3.5+各种环境


### 接口
1. /migrate/<db> 开始迁移和同步db数据
2. /status/<db> 查看db的迁移任务的执行进度，为0-100的整数，代表进度的百分比，100代表任务完成

### 参考资料
http://api.mongodb.com/python/current/examples/tailable.html
https://docs.mongodb.com/manual/