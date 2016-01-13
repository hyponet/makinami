#!/usr/bin/env python
# coding=utf-8

# 提供POJ相关API的实现

import pymongo
from flask.ext import restful

from app import api
import config

class Problem(restful.Resource):

    def connect_db(self, mongo_uri, mongo_db):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    def get(self, problem_id):
        self.connect_db(config.MONGO_URI, config.MONGO_PROBLEMS_DATABASE)
        problem_info = self.db['poj'].find({'problem_id': problem_id})
        return {
            'oj': 'POJ',
            'problem_id': problem_id,
            'title': problem_info['title'] if 'title' in problem_info else '',
            'description': problem_info['description'] if 'description' in problem_info else '',
            'input': problem_info['input'] if 'input' in problem_info else '',
            'output': problem_info['output'] if 'output' in problem_info else '',
            'sample_input': problem_info['sample_input'] if 'sample_input' in problem_info else '',
            'sample_output': problem_info['sample_output'] if 'sample_output' in problem_info else '',
            'time_limit': problem_info['time_limit'] if 'time_limit' in problem_info else '1000ms',
            'memory_limit': problem_info['memory_limit'] if 'memory_limit' in problem_info else '65535K'
        }

api.add_resource(Problem, '/poj/problem/<int:problem_id>')
