# -*- coding: utf-8 -*-

# Scrapy settings for devkb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from devkb.environments import *

BOT_NAME = 'devkb'

SPIDER_MODULES = ['devkb.spiders']
NEWSPIDER_MODULE = 'devkb.spiders'

ITEM_PIPELINES = { 'devkb.pipelines.DevkbPipeline': 1 }

LOG_LEVEL = 'INFO'

COMMANDS_MODULE = 'devkb.commands'

URL_REGEXS = {
    'stackoverflow': {
        'user': r'^http://stackoverflow\.com/users/(?P<user_id>\d+)/[^/]+/?$',
        'tag': r'^http://stackoverflow\.com/tags/(?P<tag_name>[\w.-]+)/info/?$',
        'question': r'^http://stackoverflow\.com/questions/(?P<question_id>\d+)/[^/]+/?$'
    }
}

DENY_RULES = {
    'stackoverflow': (
        r'^http://stackoverflow\.com/questions/ask[/?]',
        r'^http://stackoverflow\.com/users/login[/?]',
        r'^http://stackoverflow\.com/users/logout[/?]',
        r'^http://stackoverflow\.com/users/filter[/?]',
        r'^http://stackoverflow\.com/users/authenticate[/?]',
        r'^http://stackoverflow\.com/users/flag-weight/',
        r'^http://stackoverflow\.com/users/flag-summary/',
        r'^http://stackoverflow\.com/users/flair[/?]',
        r'^http://stackoverflow\.com/users/activity/',
        r'^http://stackoverflow\.com/users/stats/',
        r'^http://stackoverflow\.com/users/.*\?tab=accounts',
        r'^http://stackoverflow\.com/.*/ivc/',
        r'^http://stackoverflow\.com/.*\?lastactivity',
        r'^http://stackoverflow\.com/questions/.*answertab=',
        r'^http://stackoverflow\.com/questions/tagged',
        r'^http://stackoverflow\.com/questions/.*/answer/submit'
        )
}
