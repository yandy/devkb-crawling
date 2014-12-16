# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from devkb.models import Session
from devkb.items.stackoverflow import UserItem, TagItem, QuestionItem, AnswerItem
from devkb.models.stackoverflow import User, Tag, Question, Answer


class DevkbPipeline(object):

    def process_item(self, item, spider):
        session = Session()
        if isinstance(item, UserItem):
            model = User(**item)
        elif isinstance(item, TagItem):
            model = Tag(**item)
        elif isinstance(item, QuestionItem):
            model = Question(**item)
        elif isinstance(item, AnswerItem):
            model = Answer(**item)
        session.merge(model)
        session.commit()
        return item
