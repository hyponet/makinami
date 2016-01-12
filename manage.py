#!/usr/bin/env python
# coding=utf-8
from app import app
from flask.ext.script import Manager, Server

manager = Manager(app)

manager.add_command("start", Server(host="0.0.0.0", port=5000, use_debugger=True))

if __name__ == '__main__':
    manager.run()
