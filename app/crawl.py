#!/usr/bin/env python
# coding=utf-8

from billiard import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

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


class ProblemCrawler(Crawler):

    def _crawl(self, oj, problem_id):
        self.crawler.crawl(
                oj + '_problem',
                problem_id=problem_id
            )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, oj, problem_id):
        p = Process(
            target=self._crawl,
            args=[
                oj,
                problem_id
            ]
        )
        p.start()
        p.join()
    

class StatusCrawler(Crawler):

    def _crawl(self, oj, run_id):
        self.crawler.crawl(
            oj + '_status',
            run_id=run_id
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, oj, run_id):
        p = Process(
            target=self._crawl,
            args=[
                oj,
                run_id
            ]
        )
        p.start()
        p.join()


class CodeSubmitCrawler(Crawler):

    def _crawl(
            self,
            oj,
            problem_id,
            language,
            code,
            username,
            password):
        self.crawler.crawl(
            oj + '_submit',
            problem_id=problem_id,
            language=language,
            source=code,
            username=username,
            password=password
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(
            self,
            oj,
            problem_id,
            language,
            code,
            username,
            password):
        p = Process(
            target=self._crawl,
            args=[
                oj,
                problem_id,
                language,
                code,
                username,
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
