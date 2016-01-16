#!/usr/bin/env python
# coding=utf-8

from billiard import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from base64 import b64encode

settings = get_project_settings()


class Crawler():

    def __init__(self):
        self.crawler = CrawlerProcess(settings)


class OJInitCrawler(Crawler):

    def _crawl(self, oj):
        self.crawler.crawl(
            oj + '_init',
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, oj):
        p = Process(
            target=self._crawl,
            args=[oj]
        )
        p.start()
        p.join()


class CodeSubmitCrawler(Crawler):

    def _crawl(
            self,
            oj,
            solution_id,
            problem_id,
            language,
            code,
            username,
            nickname,
            password):
        self.crawler.crawl(
            oj + '_submit',
            solution_id=solution_id,
            problem_id=problem_id,
            language=language,
            source=b64encode(code),
            username=username,
            nickname=nickname,
            password=password
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(
            self,
            oj,
            solution_id,
            problem_id,
            language,
            code,
            username,
            nickname,
            password):
        p = Process(
            target=self._crawl,
            args=[
                oj,
                solution_id,
                problem_id,
                language,
                code,
                username,
                nickname,
                password
            ]
        )
        p.start()
        p.join()


class AccountCrawler(Crawler):

    def _crawl(self, oj, username, password):
        self.crawler.crawl(
            oj + '_user',
            username=username,
            password=password
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, oj, username, password):
        p = Process(
            target=self._crawl,
            args=[
                oj,
                username,
                password
            ]
        )
        p.start()
        p.join()
