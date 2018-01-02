# -*- coding:utf-8 -*-
import pymongo


def mongo_conn(**kwargs):
    host = kwargs.get('host')
    port = kwargs.get('port')
    user = kwargs.get('user')
    pwd = kwargs.get('pwd')
    authsource = kwargs.get('authsource')
    uri = "mongodb://{user}:{pwd}@{host}:{port}/?authSource={authsource}".format(user=user, pwd=pwd, host=host, port=port, authsource=authsource)
    try:
        mongo_client = pymongo.MongoClient(uri)
    except Exception as e:
        raise Exception('connect mongo fail %s' % e)
    return mongo_client
