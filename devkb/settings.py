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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'devkb (+http://www.yourdomain.com)'

DATABASE = {
    'drivername': 'sqlite',
    'database': 'devkb'
}

URL_REGEXS = {
    'stackoverflow': {
        'user': r'^http://stackoverflow\.com/users/(?P<user_id>\d+)/',
        'tag': r'^http://stackoverflow\.com/tags/(?P<tag_name>[\w.-]+)/info',
        'question': r'^http://stackoverflow\.com/questions/(?P<question_id>\d+)/',
        'answer': r'^http://stackoverflow\.com/a/(?P<answer_id>\d+)'
    }
}
