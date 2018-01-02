# -*- coding: utf-8 -*-
from migration import app
from flask_cors import CORS
from flask_restful import Api, reqparse, fields
from migration.migration import MigrationDB
from migration.status import Status


CORS(app)
api = Api(app)

migrate_get_parser = reqparse.RequestParser()
migrate_get_parser.add_argument('source', dest='source', type=str, location='args', required=True)
migrate_get_parser.add_argument('target', dest='target', type=str, location='args', required=True)

migrate_field = {'status': fields.String}
status_field = {'progress_rate': fields.String}

api.add_resource(MigrationDB, '/migrate/<db>')
api.add_resource(Status, '/status/<db>')
