#!/usr/bin/env python
# coding=utf-8

# 提供POJ相关API的实现

import pymongo
from flask import request
from flask.ext import restful
import hashlib
from datetime import datetime

from app import api
from app.crawl import ProblemCrawler, StatusCrawler, CodeSubmitCrawler, AccountCrawler
import config

class POJProblem(restful.Resource):

    def get(self, problem_id):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        
        problem_info = db['problems'].find_one({'oj': 'poj', 'problem_id': str(problem_id)})
        if problem_info is None:
            get_problem = ProblemCrawler()
            get_problem.crawl('poj', str(problem_id))

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
            'problem_id': str(problem_id),
            'title': problem_info['title'] if 'title' in problem_info else '',
            'description': problem_info['description'] if 'description' in problem_info else '',
            'input': problem_info['input'] if 'input' in problem_info else '',
            'output': problem_info['output'] if 'output' in problem_info else '',
            'sample_input': problem_info['sample_input'] if 'sample_input' in problem_info else '',
            'sample_output': problem_info['sample_output'] if 'sample_output' in problem_info else '',
            'time_limit': problem_info['time_limit'] if 'time_limit' in problem_info else '1000MS',
            'memory_limit': problem_info['memory_limit'] if 'memory_limit' in problem_info else '65535K'
        }

    def post(self, problem_id):
        md5 = hashlib.md5()
        md5.update('poj' + request.json['username'] + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        solution_id = str(md5.hexdigest())
        code_submit = CodeSubmitCrawler()
        code_submit.crawl(
            oj='poj',
            solution_id=solution_id,
            problem_id=str(problem_id),
            language=request.json['language'],
            code=request.json['code'],
            username=request.json['username'],
            password=request.json['password']
            )

        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        
        run_info = db['status'].find_one({'oj': 'poj', 'problem_id': str(problem_id), 'solution_id': solution_id})
        client.close()

        if run_info is None:
            return {
                'status': 500,
                'message': 'failed to submit'
            }

        return {
            'oj': 'poj',
            'run_id': run_info['run_id'],
            'problem_id': run_info['problem_id'],
            'result': run_info['result'],
            'memory': run_info['memory'] if 'memory' in run_info else '',
            'time': run_info['time'] if 'time' in run_info else '',
            'language': run_info['language'],
            'code_length': run_info['code_length'],
            'submit_time': run_info['submit_time']
        }


class POJProblemList(restful.Resource):

    def get(self):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        
        problems = db['problems'].find({'oj': 'poj'}, {'problem_id': 1, 'title': 1})
        
        problem_list = []
        problem_num = 0;
        for one in problems:
            problem = {
                'problem_id': one['problem_id'],
                'title': one['title']
            }
            
            problem_list.append(problem)
            problem_num += 1

        return {
            'problem_num': problem_num,
            'problem_list': problem_list
        }


class POJStatus(restful.Resource):

    def get(self, run_id):
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        
        run_info = db['status'].find_one({'oj': 'poj', 'run_id': str(run_id)})
        if run_info is None:
            get_status = StatusCrawler()
            get_status.crawl('poj', str(run_id))
            run_info = db['status'].find_one({'oj': 'poj', 'run_id': str(run_id)})
        client.close()
    
        if run_info is None:
            return {
                'status': 404,
                'message': 'not found'
            }

        return {
            'oj': 'poj',
            'run_id': str(run_id),
            'problem_id': run_info['problem_id'],
            'result': run_info['result'],
            'memory': run_info['memory'] if 'memory' in run_info else '',
            'time': run_info['time'] if 'time' in run_info else '',
            'language': run_info['language'],
            'code_length': run_info['code_length'],
            'submit_time': run_info['submit_time']
        }

class POJUsers(restful.Resource):

    def post(self, username):
        get_user = AccountCrawler()
        get_user.crawl('poj', username, request.json['password'])

        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.MONGO_DATABASE]
        user_info = db['users'].find_one({'oj': 'poj', 'username': username})
        client.close()

        if user_info is None:
            return {
                'status': 404,
                'message': 'not found'
            }

        return {
            'username': user_info['username'],
            'status': 200,
            'submit': user_info['submit'],
            'oj': user_info['oj'],
            'accept': user_info['accept'],
            'rank': user_info['rank'],
            'solved': dict(user_info['solved'])
        }

api.add_resource(POJProblem, '/poj/problem/<int:problem_id>')
api.add_resource(POJProblemList, '/poj/problems')
api.add_resource(POJStatus, '/poj/status/<int:run_id>')
api.add_resource(POJUsers, '/poj/user/<string:username>')
