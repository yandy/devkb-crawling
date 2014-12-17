# -*- coding: utf-8 -*-

# Scrapy settings for devkb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'devkb'

SPIDER_MODULES = ['devkb.spiders']
NEWSPIDER_MODULE = 'devkb.spiders'

ITEM_PIPELINES = { 'devkb.pipelines.DevkbPipeline': 1 }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Tinysoubot (+http://tinysou.com)'
#USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'

# COOKIES_ENABLED = False

DOWNLOAD_DELAY = 0.25
ROBOTSTXT_OBEY = True
RETRY_TIMES = 5

LOG_LEVEL = 'WARNING'

COMMANDS_MODULE = 'devkb.commands'

DATABASE = {
    'drivername': 'mysql+pymysql',
    'username': 'devkb',
    'password': 'game584131',
    'host': '0.0.0.0',
    'port': 3306,
    'database': 'devkb',
    'query': {
        'charset': 'utf8',
        'use_unicode': 0
    }
}

URL_REGEXS = {
    'stackoverflow': {
        'user': r'^http://stackoverflow\.com/users/(?P<user_id>\d+)/[^/]+/?$',
        'tag': r'^http://stackoverflow\.com/tags/(?P<tag_name>[\w.-]+)/info/?$',
        'question': r'^http://stackoverflow\.com/questions/(?P<question_id>\d+)/[^/]+/?$'
    }
}
