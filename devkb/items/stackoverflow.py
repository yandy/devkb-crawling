# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    reputation = scrapy.Field()
    tags = scrapy.Field()


class TagItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    qcount = scrapy.Field()
    descr = scrapy.Field()


class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()
    vote = scrapy.Field()
    user = scrapy.Field()


class AnswerItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    vote = scrapy.Field()
    accept = scrapy.Field()
    comments = scrapy.Field()
    user = scrapy.Field()
