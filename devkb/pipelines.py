# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from devkb.models import db
from devkb.items.stackoverflow import UserItem, TagItem, QuestionItem


class DevkbPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            db.stackoverflow_users.update(
                {"extid": item['extid']}, {"$set": dict(item)}, upsert=True)
        elif isinstance(item, TagItem):
            db.stackoverflow_tags.update(
                {"name": item["name"]}, {"$set": dict(item)}, upsert=True)
        elif isinstance(item, QuestionItem):
            db.stackoverflow_questions.update(
                {"extid": item["extid"]}, {"$set": dict(item)}, upsert=True)
        else:
            return item
        return item
