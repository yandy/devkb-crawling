# -*- coding: utf-8 -*-

import scrapy
import re

from devkb.items.stackoverflow import UserItem, TagItem, QuestionItem, AnswerItem
from devkb.settings import URL_REGEXS, DENY_RULES
from devkb.utils import parse_int
from scrapy.contrib.linkextractors import LinkExtractor

URL_REGEX = re.compile('|'.join(URL_REGEXS['stackoverflow'].values()))
ALLOW_REGEX = re.compile(r'^http://stackoverflow\.com/(questions|users|tags)')
DENY_REGEX = re.compile('|'.join(DENY_RULES['stackoverflow']))


class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    start_urls = ('http://stackoverflow.com',)
    link_extractor = LinkExtractor(
        allow_domains=("stackoverflow.com",), allow=ALLOW_REGEX, deny=DENY_REGEX)

    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse)

        matched = URL_REGEX.search(response.url)
        if matched is None:
            return
        elif matched.group('user_id'):
            yield self._parse_user(response, id=matched.group('user_id'))
        elif matched.group('tag_name'):
            yield self._parse_tag(response, id=matched.group('tag_name'))
        elif matched.group('question_id'):
            for item in self._parse_question(response, id=matched.group('question_id')):
                yield item

    def _parse_user(self, response, id):
        item = UserItem()
        item['id'] = int(id)
        item['url'] = response.url
        item['name'] = ''.join(
            response.css('h1#user-displayname a::text').extract())
        item['reputation'] = parse_int(
            ''.join(response.css('div#user-info-container div.reputation a::text').extract()))
        return item

    def _parse_tag(self, response, id):
        item = TagItem()
        item['name'] = id
        item['url'] = response.url
        item['qcount'] = parse_int(
            ''.join(response.css('.summarycount::text').extract()))
        descr = ''.join(response.css(
            '#questions .post-text').xpath('node()').extract())
        item['descr'] = descr.strip()
        return item

    def _parse_question(self, response, id):
        item = QuestionItem()
        item['id'] = int(id)
        item['url'] = response.url
        item['title'] = ''.join(
            response.css('div#question-header h1[itemprop=name] a::text').extract())
        body = ''.join(response.css(
            'div#question td.postcell div[itemprop=text]').xpath('node()').extract())
        item['body'] = body.strip()
        item['tags'] = response.css(
            'div#question td.postcell div.post-taglist a[rel=tag]::text').extract()
        item['vote'] = parse_int(''.join(response.css(
            'div#question div.vote span[itemprop=upvoteCount]::text').extract()))
        item['comments'] = response.css(
            'div#question tr.comment span.comment-copy::text').extract()
        user_url = ''.join(response.css(
            'div#question div.user-info div.user-gravatar32 a::attr(href)').extract())
        matched = re.match(r'/users/(?P<user_id>\d+)/', user_url)
        item['user_id'] = matched and int(matched.group('user_id'))
        yield item
        for answer in response.css('div#answers div.answer'):
            item = AnswerItem()
            item['id'] = int(''.join(answer.xpath('@data-answerid').extract()))
            item['url'] = response.url.rstrip(
                '/') + '/%d#%d' % (item['id'], item['id'])
            body = ''.join(
                answer.css('div[itemprop=text]').xpath('node()').extract())
            item['body'] = body.strip()
            item['vote'] = parse_int(
                ''.join(answer.css('div.vote span[itemprop=upvoteCount]::text').extract()))
            item['accept'] = bool(answer.css('div.vote span.vote-accepted-on'))
            item['comments'] = answer.css(
                'tr.comment span.comment-copy::text').extract()
            user_url = ''.join(
                answer.css('div.user-info div.user-gravatar32 a::attr(href)').extract())
            matched = re.match(r'/users/(?P<user_id>\d+)/', user_url)
            item['user_id'] = matched and int(matched.group('user_id'))
            item['question_id'] = int(id)
            yield item
