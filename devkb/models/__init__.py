# -*- coding: utf-8 -*-

import yaml
from devkb import settings

from pymongo import MongoClient

_db_conf = yaml.load(open(settings.DATABASE, 'r').read())

client = MongoClient(_db_conf['host'], _db_conf['port'])

db = client[_db_conf['database']]
