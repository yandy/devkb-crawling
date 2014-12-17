# -*- coding: utf-8 -*-

# Scrapy settings for devkb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import os.path

BOT_NAME = 'devkb'

SPIDER_MODULES = ['devkb.spiders']
NEWSPIDER_MODULE = 'devkb.spiders'

ITEM_PIPELINES = { 'devkb.pipelines.DevkbPipeline': 1 }

LOG_LEVEL = 'DEBUG'

COMMANDS_MODULE = 'devkb.commands'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    'devkb.randomproxy.RandomProxy': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110
}

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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'

COOKIES_ENABLED = False

# DOWNLOAD_DELAY = 0.25
# ROBOTSTXT_OBEY = True
RETRY_TIMES = 10

CONF_PATH = os.environ.get('DEVKB_CONF') or '/etc/scrapy/projects/devkb'

DATABASE = os.path.join(CONF_PATH, 'db.yml')

PROXY_LIST = os.path.join(CONF_PATH, 'proxies.txt')
