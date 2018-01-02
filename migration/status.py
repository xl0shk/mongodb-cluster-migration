# -*- coding: utf-8 -*-
from migration.views import status_field
from flask_restful import Resource, marshal_with
import time

status = {}


class Status(Resource):
    @marshal_with(status_field)
    def get(self, db):
        progress_rate = get_progress_rate(db)
        return {'progress_rate': progress_rate}


def set_status(db, num):
    value = {'progress_rate': num, 'timestamp': int(time.time())}
    status[db] = value
    return


def del_status(db):
    if db in status:
        del status[db]
    return


def get_progress_rate(db):
    if db in status:
        return status[db]['progress_rate']
    else:
        value = {'progress_rate': 0, 'timestamp': int(time.time())}
        status[db] = value
        return 0


def set_ts(db):
    status[db]['timestamp'] = int(time.time())
    return


def get_ts(db):
    if db in status:
        return status[db]['timestamp']
    else:
        ts = int(time.time())
        value = {'progress_rate': 0, 'timestamp': ts}
        status[db] = value
        return ts
