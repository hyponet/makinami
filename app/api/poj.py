#!/usr/bin/env python
# coding=utf-8

# 提供POJ相关API的实现

import pymongo
from flask.ext import restful

from app import api

class Problem(restful.Resource):
    def get(self, problem_id):
        return {
            'oj': 'POJ',
            "problem_id": problem_id
        }

api.add_resource(Problem, '/poj/problem/<int:problem_id>')
