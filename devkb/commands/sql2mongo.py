from __future__ import print_function

import re
from scrapy.command import ScrapyCommand
from scrapy.exceptions import UsageError

from devkb.models import Session
from devkb.models.stackoverflow import User, Tag, Question, Answer
from pymongo import MongoClient


class sql2mongo(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <host> [<port>]"

    def short_desc(self):
        return "migrate data from mysql to mongo"

    def run(self, args, opts):
        acount = len(args)
        if acount < 1 or acount > 2:
            raise UsageError()
        host = args[0]
        port = int(args[1]) if acount == 2 else 27017
        client = MongoClient(host, port)
        db = client.devkb
        session = Session()

        ### Clear Data
        # print('Start to clear data')
        # db.drop_collection('users')
        # db.drop_collection('tags')
        # db.drop_collection('questions')
        # print('Success')

        ### Migrate User
        print('Start migrating user')
        mongo_users = db.users
        for user in session.query(User):
            print("user: %s" % user.id)
            u_id = mongo_users.insert({'extid': user.id, 'url': user.url, 'name':
                                       user.name, 'reputation': user.reputation, 'tags': user.tags})
            if u_id:
                print('success')
        print('Migrated %d users' % mongo_users.count())
        # Migrate tag
        print('Start migrating tag')
        mongo_tags = db.tags
        for tag in session.query(Tag):
            print("tag: %s" % tag.name)
            t_id = mongo_tags.insert(
                {'url': tag.url, 'name': tag.name, 'qcount': tag.qcount, 'descr': tag.descr})
            if t_id:
                print('success')
        print('Migrated %d tags' % mongo_tags.count())
        # Migrate questions and answers
        print('Start migrating question and answer')
        mongo_questions = db.questions
        for question in session.query(Question):
            print("question: %s" % question.id)
            qdoc = {
                'extid': question.id,
                'url': question.url,
                'title': question.title,
                'body': question.body,
                'tags': question.tags,
                'vote': question.vote,
                'comments': question.comments,
                'user_id': question.user_id,
                'answers': []
            }
            for ans in question.answers:
                adoc = {
                'extid': ans.id,
                'url': ans.url,
                'body': ans.body,
                'vote': ans.vote,
                'accept': ans.accept,
                'comments': ans.comments,
                'user_id': ans.user_id
                }
                qdoc['answers'].append(adoc)
            q_id = mongo_questions.insert(qdoc)
            if q_id:
                print('success')
        print('Migrated %d tags' % mongo_tags.count())
