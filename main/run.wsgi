#! /usr/bin/python3.9

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/main')
from run import app as application
