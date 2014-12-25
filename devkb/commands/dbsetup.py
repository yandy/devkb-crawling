from __future__ import print_function
from scrapy.command import ScrapyCommand

from devkb.models import db


class DBSetup(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Setup DB schema"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("--verbose", "-v", dest="verbose", action="store_true",
                          help="show setup processing")

    def run(self, args, opts):
        db.stackoverflow_users.ensure_index("extid", unique=True)
        db.stackoverflow_tags.ensure_index("name", unique=True)
        db.stackoverflow_questions.ensure_index("extid", unique=True)
        db.github_users.ensure_index("extid", unique=True, sparse=True)
        db.github_users.ensure_index("login", unique=True)
        db.github_repos.ensure_index('extid', unique=True, sparse=True)
        db.github_repos.ensure_index('fullname', unique=True)
