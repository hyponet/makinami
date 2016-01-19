#!/usr/bin/env python
# coding=utf-8

# 提供POJ相关API的实现

import pymongo
from flask.ext import restful

from app import api
import config

class POJProblem(restful.Resource):

    def get(self, problem_id):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        
        problem_info = db['problems'].find_one({'oj': 'poj', 'problem_id': str(problem_id)})
        client.close()
        if problem_info is None:
            return{
                'status': 404,
                'message': 'not found'
            }

        return {
            'status': 200,
            'oj': 'poj',
            'problem_id': problem_id,
            'title': problem_info['title'] if 'title' in problem_info else '',
            'description': problem_info['description'] if 'description' in problem_info else '',
            'input': problem_info['input'] if 'input' in problem_info else '',
            'output': problem_info['output'] if 'output' in problem_info else '',
            'sample_input': problem_info['sample_input'] if 'sample_input' in problem_info else '',
            'sample_output': problem_info['sample_output'] if 'sample_output' in problem_info else '',
            'time_limit': problem_info['time_limit'] if 'time_limit' in problem_info else '1000MS',
            'memory_limit': problem_info['memory_limit'] if 'memory_limit' in problem_info else '65535K'
        }


class POJStatus(restful.Resource):

    def get(self, run_id):
        pass


class POJUsers(restful.Resource):

    def post(self, username):
        pass


api.add_resource(POJProblem, '/poj/problem/<int:problem_id>')
api.add_resource(POJStatus, '/poj/status/<int:run_id>')
api.add_resource(POJUsers, '/poj/user/<string:username>')
