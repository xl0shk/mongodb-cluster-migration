# -*- coding:utf-8 -*-
from migration.mongo import *
from migration.status import *
from migration.logger import *
from migration import *
from threading import current_thread
import pymongo
import time


class Sync(object):
    def __init__(self, **kwargs):
        source = kwargs.get('source')
        target = kwargs.get('target')
        db = kwargs.get('db')
        ts = kwargs.get('ts')

        self._src_host = config.get("DB", source + '_mongo_host')
        self._src_port = config.get("DB", source + '_mongo_port')
        self._src_user = config.get("DB", source + '_mongo_user')
        self._src_pwd = config.get("DB", source + '_mongo_pwd')
        self._src_authsource = config.get("DB", source + '_mongo_authsource')

        self._dst_host = config.get("DB", target + '_mongo_host')
        self._dst_port = config.get("DB", target + '_mongo_port')
        self._dst_user = config.get("DB", target + '_mongo_user')
        self._dst_pwd = config.get("DB", target + '_mongo_pwd')
        self._dst_authsource = config.get("DB", target + '_mongo_authsource')

        self._ts = ts
        self._db = db
        self._coll = config.get("DB", target + '_mongo_coll')
        self._ns = self._db + '.' + self._coll

        self._src_mc = mongo_conn(
            host=self._src_host,
            port=self._src_port,
            user=self._src_user,
            pwd=self._src_pwd,
            authsource=self._src_authsource)

        self._dst_mc = mongo_conn(
            host=self._dst_host,
            port=self._dst_port,
            user=self._dst_user,
            pwd=self._dst_pwd,
            authsource=self._dst_authsource)

    def sync(self):
        src_coll = self._src_mc['local']['oplog.rs']
        dst_coll = self._dst_mc[self._db][self._coll]

        db = self._db
        count = 0
        thread_name = current_thread().getName()

        while True:
            src_cursor = src_coll.find({"ns": self._ns, 'ts': {'$gt': self._ts}},
                                       cursor_type=pymongo.CursorType.TAILABLE_AWAIT, oplog_replay=True)
            while src_cursor.alive:
                time_interval = int(time.time()) - get_ts(db)
                if time_interval > 10:
                    logger.debug('{}:***********no op in 10s recently***********'.format(thread_name))
                    count += 1
                    progress_rate = 50 + count*10
                    set_status(db, progress_rate)
                    if progress_rate == 100:
                        logger.debug('%s:***********task end***********'.format(thread_name))
                        return

                for oplog_doc in src_cursor:
                    set_ts(db)
                    op = oplog_doc['op']
                    logger.debug('op: {}'.format(op))
                    logger.debug('o: {}'.format(oplog_doc['o']))
                    if op == 'i':
                        try:
                            dst_coll.insert_one(oplog_doc['o'])
                        except Exception as e:
                            logger.error(e)
                            pass
                    elif op == 'd':
                        dst_coll.delete_one(oplog_doc['o'])
                    elif op == 'c':
                        dst_coll.command(oplog_doc['o'])
                    elif op == 'u':
                        try:
                            dst_coll.update(oplog_doc['o2'], oplog_doc['o'])
                        except Exception as e:
                            logger.error(e)
                            pass
                    elif op == 'n':
                        pass
                    else:
                        logger.debug('unknown op')
                time.sleep(0.01)
