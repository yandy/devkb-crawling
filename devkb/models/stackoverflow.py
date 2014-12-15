# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from devkb.models import DeclarativeBase

class User(DeclarativeBase):
    __tablename__ = "stackoverflow_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    reputation = Column(Integer)
    questions = relationship('Question', backref='user')
    answers = relationship('Answer', backref='user')
    tags = Column(String) #String List

class Tag(DeclarativeBase):
    __tablename__ = "stackoverflow_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    qcount = Column(Integer)
    descr = Column(String)

class Question(DeclarativeBase):
    __tablename__ = 'stackoverflow_questions'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    tags = Column(String) #String List
    vote = Column(Integer)
    user_id = Column(Integer, ForeignKey('stackoverflow_users.id'))
    answers = relationship('Answer', backref='user')

class Answer(DeclarativeBase):
    __tablename__ = "stackoverflow_answers"

    id = Column(Integer, primary_key=True)
    ansid = Column(Integer)
    body = Column(String)
    vote = Column(Integer)
    accept = Column(Boolean)
    comments = Column(String) #String List
    user_id = Column(Integer, ForeignKey('stackoverflow_users.id'))
    question_id = Column(Integer, ForeignKey('stackoverflow_questions.id'))
