# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2

from devkb.items.stackoverflow import UserItem, TagItem, QuestionItem
from devkb.settings import URL_REGEXS
from devkb.utils import parse_int
from scrapy.contrib.linkextractors import LinkExtractor

URL_REGEX = re.compile('|'.join(URL_REGEXS['stackoverflow'].values()))

QUESTIONS_URL = 'http://stackoverflow.com/questions?pagesize=50&page=%d&sort=%s'


class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    link_extractor = LinkExtractor(
        allow_domains=("stackoverflow.com",), allow=URL_REGEX)

    def __init__(self, skip=0, limit=1000, sort='active', proxy=False, *args, **kwargs):
        super(StackoverflowSpider, self).__init__(*args, **kwargs)
        page_start = int(skip) + 1
        page_end = page_start + int(limit)
        self.start_urls = [QUESTIONS_URL % (page, sort) for page in range(page_start, page_end)]
        self.proxy = proxy

    def parse(self, response):
        if self.proxy and not response.xpath('/html/head/link[@rel="search" and contains(@title,"Stack")]'):
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
            return

        matched = URL_REGEX.search(response.url)
        if matched is None:
            for link in self.link_extractor.extract_links(response):
                yield scrapy.Request(url=link.url, callback=self.parse)
        elif matched.group('user_id'):
            yield self._parse_user(response, id=matched.group('user_id'))
        elif matched.group('tag_name'):
            yield self._parse_tag(response, id=matched.group('tag_name'))
        elif matched.group('question_id'):
            for item in self._parse_question(response, id=matched.group('question_id')):
                yield item

    def _parse_user(self, response, id):
        item = UserItem()
        item['extid'] = int(id)
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
        item['extid'] = int(id)
        item['url'] = response.url
        item['title'] = ''.join(
            response.css('div#question-header h1[itemprop=name] a::text').extract())
        body = ''.join(response.css(
            'div#question td.postcell div[itemprop=text]').xpath('node()').extract())
        item['body'] = body.strip()
        item['tags'] = response.css(
            'div#question td.postcell div.post-taglist a[rel=tag]::text').extract()
        for tag in item['tags']:
            tag_url = 'http://stackoverflow.com/tags/%s/info' % urllib2.quote(tag.encode('utf8'))
            yield scrapy.Request(url=tag_url, callback=self.parse)
        item['vote'] = parse_int(''.join(response.css(
            'div#question div.vote span[itemprop=upvoteCount]::text').extract()))
        item['comments'] = response.css(
            'div#question tr.comment span.comment-copy::text').extract()
        user_url = ''.join(response.css(
            'div#question div.user-info div.user-gravatar32 a::attr(href)').extract())
        matched = re.match(r'/users/(?P<user_id>\d+)/', user_url)
        item['user_id'] = matched and int(matched.group('user_id'))
        item['answers'] = []
        for answer in response.css('div#answers div.answer'):
            ans = {}
            ans['extid'] = int(''.join(answer.xpath('@data-answerid').extract()))
            ans['url'] = response.url.rstrip(
                '/') + '/%d#%d' % (ans['extid'], ans['extid'])
            body = ''.join(
                answer.css('div[itemprop=text]').xpath('node()').extract())
            ans['body'] = body.strip()
            ans['vote'] = parse_int(
                ''.join(answer.css('div.vote span[itemprop=upvoteCount]::text').extract()))
            ans['accept'] = bool(answer.css('div.vote span.vote-accepted-on'))
            ans['comments'] = answer.css(
                'tr.comment span.comment-copy::text').extract()
            user_url = ''.join(
                answer.css('div.user-info div.user-gravatar32 a::attr(href)').extract())
            matched = re.match(r'/users/(?P<user_id>\d+)/', user_url)
            if matched:
                ans['user_id'] = int(matched.group('user_id'))
                yield scrapy.Request(url=user_url, callback=self.parse)
            item['answers'].append(ans)
        yield item
