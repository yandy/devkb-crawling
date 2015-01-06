# -*- coding: utf-8 -*-

import yaml
from pymongo import MongoClient

from devkb import settings

_db_conf = yaml.load(open(settings.DATABASE, 'r').read())

client = MongoClient(_db_conf['host'], _db_conf['port'])

db = client[_db_conf['database']]
