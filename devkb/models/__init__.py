# -*- coding: utf-8 -*-

from devkb import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DeclarativeBase = declarative_base()
ENGINE = create_engine(URL(**settings.DATABASE))
Session = sessionmaker(bind=ENGINE)
