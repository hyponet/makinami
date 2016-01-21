# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json

class IllustriousPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        item_name = item.__class__.__name__

        if item_name == 'ProblemItem':
            self.db['problems'].update(
                {
                    'oj': item['oj'],
                    'problem_id': item['problem_id']
                },
                dict(item),
                upsert=True
                )
        
        elif item_name == 'SolutionItem':
            self.db['status'].update(
                {
                    'oj': item['oj'],
                    'run_id': item['run_id']
                },
                dict(item),
                upsert=True
                )

        elif item_name == 'AccountItem':
            self.db['users'].update(
                {
                    'oj': item['oj'],
                    'username': item['username']
                },
                dict(item),
                upsert=True
                )

        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

