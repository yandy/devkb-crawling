import scrapy
import cPickle
import re

from devkb.items.stackoverflow import UserItem, TagItem, QuestionItem, AnswerItem
from devkb.settings import URL_REGEXS
from devkb.utils import parse_int
from scrapy.contrib.linkextractors import LinkExtractor

URL_REGEX = re.compile('|'.join(URL_REGEXS['stackoverflow'].values()))


class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    start_urls = ('http://stackoverflow.com',)
    link_extractor = LinkExtractor(allow_domains=("stackoverflow.com",))

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

    def _parse_user(self, response, id):
        item = UserItem()
        item['id'] = int(id)
        item['url'] = response.url
        item['name'] = response.xpath(
            '//*[@id="user-displayname"]//a/text()').extract().pop()
        item['reputation'] = parse_int(
            response.xpath('//*[@id="user-panel-reputation"]//h1//span/text()').extract().pop())
        item['tags'] = response.xpath(
            '//*[@id="user-panel-tags"]//table/tbody//td//a/text()').extract()
        return item

    def _parse_tag(self, response, id):
        item = TagItem()
        item['name'] = id
        item['url'] = response.url
        item['qcount'] = response.xpath('//*[contains(@class,"summarycount")]/text()').extract().pop()
        item['descr'] = ''.join(response.xpath('//*[@id="questions"]//*[contains(@class,"post-text")]/node()').extract())
        return item
