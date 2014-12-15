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
        elif matched.group('question_id'):
            for item in self._parse_question(response, id=matched.group('question_id')):
                yield item

    def _parse_user(self, response, id):
        item = UserItem()
        item['id'] = int(id)
        item['url'] = response.url
        item['name'] = response.xpath(
            '//*[@id="user-displayname"]//a/text()').extract().pop()
        item['reputation'] = parse_int(
            response.xpath('//*[@id="user-panel-reputation"]//h1//span/text()').extract().pop())
        return item

    def _parse_tag(self, response, id):
        item = TagItem()
        item['name'] = id
        item['url'] = response.url
        item['qcount'] = parse_int(
            response.xpath('//*[contains(@class,"summarycount")]/text()').extract().pop())
        descr = ''.join(response.xpath(
            '//*[@id="questions"]//*[contains(@class,"post-text")]/node()').extract())
        item['descr'] = descr.strip()
        return item

    def _parse_question(self, response, id):
        item = QuestionItem()
        item['id'] = int(id)
        item['url'] = response.url
        item['title'] = response.xpath(
            '//div[@id="question-header"]//h1//a/text()').extract().pop()
        body = ''.join(response.xpath(
            '//div[@id="question"]//td[contains(@class,"postcell")]//div[contains(@class,"post-text")]/node()').extract())
        item['body'] = body.strip()
        item['tags'] = response.xpath(
            '//div[@id="question"]//td[contains(@class,"postcell")]//div[contains(@class,"post-taglist")]//a/text()').extract()
        item['vote'] = parse_int(response.xpath(
            '//div[@id="question"]//div[contains(@class,"vote")]//span[contains(@class,"vote-count-post ")]/text()').extract().pop())
        item['comments'] = response.xpath('//div[@id="question"]//tr[contains(@class,"comment")]//span[contains(@class,"comment-copy")]/text()').extract()
        user_url = response.xpath(
            '//div[@id="question"]//td[contains(@class,"postcell")]//div[contains(@class,"user-gravatar32")]/a/@href').extract().pop()
        matched = re.match(r'/users/(?P<user_id>\d+)/[\w.-]+', user_url)
        item['user_id'] = int(matched.group('user_id'))
        yield item
