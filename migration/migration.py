# -*- coding:utf-8 -*-
import subprocess
from migration.getts import *
from migration.sync import *
from migration.status import *
from flask_restful import Resource, marshal_with
from migration.logger import *
import threading
from migration.views import migrate_field, migrate_get_parser


class MigrationDB(Resource):
    @marshal_with(migrate_field)
    def get(self, db):
        args = migrate_get_parser.parse_args()
        source = args.source
        target = args.target
        thread_name = 'migration--{}'.format(db)
        logger.debug('create a migration task {} of db {} from {} to {}'.format(thread_name, db, source, target))
        thread = threading.Thread(target=migrate, name=thread_name, args=(db, source, target))
        thread.start()
        return {'status': 'ok'}, 200


def migrate(db, source, target):
    _migration = Migration(db, source, target)
    _migration.run()


class Migration(object):
    def __init__(self, db, source, target):
        self.db = db
        self.source = source
        self.target = target

    def run(self):
        db = self.db
        source = self.source
        target = self.target

        logger.debug('Start to migration db: {} ......'.format(db))
        set_status(db, 1)
        logger.debug('Start to get last timestamp value ......')

        _get_ts = GetLastTs(db=db, source=source)
        last_ts = _get_ts.get_last_ts()
        if str(last_ts) == "":
            logger.debug('Can not get the real timestamp, exit.')
            exit()

        set_status(db, 30)
        logger.debug('the timestamp is {}'.format(str(last_ts)))

        logger.debug('Start to dump and restore {} database from {} to {}s'.format(db, source, target))
        subprocess.call(['./bin/db_migration.sh', db, source, target])

        time.sleep(3)
        set_status(db, 50)
        logger.debug('Start to sync oplog .....')
        sync = Sync(source=source, target=target, ts=last_ts, db=db)
        sync.sync()

        return
