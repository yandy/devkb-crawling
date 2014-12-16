from __future__ import print_function
from scrapy.command import ScrapyCommand

from devkb.models import DeclarativeBase, ENGINE, stackoverflow


class DBSetup(ScrapyCommand):

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Setup DB schema"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("--verbose", "-v", dest="verbose", action="store_true",
                          help="show setup processing")

    def run(self, args, opts):
        rest = DeclarativeBase.metadata.create_all(ENGINE)
        if opts.verbose:
            print(rest)
