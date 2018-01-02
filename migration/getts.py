# -*- coding:utf-8 -*-
from migration import *
from migration.mongo import *
from bson.timestamp import Timestamp
from time import time
from migration.logger import *


class GetLastTs(object):
    def __init__(self, **kwargs):
        source = kwargs.get('source')
        db = kwargs.get('db')

        self._host = config.get('DB', source + '_mongo_host')
        self._port = config.get('DB', source + '_mongo_port')
        self._user = config.get('DB', source + '_mongo_user')
        self._pwd = config.get('DB', source + '_mongo_pwd')
        self._coll = config.get('DB', source + '_mongo_coll')
        self._authsource = config.get('DB', source + '_mongo_authsource')
        self._db = db
        self._ns = self._db + '.' + self._coll

        self._src_mc = mongo_conn(
            host=self._host,
            port=self._port,
            user=self._user,
            pwd=self._pwd,
            authsource=self._authsource)

    def get_last_ts(self):
        _src_coll = self._src_mc['local']['oplog.rs']
        src_doc = _src_coll.find({'ns': self._ns}).sort('ts', -1).limit(1000)
        src_doc = list(src_doc)
        lenlist = len(src_doc)
        last_ts = ''

        if lenlist == 0:
            last_ts = Timestamp(int(time()), 1)
            return last_ts

        for i in range(0, lenlist):
            # TODO:这里可能存在隐患
            if i == lenlist - 1:
                last_ts = src_doc[i]['ts']
                break
            if src_doc[i]['op'] == 'd':
                if src_doc[i + 1]['op'] != 'd':
                    last_ts = src_doc[i + 1]['ts']
                    break
                else:
                    pass

        return last_ts
