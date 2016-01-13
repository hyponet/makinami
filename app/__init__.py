#!/usr/bin/env python
# coding=utf-8
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

from .api import *
