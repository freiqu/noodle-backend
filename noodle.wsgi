#!/bin/python
import sys
sys.path.insert(0, '/home/dev/crawled/Website')
from noodle import app as application

if __name__ == '__main__':
    application.run()