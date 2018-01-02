# -*- coding: utf-8 -*-
import configparser
from flask import Flask


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('conf.ini')

import migration.views
