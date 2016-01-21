#!/usr/bin/env python
# coding=utf-8
from app import app
from flask.ext.script import Manager, Server
from config import OJS
from app.crawl import OJInitCrawler

manager = Manager(app)

manager.add_command("debug", Server(host="0.0.0.0", port=5000, use_debugger=True))
manager.add_command("start", Server(host="0.0.0.0", port=5000))

@manager.command
def init():
    for oj_code in OJS:
        init_crawler = OJInitCrawler()
        init_crawler.crawl(oj_code)


if __name__ == '__main__':
    manager.run()
