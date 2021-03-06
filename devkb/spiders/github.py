# -*- coding: utf-8 -*-

import scrapy
import re

from devkb.items.github import UserItem, RepoItem
from devkb.settings import URL_REGEXS
from devkb.utils import parse_int
from devkb.models import db
from scrapy.contrib.linkextractors import LinkExtractor

URLS_FILE = '/var/lib/scrapyd/github_repos.txt'

class GithubSpider(scrapy.Spider):
    name = "github"
    link_extractor = LinkExtractor(allow_domains=("github.com",), allow=re.compile(
        URL_REGEXS['github']['allow']), deny=re.compile(URL_REGEXS['github']['deny']))

    def __init__(self, skip=0, limit=1000, proxy=False, furls=URLS_FILE, *args, **kwargs):
        super(GithubSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.genstarturls(furls, int(skip), int(limit))
        self.item_regex = re.compile(
            '|'.join((URL_REGEXS['github']['user'], URL_REGEXS['github']['repo'])))
        self.proxy = proxy

    def genstarturls(self, furls, skip, limit):
        end = skip + limit
        times = 0
        with open(furls) as f:
            for l in f:
                times += 1
                if times <= skip:
                    continue
                if times > end:
                    break
                yield l.strip()

    def parse(self, response):
        if self.proxy and not response.xpath('/html/head/link[@rel="search" and contains(@title,"GitHub")]'):
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
            return

        matched = self.item_regex.search(response.url)
        if matched is None:
            pass
        elif matched.group('username'):
            yield self._parse_user(response, matched.group('username'))
        elif matched.group('reponame'):
            yield self._parse_repo(response, matched.group('ownername'), matched.group('reponame'))
            owner_url = 'https://github.com/%s' % matched.group('ownername')
            yield scrapy.Request(url=owner_url, callback=self.parse)

    def _parse_user(self, response, username):
        item = UserItem()
        item['url'] = response.url
        item['login'] = username
        counts = response.css('div.vcard-stats strong.vcard-stat-count::text').extract()
        if counts:
            item['follwers_count'] = parse_int(counts[0])
            item['stars_count'] = parse_int(counts[1])
            item['follwing_count'] = parse_int(counts[2])
        item['name'] = ''.join(response.css('h1.vcard-names span.vcard-fullname::text').extract())
        item['company'] = ''.join(response.css('ul.vcard-details li[itemprop=worksFor]::text').extract())
        item['blog'] = ''.join(response.css('ul.vcard-details li[itemprop=url] a::attr(href)').extract())
        item['location'] = ''.join(response.css('ul.vcard-details li[itemprop=homeLocation]::text').extract())
        item['email'] = ''.join(response.css('ul.vcard-details li a.email::text').extract())
        return item

    def _parse_repo(self, response, ownername, reponame):
        item = RepoItem()
        item['url'] = response.url
        item['fullname'] = '%s/%s' % (ownername, reponame)
        item['langs'] = response.css('div.repository-lang-stats ol.repository-lang-stats-numbers li span.lang::text').extract()
        item['readme'] = ''.join(response.css('div#readme article[itemprop=mainContentOfPage]').xpath('node()').extract())
        item['homepage'] = ''.join(response.css('.repository-meta .repository-website a::attr(href)').extract())
        item['descr'] = ''.join(response.css('.repository-meta .repository-description::text').extract())
        counts = response.css('ul.pagehead-actions li a.social-count::text').extract()
        if len(counts) == 2:
            item['stars_count'] = parse_int(counts[0])
            item['forks_count'] = parse_int(counts[1])
        stats = response.css('ul.numbers-summary li span.num::text').extract()
        if len(stats) == 4:
            item['commits_count'] = parse_int(stats[0])
            item['contributors_count'] = parse_int(stats[3])
        return item
