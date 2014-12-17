# -*- coding: utf-8 -*-

import yaml
from devkb import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_db_conf = yaml.load(open(settings.DATABASE, 'r').read())

DeclarativeBase = declarative_base()
ENGINE = create_engine(URL(**_db_conf))
Session = sessionmaker(bind=ENGINE)
