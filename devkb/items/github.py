# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    extid = scrapy.Field()
    url = scrapy.Field()
    login = scrapy.Field()
    follwers_count = scrapy.Field()
    follwing_count = scrapy.Field()
    stars_count = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    blog = scrapy.Field()
    location = scrapy.Field()
    email = scrapy.Field()


class RepoItem(scrapy.Item):
    # define the fields for your item here like:
    extid = scrapy.Field()
    url = scrapy.Field()
    fullname = scrapy.Field()
    langs = scrapy.Field()
    readme = scrapy.Field()
    homepage = scrapy.Field()
    descr = scrapy.Field()
    stars_count = scrapy.Field()
    forks_count = scrapy.Field()
    commits_count = scrapy.Field()
    contributors_count = scrapy.Field()
