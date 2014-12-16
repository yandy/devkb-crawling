# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from sqlalchemy import Integer, String, Text, PickleType, Boolean
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, backref

from devkb.models import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "stackoverflow_users"

    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    name = Column(String(40))
    reputation = Column(Integer)
    questions = relationship('Question', backref='user')
    answers = relationship('Answer', backref='user')
    tags = Column(PickleType)  # String List


class Tag(DeclarativeBase):
    __tablename__ = "stackoverflow_tags"

    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    name = Column(String(40))
    qcount = Column(Integer)
    descr = Column(Text)


class Question(DeclarativeBase):
    __tablename__ = 'stackoverflow_questions'

    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    title = Column(String(100))
    body = Column(Text)
    tags = Column(PickleType)  # String List
    vote = Column(Integer)
    comments = Column(PickleType)  # String List
    user_id = Column(Integer, ForeignKey('stackoverflow_users.id'))
    answers = relationship('Answer', backref='question')


class Answer(DeclarativeBase):
    __tablename__ = "stackoverflow_answers"

    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    body = Column(Text)
    vote = Column(Integer)
    accept = Column(Boolean)
    comments = Column(PickleType)  # String List
    user_id = Column(Integer, ForeignKey('stackoverflow_users.id'))
    question_id = Column(Integer, ForeignKey('stackoverflow_questions.id'))
