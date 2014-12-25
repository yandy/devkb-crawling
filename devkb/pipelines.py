# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from devkb.models import db
from devkb.items import stackoverflow, github


class DevkbPipeline(object):

    def process_item(self, item, spider):
        if spider.name is 'stackoverflow':
            if isinstance(item, stackoverflow.UserItem):
                db.stackoverflow_users.update(
                    {'extid': item['extid']}, {'$set': dict(item)}, upsert=True)
            elif isinstance(item, stackoverflow.TagItem):
                db.stackoverflow_tags.update(
                    {'name': item['name']}, {'$set': dict(item)}, upsert=True)
            elif isinstance(item, stackoverflow.QuestionItem):
                db.stackoverflow_questions.update(
                    {'extid': item['extid']}, {'$set': dict(item)}, upsert=True)
        elif spider.name is 'github':
            if isinstance(item, github.UserItem):
                db.github_users.update(
                    {'login': item['login']}, {'$set': dict(item)}, upsert=True)
            elif isinstance(item, github.RepoItem):
                db.github_repos.update(
                    {'fullname': item['fullname']}, {'$set': dict(item)}, upsert=True)
        return item
