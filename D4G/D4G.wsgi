#! /usr/bin/python3.7

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/debian/REC_D4G/D4G/')
from .views import app as application
application.secret_key = 'toto123'